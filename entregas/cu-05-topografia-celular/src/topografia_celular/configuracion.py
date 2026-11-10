"""Configuración compartida por la interfaz y el procesamiento."""

from dataclasses import dataclass
from pathlib import Path


PROYECTO = Path(__file__).resolve().parents[2]
DATOS = PROYECTO / "data"
TEMPORALES = PROYECTO / "tmp"
CACHE_MODELOS = TEMPORALES / "modelos" / "cellpose"

ROI = tuple[int, int, int, int]


@dataclass(frozen=True)
class Configuracion:
    datos: Path = DATOS
    paso_xy: int = 2
    z_inicio: int = 0
    z_fin: int | None = None
    modelo: str = "cpsam_v2"
    umbral_probabilidad: float = 0.5
    umbral_flujo: float = 0.4
    normalizacion: str = "global"
    area_minima_um2: float = 5.0
    roi: ROI | None = None
    sin_exclusion: bool = False
    permitir_cpu: bool = False
