# CU-05 · Topografía del scaffold y morfología nuclear

Proyecto de **Proyecto Integrador de Inteligencia Artificial II**, del Grado
en Inteligencia Artificial de la Universidade de Santiago de Compostela.

## Qué es el proyecto

Desarrollamos una herramienta para estudiar la relación entre la topografía de
un scaffold —el soporte sobre el que crecen las células— y la forma de sus
núcleos. Combinamos visión por computador para obtener medidas nucleares desde
imágenes de microscopía con un módulo experimental de predicción mediante un
LLM con ejemplos en contexto (*few-shot*).

El flujo previsto es:

1. Obtener máscaras revisables de los núcleos a partir de las pilas de imágenes.
2. Extraer medidas geométricas con la calibración física del microscopio.
3. Vincular las medidas con la topografía y la muestra experimental de origen.
4. Proporcionar al LLM unos pocos ejemplos topografía–morfología y consultar la
   morfología esperada para una topografía descrita.

La herramienta se dirige al grupo investigador que aporta los datos y necesita
analizar la respuesta nuclear a distintas condiciones de cultivo. Las imágenes
disponibles muestran la señal nuclear; el scaffold se caracteriza mediante su
tipo de patrón y su medida nominal, documentados en la información experimental
y el artículo de referencia.

## Motivación

Las características de un soporte pueden influir en la organización celular y
en la forma del núcleo. Para estudiar esa relación necesitamos primero convertir
las imágenes en medidas comparables y trazables. Después queremos explorar si
un LLM puede aprovechar pocos ejemplos para estimar esas medidas a partir de la
topografía.

El interés del proyecto está en conectar ambos pasos y evaluar sus límites con
los datos reales disponibles. Las máscaras se revisarán visualmente: actualmente
no disponemos de ground truth para cuantificar la exactitud de la segmentación.
Las medidas extraídas servirán para contrastar las predicciones, teniendo en
cuenta que también dependen de la calidad de las máscaras.

## Alcance

### Incluido

- Carga de las pilas TIFF y de sus metadatos XML, selección del canal nuclear
  DAPI, ordenación de las capas y lectura de la calibración X/Y/Z.
- Segmentación por instancias, inspección visual y registro de correcciones o
  incidencias. El piloto actual prueba Cellpose en planos 2D independientes.
- Asociación de las máscaras entre capas antes de calcular medidas por núcleo:
  volumen, ejes de un elipsoide equivalente y relaciones entre ejes.
- Exportación de máscaras, medidas y procedencia de cada resultado.
- Construcción de ejemplos topografía–morfología y de un prototipo LLM
  *few-shot* con respuestas estructuradas y evaluación frente a una referencia
  sencilla cuando existan al menos 4 grupos experimentales independientes
  (mínimo 2 grupos para ejemplos en contexto y 2 casos independientes de prueba).

### Fuera de esta primera versión

- Reconstruir la geometría o composición del scaffold desde las imágenes nucleares.
- Generar una imagen nuclear completa a partir de una topografía.
- Inferir fuerzas, tensiones o deformaciones temporales de un núcleo sin una
  referencia experimental adecuada.
- Medir orientación respecto al scaffold sin conocer su referencia geométrica.
- Incorporar superficie y esfericidad antes de comprobar su sensibilidad a la
  segmentación y al espaciado entre capas.
- Afirmar generalización a topografías nuevas si los datos no permiten evaluarla.

## Datos disponibles y estado inicial

Disponemos de **seis carpetas de pilas**: `control 1`, `control 2`, `control 3`,
`canales g10`, `canales g10 2` y `canales g10 3`. Contienen 407 planos DAPI y sus
metadatos XML. Una carpeta, un plano y un núcleo representan unidades distintas;
la independencia experimental de las muestras debe confirmarse antes de evaluar
el predictor.

