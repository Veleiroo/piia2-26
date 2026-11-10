"""Preparación de pilas y ejecución de la segmentación por lotes."""

from dataclasses import dataclass
import hashlib
import math
from pathlib import Path
import re
import sys
import time

import numpy as np
import tifffile

from .configuracion import Configuracion, ROI
from .entrada import leer_plano_dapi, listar_planos, leer_metadatos, validar_cabeceras
from .exportacion import crear_procedencia, describir_instancias, guardar_json
from .modelo import describir_modelo, sesion_modelo, segmentar_plano
from .preprocesado import (
    crear_mascara_exclusion,
    estimar_limites_globales,
    normalizar_plano,
    proponer_roi_anotaciones,
)


@dataclass
class PilaPreparada:
    nombre: str
    metadatos: dict
    planos: list[tuple[int, Path]]
    roi: ROI | None
    excluida: np.ndarray
    limites: tuple[float, float] | None
    z_fin: int
    carpeta_salida: str
    paso_xy: int

    @property
    def espaciado_yx(self) -> tuple[float, float]:
        espaciado = self.metadatos["spacing_um"]
        return espaciado["Y"] * self.paso_xy, espaciado["X"] * self.paso_xy

    def resumen(self) -> dict:
        return {
            "pila": self.nombre, "forma_nativa_zyx": self.metadatos["shape_zyx"],
            "forma_mascara_yx": list(self.excluida.shape),
            "planos_dapi_adquisicion": self.metadatos["shape_zyx"][0],
            "planos_solicitados": len(self.planos),
            "roi_excluida_px_nativos_y0y1x0x1": self.roi,
            "pixeles_excluidos_por_plano": int(self.excluida.sum()),
            "limites_globales": self.limites,
        }


def preparar_pila(configuracion: Configuracion, nombre: str) -> PilaPreparada:
    carpeta = configuracion.datos / nombre
    if not carpeta.is_dir() or carpeta.parent != configuracion.datos:
        raise ValueError(f"No existe la subcarpeta de pila: {nombre!r}")
    metadatos = leer_metadatos(carpeta)
    nz, ny, nx = metadatos["shape_zyx"]
    z_fin = nz if configuracion.z_fin is None else configuracion.z_fin
    if not 0 <= configuracion.z_inicio < z_fin <= nz:
        raise ValueError(f"Rango Z inválido en {nombre}: 0 <= inicio < fin <= {nz}.")

    planos = listar_planos(carpeta, metadatos["channel"], nz)
    validar_cabeceras(planos, (ny, nx))
    roi = configuracion.roi
    if configuracion.sin_exclusion:
        roi = None
    elif roi is None:
        roi = proponer_roi_anotaciones(planos, (ny, nx))

    excluida = crear_mascara_exclusion((ny, nx), roi, configuracion.paso_xy)
    limites = (estimar_limites_globales(planos, roi, configuracion.paso_xy, (1.0, 99.8))
              if configuracion.normalizacion == "global" else None)
    return PilaPreparada(
        nombre=nombre, metadatos=metadatos, planos=planos[configuracion.z_inicio:z_fin],
        roi=roi, excluida=excluida, limites=limites, z_fin=z_fin,
        carpeta_salida=re.sub(r"[^a-zA-Z0-9_-]+", "-", nombre).strip("-").lower(),
        paso_xy=configuracion.paso_xy,
    )


def procesar_plano(pila: PilaPreparada, configuracion: Configuracion, modelo,
                  z: int, ruta: Path, pixeles_minimos: int, salida: Path) -> dict:
    inicio = time.perf_counter()
    plano, _ = leer_plano_dapi(ruta)
    muestreada = plano[::configuracion.paso_xy, ::configuracion.paso_xy].astype(np.float32)
    imagen, limites = normalizar_plano(muestreada, pila.excluida, pila.limites)
    etiquetas = segmentar_plano(modelo, imagen, pila.excluida, configuracion, pixeles_minimos)
    instancias = describir_instancias(etiquetas, pila.espaciado_yx, pila.excluida)

    nombre_archivo = f"mascara-z{z:03d}.tif"
    tifffile.imwrite(salida / nombre_archivo, etiquetas, photometric="minisblack", metadata={
        "axes": "YX", "z_original": z, "spacing_um_yx": list(pila.espaciado_yx),
        "paso_xy": configuracion.paso_xy, "estado": "propuesta_2d_sin_validar",
    })
    return {
        "z_original": z, "posicion_z_um": z * pila.metadatos["spacing_um"]["Z"],
        "archivo_entrada": str(ruta.relative_to(configuracion.datos)),
        "sha256_entrada": hashlib.sha256(ruta.read_bytes()).hexdigest(),
        "archivo_mascara": nombre_archivo, "n_instancias": len(instancias),
        "sin_senal_tras_normalizacion": not bool(np.any(imagen)),
        "limites_normalizacion": list(limites),
        "segundos_procesamiento": round(time.perf_counter() - inicio, 3),
        "instancias": instancias,
    }


