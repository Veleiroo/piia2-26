# Extracción de pollos individuales

## Qué construir

Queremos desarrollar una funcionalidad que reciba la imagen de una escena de la nave con cero, uno o varios pollos, localice a los animales y genere una imagen individual (recorte) por cada detección aceptada.

Para cada detección, la funcionalidad guarda:

- Identificador de la imagen original y de la detección.
- Coordenadas del rectángulo que delimita al pollo, expresadas sobre la imagen original.
- Confianza de la detección.
- Recorte generado y sus coordenadas sobre la imagen original, si la detección es aceptada.
- Estado de la detección (aceptada o descartada) y motivo de descarte, si corresponde.
- Máscara del animal, solo si se adopta segmentación.

Esta funcionalidad es el puente entre las escenas con varios pollos de la segunda fase de captura y el módulo de estimación de peso individual, que trabaja con un único pollo por imagen. Sus recortes son la entrada de ese módulo.

**Detección y segmentación.** La detección localiza al pollo mediante un rectángulo, y el recorte puede incluir fondo o parte de otro animal. La segmentación identifica los píxeles del propio pollo y permite aislar mejor su silueta. El resultado mínimo exigido a esta spec es la **detección con recorte rectangular**. La segmentación se plantea como ampliación si la evaluación muestra que el fondo o los animales vecinos perjudican la estimación del peso. Sus criterios de aceptación se añadirían entonces como extensión de esta spec.

**Formato del recorte.** Cada recorte corresponde al rectángulo de la detección ampliado con un margen configurable, inicialmente del 10 % del ancho y del alto por cada lado, limitado a los bordes de la imagen. Se guarda a la resolución original, sin redimensionar. El cambio de tamaño y el tratamiento de las proporciones pertenecen al preprocesado del estimador de peso.

La preparación de las imágenes individuales utilizadas para entrenar el estimador y de los recortes generados por este módulo seguirá un criterio común de encuadre y tratamiento del fondo. Este criterio se acordará entre los responsables de las specs de preparación del dataset, extracción de pollos y estimación de peso, y quedará documentado antes de realizar los experimentos de integración. La calidad de la estimación sobre los recortes se comprobará experimentalmente; no se presupone que sea equivalente a la obtenida con las capturas individuales.

No se decide todavía el modelo concreto de detección. Se probarán distintas alternativas y se compararán sobre el mismo conjunto de validación antes de elegir una. El conjunto de test se reservará para la evaluación final.

## Por qué

En las capturas de la primera fase podremos controlar que aparezca un único pollo, pero una cámara situada sobre la nave verá varios animales a la vez, a veces juntos o parcialmente ocultos. El estimador de peso individual no está diseñado para recibir la escena completa ni para asignar un peso a cada animal dentro de ella.

Necesitamos separar los individuos aprovechables y filtrar las detecciones problemáticas para reducir la entrada al estimador de imágenes con animales cortados, solapados o mal delimitados. Esta separación permite estudiar el paso de un experimento en condiciones controladas a una estimación del peso sobre escenas reales de la granja.

También queremos que cada decisión de la funcionalidad quede registrada para revisar qué detecciones se aceptan, cuáles se descartan y por qué. Esto permitirá conocer cuántos animales se pierden por cada regla y ajustar sus parámetros utilizando el conjunto de validación.

## Restricciones

- La entrada es una imagen ya extraída. La extracción de fotogramas a partir de los vídeos se realiza antes y no forma parte de esta spec.
- La funcionalidad no estima pesos: entrega los recortes al módulo de estimación de peso individual.
- No reconoce al mismo pollo entre fotogramas distintos. El seguimiento de individuos (tracking) queda fuera de esta spec.
- Las coordenadas se expresan en píxeles sobre la imagen original, utilizando el formato `(x_min, y_min, x_max, y_max)`. Se guardan tanto las del rectángulo de detección como las del recorte ampliado.
- Las detecciones duplicadas se eliminan antes de aplicar el filtro de solapamiento entre animales. El procedimiento utilizado y sus parámetros quedan documentados y registrados.
- Las reglas de filtrado deben ser comprobables y sus parámetros, configurables y registrados:
  - **Baja confianza:** se descarta toda detección con confianza inferior a un umbral configurable, inicialmente 0,5.
  - **Animal próximo al borde:** se descarta toda detección cuyo rectángulo esté a una distancia igual o inferior a un margen configurable de cualquiera de los bordes de la imagen, inicialmente 2 píxeles.
  - **Solapamiento entre animales:** tras filtrar por confianza y eliminar duplicados, se calcula la intersección entre cada pareja de rectángulos. Se descarta una detección si la intersección con cualquier otra supera un porcentaje configurable de su propia área, inicialmente el 20 %. La decisión se calcula para cada rectángulo por separado, antes de retirar los descartados, para que no dependa del orden de procesamiento.
  - **Sin detecciones aceptadas:** se devuelve una lista vacía de recortes y el procesamiento continúa sin error, conservando los registros de las detecciones descartadas.
