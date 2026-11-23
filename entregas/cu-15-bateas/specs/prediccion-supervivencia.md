# Spec: predicción de supervivencia

## Qué construir

Un modelo que, a partir de `panel_diario.csv` (generado por la [preparación de datos](preparacion-datos-multi-ria.md)), estima durante cuánto tiempo seguirá un polígono en su estado actual. Incluye tres partes:

1. **Entrenamiento** de dos modelos con el mismo método: uno para el riesgo de **cierre** y otro para la **reapertura**.
2. **Consulta:** una función `predecir(punto, fecha)` para usar desde un notebook.
3. **Evaluación:** un notebook que calcula los resultados y los compara con dos referencias simples.

### Ejemplo de consulta

```
predecir("GROVE-C1", "2025-09-01")

Polígono: GROVE-C1 | Estado: ABIERTO
P(seguir abierto  1 día)  = ...
P(seguir abierto  3 días) = ...
P(seguir abierto  7 días) = ...
P(seguir abierto 14 días) = ...
```

Si el polígono está cerrado, da las probabilidades de seguir cerrado. Si su estado es `desconocido`, responde "sin predicción".

### Cómo funciona el método

Usamos **supervivencia en tiempo discreto**, que convierte el problema en una clasificación como la de PIIA 1:

- **Vida y muerte.** Un polígono "vive" mientras sigue en un estado y "muere" al cambiar.
- **Qué aprende.** El modelo aprende el riesgo de cambiar el día *k* (de 1 a 14) si ha aguantado hasta el día anterior.
- **Cómo se construyen los datos.** Cada día genera una fila por cada día *k* observado. Por ejemplo, un polígono abierto que cierra 4 días después genera 4 filas: "no cierra" en los días 1, 2 y 3, y "cierra" en el día 4.
- **Censura.** Si dejamos de conocer el estado, no se generan más filas. Así no inventamos un final.
- **De riesgo a probabilidad.** La probabilidad de seguir igual *h* días es el producto de (1 - riesgo del día *k*) para *k* de 1 a *h*.

El clasificador es un gradient boosting de scikit-learn que admite valores nulos, sin búsqueda de hiperparámetros.

### Variables

| Grupo | Qué contiene |
|---|---|
| Toxinas propias | Últimos valores del polígono respecto a su límite legal y su evolución reciente |
| Contexto de la ría | Toxinas recientes en toda la ría y porcentaje de polígonos cerrados |
| Historial del polígono | Días en el estado actual y cierres recientes |
| Estacionalidad | Época del año |
| Meteorología y agua | Lluvia, viento, temperatura y salinidad de los últimos días |

### Cómo se evalúa

Comparamos el modelo con dos referencias:

- **Kaplan-Meier:** da la misma curva a todos los polígonos, sin usar variables.
- **Regla simple:** da más riesgo a los polígonos cuya última muestra está más cerca del límite.

Hacemos dos pruebas:

- **Por años.** Para evaluar un año, se entrena solo con los años anteriores.
- **Dejando fuera una ría.** Se entrena sin esa ría y se evalúa en ella.

Y usamos dos métricas a 7 días:

- **AUC:** si el modelo da más riesgo a los polígonos que cambian de estado.
- **Brier:** el error de la probabilidad; cuanto más bajo, mejor.

## Por qué

**Problema.** En PIIA 1, copiar el estado de hoy daba un F1 de 0,942, frente al 0,93 de nuestro modelo, porque casi nunca cambia el estado de un día para otro. Esa métrica no decía si sabíamos anticipar un cierre.

**Resultado que buscamos.** Una probabilidad que ayude a planificar, medida solo en los casos en los que el cambio es posible, y que siga funcionando en rías que el modelo no ha visto.

**Por qué este método.** Reutiliza lo que ya sabemos de clasificación, trata bien los datos censurados y no necesita librerías nuevas. Un prototipo en Arousa da un AUC a 7 días de 0,877, frente al 0,785 de la regla simple, lo que indica que el objetivo es alcanzable.


## Restricciones

- **Sin información del futuro:** las variables de un día no pueden depender de datos posteriores. Las particiones son siempre temporales, nunca aleatorias.
- **Transferible:** el modelo no usa identificador de polígono, zona ni coordenadas.
- **Un único modelo por dirección:** el mismo modelo de cierre y el mismo de reapertura para todas las rías.
- **Horizonte:** máximo de 14 días; se informa a 1, 3, 7 y 14 días.
- **Herramientas:** Python, con pandas, numpy y scikit-learn.

**Supuestos:**

- Tendremos al menos una ría además de Arousa. **Si los datos nuevos no llegan a tiempo**, se deja fuera cada zona de Arousa en lugar de una ría, y se indica que esta prueba es menos exigente.
- El resultado del laboratorio se conoce el mismo día de la muestra. Si en la realidad tarda más, los resultados son algo optimistas.

**Limitaciones conocidas:**

- En el prototipo, el modelo ordena bien los polígonos, pero sus probabilidades fallan más en años atípicos. Por eso, se presentan como orientativas.
- Hay cierres imposibles de anticipar solo con toxinas, porque la toxina puede pasar de 0 a superar el límite entre dos muestras semanales.

## Criterios de aceptación

| ID | Comprobación | Resultado esperado |
|---|---|---|
| CA1 | Llamar a `predecir` con un polígono abierto o cerrado. | Devuelve el estado y cuatro probabilidades entre 0 y 1, que no aumentan al ampliar el horizonte. |
| CA2 | Llamar a `predecir` con un polígono en estado `desconocido` o que no existe. | No da ninguna probabilidad e indica el motivo. |
| CA3 | Con datos de prueba, un polígono abierto cierra a los 4 días. | Se generan 4 filas, y solo la última marca el cierre. |
| CA4 | Con datos de prueba, cambiar los valores de toxinas a partir de una fecha y recalcular las variables. | Las variables de los días anteriores a esa fecha no cambian. |
| CA5 | Evaluar el modelo de cierre por años en Arousa. | El AUC a 7 días supera al de la regla simple en la mayoría de los años, y el Brier a 7 días mejora al de Kaplan-Meier en la mayoría de los años. |
| CA6 | Dejar fuera, una a una, las rías que se puedan evaluar por separado. | Se publica el AUC a 7 días de cada ría junto al de la regla simple, y el AUC medio del modelo es superior. |
| CA7 | Evaluar el modelo de reapertura en Arousa. | El AUC a 7 días supera al de la regla simple. |
| CA8 | Evaluar por años el modelo completo, sin toxinas propias, sin contexto de la ría, sin meteorología ni agua, y solo con datos ambientales. | Se obtiene una tabla con el AUC a 7 días por configuración, que usa el informe de dependencia de datos. |
