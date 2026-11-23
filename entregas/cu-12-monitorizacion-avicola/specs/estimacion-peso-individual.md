# Estimación de peso individual

## Qué construir

Queremos desarrollar una funcionalidad que reciba la imagen de un único pollo y sea capaz de estimar su peso en gramos.
La imagen de entrada puede proceder tanto de una grabación individual realizada durante la recogida de datos como de la salida del módulo encargado de extraer pollos individuales de escenas con varios animales.
Durante el entrenamiento utilizaremos imágenes de pollos individuales asociadas a su peso real. Como de un mismo pollo podremos tener varios fotogramas, el modelo tendrá acceso a distintas imágenes del mismo animal.
Por ahora no queremos limitar la solución a una arquitectura concreta, ya que la idea es probar diferentes modelos y comparar sus resultados antes de decidir cuál funciona mejor en nuestro caso.

## Por qué

Queremos estudiar si es posible estimar el peso de los pollos a partir de imágenes y reducir así la dependencia de los pesajes manuales.
Si conseguimos obtener estimaciones fiables mediante visión artificial, podríamos seguir la evolución del peso de los animales de una forma más frecuente y menos invasiva, sin necesidad de manipularlos continuamente para pesarlos.
Esta funcionalidad es una parte central del proyecto, ya que convierte la información visual de cada pollo en una estimación concreta de peso. También nos permitirá comparar diferentes modelos y comprobar cuáles se adaptan mejor a las imágenes obtenidas en condiciones reales de granja.
Más adelante, este estimador deberá poder trabajar también con las imágenes individuales generadas a partir de escenas con varios pollos.

## Restricciones

La funcionalidad trabajará únicamente con imágenes en las que aparezca un solo pollo. La detección, segmentación o extracción de animales desde escenas con varios pollos pertenece a otro módulo del proyecto, por lo que no forma parte de esta spec.
Durante el entrenamiento y la evaluación, cada imagen deberá estar asociada al peso real del pollo correspondiente. Como tendremos varios fotogramas del mismo animal, todos los frames de un mismo pollo deberán mantenerse dentro del mismo conjunto (train, validation o test) para evitar que el modelo vea durante el entrenamiento imágenes de un individuo que luego aparezca también en la evaluación.
El preprocesado de las imágenes deberá ser coherente entre entrenamiento y predicción, de forma que el modelo reciba siempre datos preparados de la misma manera.
No fijamos por ahora una arquitectura concreta, ya que queremos probar varios modelos y comparar sus resultados antes de elegir uno.

## Criterios de aceptación

La funcionalidad se considerará correctamente implementada cuando se cumplan los siguientes criterios:
- Dada una imagen válida que contenga un único pollo, el sistema devuelve una estimación numérica positiva de su peso en gramos.
- Si la imagen no puede leerse o el archivo es inválido, el sistema devuelve un error identificable en lugar de generar una predicción.
- La evaluación se realiza sobre un conjunto de test independiente, asegurando que ningún pollo utilizado en test aparezca también en train o validation, aunque existan varios fotogramas del mismo animal.
- Se genera un informe de evaluación que incluya, como mínimo, el MAPE, el MAE en gramos, el número de imágenes evaluadas y el número de animales diferentes presentes en el conjunto de test.
- Se establece como objetivo ideal de rendimiento un MAPE igual o inferior al 10% sobre el conjunto de test. Este valor se utilizará como referencia para valorar la calidad de la estimación.
- El mismo procedimiento de preprocesado definido para el modelo se aplica de forma consistente durante entrenamiento, validación y predicción.
- Las predicciones quedan asociadas de forma inequívoca a la imagen de entrada utilizada para generarlas.
