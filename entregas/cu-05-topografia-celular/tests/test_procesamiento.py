"""Pruebas del flujo y la calibración; no evalúan la calidad de Cellpose."""

from contextlib import contextmanager, redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np
import tifffile

from topografia_celular.cli import ejecutar
from topografia_celular.preprocesado import crear_mascara_exclusion, estimar_limites_globales


class ModeloSimulado:
    def __init__(self, fallo_en: int | None = None, interrupcion: bool = False):
        self.llamadas = 0
        self.fallo_en = fallo_en
        self.interrupcion = interrupcion

    def eval(self, imagen, **parametros):
        self.llamadas += 1
        if self.llamadas == self.fallo_en:
            if self.interrupcion:
                raise KeyboardInterrupt()
            raise RuntimeError("Fallo de inferencia simulado")
        return (np.ones(imagen.shape[:2], dtype=np.int32),)


def crear_pila(datos: Path, nombre: str) -> Path:
    carpeta = datos / nombre
    carpeta.mkdir(parents=True)
    dimensiones = """
      <DimensionDescription DimID="1" NumberOfElements="11" Length="0.000001" Unit="m"/>
      <DimensionDescription DimID="2" NumberOfElements="9" Length="0.0000008" Unit="m"/>
      <DimensionDescription DimID="3" NumberOfElements="3" Length="0.000001" Unit="m"/>
    """
    (carpeta / "captura.xml").write_text(
        f"<Raiz>{dimensiones}<ChannelDescription ChannelTag='0'><ChannelProperty>"
        "<Key>DyeName</Key><Value>DAPI</Value></ChannelProperty></ChannelDescription></Raiz>"
    )
    (carpeta / "captura_Properties.xml").write_text("<Raiz/>")
    for z in range(3):
        imagen = np.arange(99, dtype=np.uint8).reshape(9, 11) + z
        tifffile.imwrite(carpeta / f"captura_z{z:02d}_ch00_SV.tif", imagen)
    return carpeta


