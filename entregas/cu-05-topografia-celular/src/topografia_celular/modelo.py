"""Carga única de Cellpose y predicción de etiquetas por plano."""

from contextlib import contextmanager
import gc
import hashlib
from importlib import metadata as metadatos_paquetes
import os
from pathlib import Path

import numpy as np

from .configuracion import CACHE_MODELOS, Configuracion


@contextmanager
def sesion_modelo(configuracion: Configuracion):
    # Importación diferida: validar los datos no requiere instalar ni cargar Cellpose.
    os.environ.setdefault("CELLPOSE_LOCAL_MODELS_PATH", str(CACHE_MODELOS))
    try:
        import torch
        from cellpose import models
    except ImportError as error:
        raise RuntimeError(
            "Falta Cellpose/PyTorch. Usa el entorno vpc2 o instala el extra [cellpose]."
        ) from error

    dispositivo = torch.device("cuda" if torch.cuda.is_available() else
                          "mps" if torch.backends.mps.is_available() else "cpu")
    if dispositivo.type == "cpu" and not configuracion.permitir_cpu:
        raise RuntimeError("No se detectó GPU; --permitir-cpu acepta una ejecución más lenta.")

    modelo = models.CellposeModel(
        pretrained_model=configuracion.modelo, device=dispositivo,
        use_bfloat16=dispositivo.type == "cuda" and torch.cuda.is_bf16_supported(),
    )
    try:
        yield modelo, dispositivo
    finally:
        del modelo
        gc.collect()
        if dispositivo.type == "cuda":
            torch.cuda.empty_cache()


def describir_modelo(modelo, dispositivo) -> dict:
    archivo_pesos = getattr(modelo, "pretrained_model", None)
    ruta = Path(archivo_pesos) if isinstance(archivo_pesos, (str, os.PathLike)) else None
    # Calcular una vez para todo el lote: los pesos ocupan más de un GB.
    huella = None
    if ruta is not None and ruta.is_file():
        hash_pesos = hashlib.sha256()
        with ruta.open("rb") as archivo:
            for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
                hash_pesos.update(bloque)
        huella = hash_pesos.hexdigest()
    return {
        "checkpoint": str(ruta) if ruta is not None else None,
        "sha256_checkpoint": huella,
        "dispositivo": str(dispositivo),
        "versiones": {nombre: metadatos_paquetes.version(nombre)
                      for nombre in ("cellpose", "torch", "numpy", "tifffile", "scipy")},
    }


def segmentar_plano(modelo, imagen: np.ndarray, excluida: np.ndarray,
                  configuracion: Configuracion, pixeles_minimos: int) -> np.ndarray:
    if not np.any(imagen):
        return np.zeros(imagen.shape, dtype=np.uint32)

    # La señal DAPI extraída del LUT azul ocupa el primer canal explícito.
    ceros = np.zeros_like(imagen)
    entrada_modelo = np.stack((imagen, ceros, ceros), axis=-1)
    etiquetas = np.asarray(modelo.eval(
        entrada_modelo, channel_axis=-1, batch_size=1, normalize=False,
        diameter=None, do_3D=False, max_size_fraction=1.0,
        flow_threshold=configuracion.umbral_flujo,
        cellprob_threshold=configuracion.umbral_probabilidad,
        min_size=pixeles_minimos,
    )[0])
    if (etiquetas.shape != imagen.shape or not np.issubdtype(etiquetas.dtype, np.integer)
            or np.any(etiquetas < 0) or np.any(etiquetas > np.iinfo(np.uint32).max)):
        raise ValueError(f"Etiquetas Cellpose inválidas: {etiquetas.shape}, {etiquetas.dtype}")

    etiquetas = etiquetas.astype(np.uint32, copy=True)
    etiquetas[excluida] = 0
    return etiquetas
