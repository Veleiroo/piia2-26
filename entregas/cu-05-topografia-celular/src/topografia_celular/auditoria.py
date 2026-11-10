"""Inventario de las exportaciones Leica, sin modificar los originales."""

import argparse
from collections import defaultdict
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import tifffile

from .configuracion import DATOS, TEMPORALES
from .entrada import leer_metadatos
from .exportacion import guardar_json


def inspeccionar_exportaciones(carpeta: Path, forma_yx: tuple[int, int]) -> tuple:
    grupos = defaultdict(list)
    formatos = set()
    errores_dimensiones = []
    for ruta in sorted(carpeta.glob("*.tif")):
        coincidencia = re.search(r"_z(\d+)_(ch\d+_SV|overlay)\.tif$", ruta.name, re.IGNORECASE)
        if coincidencia is None:
            raise ValueError(f"Nombre no contemplado: {ruta.name}")
        grupos[coincidencia[2]].append(int(coincidencia[1]))
        with tifffile.TiffFile(ruta) as tif:
            pagina = tif.pages[0]
            formatos.add((str(pagina.dtype), pagina.photometric.name, tuple(pagina.shape)))
            if len(tif.pages) != 1 or pagina.shape[:2] != forma_yx:
                errores_dimensiones.append(ruta.name)
    return grupos, formatos, errores_dimensiones


def auditar_pila(carpeta: Path, datos: Path) -> dict:
    metadatos = leer_metadatos(carpeta)
    propiedades = ET.parse(metadatos["properties_xml"]).getroot()
    numerico = ET.parse(metadatos["numeric_xml"]).getroot()
    dimensiones = {elemento.get("DimID"): elemento.attrib
                   for elemento in propiedades.iter("DimensionDescription")}
    nz, ny, nx = metadatos["shape_zyx"]
    grupos, formatos, errores_dimensiones = inspeccionar_exportaciones(carpeta, (ny, nx))

    canales = []
    for canal in numerico.iter("ChannelDescription"):
        valores = {elemento.findtext("Key"): elemento.findtext("Value")
                   for elemento in canal.findall("ChannelProperty")}
        canales.append({"tag": canal.get("ChannelTag"), "dye": valores.get("DyeName")})
    equipo = next((elemento for elemento in propiedades.iter("Attachment")
                   if elemento.get("Name") == "HardwareSetting"), None)

    # Se conserva el esquema del inventario que utiliza el notebook exploratorio.
    return {
        "folder": carpeta.name,
        "properties_xml": str(metadatos["properties_xml"].relative_to(datos)),
        "numeric_xml": str(metadatos["numeric_xml"].relative_to(datos)),
        "shape_zyx": [nz, ny, nx],
        "spacing_um": metadatos["spacing_um"],
        "voxel_properties_um": {clave: float(valor["Voxel"]) for clave, valor in dimensiones.items()},
        "channels": canales,
        "exports": {
            nombre: {
                "files": len(indices),
                "missing_z": sorted(set(range(nz)) - set(indices)),
                "duplicate_z": len(indices) - len(set(indices)),
                "unexpected_z": sorted(set(indices) - set(range(nz))),
            }
            for nombre, indices in sorted(grupos.items())
        },
        "tiff_formats": [
            {"dtype": tipo, "photometric": color, "shape_yxs": forma}
            for tipo, color, forma in sorted(formatos)
        ],
        "shape_errors": errores_dimensiones,
        "start_time": propiedades.findtext(".//StartTime"),
        "end_time": propiedades.findtext(".//EndTime"),
        "microscope": equipo.get("SystemTypeName") if equipo is not None else None,
        "acquisition_type": equipo.get("DataSourceTypeName") if equipo is not None else None,
    }


def auditar(datos: Path) -> list[dict]:
    datos = datos.resolve()
    if not datos.is_dir():
        raise ValueError(f"No existe la carpeta de datos: {datos}")
    carpetas = sorted(ruta for ruta in datos.iterdir()
                      if ruta.is_dir() and not ruta.name.startswith("."))
    if not carpetas:
        raise ValueError("No se encontraron pilas.")
    return [auditar_pila(carpeta, datos) for carpeta in carpetas]


def principal() -> None:
    argumentos = argparse.ArgumentParser(description=__doc__)
    argumentos.add_argument("--datos", "--data", type=Path, default=DATOS)
    argumentos.add_argument("--salida", "--output", type=Path,
                            default=TEMPORALES / "inventario-metadatos.json")
    opciones = argumentos.parse_args()
    if opciones.salida.resolve().is_relative_to(opciones.datos.resolve()):
        argumentos.error("El inventario debe guardarse fuera de los datos originales.")
    resultado = auditar(opciones.datos)
    opciones.salida.parent.mkdir(parents=True, exist_ok=True)
    guardar_json(opciones.salida, resultado)
    for fila in resultado:
        print(fila["folder"], fila["shape_zyx"], fila["exports"])
    print(f"Inventario guardado en {opciones.salida}")


if __name__ == "__main__":
    principal()
