# Generación de informes clínicos sintéticos

## Qué construir

Queremos desarrollar una funcionalidad que permita generar automáticamente informes clínicos sintéticos de pacientes adultos con cáncer de cabeza y cuello, utilizando diferentes modelos de lenguaje.

El sistema recibirá unas instrucciones que definirán la estructura y el contenido esperado del informe. A partir de ellas, el modelo generará un caso clínico ficticio que incluirá información sobre el paciente, sus antecedentes, el diagnóstico, las pruebas realizadas, el tratamiento y la evolución clínica.

Los informes se generarán en formato de texto y se guardarán en archivos individuales, para poder analizarlos posteriormente y comparar los resultados obtenidos con los distintos modelos.

Esta funcionalidad será la base del proyecto, ya que proporcionará los informes que después utilizaremos para estudiar las diferentes estrategias de generación y evaluar su calidad.

## Por qué

La generación de informes clínicos sintéticos puede ser útil para disponer de documentos con los que investigar y experimentar sin necesidad de trabajar directamente con información personal de pacientes reales.

Sin embargo, generar este tipo de informes mediante modelos de lenguaje presenta dificultades. Aunque los modelos pueden producir textos que parecen informes hospitalarios, también pueden cometer errores médicos, introducir contradicciones o generar tratamientos que no se corresponden con el diagnóstico.

Por eso, queremos desarrollar un proceso que nos permita generar diferentes informes sintéticos de forma organizada y reproducible. Estos informes servirán como punto de partida para analizar los errores más frecuentes, estudiar las capacidades y limitaciones de cada modelo y comprobar qué estrategias permiten mejorar los resultados.

Con esta funcionalidad buscamos obtener un conjunto de informes variados que podamos utilizar posteriormente en las tareas de evaluación y comparación del proyecto.

## Restricciones y supuestos

- **Ámbito clínico:** los informes generados estarán limitados a pacientes adultos con cáncer de cabeza y cuello, dentro de la especialidad de Oncología Radioterápica.

- **Datos sintéticos:** los pacientes y sus historias clínicas serán ficticios. No se deberán reproducir datos personales identificativos procedentes de los informes reales utilizados como referencia.

- **Estructura de los informes:** los documentos deberán seguir una estructura hospitalaria, incluyendo información del paciente, antecedentes, pruebas diagnósticas, diagnóstico, tratamiento y evolución clínica.

- **Coherencia de la información:** se indicará a los modelos que mantengan la consistencia entre las localizaciones anatómicas, las pruebas realizadas, los diagnósticos, las dosis de tratamiento y las fechas. El cumplimiento de estas condiciones se comprobará posteriormente durante la evaluación.

- **Modelos utilizados:** trabajaremos con modelos de lenguaje existentes, como Llama, Qwen, GPT y Mistral, sin entrenar modelos nuevos desde cero.

- **Formato de salida:** cada informe se guardará individualmente en un archivo de texto plano (`.txt`), para facilitar su revisión y comparación.

- **Reproducibilidad:** siempre que sea posible, se conservarán las instrucciones utilizadas, el modelo, los parámetros de generación y la semilla aleatoria de cada experimento.

- **Limitaciones clínicas:** los informes generados tendrán únicamente fines de investigación y experimentación. No podrán utilizarse como documentación clínica real ni como base para tomar decisiones médicas.

## Criterios de aceptación

1. **Generación de informes:** el sistema permite generar al menos 5 informes clínicos sintéticos en una misma ejecución, utilizando uno de los modelos de lenguaje seleccionados.

2. **Formato de salida:** cada informe generado se guarda en un archivo independiente con extensión `.txt`, que puede abrirse y leerse correctamente.

3. **Estructura de los informes:** todos los informes contienen apartados identificables de antecedentes, pruebas diagnósticas, diagnóstico, tratamiento y evolución clínica. Se comprobará su presencia mediante una revisión de los archivos generados.

4. **Información sintética:** los informes no contienen datos identificativos copiados de los ejemplos reales utilizados. Se comprobará comparando los nombres, números de historia clínica y otros identificadores presentes en los informes con los documentos de referencia.

5. **Registro de los experimentos:** cada ejecución conserva el modelo utilizado, el prompt, los parámetros de generación y, cuando corresponda, la semilla aleatoria, permitiendo identificar las condiciones con las que se generaron los informes.

6. **Disponibilidad para evaluación:** los informes generados quedan almacenados y organizados de forma que puedan recuperarse e identificarse para su posterior análisis y comparación.

