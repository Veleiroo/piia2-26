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

**Consulta:** identificador del caso, descripción del tipo de patrón y su medida
nominal, según la información disponible y el artículo de referencia. El tipo
indica, por ejemplo, si la superficie es lisa o presenta surcos o agujeros. La
medida incluye valor, unidad y la dimensión que describe según esa fuente.
Para una superficie lisa, se admite que la medida de patrón sea `no_aplica`.

Estas son las entradas topográficas disponibles para la primera versión. No se
presuponen medidas adicionales de profundidad, separación, orientación o curvatura,
ni se exige reconstruir el scaffold. Se conserva la fuente de la descripción.

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
   procedencia de los ejemplos. Asociar cada etiqueta experimental, como `G10`,
   con el tipo y la medida nominal documentados en la descripción del patrón.
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

- El LLM recibe el tipo de patrón y su medida nominal para la consulta. Las
  medidas nucleares de esa consulta son la respuesta que se quiere predecir;
  solo se aportan para los ejemplos de entrenamiento.
- Las respuestas observadas proceden de máscaras revisadas visualmente, sin
  ground truth de segmentación. Por ello, el error del predictor expresa su
  diferencia respecto a las medidas obtenidas por el flujo de CV; no demuestra
  exactitud respecto a la morfología real y puede heredar errores de las máscaras.
- La descripción del artículo se usa para caracterizar nominalmente cada tipo
  de scaffold. Se conserva qué dimensión representa la medida; un mismo valor
  numérico no implica la misma geometría para patrones distintos. No se
  requieren otras propiedades físicas como entrada de esta primera versión.
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
- Para ejecutar la evaluación predictiva frente a la referencia sencilla se fija
  un mínimo provisional de **4 grupos experimentales independientes**: al menos
  **2 grupos en entrenamiento** (para seleccionar ejemplos en contexto) y al
  menos **2 casos independientes de prueba** fuera del prompt. Si no se alcanza
  ese mínimo, se podrá demostrar la integración, pero el resultado se
  identificará como prototipo sin evaluación predictiva independiente.

## Criterios de aceptación

Para comprobar que esta parte funciona, revisaremos lo siguiente:

1. **Los ejemplos contienen los datos necesarios.** Cada uno relaciona un tipo
   de patrón y su medida con las medidas nucleares obtenidas mediante CV. Se
   indica de qué muestra proceden y qué núcleos se han usado para calcular las
   medianas, de modo que podamos comprobar los valores.

2. **El sistema avisa si falta información.** Si no se indica el tipo de patrón,
   falta su medida cuando es necesaria o no hay ejemplos disponibles, explica
   qué falta y no devuelve una predicción. Un control liso se admite sin asignarle
   un tamaño de patrón que no tiene.

3. **El LLM devuelve una respuesta que podamos utilizar.** Al recibir una consulta
   y ejemplos completos, devuelve el volumen y los tres ejes, con sus unidades,
   junto a una explicación breve. Se comprueba que los valores sean positivos y
   que los ejes estén ordenados de mayor a menor. Si la respuesta no se puede leer
   o incumple estas condiciones, se guarda como un fallo.

4. **La prueba no incluye la respuesta que queremos predecir.** Las medidas
   nucleares del caso que estamos probando no aparecen entre los ejemplos del
   prompt. Tampoco se usan recortes o capas de esa misma captura como si
   fueran ejemplos independientes.

5. **Podemos configurar el número de ejemplos y consultar qué ocurrió en cada ejecución.**
   Se guardan el modelo y su configuración, el parámetro de número de ejemplos
   solicitados, las instrucciones, los ejemplos en el orden enviado, la consulta
   y la respuesta original. Se comprueba ejecutando una misma consulta con dos
   valores distintos de ejemplos en contexto (por ejemplo, `k = 1` y `k = 2`) y
   verificando en el registro guardado que el prompt incluye exactamente `1` y `2`
   ejemplos respectivamente.

6. **Comparamos el resultado con una alternativa sencilla.**
   Se comparan las predicciones del LLM con una referencia base consistente en predecir siempre la media de las medidas de entrenamiento. Como mínimo, se realizará esta evaluación reservando una partición de los datos disponibles como prueba, calculando cuánto se alejan las predicciones, en promedio, de las medidas obtenidas por CV (error absoluto medio, MAE).


7. **Las conclusiones reflejan los datos que tenemos.** Si se dispone de menos de
   4 grupos experimentales independientes (o menos de 2 casos de prueba
   independientes), explicamos la limitación y mostramos únicamente que la
   integración funciona. La revisión visual de las máscaras y una demostración
   del LLM no se presentan como pruebas de exactitud predictiva.
   
## Decisiones pendientes

Antes de implementar y probar esta parte tenemos que decidir:

- **Qué LLM vamos a usar y cómo ejecutarlo:** elegir el modelo y si lo ejecutamos
  en nuestro equipo o mediante un servicio externo.
- **Cómo presentarle los ejemplos:** redactar las instrucciones, elegir cuántos
  ejemplos incluir y cómo seleccionarlos entre los disponibles.
- **Qué muestras podemos reservar para probarlo:** aclarar qué carpetas son
  capturas distintas del microscopio y cuáles pueden ser recortes de la misma
  captura. Con esa información separaremos los ejemplos del prompt de los casos
  de prueba.

Además, dejaremos registrada la correspondencia entre cada muestra y el tipo y
la medida del scaffold descritos en el artículo. Esa información es la que se
usará para preparar las entradas del modelo.
