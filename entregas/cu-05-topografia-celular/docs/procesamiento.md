# Procesamiento de pilas nucleares

## Organización del código

El paquete `src/topografia_celular/` concentra el procesamiento reutilizable.
Los nombres del proyecto, comentarios y documentación están en español. Los
parámetros de bibliotecas y el esquema previo del inventario conservan sus
nombres para mantener compatibilidad con Cellpose, TIFF y el notebook.

| Módulo | Responsabilidad |
|---|---|
| `configuracion.py` | Parámetros de ejecución y rutas predeterminadas. |
| `entrada.py` | Lectura Leica/TIFF, canal DAPI, orden Z y comprobación de dimensiones. |
| `preprocesado.py` | Propuesta de exclusión, proyección al submuestreo y contraste. |
| `modelo.py` | Carga de Cellpose, inferencia por plano y liberación de recursos. |
| `exportacion.py` | Procedencia, incidencias por instancia y escritura segura del registro JSON. |
| `ejecucion.py` | Preparación de pilas, procesamiento y seguimiento del lote. |
| `cli.py` | Argumentos y comandos de terminal. |
| `auditoria.py` | Inventario de todos los canales y overlays de las exportaciones. |

## Entorno y comandos

Desde la carpeta del equipo y con el entorno `vpc2` activo:

```bash
python -m pip install --no-deps --no-build-isolation -e .
python -m topografia_celular --todas --solo-validar
python -m topografia_celular --todas --paso-xy 2
```

En un entorno nuevo, `python -m pip install -e '.[cellpose]'` instala el paquete
y las dependencias de inferencia; el notebook requiere además sus dependencias
en `notebooks/requirements-base.txt`.

La comprobación previa recorre las seis pilas antes de cargar el modelo. Los
pesos se cargan una sola vez por lote. La primera inferencia puede descargarlos
si todavía no están en la caché local.

Para comprobar una parte de una pila sin sobrescribir ejecuciones anteriores:

```bash
python -m topografia_celular --pila "control 1" --z-inicio 20 --z-fin 30
python -m topografia_celular.auditoria
```

`--z-fin` es exclusivo. El rango limita lo que se segmenta; la validación y el
contraste global siguen usando la adquisición completa. La normalización por
plano se selecciona con `--normalizacion plano`. Se conservan los ajustes del
piloto como valores predeterminados; que una configuración funcione visualmente
en un caso no demuestra su exactitud en las demás pilas.

## Exclusión de anotaciones

La detección automática propone un rectángulo alrededor del texto y la barra
del margen inferior. Debe revisarse visualmente. Si ocupa más del 12% de la
imagen, la comprobación se detiene para que se defina una exclusión manual con
`--pila` y `--roi y0,y1,x0,x1`. No se reutiliza una ROI manual para todas las
pilas, que tienen dimensiones distintas. `--sin-exclusion` permite desactivarla
de forma explícita cuando corresponda.

La ROI siempre está en píxeles nativos. Primero se construye su máscara nativa
y después se aplica el mismo submuestreo que a la imagen. Esa máscara se utiliza
para el contraste, la entrada al modelo y la salida; las anotaciones no deben
quedar desplazadas cuando `--paso-xy` es mayor que uno.

## Salidas y progreso

Cada ejecución crea una carpeta nueva en `tmp/segmentacion-cellpose/`, o en la
ruta indicada con `--salida`. Se rechazan rutas existentes y salidas dentro de
los datos originales. En un lote hay una subcarpeta por pila; en una ejecución
individual se usa la subcarpeta `mascaras/`.

```text
lote-<fecha-UTC>/
  resumen.json
  control-1/
    procedencia.json
    zona-excluida.tif
    mascara-z000.tif
    mascara-z001.tif
    ...
  canales-g10/
    ...
```

Cada máscara usa `uint32`: cero es fondo y los valores positivos son instancias
locales al plano. El JSON conserva el orden Z, unidades, espaciado de trabajo
Z/Y/X, desplazamiento del primer plano, parámetros, versiones, exclusión y
huellas de los archivos de entrada y de los pesos. Se registran las instancias
que tocan un borde o la zona excluida, sin eliminarlas automáticamente.

`resumen.json` distingue comprobación previa, ejecución y fallo. Cada pila
conserva su progreso en `procedencia.json` después de cada plano. Si una falla,
se continúa con las siguientes y el programa devuelve código 1. Una interrupción
con Ctrl+C detiene el lote, conserva el progreso y devuelve código 130. Las
pilas que no llegaron a ejecutarse quedan pendientes.

Conservar el progreso no implica reanudar automáticamente una ejecución. Para
repetir una pila fallida, usar `--pila` con una carpeta nueva y revisar el error
anterior. Una carpeta parcial no debe consumirse como una pila completa: el
módulo posterior debe comprobar `estado_ejecucion == "completada"`.

Estas son propuestas automáticas 2D pendientes de revisión. Para medir el
volumen por núcleo falta asociar las instancias entre planos y revisar uniones,
fragmentaciones y truncamientos. No se exportan todavía volúmenes por núcleo.

## Verificación

```bash
python -m unittest discover -s tests -v
```

Las pruebas sintéticas comprueban coordenadas de exclusión, contraste, escala,
exportación, conservación de originales, carga única del modelo, fallos e
interrupciones. No miden la calidad biológica de la segmentación.
