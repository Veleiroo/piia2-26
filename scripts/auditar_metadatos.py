"""Auditoría de las exportaciones Leica, sin modificar las imágenes originales.

Ejecutar desde la raíz del repositorio: python3 scripts/auditar_metadatos.py
Requiere tifffile. La salida JSON contiene una fila por carpeta, no por célula.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import tifffile

REPO = Path(__file__).resolve().parents[1]


def audit(data):
    rows = []
    for folder in sorted(p for p in data.iterdir() if p.is_dir()):
        props = list(folder.rglob("*_Properties.xml"))
        raw = [p for p in folder.rglob("*.xml") if not p.name.endswith("_Properties.xml")]
        if len(props) != 1 or len(raw) != 1:
            raise ValueError(f"Par XML ambiguo o ausente: {folder.name}")
        prop = ET.parse(props[0]).getroot()
        root = ET.parse(raw[0]).getroot()
        dims = {x.get("DimID"): x.attrib for x in root.iter("DimensionDescription")}
        human = {x.get("DimID"): x.attrib for x in prop.iter("DimensionDescription")}
        spacing = {}
        shape = {}
        for number, axis in (("1", "X"), ("2", "Y"), ("3", "Z")):
            dim = dims[number]
            n = int(dim["NumberOfElements"])
            if dim["Unit"] != "m" or n <= 1:
                raise ValueError(f"Dimensión no contemplada: {folder.name}/{axis}")
            # Leica Length representa la distancia entre los centros extremos.
            spacing[axis] = float(dim["Length"]) * 1e6 / (n - 1)
            shape[axis] = n
        groups = defaultdict(list)
        formats = set()
        shape_errors = []
        for file in sorted(folder.glob("*.tif")):
            match = re.search(r"_z(\d+)_(ch\d+_SV|overlay)\.tif$", file.name)
            if match is None:
                raise ValueError(f"Nombre no contemplado: {file.name}")
            groups[match[2]].append(int(match[1]))
            with tifffile.TiffFile(file) as tif:
                page = tif.pages[0]
                formats.add((str(page.dtype), page.photometric.name, tuple(page.shape)))
                if page.shape[:2] != (shape["Y"], shape["X"]):
                    shape_errors.append(file.name)
        channel_info = []
        for channel in root.iter("ChannelDescription"):
            values = {x.findtext("Key"): x.findtext("Value") for x in channel.findall("ChannelProperty")}
            channel_info.append({"tag": channel.get("ChannelTag"), "dye": values.get("DyeName")})
        hardware = next(x for x in prop.iter("Attachment") if x.get("Name") == "HardwareSetting")
        rows.append({
            "folder": folder.name,
            "properties_xml": str(props[0].relative_to(data)),
            "numeric_xml": str(raw[0].relative_to(data)),
            "shape_zyx": [shape["Z"], shape["Y"], shape["X"]],
            "spacing_um": spacing,
            "voxel_properties_um": {k: float(v["Voxel"]) for k, v in human.items()},
            "channels": channel_info,
            "exports": {key: {"files": len(z), "missing_z": sorted(set(range(shape["Z"])) - set(z)),
                               "duplicate_z": len(z) - len(set(z)),
                               "unexpected_z": sorted(set(z) - set(range(shape["Z"])))}
                        for key, z in sorted(groups.items())},
            "tiff_formats": [{"dtype": dtype, "photometric": photo, "shape_yxs": s}
                             for dtype, photo, s in sorted(formats)],
            "shape_errors": shape_errors,
            "start_time": prop.findtext(".//StartTime"),
            "end_time": prop.findtext(".//EndTime"),
            "microscope": hardware.get("SystemTypeName"),
            "acquisition_type": hardware.get("DataSourceTypeName"),
        })
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=REPO / "data")
    parser.add_argument("--output", type=Path, default=REPO / "tmp" / "inventario-metadatos.json")
    args = parser.parse_args()
    result = audit(args.data)
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for row in result:
        print(row["folder"], row["shape_zyx"], row["spacing_um"], row["exports"])
    print(f"Inventario guardado en {output}")
