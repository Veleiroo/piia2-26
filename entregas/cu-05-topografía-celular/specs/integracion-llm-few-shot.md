# Integración LLM few-shot: predicción de morfología desde topografías

## Qué construir y para qué

Un módulo experimental que reciba una descripción estructurada de la topografía
de un scaffold y estime medidas de morfología nuclear usando un LLM con unos
pocos ejemplos en el contexto. Cada ejemplo relacionará una topografía conocida
con medidas observadas mediante la [funcionalidad de CV](vision-por-computador.md).

La escasez de datos motiva explorar *few-shot*: proporcionar ejemplos al modelo
en el momento de la consulta. El objetivo es comprobar si aporta valor frente a
una referencia sencilla, con resultados numéricos que puedan contrastarse. La
salida inicial será una estimación de medidas geométricas, sin generar una imagen
3D del núcleo.

## Entradas y salidas

**Consulta:** identificador del caso, tipo de patrón y descriptores físicos que
estén documentados, con sus unidades. Entre los posibles descriptores están
anchura, profundidad y separación entre elementos. Se podrán incorporar tipo
celular o tiempo de cultivo cuando estén confirmados y sean necesarios para
comparar los ejemplos. Los campos ausentes se indican explícitamente.

**Ejemplos few-shot:** pares de esos mismos descriptores con una respuesta nuclear
observada, su procedencia y su grupo experimental. Para reducir la influencia de
múltiples núcleos de una misma muestra, la primera versión resumirá sus núcleos
admitidos mediante la mediana de volumen y de cada eje `a ≥ b ≥ c`. La pertenencia
de las adquisiciones a muestras independientes debe quedar documentada antes de
construir estos resúmenes.

**Respuesta:** un objeto estructurado con:

- Estado de la consulta: `prediccion`, `datos_insuficientes` o `error`.
- Si procede, volumen esperado en µm³ y ejes esperados `a ≥ b ≥ c` en µm. Las
  relaciones `a/b` y `b/c` se calculan a partir de esos ejes.
- Identificadores de los ejemplos utilizados y una explicación breve apoyada en
  la información suministrada.
- Motivo de la abstención o del error, cuando no se produzca una predicción válida.

La estimación representa una respuesta típica de la muestra bajo esas condiciones;
no identifica la forma exacta de un núcleo individual aún no observado.

## Comportamiento esperado

1. **Preparar los pares.** Unir descriptores experimentales y medidas CV revisadas
   mediante identificadores explícitos. Conservar las unidades, el número de
   núcleos incluidos en el resumen y las exclusiones aplicadas.
2. **Comprobar viabilidad.** Verificar que se conoce la respuesta objetivo y la
   procedencia de los ejemplos. La etiqueta `G10` puede utilizarse como categoría;
   no se traduce automáticamente a una dimensión de 10 µm.
3. **Separar ejemplos y evaluación.** Agrupar imágenes relacionadas y réplicas
   según su procedencia experimental. Todos los datos de un mismo grupo quedan
   en la misma partición. Elegir los ejemplos del contexto únicamente entre los
   grupos disponibles para entrenamiento.
4. **Construir el prompt.** Combinar una plantilla versionada, el significado y
   unidades de los campos, los ejemplos seleccionados y la consulta. Las medidas
   observadas de la consulta de evaluación permanecen fuera del prompt.
5. **Consultar y validar.** Enviar el contexto al LLM elegido, interpretar su
   respuesta y comprobar estructura, unidades, valores positivos y orden de los
   ejes. Una respuesta inválida se registra como fallo; no se sustituye por una
   cifra inventada ni se descarta silenciosamente de la evaluación.
6. **Evaluar y guardar.** Comparar las predicciones con las medidas reservadas y
   con una referencia que prediga la media de entrenamiento por variable, usando
   exactamente los mismos casos. Conservar prompts, respuestas y resultados.

## Restricciones y supuestos