class PruebasProcesamiento(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporal.cleanup)
        self.raiz = Path(self.temporal.name)
        self.datos = self.raiz / "datos"
        self.datos.mkdir()

    def ejecutar_con_modelo(self, opciones: list[str], modelo: ModeloSimulado) -> int:
        @contextmanager
        def sesion(configuracion):
            yield modelo, SimpleNamespace(type="cpu")

        with patch("topografia_celular.ejecucion.sesion_modelo", side_effect=sesion) as carga:
            with patch("topografia_celular.ejecucion.describir_modelo", return_value={}):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    codigo = ejecutar(["--datos", str(self.datos), *opciones])
        self.assertEqual(carga.call_count, 1)
        return codigo

    def test_exclusion_respeta_coordenadas_nativas_con_distintos_pasos(self):
        for paso in (1, 2, 3):
            for roi in ((1, 6, 3, 8), (4, 7, 0, 5)):
                original = np.zeros((7, 9), dtype=bool)
                y0, y1, x0, x1 = roi
                original[y0:y1, x0:x1] = True
                np.testing.assert_array_equal(
                    crear_mascara_exclusion(original.shape, roi, paso), original[::paso, ::paso]
                )

    def test_contraste_no_incluye_la_zona_excluida(self):
        imagen = np.arange(63, dtype=np.uint8).reshape(7, 9)
        imagen[3:7, 5:9] = 255
        ruta = self.raiz / "plano.tif"
        tifffile.imwrite(ruta, imagen)
        mascara = crear_mascara_exclusion(imagen.shape, (3, 7, 5, 9), 2)
        esperado = np.percentile(imagen[::2, ::2][~mascara], (1.0, 99.8))
        obtenido = estimar_limites_globales([(0, ruta)], (3, 7, 5, 9), 2, (1.0, 99.8))
        np.testing.assert_allclose(obtenido, esperado)

    def test_lote_guarda_escala_mascaras_y_una_sola_carga_del_modelo(self):
        for nombre in ("pila A", "pila B"):
            crear_pila(self.datos, nombre)
        originales = {ruta: ruta.read_bytes() for ruta in self.datos.rglob("*.tif")}
        salida = self.raiz / "lote"
        modelo = ModeloSimulado()
        codigo = self.ejecutar_con_modelo(["--todas", "--salida", str(salida)], modelo)
        self.assertEqual(codigo, 0)
        self.assertEqual(modelo.llamadas, 6)
        resumen = json.loads((salida / "resumen.json").read_text())
        self.assertEqual(resumen["estado"], "completado")
        for entrada in resumen["pilas"]:
            carpeta = salida / entrada["carpeta"]
            procedencia = json.loads((carpeta / "procedencia.json").read_text())
            np.testing.assert_allclose(procedencia["spacing_mascara_um_zyx"], [0.5, 0.2, 0.2])
            self.assertEqual([plano["z_original"] for plano in procedencia["planos"]], [0, 1, 2])
            self.assertEqual(procedencia["estado_ejecucion"], "completada")
            etiquetas = tifffile.imread(carpeta / "mascara-z000.tif")
            self.assertEqual(etiquetas.shape, (5, 6))
            self.assertEqual(etiquetas.dtype, np.uint32)
        for ruta, contenido in originales.items():
            self.assertEqual(ruta.read_bytes(), contenido)

    def test_exclusion_tambien_se_aplica_a_las_etiquetas_y_al_origen_z(self):
        crear_pila(self.datos, "pila A")
        salida = self.raiz / "individual"
        self.ejecutar_con_modelo([
            "--pila", "pila A", "--roi", "3,9,5,11", "--z-inicio", "1",
            "--salida", str(salida),
        ], ModeloSimulado())
        carpeta = salida / "mascaras"
        etiquetas = tifffile.imread(carpeta / "mascara-z001.tif")
        exclusion = crear_mascara_exclusion((9, 11), (3, 9, 5, 11), 2)
        self.assertFalse(etiquetas[exclusion].any())
        self.assertTrue(etiquetas[~exclusion].all())
        procedencia = json.loads((carpeta / "procedencia.json").read_text())
        self.assertEqual(procedencia["origen_mascara_um_zyx"], [0.5, 0.0, 0.0])

    def test_fallo_conserva_progreso_y_permite_continuar_la_siguiente_pila(self):
        for nombre in ("pila A", "pila B"):
            crear_pila(self.datos, nombre)
        salida = self.raiz / "lote"
        codigo = self.ejecutar_con_modelo(
            ["--todas", "--salida", str(salida)], ModeloSimulado(fallo_en=2)
        )
        self.assertEqual(codigo, 1)
        resumen = json.loads((salida / "resumen.json").read_text())
        self.assertEqual(resumen["estado"], "con_errores")
        self.assertEqual([pila["estado"] for pila in resumen["pilas"]], ["error", "completada"])
        procedencia = json.loads((salida / "pila-a/procedencia.json").read_text())
        self.assertEqual(procedencia["estado_ejecucion"], "error")
        self.assertEqual(len(procedencia["planos"]), 1)

    def test_interrupcion_conserva_el_registro_parcial(self):
        crear_pila(self.datos, "pila A")
        salida = self.raiz / "interrupcion"
        with self.assertRaises(KeyboardInterrupt):
            self.ejecutar_con_modelo(
                ["--todas", "--salida", str(salida)], ModeloSimulado(fallo_en=2, interrupcion=True)
            )
        resumen = json.loads((salida / "resumen.json").read_text())
        self.assertEqual(resumen["estado"], "interrumpido")
        procedencia = json.loads((salida / "pila-a/procedencia.json").read_text())
        self.assertEqual(procedencia["estado_ejecucion"], "interrumpida")
        self.assertEqual(len(procedencia["planos"]), 1)

    def test_validacion_detecta_un_plano_ausente_antes_de_cargar_el_modelo(self):
        carpeta = crear_pila(self.datos, "pila A")
        (carpeta / "captura_z01_ch00_SV.tif").unlink()
        salida = self.raiz / "validacion"
        with patch("topografia_celular.ejecucion.sesion_modelo") as carga:
            with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                ejecutar(["--datos", str(self.datos), "--todas", "--solo-validar", "--salida", str(salida)])
        carga.assert_not_called()
        self.assertFalse(salida.exists())

    def test_validacion_no_carga_modelo_y_no_sobrescribe(self):
        crear_pila(self.datos, "pila A")
        salida = self.raiz / "validacion"
        opciones = ["--datos", str(self.datos), "--todas", "--solo-validar", "--salida", str(salida)]
        with patch("topografia_celular.ejecucion.sesion_modelo") as carga, redirect_stdout(io.StringIO()):
            self.assertEqual(ejecutar(opciones), 0)
        carga.assert_not_called()
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            ejecutar(opciones)


if __name__ == "__main__":
    unittest.main()