- Si una detección incumple varias reglas de filtrado, se registran todos los motivos correspondientes.
- Estas reglas son aproximaciones basadas en la confianza y la geometría de los rectángulos. No garantizan que todos los animales aceptados estén completos o libres de oclusiones. Tampoco garantizan que el margen añadido al recorte no incluya parte de otro animal.
- No se promete detectar oclusiones causadas por comederos u otros objetos mientras no se defina un procedimiento específico para hacerlo.
- Para entrenar o adaptar el modelo y evaluarlo se necesitan escenas anotadas con un rectángulo por pollo visible, siguiendo un criterio común para los animales parcialmente visibles. Estas anotaciones dependen del dataset propio de la segunda fase.
- Las particiones se realizan por sesión de captura, no por fotograma. Ninguna sesión puede aparecer en más de uno de los conjuntos de entrenamiento, validación y test.
- La elección del modelo y el ajuste de los umbrales se realizan con entrenamiento y validación. La configuración queda fijada antes de evaluar el conjunto de test.
- Los datos y las imágenes reales de la granja están sujetos al acuerdo de confidencialidad (NDA), por lo que no se incluyen en el repositorio de entrega.
- La funcionalidad se validará inicialmente con las condiciones de cámara, encuadre e iluminación de la campaña de captura. No se da por hecho que el rendimiento se mantenga en otras naves o condiciones.

## Criterios de aceptación

La funcionalidad se considerará correctamente implementada cuando se cumplan los siguientes criterios:

- Cada detección aceptada genera un recorte legible, con ancho y alto mayores que cero, y su registro de metadatos.
- Las coordenadas de las detecciones y de los recortes están dentro de los límites de la imagen original.
- Cada recorte queda asociado de forma inequívoca a su imagen de origen y a su detección. Sus coordenadas permiten reconstruir la región exacta extraída, incluido el margen aplicado.
- Los recortes se guardan sin redimensionar y respetan el margen configurado, limitado a los bordes de la imagen.
- El criterio común de encuadre y tratamiento del fondo está documentado y acordado con los módulos de preparación del dataset y estimación de peso.
- Si una escena no contiene detecciones aceptadas, el sistema devuelve una lista vacía de recortes y continúa procesando el resto de imágenes sin interrumpirse.
- Si el archivo de imagen no puede leerse, el sistema devuelve un error identificable y continúa con las siguientes imágenes cuando se procesa un lote.
- Un conjunto de pruebas con coordenadas y confianzas conocidas comprueba los filtros de borde, baja confianza y solapamiento, incluidos los valores exactamente iguales a los umbrales. Cada descarte registra los motivos correspondientes.
- Una prueba verifica que una detección de baja confianza o eliminada como duplicada no provoca por sí misma el descarte de otra mediante el filtro de solapamiento.
- Los parámetros utilizados en cada ejecución quedan registrados junto con los resultados, incluidos el umbral de confianza, el procedimiento de eliminación de duplicados, el margen de borde, el umbral de solapamiento y el margen del recorte.
- La evaluación se realiza sobre escenas anotadas reservadas para test, sin sesiones compartidas con entrenamiento ni validación.
- La precision y el recall del detector se calculan después del umbral de confianza y de la eliminación de duplicados, pero antes de los filtros de borde y solapamiento destinados a seleccionar recortes para el estimador.
- Una detección se considera correcta si su IoU con una anotación es igual o superior a 0,5. El emparejamiento se realiza en orden descendente de confianza, asignando a cada detección la anotación disponible de mayor IoU que cumpla el umbral. Cada detección y cada anotación pueden participar en un único emparejamiento.
- Se genera un informe con la precision, el recall, el número de escenas de test, el número de pollos anotados, el número de detecciones aceptadas y el número de detecciones descartadas por cada regla. Si un descarte tiene varios motivos, se aclara que puede contabilizarse en más de una categoría.

**Objetivos experimentales de rendimiento.** Se plantean como referencias iniciales una precision igual o superior a 0,90 y un recall igual o superior a 0,80 con IoU ≥ 0,5, calculados sobre las salidas del detector antes de los filtros de borde y solapamiento. Estos valores deben revisarse con los tutores y el cliente cuando se conozcan las condiciones de captura, y quedar acordados antes de la evaluación final en test.

Estos objetivos no son condiciones obligatorias de aceptación de esta primera implementación. Si no se alcanzan, el informe deberá reflejar los resultados obtenidos, las limitaciones observadas y las mejoras propuestas.
