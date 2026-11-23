# Spec: preparación de datos multi-ría

## Qué construir

Un proceso que recibe los CSV de una o varias rías y genera dos ficheros:

1. **`panel\\\_diario.csv`**: una fila por polígono y día, con el estado de ese día (`abierto`, `cerrado` o `desconocido`).
2. **`informe\\\_validacion.txt`**: qué problemas tienen los datos y qué se ha hecho con ellos.

Es el primer paso del sistema: la [predicción de supervivencia](prediccion-supervivencia.md) trabaja con `panel\\\_diario.csv`.

### Qué hace, en orden

1. **Validar.** Comprueba que estén las columnas obligatorias: `Punto`, `Fecha`, `Ria`, `Especie` y al menos una toxina. Si falta alguna, se detiene con un error. Si falta una columna opcional, como la meteorología, avisa y continúa.
2. **Filtrar.** Se queda solo con las muestras de mejillón.
3. **Limpiar.** Los códigos de "sin dato" (como `-9999`) y los valores imposibles pasan a nulo. Una toxina por debajo de lo que el laboratorio puede cuantificar (`< LQ`) pasa a 0, y de un valor como `159,1 ±32,6` se conserva 159,1.
4. **Agrupar por día.** Si un polígono tiene varias muestras el mismo día, se queda con el valor máximo de cada toxina. También añade los días sin datos.
5. **Calcular el estado de cada día.** Cada toxina mantiene su último valor medido durante un máximo de 28 días.

   * `cerrado`: alguna toxina vigente alcanza su límite legal.
   * `abierto`: hay alguna toxina vigente y ninguna alcanza su límite.
   * `desconocido`: no hay ninguna toxina vigente.

|Toxina|Límite legal|
|-|-|
|AO|160 µg/kg|
|ASP|20 mg/kg|
|PSP|800 µg/kg|
|AZA|160 µg/kg|
|YTX|3,75 mg/kg|

6. **Resumir cada ría.** El informe indica sus polígonos, sus fechas, los cierres por año y cuántos datos faltan. Un cierre es un día `cerrado` cuyo día anterior estaba `abierto`. También indica si la ría se puede evaluar por separado, para lo que necesita al menos 5 años de datos y 10 cierres.

## Por qué

**Problema.** Si cada ría se prepara de una forma distinta, el modelo no se puede entrenar con todas ni comparar los resultados.

**Resultado que buscamos.** Añadir una ría debe ser sencillo: pasar su CSV por el proceso y leer en el informe si sirve y qué le falta. Esto también permite trabajar ya con Arousa mientras llegan los datos nuevos.

**Criterio ante las dudas.** Ante un dato dudoso, se prefiere marcarlo como desconocido antes que inventarlo.

## Restricciones

* **Formato:** los CSV nuevos deben seguir el formato de Arousa.
* **Sin cambios de código por ría:** añadir una ría no debe requerir modificar la lógica del proceso.
* **Datos originales:** el proceso no modifica los CSV de entrada.
* **Herramientas:** Python, con pandas y numpy.

**Supuestos:**

* El estado es una **estimación** a partir de las toxinas, no el estado oficial. No refleja cierres preventivos ni reglas oficiales de reapertura.
* Los 28 días de vigencia son una decisión nuestra y podemos revisarla: pasado ese tiempo, consideramos que la última analítica ya no informa del estado actual.

## Criterios de aceptación

|ID|Comprobación|Resultado esperado|
|-|-|-|
|CA1|Procesar el CSV de Arousa.|`panel\\\_diario.csv` tiene una sola fila por polígono y día, y solo incluye polígonos de mejillón.|
|CA2|Revisar los valores de `panel\\\_diario.csv`.|No queda ningún código de "sin dato" como `-9999`.|
|CA3|Procesar un polígono de prueba con una muestra por debajo del límite y, días después, otra por encima, sin más muestras.|El estado pasa de `abierto` a `cerrado`, y a `desconocido` cuando pasan 28 días desde la última muestra.|
|CA4|Procesar un polígono de prueba con dos muestras el mismo día, una por debajo del límite y otra por encima.|Hay una sola fila ese día, con el valor máximo y estado `cerrado`.|
|CA5|Procesar un CSV al que le falta una columna obligatoria.|El informe muestra un error que nombra la columna y no se genera `panel\\\_diario.csv`.|
|CA6|Procesar Arousa junto a una segunda ría, sin tocar el código.|`panel\\\_diario.csv` contiene las dos rías, y el informe tiene un resumen de cada una e indica si se puede evaluar por separado.|



