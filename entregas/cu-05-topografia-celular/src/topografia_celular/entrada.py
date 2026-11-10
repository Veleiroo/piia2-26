"""Lectura y validación de pilas TIFF y metadatos Leica."""

from pathlib import Path
import math
import re
import xml.etree.ElementTree as ET

import numpy as np
import tifffile


def leer_metadatos(carpeta: Path) -> dict:
    """Leer dimensiones Leica e identificar el único canal DAPI del XML."""
    propiedades = list(carpeta.rglob("*_Properties.xml"))
    numericos = [p for p in carpeta.rglob("*.xml") if not p.name.endswith("_Properties.xml")]
    if len(propiedades) != 1 or len(numericos) != 1:
        raise ValueError(f"Se esperaba un par de XML Leica en {carpeta.name!r}.")
    ET.parse(propiedades[0])  # Comprobar también que el XML de propiedades sea legible.
    raiz_datos = ET.parse(numericos[0]).getroot()
    descripciones_dimensiones = {d.get("DimID"): d.attrib for d in raiz_datos.iter("DimensionDescription")}
    dimensiones = {}
    espaciado = {}
    for id_dimension, eje in (("1", "X"), ("2", "Y"), ("3", "Z")):
        d = descripciones_dimensiones.get(id_dimension)
        if d is None or d.get("Unit") != "m":
            raise ValueError(f"Dimensión {eje} ausente o con unidades inesperadas en {carpeta.name}.")
        cantidad = int(d["NumberOfElements"])
        if cantidad < 1:
            raise ValueError(f"Dimensión {eje} vacía en {carpeta.name}.")
        dimensiones[eje] = cantidad
        espaciado[eje] = (
            float(d["Length"]) * 1e6 / (cantidad - 1)
            if cantidad > 1 else float(d["Voxel"]) * 1e6
        )
        if not math.isfinite(espaciado[eje]) or espaciado[eje] <= 0:
            raise ValueError(f"Calibración {eje} inválida en {carpeta.name}.")

    canales_dapi = []
    for canal in raiz_datos.iter("ChannelDescription"):
        mapa_propiedades = {x.findtext("Key"): x.findtext("Value")
                          for x in canal.findall("ChannelProperty")}
        if "dapi" in (mapa_propiedades.get("DyeName") or "").lower():
            canales_dapi.append((int(canal.get("ChannelTag")), mapa_propiedades.get("DyeName")))
    if len(canales_dapi) != 1:
        raise ValueError(f"Canal DAPI ambiguo o ausente en {carpeta.name}: {canales_dapi}")

    return {
        "shape_zyx": [dimensiones["Z"], dimensiones["Y"], dimensiones["X"]],
        "spacing_um": espaciado,
        "channel": canales_dapi[0][0],
        "dye": canales_dapi[0][1],
        "numeric_xml": numericos[0],
        "properties_xml": propiedades[0],
    }


def listar_planos(carpeta: Path, canal: int, nz: int) -> list[tuple[int, Path]]:
    patron = re.compile(rf"_z(\d+)_ch{canal:02d}_SV\.tif$", re.IGNORECASE)
    planos = []
    for ruta in carpeta.glob("*.tif"):
        coincidencia = patron.search(ruta.name)
        if coincidencia:
            planos.append((int(coincidencia.group(1)), ruta))
    planos.sort(key=lambda par: par[0])
    if [z for z, _ in planos] != list(range(nz)):
        raise ValueError(f"La secuencia DAPI de {carpeta.name} no contiene exactamente Z=0..{nz-1}.")
    return planos


def leer_plano_dapi(ruta: Path) -> tuple[np.ndarray, np.ndarray | None]:
    """Leer la señal nuclear y conservar el RGB para detectar anotaciones."""
    imagen = tifffile.imread(ruta)
    if imagen.ndim == 3 and imagen.shape[-1] in (3, 4):
        rgb = imagen[..., :3]
        # En estas exportaciones Leica el LUT nuclear azul se almacena en B.
        return rgb[..., 2], rgb
    if imagen.ndim == 2:
        return imagen, None
    raise ValueError(f"Formato TIFF no contemplado en {ruta.name}: {imagen.shape}")


def validar_cabeceras(planos: list[tuple[int, Path]], forma_yx: tuple[int, int]) -> None:
    """Comprobar toda la adquisición antes de cargar pesos o producir máscaras."""
    for _, ruta in planos:
        with tifffile.TiffFile(ruta) as tif:
            forma = tif.pages[0].shape
            if len(tif.pages) != 1 or forma[:2] != forma_yx:
                raise ValueError(f"Dimensiones TIFF/XML incompatibles en {ruta.name}: {forma}.")
            if len(forma) != 2 and not (len(forma) == 3 and forma[-1] in (3, 4)):
                raise ValueError(f"Formato TIFF no contemplado en {ruta.name}: {forma}.")
