# Estrategias de generación de informes clínicos

## Qué construir

Queremos desarrollar y comparar diferentes estrategias de generación de informes clínicos sintéticos para estudiar cómo influyen las instrucciones y la información proporcionada a los modelos en los resultados obtenidos.

Para ello, trabajaremos con tres estrategias principales:

- **Generación mediante prompting:** el modelo recibe unas instrucciones que describen el contenido y la estructura del informe, sin proporcionar ejemplos adicionales.
- **Generación mediante few-shot prompting:** además de las instrucciones, se incluyen informes clínicos de referencia para que el modelo pueda utilizar su estructura y estilo como ejemplo.
- **Generación en dos fases:** primero se construye la información clínica del paciente ficticio y, después, se utiliza esa información para redactar el informe final en el idioma solicitado.
  

En cada estrategia podremos probar diferentes versiones de los prompts, introduciendo modificaciones a partir de los errores detectados en los informes anteriores.

Los informes obtenidos se guardarán junto con la información necesaria para identificar el modelo, la estrategia y las instrucciones utilizadas. Esto nos permitirá evaluar posteriormente si las distintas formas de generación producen diferencias en la estructura, el realismo y la coherencia clínica de los informes.

## Por qué

La calidad de los informes clínicos generados no depende únicamente del modelo de lenguaje utilizado, sino también de las instrucciones y de la información que recibe. Un mismo modelo puede producir resultados diferentes según cómo se formule el prompt o si se le proporcionan ejemplos de informes reales.

Durante nuestras primeras pruebas hemos observado que algunas modificaciones en los prompts mejoran la estructura y reducen ciertos errores, mientras que otras no consiguen mejorar la coherencia clínica. También hemos comprobado que utilizar ejemplos puede ayudar a reproducir mejor el formato hospitalario, pero no garantiza que el contenido médico sea correcto.

Por este motivo, queremos probar distintas estrategias de generación para analizar cómo afectan a la calidad de los informes. Nuestro objetivo es identificar qué métodos permiten reducir los errores, mejorar la coherencia clínica y conseguir documentos más realistas, sin asumir que una estrategia más compleja tiene que ofrecer necesariamente mejores resultados.

## Restricciones y supuestos

- **Ámbito clínico:** todas las estrategias se aplicarán a la generación de informes sintéticos de pacientes adultos con cáncer de cabeza y cuello, dentro del ámbito de la Oncología Radioterápica.

- **Modelos utilizados:** se trabajará con los modelos de lenguaje seleccionados para el proyecto. No será necesario modificar ni entrenar sus parámetros, ya que las estrategias se basarán en cambiar las instrucciones y la información proporcionada.

- **Prompting:** la generación sin ejemplos utilizará únicamente las instrucciones del prompt, que definirán la estructura y el contenido esperado de los informes.

- **Few-shot prompting:** los informes de referencia se utilizarán como ejemplos de estructura y estilo. Se deberá evitar que los modelos reproduzcan datos identificativos de pacientes reales. Cuando se utilicen ejemplos para la generación, estos se mantendrán separados de los reservados para evaluación.

- **Generación en dos fases:** la información clínica creada en la primera fase deberá utilizarse como base para redactar el informe final, sin introducir cambios injustificados en los datos del paciente, el diagnóstico o el tratamiento. Esta estrategia se desarrollará y comprobará experimentalmente.

- **Comparación de estrategias:** cuando se quiera estudiar el efecto de una estrategia, se mantendrán constantes el modelo y los parámetros de generación, siempre que sea posible, modificando únicamente las instrucciones o los ejemplos correspondientes.

- **Registro de experimentos:** se conservarán las versiones de los prompts, los ejemplos utilizados, el modelo y los parámetros de generación para poder identificar las condiciones de cada prueba.

- **Limitaciones:** ninguna estrategia garantiza por sí sola que los informes sean clínicamente correctos. La coherencia médica y los posibles errores se analizarán posteriormente durante la evaluación.

## Criterios de aceptación

1. **Generación mediante prompting:** el sistema permite generar al menos 5 informes sintéticos utilizando únicamente las instrucciones del prompt, sin proporcionar informes de ejemplo.

2. **Generación mediante few-shot prompting:** el sistema permite generar al menos 5 informes sintéticos utilizando un prompt acompañado de 3 informes clínicos de referencia. Los ejemplos utilizados quedan identificados y registrados.

3. **Generación en dos fases:** el sistema permite crear primero la información clínica de un paciente ficticio y utilizarla posteriormente para redactar un informe completo. Se comprueba que ambas fases generan archivos de salida independientes y que los datos básicos del paciente, el diagnóstico y el tratamiento se mantienen entre ellas.

4. **Modificación de prompts:** es posible ejecutar un mismo modelo con al menos dos versiones diferentes de un prompt, conservando ambas versiones para identificar las instrucciones utilizadas en cada ejecución.

5. **Registro de estrategias:** cada experimento queda identificado con el nombre del modelo, la estrategia utilizada, la versión del prompt y los parámetros de generación. En los experimentos few-shot también se registran los ejemplos empleados.

6. **Organización de resultados:** los informes se guardan en carpetas diferenciadas por modelo y estrategia, de manera que sea posible localizar los resultados de cada experimento sin mezclarlos.

7. **Comparación controlada:** para comparar dos estrategias de un mismo modelo, se documentan los parámetros de generación utilizados y se mantienen iguales aquellos que no forman parte de la variable estudiada. Cualquier diferencia en estos parámetros queda registrada.
