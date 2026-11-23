# Spec: explorar la comparación de resultados

## Qué construir

Una vista de Streamlit que resuma y compare los resultados de los modelos fundacionales ejecutados para un dataset y, cuando exista, su baseline tradicional. La vista utilizará los resultados de la funcionalidad definida en [comparar-modelos.md](./comparar-modelos.md) y comunicará las métricas de clasificación binaria, los tiempos y el protocolo usado, con gráficos que ayuden a entender los resultados sin exigir conocimientos de programación.

La tabla de resultados incluirá ROC-AUC, average precision, recall y F1. Se mostrará una matriz de confusión por modelo cuando estén disponibles las etiquetas reales y predichas. Cuando existan probabilidades de la clase positiva y ambas clases estén presentes en el conjunto de evaluación, se mostrarán ROC-AUC, average precision y las curvas ROC y precisión–recall. Los valores que no puedan calcularse se identificarán como «No disponible», con su motivo.

Como resultado del análisis, el equipo elaborará un informe independiente en formato Markdown que compare los experimentos realizados y documente las conclusiones y limitaciones. No se requiere que la aplicación genere automáticamente este informe.

## Por qué

El resultado esperado del caso de uso es un prototipo interactivo que permita consultar e interpretar los experimentos. Una tabla de puntuaciones aislada no explica qué errores comete el modelo ni si la comparación con el baseline es válida. Esta vista permite a estudiantes y analistas revisar las capacidades y limitaciones de cada enfoque. El informe recogerá las conclusiones justificadas por los resultados obtenidos.

## Restricciones y supuestos

- Las comparaciones directas utilizan el mismo dataset, variable objetivo y conjunto de evaluación, con las mismas definiciones de métricas. Las referencias externas se presentan identificadas y separadas de la comparación directa.
- Las métricas, ejes, clases positiva y negativa y unidades de tiempo están etiquetados en la interfaz. Recall y F1 se calculan para la clase positiva registrada.
- Si el modelo produce probabilidades, las etiquetas predichas se obtienen con el umbral registrado antes de la evaluación, que será visible junto a la matriz de confusión. Si solo produce etiquetas, se indicará que se utiliza la decisión del modelo y que el umbral no está disponible.
- ROC y precisión–recall reflejan distintos umbrales. Si faltan probabilidades o el conjunto evaluado no contiene ambas clases, no se muestran esas curvas y se explica el motivo.
- Si no puede calcularse una métrica, se muestra «No disponible» con una explicación. Cuando no existan predicciones individuales del baseline, no se genera una matriz de confusión ni curvas a partir de sus métricas agregadas. Si no hay predicciones positivas, se adopta la convención de asignar F1 = 0 y se indica esta convención.
- La interfaz indica si el baseline procede de la misma evaluación o de resultados proporcionados externamente, e identifica las diferencias conocidas o la información que falta sobre el protocolo.
- Los tiempos de ajuste y predicción se muestran por separado, en segundos, junto con el dispositivo utilizado (CPU/GPU y modelo de hardware). Cuando no existe fase de ajuste, se muestra «No aplica»; cuando falta una medición o información de hardware, se muestra «No disponible». Los tiempos no se presentan como una comparación equivalente si el hardware difiere o es desconocido.
- Los resultados describen rendimiento en los datos evaluados y no demuestran causalidad, generalización a cualquier industria ni superioridad universal de un modelo.

## Criterios de aceptación

1. Para cada modelo completado y baseline compatible, se muestra una tabla con ROC-AUC, average precision, recall y F1. Cada celda contiene un valor calculado o «No disponible» con su motivo.
2. Cuando existen etiquetas reales y predichas, se presenta una matriz de confusión por modelo, con clases y ejes real/predicho identificados. Se muestra el umbral aplicado o se indica que se utiliza la decisión del modelo sin un umbral disponible.
3. Cuando existen probabilidades y ambas clases en el conjunto de evaluación, se muestran curvas ROC y precisión–recall con leyendas que identifican los modelos. En caso contrario, se explica por qué no se muestran.
4. La vista muestra el dataset, la variable objetivo, las clases positiva y negativa, el tamaño del conjunto de evaluación y el protocolo utilizado.
5. Los tiempos de ajuste y predicción aparecen por separado, con sus unidades y el hardware empleado. Las fases que no existen figuran como «No aplica» y las mediciones o datos de hardware ausentes como «No disponible».
6. Si el baseline utiliza otro protocolo o este es desconocido, la interfaz lo presenta como referencia externa e indica que la comparación no es directa. Si no existe baseline, permite consultar los resultados de los modelos e informa de su ausencia.
7. El informe en Markdown identifica los datasets y modelos evaluados, el protocolo, las métricas, los tiempos y el hardware disponibles. Expone las limitaciones observadas y fundamenta cada conclusión sobre el uso de un modelo en resultados concretos. Si faltan datos para recomendar un modelo, lo indica expresamente.
