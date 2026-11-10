"""Exclusión de anotaciones y normalización de la señal nuclear."""

import math
from pathlib import Path

import numpy as np

from .entrada import leer_plano_dapi


def crear_mascara_exclusion(
    forma_yx: tuple[int, int], roi: tuple[int, int, int, int] | None, paso: int,
) -> np.ndarray:
    """Proyectar exactamente la exclusión nativa sobre la rejilla submuestreada."""
    if paso < 1:
        raise ValueError("El paso XY debe ser >= 1.")
    mascara = np.zeros(forma_yx, dtype=bool)
    if roi is not None:
        y0, y1, x0, x1 = roi
        ny, nx = forma_yx
        if not (0 <= y0 < y1 <= ny and 0 <= x0 < x1 <= nx):
            raise ValueError(f"ROI fuera de imagen Y={ny}, X={nx}: {roi}")
        mascara[y0:y1, x0:x1] = True
    muestreada = mascara[::paso, ::paso].copy()
    if muestreada.all():
        raise ValueError("La exclusión no deja píxeles válidos en la resolución de trabajo.")
    return muestreada


def proponer_roi_anotaciones(
    planos: list[tuple[int, Path]], forma_yx: tuple[int, int],
) -> tuple[int, int, int, int] | None:
    """Proponer una exclusión para el texto y la barra del margen inferior."""
    ny, nx = forma_yx
    candidatos = np.zeros((ny, nx), dtype=bool)
    hay_rgb = False
    for _, ruta in planos:
        _, rgb = leer_plano_dapi(ruta)
        if rgb is None:
            continue
        hay_rgb = True
        escala = np.iinfo(rgb.dtype).max if np.issubdtype(rgb.dtype, np.integer) else 1.0
        normalizada = rgb.astype(np.float32) / escala
        claros_neutros = (np.ptp(normalizada, axis=-1) < 0.05) & (normalizada.min(axis=-1) > 0.35)
        claros_neutros[:int(0.8 * ny)] = False
        candidatos |= claros_neutros
    if not hay_rgb or not candidatos.any():
        return None
    yy, xx = np.where(candidatos)
    roi = (max(0, int(yy.min()) - 4), min(ny, int(yy.max()) + 5),
           max(0, int(xx.min()) - 4), min(nx, int(xx.max()) + 5))
    superficie = (roi[1] - roi[0]) * (roi[3] - roi[2])
    if superficie > 0.12 * ny * nx:
        raise ValueError("La exclusión automática ocupa >12% del plano; usa --roi o --sin-exclusion.")
    return roi


def estimar_limites_globales(
    planos: list[tuple[int, Path]], roi: tuple[int, int, int, int] | None,
    paso: int, percentiles: tuple[float, float], semilla: int = 0,
) -> tuple[float, float]:
    """Estimar un contraste común mediante un muestreo reproducible de toda Z."""
    generador = np.random.default_rng(semilla)
    muestras = []
    for _, ruta in planos:
        imagen, _ = leer_plano_dapi(ruta)
        excluida = crear_mascara_exclusion(imagen.shape, roi, paso)
        imagen = imagen[::paso, ::paso]
        valores = imagen[~excluida]
        if valores.size:
            # Limitar la memoria del muestreo manteniendo representación de todos los planos.
            cantidad = min(25_000, valores.size)
            indices = (
                generador.choice(valores.size, size=cantidad, replace=False)
                if cantidad < valores.size else None
            )
            muestras.append(valores[indices] if indices is not None else valores)
    if not muestras:
        raise ValueError("No hay píxeles válidos para normalizar.")
    inferior, superior = np.percentile(np.concatenate(muestras), percentiles)
    if not np.isfinite(inferior) or not np.isfinite(superior) or superior <= inferior:
        raise ValueError("Rango de intensidad inválido; revisa canal y exclusión.")
    return float(inferior), float(superior)


def normalizar_plano(muestreada: np.ndarray, excluida: np.ndarray,
                    limites: tuple[float, float] | None) -> tuple[np.ndarray, tuple[float, float]]:
    """Usar la misma exclusión para estimar contraste y preparar la entrada."""
    if not np.isfinite(muestreada).all():
        raise ValueError("La imagen contiene intensidades no finitas.")
    inferior, superior = limites if limites is not None else np.percentile(muestreada[~excluida], (1.0, 99.8))
    inferior, superior = float(inferior), float(superior)
    if not math.isfinite(inferior) or not math.isfinite(superior) or superior < inferior:
        raise ValueError(f"Rango de intensidad inválido: {inferior}, {superior}.")
    # Un plano constante no debe inventar contornos ni interrumpir una pila válida.
    imagen = (np.zeros_like(muestreada, dtype=np.float32) if superior == inferior else
             np.clip((muestreada - inferior) / (superior - inferior), 0, 1).astype(np.float32))
    imagen[excluida] = 0
    return imagen, (inferior, superior)
