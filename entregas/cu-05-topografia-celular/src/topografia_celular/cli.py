"""Interfaz de terminal para validar y segmentar pilas nucleares."""

import argparse
from dataclasses import fields
from datetime import datetime, timezone
import math
from pathlib import Path
import re
import sys

from .configuracion import Configuracion, DATOS, TEMPORALES
from .ejecucion import PilaPreparada, preparar_pila, procesar_lote
from .exportacion import guardar_json


def interpretar_roi(texto: str) -> tuple[int, int, int, int]:
    try:
        coordenadas = tuple(int(parte.strip()) for parte in texto.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("Formato esperado: y0,y1,x0,x1") from error
    if len(coordenadas) != 4:
        raise argparse.ArgumentTypeError("Formato esperado: y0,y1,x0,x1")
    return coordenadas


def crear_argumentos() -> argparse.ArgumentParser:
    argumentos = argparse.ArgumentParser(description=__doc__)
    seleccion = argumentos.add_mutually_exclusive_group(required=True)
    seleccion.add_argument("--pila", help="Nombre exacto de una subcarpeta de datos.")
    seleccion.add_argument("--todas", action="store_true", help="Procesar todas las pilas en un lote.")
    argumentos.add_argument("--datos", "--data", type=Path, default=DATOS)
    argumentos.add_argument("--paso-xy", type=int, default=2,
                            help="1 conserva la resolución nativa; 2 usa el muestreo del piloto.")
    argumentos.add_argument("--z-inicio", type=int, default=0)
    argumentos.add_argument("--z-fin", type=int, help="Límite exclusivo; por defecto toda la pila.")
    argumentos.add_argument("--modelo", default="cpsam_v2")
    argumentos.add_argument("--umbral-probabilidad", "--cellprob-threshold", type=float, default=0.5)
    argumentos.add_argument("--umbral-flujo", "--flow-threshold", type=float, default=0.4)
    argumentos.add_argument("--normalizacion", choices=("global", "plano"), default="global")
    argumentos.add_argument("--area-minima-um2", "--area-min-um2", type=float, default=5.0,
                            help="Filtro exploratorio, pendiente de validación biológica.")
    exclusion = argumentos.add_mutually_exclusive_group()
    exclusion.add_argument("--roi", type=interpretar_roi,
                           help="y0,y1,x0,x1 en píxeles nativos; solo con --pila.")
    exclusion.add_argument("--sin-exclusion", "--no-exclude-roi", action="store_true")
    argumentos.add_argument("--permitir-cpu", action="store_true")
    argumentos.add_argument("--solo-validar", action="store_true",
                            help="Comprobar imágenes/XML, exclusión y contraste sin cargar Cellpose.")
    argumentos.add_argument("--salida", "--output", type=Path,
                            help="Carpeta nueva de ejecución; no se sobrescriben resultados.")
    return argumentos


def validar_argumentos(argumentos: argparse.Namespace) -> Configuracion:
    datos = argumentos.datos.resolve()
    if not datos.is_dir():
        raise ValueError(f"No existe la carpeta de datos: {datos}")
    if argumentos.paso_xy < 1:
        raise ValueError("--paso-xy debe ser >= 1")
    if argumentos.todas and argumentos.roi is not None:
        raise ValueError("--roi es específico de una pila; utiliza --pila para una exclusión manual.")

    for nombre in ("area_minima_um2", "umbral_probabilidad", "umbral_flujo"):
        if not math.isfinite(getattr(argumentos, nombre)):
            raise ValueError(f"{nombre} debe ser finito")
    if argumentos.area_minima_um2 < 0 or argumentos.umbral_flujo < 0:
        raise ValueError("El área mínima y el umbral de flujo deben ser >= 0")

    valores = {campo.name: getattr(argumentos, campo.name) for campo in fields(Configuracion)}
    valores["datos"] = datos
    return Configuracion(**valores)


def preparar_ejecucion(
    argumentos: argparse.Namespace, configuracion: Configuracion,
) -> tuple[list[PilaPreparada], Path, dict]:
    nombres = ([argumentos.pila] if argumentos.pila else sorted(
        ruta.name for ruta in configuracion.datos.iterdir()
        if ruta.is_dir() and not ruta.name.startswith(".")
    ))
    if not nombres:
        raise ValueError("No hay pilas para procesar.")

    identificador = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    nombre_carpeta = re.sub(r"[^a-zA-Z0-9_-]+", "-", nombres[0]).strip("-").lower()
    salida = (argumentos.salida.resolve() if argumentos.salida else
              TEMPORALES / "segmentacion-cellpose" /
              (f"lote-{identificador}" if argumentos.todas else f"{nombre_carpeta}/{identificador}"))
    if salida.is_relative_to(configuracion.datos):
        raise ValueError("La salida debe estar separada de los datos originales.")
    if salida.exists():
        raise ValueError(f"La salida ya existe; usa una carpeta nueva: {salida}")

    # Comprobar todo el lote antes de reservar la GPU o empezar a guardar máscaras.
    pilas = [preparar_pila(configuracion, nombre) for nombre in nombres]
    carpetas = [pila.carpeta_salida for pila in pilas]
    if any(not nombre for nombre in carpetas) or len(set(carpetas)) != len(carpetas):
        raise ValueError("Los nombres de las pilas generan carpetas de salida ambiguas.")

    resumen = {
        "id_ejecucion": identificador,
        "estado": "validado" if argumentos.solo_validar else "en_curso",
        "solo_validacion": argumentos.solo_validar,
        "datos": str(configuracion.datos), "modelo": configuracion.modelo,
        "paso_xy": configuracion.paso_xy, "normalizacion": configuracion.normalizacion,
        "umbral_probabilidad": configuracion.umbral_probabilidad,
        "umbral_flujo": configuracion.umbral_flujo,
        "area_minima_um2": configuracion.area_minima_um2,
        "pilas": [dict(pila.resumen(), estado="pendiente",
                       carpeta=pila.carpeta_salida if argumentos.todas else "mascaras") for pila in pilas],
    }
    return pilas, salida, resumen


def ejecutar(argumentos: list[str] | None = None) -> int:
    interfaz = crear_argumentos()
    opciones = interfaz.parse_args(argumentos)
    try:
        configuracion = validar_argumentos(opciones)
        pilas, salida, resumen = preparar_ejecucion(opciones, configuracion)
    except ValueError as error:
        interfaz.error(str(error))

    salida.mkdir(parents=True, exist_ok=False)
    guardar_json(salida / "resumen.json", resumen)
    for pila in pilas:
        print(f"Validada {pila.nombre}: {len(pila.planos)} planos DAPI, "
              f"máscaras YX={pila.excluida.shape}, ROI={pila.roi}", flush=True)
    print(f"Salida: {salida}", flush=True)
    if opciones.solo_validar:
        return 0
    return procesar_lote(pilas, configuracion, salida, resumen)


def principal() -> None:
    try:
        codigo = ejecutar()
    except KeyboardInterrupt:
        print("Interrumpido; se conserva el registro del progreso.", file=sys.stderr)
        codigo = 130
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        codigo = 1
    raise SystemExit(codigo)