- El LLM recibe descriptores de topografía y condiciones conocidas para la
  consulta. Las medidas nucleares de esa consulta son la respuesta que se quiere
  predecir; solo se aportan para los ejemplos de entrenamiento.
- Se emplearán las variables realmente disponibles. Los artículos pueden orientar
  la elección de descriptores, pero sus condiciones no se atribuyen a nuestras
  muestras sin confirmación.
- Los pocos datos actuales cubren las etiquetas control y G10. No permiten dar
  por demostrada la predicción para nuevas geometrías o condiciones.
- Los planos Z, recortes y aumentos de una misma adquisición no se convierten en
  ejemplos independientes. La posible relación entre `control 2` y `control 3`
  debe resolverse o agruparse conservadoramente al preparar la evaluación.
- El número de ejemplos en contexto debe poder configurarse. Su selección y
  cualquier ajuste del prompt se hacen sin consultar las respuestas reservadas
  para evaluación.
- La primera versión usa un modelo preentrenado mediante ejemplos en contexto.
  La elección del LLM y de cómo ejecutarlo se justificará en las decisiones de
  implementación; no se presupone entrenamiento ni ajuste de sus pesos.
- La explicación del LLM se presenta como justificación de una estimación, sin
  atribuirle una relación causal demostrada. Tampoco se interpreta una confianza
  verbal del modelo como incertidumbre calibrada.
- Si no es posible reservar un grupo independiente con ejemplos en entrenamiento,
  se podrá demostrar la integración, pero el resultado se identificará como
  prototipo sin evaluación predictiva independiente.

## Criterios de aceptación

| ID | Condición verificable |
|---|---|
| LLM-01 | Cada ejemplo puede rastrearse hasta sus descriptores experimentales, grupo de origen y núcleos CV admitidos. El resumen de respuesta coincide con las medianas de esos núcleos y conserva unidades y tamaño del grupo. |
| LLM-02 | Una consulta con campos obligatorios ausentes, unidades incompatibles o sin ejemplos utilizables devuelve `datos_insuficientes` con la causa y no produce medidas numéricas como si fueran válidas. Los campos obligatorios se fijan en la configuración del experimento antes de evaluarlo. |
| LLM-03 | El prompt guardado permite verificar qué ejemplos recibió el modelo, cuántos son y qué consulta se realizó. Ninguna medida objetivo de la consulta ni dato de un grupo reservado aparece entre los ejemplos few-shot. |
| LLM-04 | La respuesta se valida contra un esquema con los estados y campos definidos. Una predicción admitida contiene volumen y ejes positivos en las unidades acordadas, `a ≥ b ≥ c` y relaciones calculadas coherentes; las salidas inválidas quedan registradas como fallos. |
| LLM-05 | Cada ejecución registra modelo y versión o identificador disponible, plantilla, configuración de generación, selección y orden de ejemplos, consulta y respuesta original. Estos registros permiten repetir la configuración, aunque un servicio externo pueda introducir variación. |
| LLM-06 | Cuando los grupos disponibles lo permiten, se realiza una evaluación reservando grupos completos y se exportan predicciones LLM y de la media de entrenamiento para los mismos casos. Se informa MAE por variable con sus unidades, número de grupos evaluados, cobertura de respuestas válidas y fallos o abstenciones. |
| LLM-07 | Si los grupos o los pares disponibles impiden esa evaluación, el informe registra el motivo y distingue la demostración funcional de una validación predictiva. No se genera una puntuación de generalización a partir de capas o recortes relacionados. |

## Decisiones pendientes

Confirmar los descriptores físicos disponibles y la agrupación experimental;
elegir el LLM, la plantilla y el número de ejemplos; y definir las particiones
con los pares que finalmente puedan construirse. La integración se evaluará
aunque no supere a la referencia: el criterio de esta funcionalidad es producir
una comparación trazable y comunicar sus resultados y límites.
