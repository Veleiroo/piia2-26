# Preparación del dataset de imágenes y pesos

## Qué construir

Queremos desarrollar una funcionalidad que transforme las grabaciones individuales de los pollos y sus registros de pesaje en un dataset de imágenes etiquetadas, preparado para entrenar y evaluar el estimador de peso. Para ello, el sistema recibirá los vídeos y un registro que permita relacionar cada grabación, o intervalo de grabación, con el identificador del animal y su peso real en gramos. A partir de esta información, extraerá fotogramas con una frecuencia configurable y generará un fichero de etiquetas que asocie cada imagen con el animal, el peso, la sesión de captura y el vídeo de procedencia. Finalmente, permitirá dividir los datos en conjuntos de entrenamiento, validación y test, manteniendo juntas todas las imágenes de un mismo individuo.

## Por qué

Las grabaciones obtenidas en la explotación no pueden utilizarse directamente para entrenar el estimador, necesitamos convertirlas en imágenes y asegurar que cada una tenga asociado el peso real del animal que aparece en ella. Esta funcionalidad permitirá organizar los datos de forma consistente y reducir los errores de asociación entre imágenes y pesajes. También facilitará ampliar el dataset a través de nuevas jornadas de captura. La separación por individuos será especialmente importante para evaluar si el modelo puede estimar el peso de pollos que no haya visto durante el entrenamiento, evitando que fotogramas similares del mismo animal aparezcan en conjuntos diferentes.

## Restricciones

La funcionalidad trabajará con grabaciones o intervalos previamente identificados en los que aparezca un único pollo. La identificación del animal y su asociación con el pesaje deberán registrarse durante la recogida de datos. El sistema no intentará deducir automáticamente a qué pollo corresponde cada vídeo. Cada intervalo utilizado deberá tener un identificador de animal, una sesión de captura y un peso de referencia positivo expresado en gramos, obtenido en esa sesión. Si un mismo animal se graba en varias sesiones y puede reconocerse de forma fiable, conservará el mismo identificador, aunque su peso pueda cambiar.

Los vídeos originales se conservarán sin modificaciones. La extracción de fotogramas tendrá una frecuencia configurable y permitirá seleccionar los intervalos válidos de cada grabación. Antes de incorporar las imágenes al dataset definitivo, se realizará una revisión para excluir aquellas en las que no aparezca un único pollo suficientemente visible, por ejemplo por desenfoque acusado o por quedar cortado en el encuadre. Esta revisión podrá ser manual y no implica desarrollar un modelo automático de control de calidad.

Todos los fotogramas de un mismo animal deberán permanecer en un único conjunto: entrenamiento, validación o test. La división se realizará mediante proporciones y una semilla configurables, dejando registrada la asignación de cada individuo. 

Esta spec no incluye el entrenamiento de modelos ni la detección o segmentación de pollos en escenas con varios animales. Las transformaciones específicas que necesite el estimador, como el redimensionado o la normalización, se definirán de forma coordinada con su módulo.

## Criterios de aceptación

La funcionalidad se considerará correctamente implementada cuando se cumplan los siguientes criterios:

- Dado un vídeo legible y un registro válido de sus intervalos, animales y pesajes, se extraen fotogramas de los intervalos indicados conforme a la frecuencia configurada.
- Cada imagen incorporada al dataset dispone de una entrada en un fichero CSV que incluye, como mínimo, su ruta, el identificador del animal, el peso en gramos, la sesión de captura, el vídeo de origen y el instante del fotograma.
- Si falta el identificador del animal, el peso o la asociación inequívoca con el intervalo de vídeo, los datos afectados no se incorporan al dataset y se registra el motivo.
- Los pesos ausentes, no numéricos, nulos o negativos se rechazan mediante un error identificable.
- Las imágenes descartadas durante la revisión quedan identificadas junto con el motivo de exclusión y no aparecen en el dataset definitivo.
- Los conjuntos de entrenamiento, validación y test no comparten identificadores de animales. La regla de agrupación utilizada para garantizar esta separación queda documentada.
- La asignación a los conjuntos puede reproducirse utilizando los mismos datos de entrada, configuración y semilla. Si no hay suficientes grupos independientes para crear los tres conjuntos, el sistema informa de ello.
- Se genera un resumen con el número de imágenes y animales por conjunto, el rango de pesos y las incidencias o descartes registrados.
- Todas las rutas incluidas en el CSV corresponden a imágenes existentes, y los vídeos originales permanecen sin modificaciones.