def procesar_pila(pila: PilaPreparada, configuracion: Configuracion, salida: Path,
                  modelo, detalles_modelo: dict) -> dict:
    sy, sx = pila.espaciado_yx
    pixeles_minimos = max(1, math.ceil(configuracion.area_minima_um2 / (sy * sx)))
    procedencia = crear_procedencia(pila, configuracion, pixeles_minimos, detalles_modelo)
    salida.mkdir(parents=True, exist_ok=False)
    ruta_procedencia = salida / "procedencia.json"
    inicio = time.perf_counter()
    guardar_json(ruta_procedencia, procedencia)

    try:
        tifffile.imwrite(salida / "zona-excluida.tif", pila.excluida.astype(np.uint8),
                         photometric="minisblack", metadata={"axes": "YX"})
        for z, ruta in pila.planos:
            registro = procesar_plano(pila, configuracion, modelo, z, ruta, pixeles_minimos, salida)
            procedencia["planos"].append(registro)
            procedencia["normalizacion"]["limites_por_plano"][str(z)] = registro["limites_normalizacion"]
            procedencia["tiempo_total_s"] = round(time.perf_counter() - inicio, 3)
            guardar_json(ruta_procedencia, procedencia)
            print(f"{pila.nombre} Z={z:03d}: {registro['n_instancias']} propuestas "
                  f"({registro['segundos_procesamiento']:.2f} s)", flush=True)
        procedencia["estado_ejecucion"] = "completada"
    except BaseException as error:
        procedencia["estado_ejecucion"] = (
            "interrumpida" if isinstance(error, KeyboardInterrupt) else "error"
        )
        procedencia["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        procedencia["tiempo_total_s"] = round(time.perf_counter() - inicio, 3)
        guardar_json(ruta_procedencia, procedencia)
    return procedencia


def procesar_lote(pilas: list[PilaPreparada], configuracion: Configuracion,
                  salida: Path, resumen: dict) -> int:
    ruta_resumen = salida / "resumen.json"
    try:
        with sesion_modelo(configuracion) as (modelo, dispositivo):
            detalles_modelo = describir_modelo(modelo, dispositivo)
            for pila, entrada_resumen in zip(pilas, resumen["pilas"]):
                entrada_resumen["estado"] = "en_curso"
                guardar_json(ruta_resumen, resumen)
                destino = salida / entrada_resumen["carpeta"]
                entrada_resumen["procedencia"] = str((destino / "procedencia.json").relative_to(salida))
                try:
                    resultado = procesar_pila(pila, configuracion, destino, modelo, detalles_modelo)
                    entrada_resumen["estado"] = "completada"
                    entrada_resumen["planos_guardados"] = len(resultado["planos"])
                except KeyboardInterrupt:
                    entrada_resumen["estado"] = "interrumpida"
                    raise
                except Exception as error:
                    entrada_resumen["estado"] = "error"
                    entrada_resumen["error"] = f"{type(error).__name__}: {error}"
                    print(f"Error en {pila.nombre}: {error}", file=sys.stderr, flush=True)
                finally:
                    guardar_json(ruta_resumen, resumen)
        hay_errores = any(entrada_resumen["estado"] == "error" for entrada_resumen in resumen["pilas"])
        resumen["estado"] = "con_errores" if hay_errores else "completado"
        return 1 if hay_errores else 0
    except BaseException as error:
        resumen["estado"] = "interrumpido" if isinstance(error, KeyboardInterrupt) else "error"
        resumen["error"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        guardar_json(ruta_resumen, resumen)
