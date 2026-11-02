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
disponibles muestran la señal nuclear; la geometría del scaffold se incorpora
como información experimental cuando esté documentada.

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
  sencilla, cuando existan muestras independientes suficientes.

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
respetar la calibración de cada eje. `G10` se conserva como etiqueta experimental:
su nombre por sí solo no determina una dimensión física del patrón.

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
`entregas/cu-05-topografía-celular/`, dentro del fork de la asignatura.

| Ruta | Contenido |
|---|---|
| `README.md` | Presentación, alcance y organización del proyecto. |
| `specs/vision-por-computador.md` | Definición funcional de segmentación y medición nuclear. |
| `specs/integracion-llm-few-shot.md` | Definición funcional del predictor LLM con ejemplos en contexto. |
| `scripts/` | Código de auditoría de metadatos y prototipos de procesamiento. |
| `notebooks/` | Exploración de datos, comparación de máscaras y dependencias del piloto. |
| `docs/` | Bibliografía, requisitos de la asignatura y planificación del proyecto. |
| `data/` | Imágenes y metadatos experimentales locales; excluidos de Git. |
| `tmp/` | Resultados, máscaras, pesos y archivos temporales; excluidos de Git. |

La primera entrega comprende este README y las dos specs. La arquitectura y las
decisiones de implementación se documentarán en la siguiente entrega.