Los TIFF son exportaciones RGB de visualización con anotaciones integradas. El
procesamiento debe excluir texto y barras de escala, conservar los originales y
respetar la calibración de cada eje. Del scaffold disponemos del tipo de patrón
y su medida nominal, descritos en el artículo de referencia. Estas son las
entradas previstas para el LLM: se registrarán el valor, la unidad y qué dimensión
describe la medida. Para un control liso, una medida de patrón puede no aplicar.
La correspondencia con etiquetas como `G10` se recoge desde esa descripción.

Ya existe un inventario de metadatos y un notebook exploratorio de segmentación.
Cellpose es el candidato actual del piloto; la asociación entre capas, las
medidas finales y la integración LLM forman parte del trabajo por desarrollar.

## Funcionalidades especificadas

| Spec | Funcionalidad |
|---|---|
| [Visión por computador](specs/vision-por-computador.md) | Obtener máscaras nucleares revisadas y medidas geométricas desde las pilas calibradas. |
| [Integración LLM few-shot](specs/integracion-llm-few-shot.md) | Construir ejemplos y estimar morfología nuclear desde descriptores de topografía, con evaluación y trazabilidad. |

## Equipo

Los tres integrantes comparten la preparación de datos, la visión por computador,
la integración LLM, la evaluación y la documentación del proyecto.

| Integrante | Rol | Correo de contacto |
|---|---|---|
| Pablo Pérez Rodríguez | Desarrollo, validación y documentación (compartido) | pablo.perez.rodriguez2@rai.usc.es |
| Alba Castro Groba | Desarrollo, validación y documentación (compartido) | alba.castro.groba@rai.usc.es |
| Franco Alonso Cardozo | Desarrollo, validación y documentación (compartido) | franco.alonso@rai.usc.es |

## Estructura de la carpeta

Todo el material del equipo se mantiene en
`entregas/cu-05-topografia-celular/`, dentro del fork de la asignatura.

| Ruta | Contenido |
|---|---|
| `README.md` | Presentación, alcance y organización del proyecto. |
| `specs/vision-por-computador.md` | Definición funcional de segmentación y medición nuclear. |
| `specs/integracion-llm-few-shot.md` | Definición funcional del predictor LLM con ejemplos en contexto. |
| `src/topografia_celular/` | Paquete Python: lectura, preprocesado, Cellpose, exportación y ejecución por lotes. |
| `tests/` | Pruebas de exclusión, escala, exportación y gestión de fallos. |
| `pyproject.toml` | Instalación del paquete y comandos de terminal. |
| `notebooks/` | Exploración de datos, comparación de máscaras y dependencias del piloto. |
| `docs/` | Bibliografía, requisitos de la asignatura y planificación del proyecto. |
| `data/` | Imágenes y metadatos experimentales locales; excluidos de Git. |
| `tmp/` | Resultados, máscaras, pesos y archivos temporales; excluidos de Git. |

La primera entrega comprende este README y las dos specs. La arquitectura y las
decisiones de implementación se documentarán en la siguiente entrega.

## Procesar las pilas

El procesamiento se ejecuta desde el paquete Python; el notebook se mantiene
para exploración. En el entorno `vpc2`, que ya contiene las dependencias del
piloto, instalar el paquete local desde la carpeta del equipo:

```bash
python -m pip install --no-deps --no-build-isolation -e .
python -m topografia_celular --todas --solo-validar
python -m topografia_celular --todas --paso-xy 2
```

La comprobación previa valida archivos, calibración, exclusión y contraste, sin
ejecutar Cellpose. Las seis pilas actuales contienen 407 planos DAPI; otros
canales y overlays quedan fuera del lote de segmentación. La configuración
predeterminada conserva la del piloto: `cpsam_v2`, contraste global, paso XY 2
y umbrales 0.5/0.4. `--paso-xy 1` conserva la resolución nativa; cualquier cambio
de configuración requiere revisar las máscaras resultantes.

Las máscaras y su procedencia se guardan bajo `tmp/segmentacion-cellpose/`.
Todavía tienen identificadores locales a cada plano: la asociación en Z y el
cálculo de volúmenes son pasos posteriores.

Ver [guía de procesamiento](docs/procesamiento.md) para estructura de salidas,
opciones, incidencias y pruebas.
