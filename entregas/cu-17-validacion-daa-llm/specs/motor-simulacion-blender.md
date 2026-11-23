# Optimización automática de escenarios

## 1. Qué hay que construir

Se debe desarrollar un sistema de optimización automática de los parámetros de generación de escenarios sintéticos mediante un modelo de lenguaje ya existente (LLM). Esta funcionalidad se integrará con el script de Python desarrollado en PIIA 1 (implementando las nuevas condiciones de escenario necesarias) y con el modelo de detección YOLO-X, creando un ciclo iterativo de generación, evaluación y ajuste de parámetros.

El sistema permitirá definir inicialmente los parámetros que se desean optimizar y sus respectivos rangos de valores como, por ejemplo, la intensidad de la niebla. A partir de esta configuración inicial, el LLM se encargará de proponer los valores que se evaluarán en cada iteración, teniendo en cuenta los resultados obtenidos en las ejecuciones anteriores. Las configuraciones propuestas se aplicarán automáticamente al script de Python desarrollado en PIIA 1, que generará las imágenes y sus correspondientes anotaciones en formato COCO. A continuación, se ejecutará el modelo YOLO-X sobre estas para obtener las métricas necesarias para valorar el rendimiento de cada configuración. El LLM será responsable de analizar estos resultados, comparar las distintas configuraciones y decidir qué parámetros es mejor modificar o mantener. Para eso, este comenzará explorando de forma amplia los rangos definidos y después concentrará la búsqueda en aquellas regiones que tengan mejores resultados con el objetivo de identificar los valores más adecuados. Por último, el LLM devuelve un json con las configuraciones utilizadas y las métricas devueltas por estas.

El proceso iterativo del LLM se repetirá hasta que este determine que la evaluación de nuevos valores de parámetros no ofrece mejoras significativas en el rendimiento del modelo.

## 2. Por qué

La funcionalidad pretende automatizar la búsqueda de los parámetros de generación de escenarios que permiten obtener un mejor rendimiento del modelo de detección YOLO-X.

La modificación manual de los parámetros y la ejecución individual de mucha cantidad de experimentos necesitan tiempo y dificultan la exploración de los distintos valores posibles. Además, no siempre resulta evidente cómo afectan los cambios en las condiciones de los escenarios (como la intensidad de la niebla) al rendimiento del modelo YOLO-X.

Mediante el uso de un LLM como componente de decisión, se pretende utilizar los resultados de experimentos anteriores para orientar las siguientes pruebas, reducir evaluaciones innecesarias y concentrar la búsqueda en las regiones con mayor rendimiento.

De este modo no habrá necesidad de modificar manualmente el código en cada iteración.

## 3. Restricciones

- **Integración con PIIA 1:** el sistema deberá reutilizar el script de generación de escenarios de PIIA 1, lo que necesitará una mejora de este script para adaptarse a las necesidades del LLM o el aumento de requisitos de parámetros.

- **Responsabilidad del LLM:** el LLM propondrá los valores de los parámetros, analizará los resultados y considerará el criterio de parada.

- **Rangos:** todas las configuraciones propuestas deberán respetar los rangos, tipos de datos y restricciones definidos para cada parámetro. Las configuraciones no válidas deberán rechazarse antes de ejecutar el generador.

- **Comparación:** las configuraciones deberán evaluarse bajo las mismas condiciones. El conjunto de evaluación y la configuración de YOLO-X deberán permanecer fijos durante la comparación y deberá definirse una métrica principal de las devueltas por YOLO-X para comparar las configuraciones.

- **Asociación etiquetas:** cada evaluación deberá quedar asociada a los valores de los parámetros utilizados y a las métricas obtenidas. 

- **Criterios de parada:** la búsqueda deberá finalizar cuando el LLM asi lo decida, pudiendo tardar bastante en la ejecución del proceso iterativo

## 4. Criterios de aceptación

- **Configuración de parámetros:** el sistema permite definir los rangos iniciales de los parámetros a optimizar y utiliza esta información para generar configuraciones de prueba.

- **Integración con el script de Python:** los valores propuestos por el LLM se utilizan automáticamente en el script de PIIA 1, sin necesidad de modificar manualmente el código entre iteraciones.

- **Generación de datos:** para cada configuración válida, el sistema genera los escenarios correspondientes y sus anotaciones en formato COCO.

- **Evaluación con YOLO-X:** el sistema ejecuta la evaluación de cada configuración válida y registra las métricas seleccionadas para comparar su rendimiento.

- **Comparación de resultados:** el sistema identifica cuál de las configuraciones evaluadas obtiene el mejor resultado según la métrica principal definida.

- **Optimización rangos:** las siguientes propuestas del LLM utilizan las configuraciones y resultados de las anteriores y permiten explorar nuevas regiones de los rangos o refinar la búsqueda en regiones interesantes.

- **SIN evaluaciones redundantes:** el sistema no repite automáticamente una configuración ya evaluada.

- **Parada del bucle:** el proceso se detiene y no continúa ejecutando iteraciones indefinidamente.

- **Resultados:** al finalizar, el sistema devuelve el json y almacena las configuraciónes encontradas y las métricas asociadas.

- **Gestión de errores:** si falla la generación de escenarios o la evaluación de YOLO-X el sistema registra el error.