# Spec: informe de dependencia de datos

## Qué construir

Un documento breve, `informe_dependencia_datos.md`, que responde a tres preguntas: qué datos usa el modelo, cuánto empeora si falta cada fuente y qué tiene que aportar una ría nueva para poder usarse.

Es el último paso del sistema. No entrena ni limpia nada: reúne los resultados de la [preparación de datos](preparacion-datos-multi-ria.md) y de la [predicción de supervivencia](prediccion-supervivencia.md).

### Contenido

| Sección | Qué contiene | De dónde sale |
|---|---|---|
| 1. Fuentes y calidad | Qué fuentes usamos, para qué sirve cada una y un resumen de los datos de cada ría. | `informe_validacion.txt` (spec 1) |
| 2. Aporte de cada fuente | La tabla de AUC a 7 días por configuración y la clasificación de cada fuente. | Tabla de configuraciones de la spec 2 |
| 3. Requisitos y conclusiones | Qué necesita una ría nueva para usarse, qué hacer si le falta una fuente y qué limitaciones tienen los resultados. | Secciones anteriores |

### Cómo se clasifica cada fuente

Se compara el AUC medio del modelo completo con el del modelo sin esa fuente:

- **Imprescindible:** el AUC medio baja 0,03 o más.
- **Complementaria:** baja menos de 0,03. El modelo puede funcionar sin ella, aunque pierda algo de calidad.

Se clasifican las toxinas propias, el contexto de la ría, y la meteorología y el agua. La configuración "solo con datos ambientales" no clasifica ninguna fuente: sirve para responder si se puede predecir sin ningún dato de toxinas.

## Por qué

**Problema.** Todavía no sabemos qué datos traerá cada ría, y puede que alguna llegue sin sensor de agua o con la meteorología incompleta. Sin medir el aporte de cada fuente, no podríamos saber si eso invalida la ría o apenas afecta.

**Resultado que buscamos.** Responde al tercer objetivo del proyecto: saber qué datos son imprescindibles y cuáles aportan poco. Debe permitir decidir con datos si una ría se puede usar y qué merece la pena pedir.

**Criterio ante las dudas.** El informe debe ser corto y útil para decidir. Si los datos no permiten concluir algo, se dice.

## Restricciones

- **Sin experimentos propios:** solo usa resultados de las specs 1 y 2.
- **Sin ampliar el alcance:** puede recomendar datos para el futuro, pero el proyecto no los incorpora.
- **Brevedad:** el texto se limita a lo necesario para interpretar las tablas y decidir.

**Supuestos:**

- Las specs 1 y 2 ya se han ejecutado. **Si los datos nuevos no llegan a tiempo**, el informe cubre solo Arousa, lo indica al principio y avisa de que la clasificación podría cambiar en otras rías.
- Quitar una fuente del modelo simula que una ría no la tiene. Es una aproximación: no recoge los casos en los que una fuente está solo parcialmente incompleta.

**Referencia del prototipo en Arousa.** Son valores orientativos: el informe definitivo se calcula con los datos que recibamos.

| Configuración | AUC medio a 7 días | Diferencia frente al completo | Clasificación |
|---|---|---|---|
| Modelo completo | 0,877 | | |
| Sin toxinas propias | 0,841 | -0,036 | Imprescindible |
| Sin contexto de la ría | 0,837 | -0,040 | Imprescindible |
| Sin meteorología ni agua | 0,861 | -0,016 | Complementaria |
| Solo datos ambientales | 0,638 | -0,239 | No se clasifica |

## Criterios de aceptación

| ID | Comprobación | Resultado esperado |
|---|---|---|
| CA1 | Abrir `informe_dependencia_datos.md`. | Contiene las tres secciones. |
| CA2 | Comparar la sección 1 con `informe_validacion.txt`. | Aparecen todas las rías procesadas y los datos coinciden. |
| CA3 | Comparar la tabla de la sección 2 con los resultados de la spec 2. | Aparecen todas las configuraciones y los valores coinciden. |
| CA4 | Aplicar a mano la regla de clasificación a la tabla de la sección 2. | Se obtiene la misma clasificación que indica el informe. |
| CA5 | Leer la sección 3. | Indica qué necesita una ría nueva, con los mismos requisitos que la spec 1, y responde si se puede predecir sin datos de toxinas. |
