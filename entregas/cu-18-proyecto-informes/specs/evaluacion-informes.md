# Evaluación de informes clínicos sintéticos

## Qué construir

Queremos desarrollar un procedimiento de evaluación que nos permita analizar la calidad de los informes clínicos sintéticos generados por los distintos modelos de lenguaje.

Para ello, definiremos unos criterios comunes con los que revisar aspectos como la estructura y el formato del informe, la coherencia entre los síntomas, las pruebas diagnósticas, el diagnóstico y el tratamiento, la consistencia de las fechas y las dosis, y la variedad de los casos generados.

La evaluación incluirá la identificación y clasificación de errores concretos, como contradicciones clínicas, incoherencias temporales, información inventada o tratamientos que no se corresponden con el diagnóstico. También estudiaremos el uso de métricas automáticas, como BLEU, ROUGE y BERTScore, para analizar la similitud textual y semántica con los informes de referencia, sin considerar estas métricas como una medida directa de corrección médica.

Además, contaremos con la valoración de un profesional sanitario, que revisará una selección de informes para identificar posibles errores clínicos y valorar su coherencia médica.

Los resultados de las evaluaciones se registrarán de forma organizada, asociando cada valoración al informe, modelo y estrategia de generación correspondientes. Esto nos permitirá analizar los errores más frecuentes y utilizar la información obtenida para comparar y mejorar las estrategias de generación.

## Por qué

Los modelos de lenguaje pueden generar informes clínicos que parecen reales por su estructura y vocabulario, pero esto no significa que su contenido sea médicamente correcto. Durante nuestras primeras pruebas hemos encontrado errores relacionados con las localizaciones anatómicas, los diagnósticos, las dosis de tratamiento y la cronología de los pacientes, incluso en informes que estaban bien redactados.

Por este motivo, necesitamos un procedimiento de evaluación que nos permita identificar estos problemas de forma sistemática y no basarnos únicamente en la apariencia de los textos. Las métricas automáticas pueden ayudarnos a estudiar la similitud entre informes, pero no son suficientes para determinar si la información clínica es correcta, por lo que resulta especialmente importante contar con la revisión de un profesional sanitario.

Con esta funcionalidad buscamos conocer los errores más frecuentes de los informes generados, comprobar qué aspectos mejoran o empeoran al modificar las estrategias de generación y disponer de resultados que nos permitan realizar comparaciones fundamentadas entre los distintos experimentos.

## Restricciones y supuestos

- **Ámbito de evaluación:** únicamente se evaluarán informes clínicos sintéticos de pacientes adultos con cáncer de cabeza y cuello, dentro del ámbito de la Oncología Radioterápica.

- **Criterios comunes:** todos los informes se evaluarán siguiendo unos mismos criterios, que incluirán estructura, coherencia clínica, consistencia temporal, información médica y cumplimiento de las instrucciones del prompt.

- **Clasificación de errores:** se utilizará una clasificación común para registrar los errores encontrados, diferenciando entre contradicciones clínicas, errores de tratamiento, incoherencias temporales, información irrelevante, omisiones y problemas de formato. Cada error deberá quedar asociado al informe en el que se detectó.

- **Métricas automáticas:** se estudiará el uso de BLEU, ROUGE y BERTScore como medidas complementarias de similitud textual y semántica. Sus resultados no se interpretarán como una medida directa de corrección clínica, especialmente cuando los informes comparados describan pacientes diferentes.

- **Evaluación profesional:** un profesional sanitario revisará una selección de informes para valorar su coherencia clínica. La cantidad de informes revisados dependerá de su disponibilidad y las conclusiones se limitarán a los casos efectivamente evaluados.

- **Evaluación mediante LLMs:** se podrá estudiar el uso de un modelo de lenguaje como evaluador automático (*LLM-as-a-Judge*). Sus valoraciones no sustituirán a las del profesional sanitario y, si se utilizan para valorar la calidad clínica, se contrastarán con la evaluación humana.

- **Comparabilidad:** para comparar los resultados de diferentes modelos o estrategias, se utilizarán los mismos criterios de evaluación y se documentará el número de informes analizados en cada experimento.

- **Registro de resultados:** cada evaluación deberá poder relacionarse con el informe correspondiente, el modelo que lo generó y la estrategia utilizada. Se conservarán los errores detectados y las valoraciones realizadas.

- **Limitaciones:** la evaluación tendrá un carácter experimental y no servirá para certificar la seguridad clínica de los modelos. Los resultados obtenidos no permitirán afirmar que los informes sean adecuados para su utilización con pacientes reales.

## Criterios de aceptación

1. **Definición de criterios de evaluación:** se dispone de un documento que establece los aspectos que se evaluarán en los informes, incluyendo estructura, coherencia clínica, consistencia temporal, tratamientos y cumplimiento del prompt. Cada aspecto tendrá una descripción que permita aplicar el mismo criterio a todos los informes.

2. **Clasificación de errores:** se utiliza una clasificación común de errores que incluye, como mínimo, contradicciones clínicas, incoherencias temporales, errores de tratamiento, omisiones, información irrelevante y problemas de formato. Cada error identificado queda registrado junto con el informe correspondiente, su categoría y el fragmento de texto donde aparece.

3. **Evaluación de informes:** el procedimiento permite evaluar al menos 5 informes generados, registrando para cada uno los criterios revisados y los errores encontrados. Los informes sin errores detectados también quedan registrados.

4. **Métricas automáticas:** se pueden calcular BLEU, ROUGE-L y BERTScore para al menos 5 informes generados, utilizando un conjunto identificado de referencias. Los resultados se almacenan indicando la métrica y las referencias utilizadas, y se presentan como medidas de similitud, no de corrección clínica.

5. **Evaluación profesional:** se prepara una selección identificada de al menos 5 informes para su revisión por un profesional sanitario, junto con una plantilla común para registrar los errores clínicos. Cuando se reciba la valoración, esta quedará asociada a cada informe evaluado, diferenciándola del análisis realizado por el equipo.

6. **Registro de evaluaciones:** los resultados se guardan en un formato que permite identificar el informe evaluado, el modelo y la estrategia con los que se generó, los criterios aplicados y los errores detectados.

7. **Resumen de resultados:** se elabora un resumen con el número de informes evaluados, el número de errores detectados por categoría y el número de informes afectados por cada tipo de error. Los resultados de la revisión profesional se presentan por separado cuando estén disponibles.
