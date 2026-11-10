"""Máscaras enteras, incidencias y registros de procedencia."""

import hashlib
import json
from pathlib import Path

import numpy as np
from scipy import ndimage as ndi

from .configuracion import Configuracion


def guardar_json(ruta: Path, valor: dict | list) -> None:
    """Sustituir el registro completo para no dejar JSON truncado al interrumpir."""
    temporal = ruta.with_suffix(ruta.suffix + ".tmp")
    temporal.write_text(json.dumps(valor, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                         encoding="utf-8")
    temporal.replace(ruta)


def describir_instancias(
    etiquetas: np.ndarray, espaciado_yx_um: tuple[float, float], mascara_exclusion: np.ndarray,
) -> list[dict]:
    instancias = []
    sy, sx = espaciado_yx_um
    ny, nx = etiquetas.shape
    cerca_roi = (
        ndi.binary_dilation(mascara_exclusion, iterations=2)
        if mascara_exclusion.any() else mascara_exclusion
    )
    for id_etiqueta in np.unique(etiquetas):
        if id_etiqueta == 0:
            continue
        yy, xx = np.where(etiquetas == id_etiqueta)
        toca_borde = bool((yy == 0).any() or (yy == ny - 1).any() or
                              (xx == 0).any() or (xx == nx - 1).any())
        toca_exclusion = bool(cerca_roi[yy, xx].any())
        instancias.append({
            "id_local_al_plano": int(id_etiqueta),
            "area_px": int(len(yy)),
            "area_um2": float(len(yy) * sy * sx),
            "bbox_yx_px": [int(yy.min()), int(yy.max()) + 1, int(xx.min()), int(xx.max()) + 1],
            "toca_borde": toca_borde,
            "cerca_anotacion_excluida": toca_exclusion,
        })
    return instancias


def crear_procedencia(
    pila, configuracion: Configuracion, pixeles_minimos: int, detalles_modelo: dict,
) -> dict:
    metadatos = pila.metadatos
    sy, sx = pila.espaciado_yx
    sz = metadatos["spacing_um"]["Z"]
    excluida = pila.excluida
    procedencia = {
        "estado": "propuestas_sin_validar", "estado_ejecucion": "en_curso",
        "estado_revision": "pendiente", "ground_truth_disponible": False,
        "modo": "2D independiente por plano; sin asociación de IDs entre Z",
        "pila": pila.nombre, "forma_nativa_zyx": metadatos["shape_zyx"],
        "forma_mascara_yx": list(excluida.shape),
        "forma_mascaras_zyx_prevista": [len(pila.planos), *excluida.shape],
        "canal": {"tag": metadatos["channel"], "tinte": metadatos["dye"]},
        "spacing_nativo_um_xyz": metadatos["spacing_um"],
        "spacing_mascara_um_yx": [sy, sx],
        "spacing_mascara_um_zyx": [sz, sy, sx],
        "origen_mascara_um_zyx": [configuracion.z_inicio * sz, 0.0, 0.0],
        "paso_xy": configuracion.paso_xy,
        "rango_z_exclusivo": [configuracion.z_inicio, pila.z_fin],
        "roi_excluida_px_nativos_y0y1x0x1": pila.roi,
        "archivo_zona_excluida": "zona-excluida.tif",
        "exclusion_requiere_revision_visual": True,
        "normalizacion": {
            "modo": configuracion.normalizacion, "percentiles": [1.0, 99.8],
            "limites_globales": pila.limites, "limites_por_plano": {},
        },
        "modelo": configuracion.modelo,
        **detalles_modelo,
        "parametros_cellpose": {
            "do_3D": False, "diameter": None,
            "cellprob_threshold": configuracion.umbral_probabilidad,
            "flow_threshold": configuracion.umbral_flujo,
            "min_size_px": pixeles_minimos, "area_min_um2": configuracion.area_minima_um2,
            "batch_size": 1, "normalize": False,
        },
        "xml_numerico": str(metadatos["numeric_xml"].relative_to(configuracion.datos)),
        "sha256_xml_numerico": hashlib.sha256(metadatos["numeric_xml"].read_bytes()).hexdigest(),
        "xml_propiedades": str(metadatos["properties_xml"].relative_to(configuracion.datos)),
        "sha256_xml_propiedades": hashlib.sha256(metadatos["properties_xml"].read_bytes()).hexdigest(),
        "planos": [], "tiempo_total_s": 0.0,
    }
    return procedencia
