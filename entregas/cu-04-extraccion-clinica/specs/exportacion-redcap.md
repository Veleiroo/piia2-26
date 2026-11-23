# RCP-001 — Estructuración y preparación de resultados compatibles con REDCap

## 1. Identificación y propósito

| Referencia | Descripción |
|---|---|
| Identificador | `RCP-001` |
| Proyecto | CU-04 — Extracción y estructuración de información clínica para REDCap |
| Propósito | Relacionar los candidatos clínicos con los campos seleccionados del estudio, validar su correspondencia, tipos y códigos y preparar resultados para su eventual incorporación a REDCap. |
| Entrada clínica | Resultados de [CLI-001](extraccion-datos-clinicos.md), con sus estados, contextos y evidencias procedentes de [DOC-001](ingesta-documentos.md). |
| Resultado inicial propuesto | Representación intermedia con valores preparados, incidencias y decisiones de incorporación pendientes. |
| Marco de alcance | [README del proyecto](../README.md) |
| Referencia de evaluación | [Entrega 1](../../../evaluacion/entrega-1.md) |

Esta spec define la **propuesta funcional del equipo**. Las obligaciones descritas no constituyen decisiones ya confirmadas por Ceres Fernández Rozadilla. «Compatible» significa conforme a las definiciones y reglas suministradas para los campos seleccionados; no acredita por sí solo validez clínica, aprobación humana ni aceptación por una operación real de importación.

## 2. Motivación y problema que resuelve

Los candidatos clínicos no son todavía valores listos para un estudio: deben relacionarse con campos concretos, categorías codificadas, formatos y dependencias. Transcribirlos sin esas comprobaciones puede perder contexto o convertir una ausencia documental en una respuesta negativa.

RCP-001 busca reducir la transcripción y codificación manual, conservando las evidencias y señalando lo que no puede prepararse sin una decisión adicional. Su responsabilidad es validar la representación de resultados ya interpretados por CLI-001; no volver a interpretar la historia clínica.

## 3. Alcance funcional

**Incluido en la propuesta:**

- Trabajar con una selección explícita de campos y las definiciones aplicables del libro de códigos.
- Aplicar correspondencias explícitas entre resultados clínicos y campos, considerando concepto, sujeto, contexto y ámbito temporal.
- Validar texto, números, fechas, valores binarios, categorías y selecciones múltiples, usando los códigos definidos cuando corresponda.
- Considerar dependencias conocidas, campos calculados y descriptivos, distinguiendo preparación de valores de inclusión en una incorporación posterior.
- Conservar estados clínicos, trazabilidad e incidencias en una representación intermedia.

**Fuera del alcance:**

- Seleccionar las variables prioritarias del estudio, inventar definiciones o deducir correspondencias únicamente por semejanza de nombres.
- Recuperar documentación original, reinterpretar evidencias, resolver contradicciones clínicas o elegir candidatos sin reglas acordadas.
- Recalcular automáticamente campos calculados como si fueran entradas clínicas ordinarias.
- Crear campos en REDCap, acceder a su base de datos, escribir registros o imponer una integración mediante API.
- Fijar CSV, JSON u otro formato de salida definitivo, ni reglas de creación, actualización o sobrescritura de registros.

## 4. Entradas y resultados esperados

### Entradas

1. **Resultados de CLI-001 de un único paciente:** variables solicitadas, candidatos, estados de interpretación, sujeto, fechas, ámbito temporal, relaciones entre menciones, evidencias y limitaciones de DOC-001.
2. **Selección de campos del estudio y diccionario aplicable:** identificadores internos, etiquetas, tipos, opciones y códigos, validaciones, dependencias y naturaleza de los campos calculados o descriptivos. Debe poder identificarse qué versión o referencia documental se ha utilizado, sin imponer un mecanismo técnico de versionado.
3. **Reglas de correspondencia y del estudio:** relación entre cada variable clínica y campo, contextos admitidos, transformaciones permitidas, tratamiento de estados sin valor y condiciones conocidas de incorporación. Estas reglas no se consideran disponibles ni aprobadas por defecto.

Si faltan el diccionario o la selección, no se generan valores de destino y se comunica la entrada incompleta; una selección vacía produce un resultado sin campos que preparar. Si solo falta la definición de un campo o su correspondencia, se informa por campo y se continúa con los que sí puedan evaluarse.

### Representación intermedia

Cada campo solicitado debe figurar con un resultado, incluso si es desconocido, no admite entrada o carece de valor. Los campos no seleccionados no generan asignaciones de destino. La salida debe ofrecer:

| Información | Contenido necesario |
|---|---|
| Definición aplicada | Identificador de campo, referencia del diccionario, regla de correspondencia y validaciones utilizadas, o motivo por el que no están disponibles. |
| Valor preparado | Valor o códigos internos conformes a la definición, cuando pueda obtenerse una asignación justificada. Un candidato original incompatible puede conservarse para revisión, identificado como tal y separado del valor preparado. |
| Estado de preparación | Preparado y validado; sin dato para preparar; incompatible; pendiente de resolución o revisión; o no es campo de entrada. |
| Contexto clínico | Estado recibido de CLI-001, sujeto, fechas, sospecha o afirmación, selección temporal pendiente y limitaciones de cobertura. La codificación no elimina estos datos. |
| Trazabilidad | Resultado y evidencias de CLI-001 que originan la asignación; referencias de DOC-001 a documentos, páginas y bloques o elementos. Deben identificarse también las reglas o transformaciones aplicadas. |
| Dependencias | Condiciones evaluadas, resultado —cumplida, no cumplida o no evaluable— y valores o estados utilizados para evaluarlas. |
| Incorporación propuesta | Proponible según las reglas suministradas, excluida por una regla explícita o pendiente de decidir, con su motivo. No equivale a importación ejecutada ni a aprobación humana. |
| Incidencias | Errores de definición, correspondencia, validación o trazabilidad y advertencias que requieran resolución. |

Los estados de preparación se distinguen de los estados clínicos: **sin dato para preparar** puede conservar «no encontrado» de CLI-001; **pendiente de resolución o revisión** conserva la ambigüedad, contradicción o selección temporal pendiente que lo motiva. **Incompatible** identifica un valor o código que incumple una regla suministrada. Un campo desconocido queda pendiente por definición ausente, sin inventar su tipo.

La trazabilidad, los estados internos y las incidencias son metadatos de la representación intermedia. No se convierten en campos de REDCap ni se proponen como asignaciones si esos campos no existen y no han sido seleccionados. La representación permite identificar los valores validados y las exclusiones, pero su adaptación a un mecanismo real de incorporación queda pendiente.

## 5. Comportamiento funcional

### 5.1. Selección y correspondencia

1. Comprobar que cada campo solicitado existe y tiene definición suficiente. Una etiqueta sin tipo o sin opciones necesarias no permite inventar su configuración.
2. Asociar los candidatos utilizando una regla explícita compatible con la definición clínica del campo. La similitud entre etiquetas o identificadores no basta; un antecedente familiar, una sospecha o una prescripción no se convierte en un dato de otro sujeto o contexto.
3. Si falta una correspondencia inequívoca, conservar los candidatos con una incidencia de correspondencia pendiente y no asignar un valor de destino.
4. Si un campo necesita datos no solicitados o no aportados por CLI-001, informar de la dependencia sin ampliar automáticamente la extracción ni incluir nuevos campos.
5. No deducir el tipo a partir de la etiqueta. En el libro consultado las fechas y números pueden ser campos `text` con validación, y un campo que parece numérico puede estar definido solo como `text`. Los campos de identificación o estado del formulario requieren una fuente y correspondencia propias; no se rellenan por el mero éxito de la extracción.

### 5.2. Tipos, códigos y transformaciones

| Tipo o restricción | Comportamiento propuesto |
|---|---|
| Texto | Conservar el contenido que la regla permita transferir y comprobar las restricciones expresas, como longitud. No truncar ni sustituir contenido para superar una validación sin regla autorizada. |
| Numérico | Verificar que el valor es numérico y respeta unidad, precisión y límites definidos. No redondear, recortar al límite ni convertir unidades sin una regla explícita. |
| Fecha | Comprobar la fecha de calendario y la precisión y representación exigidas. No completar día o mes ausentes ni sustituir la fecha del hecho por la del informe. |
| Binario | Aplicar los códigos definidos para la afirmación o negación pertinente. No suponer que sus códigos son siempre 1 y 0 ni que un campo vacío significa «No». |
| Categórico | Utilizar el código interno de la opción que corresponda al significado del candidato y a las reglas del estudio. Una etiqueta parecida o un código válido de otro campo no bastan. |
| Selección múltiple | Relacionar cada selección respaldada con su código y conservar su evidencia. No convertir una selección parcial en una declaración de ausencia de las demás opciones. La representación o incorporación de opciones no documentadas necesita reglas explícitas. |

Una transformación meramente representacional solo se aplica si está definida y no cambia el significado clínico; deben conservarse su regla y el candidato de origen. Si el código propuesto no está definido para ese campo, un valor excede el rango o el tipo no es admitido, señalar la incompatibilidad y no ofrecer ese dato como valor validado.

Conservar también las marcas de obligatoriedad que aparezcan en la definición. Su efecto en la preparación o incorporación debe establecerse mediante la regla aplicable; una marca `Required` no permite deducir por sí sola el comportamiento de una importación. Si falta un valor exigido por una regla acordada, comunicar la incidencia sin inventarlo.

### 5.3. Estados clínicos e incertidumbre

- Un valor respaldado por evidencia solo se prepara cuando su contexto cumple la definición del campo; el estado «respaldado» de CLI-001 también puede corresponder a una sospecha o antecedente.
- Una negación explícita se codifica como respuesta negativa únicamente cuando es aplicable al sujeto, dato y ámbito temporal del campo y existe una regla de correspondencia.
- «No encontrado», «información ambigua o insuficiente», «información contradictoria» y «selección temporal pendiente» se conservan de forma diferenciada. No se rellenan con un valor negativo, una opción arbitraria o el candidato más reciente.
- Si el diccionario incluye códigos para estados sin valor, solo se utilizan cuando la regla del estudio autoriza ese estado y su significado coincide. Un código «no documentado» no representa automáticamente contradicción, sospecha o ilegibilidad.
- Si no existe esa regla, se deja el campo sin valor preparado y se comunica el motivo. No se usa una cadena vacía como instrucción de borrar ni se pierde el estado clínico.
- El resultado de CLI-001 **no evaluable por definición insuficiente** y un rechazo de entrada procedente de DOC-001 son incidencias de entrada, no «no encontrado». Se conservan como pendientes con su motivo, sin aplicarles un código de ausencia documental. No se presenta una extracción no realizada como un dato clínico ausente.
- Una limitación de DOC-001 debe mantenerse asociada a la evidencia afectada. No bloquea automáticamente un candidato legible independiente, pero tampoco permite declarar completa la cobertura documental.

### 5.4. Dependencias y campos especiales

1. Evaluar las dependencias con valores preparados y estados utilizables según la regla. Un valor ausente, contradictorio o no validado no satisface ni incumple por defecto una condición: esta queda **no evaluable**.
2. Conservar la distinción entre **visibilidad condicional** y **regla de incorporación**. Que un campo no sea visible no demuestra por sí solo que deba omitirse, borrarse o rechazarse al importar. Si falta una regla de incorporación, indicar que esa decisión está pendiente.
3. Si una regla explícita impide incorporar un campo cuando no se cumple una condición, excluirlo de los valores propuestos para incorporación y conservar el motivo y cualquier candidato en la representación intermedia. No forzar el campo del que depende para habilitarlo.
4. Si una dependencia no puede evaluarse, mantener la preparación local que sea posible y dejar pendiente su incorporación. Las dependencias circulares o las reglas no interpretables se comunican sin inventar una resolución.
5. Identificar los campos calculados y descriptivos como **no es campo de entrada**. No asignarles automáticamente candidatos, ejecutar sus fórmulas ni tratarlos como campos ordinarios; su eventual tratamiento en una incorporación requiere una decisión específica.
6. Revisar las anotaciones además del tipo: el libro contiene campos `text` con `@CALCTEXT` o `@SETVALUE`, y campos con `@DEFAULT`. No se ejecutan esas anotaciones ni se sustituyen por un candidato ordinario sin una regla de tratamiento acordada. Un valor por defecto no constituye evidencia clínica. La presencia de estas anotaciones no documenta su comportamiento en una importación.

### 5.5. Trazabilidad y preparación de la salida

- Cada asignación preparada debe permitir seguir la relación campo → resultado de CLI-001 → evidencias de DOC-001. Si intervienen varios resultados, conservar sus respectivas referencias y la regla que los combina.
- Si un valor clínico no tiene evidencia verificable, no se presenta como preparado y validado. Se conserva la incidencia de trazabilidad; no se inventan fragmentos ni referencias.
- Un código especial de ausencia se justifica mediante el estado de CLI-001, la cobertura evaluada y la regla del estudio, sin inventar una evidencia textual de la ausencia.
- Un fallo de un campo no elimina los resultados independientes válidos. Las dependencias sobre el campo fallido deben reevaluarse como no evaluables cuando corresponda.
- La salida distingue asignaciones validadas, campos sin dato, incompatibilidades y pendientes de revisión. Debe poder separarse el contenido propuesto para destino de sus metadatos, sin perder la relación entre ambos.
- Una asignación validada sin dependencias ni reglas de incorporación pendientes puede marcarse como proponible según las reglas suministradas. Si hay una exclusión explícita se marca excluida; si falta una decisión aplicable, su incorporación queda pendiente aunque el valor tenga validación local.
- «Preparado y validado» no significa revisado por una persona ni autorización de escritura. El mecanismo, la identificación de registros, los eventos o repeticiones que pueda exigir el estudio y las operaciones de incorporación deberán definirse antes de una integración real.

## 6. Restricciones y supuestos

### Contexto confirmado

- Se ha consultado `data/redcap-codes-book.pdf`, de 59 páginas, con fecha impresa de generación `15-10-2026 09:23`. Las referencias siguientes utilizan páginas físicas, coincidentes con la numeración impresa. Contiene tipos, códigos, validaciones, condiciones, anotaciones y campos calculados y descriptivos.
- La tutora ha indicado que no es necesario extraer todas las variables.
- Siguen pendientes el subconjunto prioritario, las correspondencias definitivas, la integración, el formato preferido y la eventual revisión humana.

### Definiciones verificadas en el libro real

Son referencias documentales, no variables prioritarias ni reglas de correspondencia clínica aprobadas:

| Campo o característica | Definición directamente verificada | Página |
|---|---|---|
| `entrada_por_proyecto_de_in` | Etiqueta «Entrada por proyecto de investigación», tipo `yesno`, `1` = «Sí», `0` = «No». Es una codificación específica de este campo. | 1 |
| `mes` | Tipo `dropdown`: códigos `1` a `12` para etiquetas «01» a «12». El código y la etiqueta no son intercambiables. | 1 |
| `fecha_nacimiento` | Etiqueta «Fecha Nacimiento», `text (date_dmy)`. El PDF documenta esta validación; no establece aquí el formato de una operación de transferencia. | 1 |
| `altura` e `imc` | `altura`: «Altura (cm)», `text (number)`; `imc`: «IMC», `text`, sin validación numérica indicada en esa fila. No se atribuyen límites no impresos. | 6 |
| `tipo_panel_genes` | Tipo `radio`, `0` = «Comercial», `1` = «Custom»; condición impresa `[panel_de_genes] = '1'`. `panel_de_genes` es `yesno`, con `1` = «Sí» y `0` = «No». El `0` de la categoría no es una negación clínica. | 9 |
| `utilizado_en` | Tipo `checkbox`, entre otras opciones `3` = «IMPaCT-Genómica» y `4` = «IMPaCT-Data»; figuran `utilizado_en___3` y `utilizado_en___4`. Su visibilidad depende de `[entrada_por_proyecto_de_in] = '1'`. No se infiere de esos nombres una convención universal de importación. | 4 |
| `gen_es` | Tipo `checkbox`, entre otras opciones `0` = «APC», con nombre asociado `gen_es___0`. El código de opción `0` tampoco significa «no seleccionado». No se transcribe aquí su condición completa, afectada por ligaduras tipográficas en el identificador de dependencia. | 5 |
| `etnia` | Tipo `dropdown`, contiene `777` = «Otra (especificar)» y `999` = «No Disponible». Su existencia no autoriza a utilizar `999` para cualquier incertidumbre de CLI-001. | 6 |
| `edad_entrada_al_proyecto` y `ano_nacimiento` | El primero es `calc`, con cálculo impreso `[a_o_ci]-[a_o]`; el segundo es `descriptive`. Se conserva la definición, sin corregir o reinterpretar la fórmula. | 3 y 1 |
| `c_digo_ceic` y otras anotaciones | `c_digo_ceic` es `text` con una expresión `@CALCTEXT`. También aparecen `@DEFAULT` en pp. 37 y 59 y `@SETVALUE` en p. 50. El tipo básico no basta para decidir su tratamiento. | 2, 37, 50 y 59 |
| Obligatoriedad y estado de formulario | Hay una marca `Required` junto a `text (date_dmy)` en p. 3. `informacin_general_complete` es un `dropdown` de estado; incluye `2` = «Complete». Ese código no demuestra revisión clínica ni debe asignarse por terminar RCP-001. | 3 y 4 |
| Dependencia cruzada | La condición impresa para `resultado_exoma` remite a `resultado_genoma_completo`, cuyo campo aparece en p. 11. No se sustituye por una dependencia que parezca más plausible. | 10 y 11 |

Algunos identificadores y expresiones del PDF contienen ligaduras tipográficas o se parten entre líneas. Si su lectura no permite establecer el identificador o la expresión exactos, quedan pendientes de una fuente inequívoca; no se normalizan por intuición. Tampoco se transforma «Mostrar el archivo SOLO si» en una prohibición de importación. No constan en las filas citadas de `altura` límites numéricos, ni en ellas una regla de revisión o transferencia; DS-01 no completa esas ausencias.

### Propuestas funcionales del equipo

- Salida intermedia sin escritura automática, con validación por campo y separación entre valor, estado clínico, trazabilidad y decisión de incorporación.
- Correspondencias explícitas, conservación de incertidumbre y tratamiento independiente de las incidencias que no afecten a otros campos.
- Los estados, el diccionario sintético y los criterios siguientes son propuestas para verificar el contrato, no reglas reales confirmadas del estudio.

### Supuestos de funcionamiento

- CLI-001 entrega conjuntamente candidatos, contextos, estados y referencias; no se presupone que todos los resultados puedan resolverse.
- Para validar un campo se dispondrá de sus definiciones y dependencias aplicables, y de una correspondencia acordada. Su disponibilidad se verifica, no se da por hecha.
- La sintaxis técnica de las reglas podrá definirse posteriormente. Una regla no interpretable no se considera cumplida por omisión.

### Referencias, privacidad y límites técnicos

Esta spec conserva referencias puntuales al libro de códigos consultado y un diccionario sintético para probar comportamientos generales. No reproduce el documento completo. Las correspondencias clínicas y los campos finalmente seleccionados requieren validación con la entidad; verificar una definición documental no equivale a aprobar su uso en el estudio.

No se incorporan historias clínicas reales, datos de pacientes ni ejemplos derivados de ellos. El acceso, conservación y tratamiento de los resultados y evidencias reales deben acordarse con la entidad. No se fijan tecnologías, proveedores, formato de serialización, comportamiento de la API ni métricas arbitrarias.

## 7. Criterios de aceptación

### Diccionario sintético de referencia DS-01

DS-01 es exclusivamente una referencia de prueba, no una propuesta de variables prioritarias ni una reproducción del diccionario real. Sus identificadores, códigos y reglas se definen expresamente a continuación. «Afección Alfa», «marcador Gamma» y los tratamientos son ficticios.

Se conserva para comprobar rangos, longitudes, codificación de incertidumbre y reglas de incorporación que no están establecidos para los campos reales citados. Sus límites 0–100 y 40 caracteres, el código `99`, la fecha `AAAA-MM-DD` y las reglas de incorporación son exclusivamente sintéticos; no se atribuyen al libro real.

| Campo | Tipo y definición de prueba | Correspondencia y reglas expresas del estudio sintético |
|---|---|---|
| `alfa_presente` | Binario: `1` = afirmación diagnóstica confirmada documentada; `0` = negación explícita documentada. | Resultado de Alfa referido al paciente y al ámbito solicitado. Una sospecha no corresponde a ninguno de los dos códigos. No hay código para ausencia de información. |
| `alfa_estado` | Categórico: `11` = confirmada; `22` = sospechada; `99` = no encontrado en la documentación disponible. | Resultado de Alfa en el ámbito solicitado. Se autoriza `99` solo para el estado «no encontrado» de CLI-001, conservando su cobertura; no para ambigüedad, contradicción o falta total de contenido evaluable. |
| `gamma_valor` | Decimal, de 0 a 100 inclusive, en unidad ficticia `u`. | Valor de Gamma en el ámbito solicitado. Se admite representar `7,5` como el número 7.5; no hay conversión de unidades ni redondeo autorizado. |
| `fecha_hecho` | Fecha completa válida de calendario, representada como `AAAA-MM-DD`. | Fecha del hecho seleccionado por CLI-001, no fecha del documento. No se permite completar fechas parciales. |
| `nota_estudio` | Texto de hasta 40 caracteres. | Transferencia literal del candidato textual «nota para el estudio» de CLI-001, sin truncado ni generación de texto nuevo. |
| `tratamientos` | Selección múltiple: `3` = Beta; `8` = Delta; `12` = Épsilon. | Tratamientos que CLI-001 identifica como administrados en el ámbito solicitado. Se preparan códigos por opción respaldada; una opción no documentada queda sin determinación. La incorporación de una selección parcial queda pendiente de una regla que preserve las opciones no determinadas. |
| `alfa_detalle` | Texto de hasta 40 caracteres; visible si `alfa_presente` es `1`. | Candidato textual de detalle de Alfa. Regla adicional de incorporación: proponerlo solo si `alfa_presente` tiene valor validado `1`; excluirlo si es `0`; si no puede evaluarse, dejar la incorporación pendiente. |
| `derivado_gamma` | Calculado: Gamma más 1. | Campo calculado, no asignable como entrada en estos escenarios. No se ejecuta la fórmula en RCP-001. |
| `instrucciones` | Descriptivo: texto de instrucciones del formulario. | No admite asignación de un valor clínico en estos escenarios. |
| `sin_tipo` | Solo etiqueta «Campo sin completar»; no se define tipo ni validaciones. | Definición insuficiente; no hay correspondencia autorizada. |

### Escenarios y resultados exigidos

Cada escenario indica los campos seleccionados, la parte de DS-01 aplicable y la salida sintética de CLI-001. Salvo indicación contraria, el ámbito temporal y el sujeto coinciden con la definición del campo, las correspondencias anteriores están disponibles y los candidatos son inequívocos y respaldados por evidencia.

Cada resultado clínico tiene una referencia propia —C1, C2, etc.— y evidencias de DOC-001 con documento, página y bloque o elemento. La verificación utiliza estas entradas ya preparadas; no exige ejecutar extracción clínica, procesar PDF ni contactar con REDCap. Los valores concretos exigidos no pueden sustituirse siempre por un error o un estado desconocido.

| Identificador | Entrada y fragmento de diccionario aplicable | Resultado observable exigido |
|---|---|---|
| `RCP-001-CA01` | DS-01, `nota_estudio` seleccionado; C1 contiene la nota «Control programado». | Valor preparado «Control programado», estado preparado y validado, con referencia a C1 y su evidencia. No se genera otro texto ni se devuelve solo un error. |
| `RCP-001-CA02` | DS-01; solo `gamma_valor` seleccionado. CLI-001 aporta Gamma = 5 u y una afirmación confirmada de Alfa. | Se prepara `gamma_valor` = 5. No se crean asignaciones para `alfa_presente`, `alfa_estado` ni otros campos no seleccionados. |
| `RCP-001-CA03` | DS-01, `alfa_estado` seleccionado; C1 indica sospecha de Alfa. | Se prepara el código `22`, no la etiqueta «sospechada» como valor de destino ni el código `11`. Se conserva el contexto de sospecha de CLI-001. |
| `RCP-001-CA04` | DS-01, `gamma_valor`; tres entradas independientes: 7,5 u, 125 u y «alto» sin valor numérico. | La primera prepara el número 7.5 y registra la transformación permitida. La segunda indica incompatibilidad de rango y no prepara 100 ni 125. La tercera indica incompatibilidad con el tipo numérico, sin inventar una cifra. |
| `RCP-001-CA05` | DS-01, `fecha_hecho`; tres entradas: hecho fechado el 4 de abril de 2021, hecho con fecha «31 de febrero de 2025» y hecho fechado solo en 2021. El informe tiene fecha 10 de junio de 2026. | La primera prepara `2021-04-04`. La segunda indica fecha de calendario inválida y no prepara valor. La tercera queda sin valor preparado por precisión insuficiente. En ninguna se utiliza la fecha del informe para sustituir la del hecho. |
| `RCP-001-CA06` | DS-01, `tratamientos`; C1 indica administración de Beta y C2 de Delta. No hay información sobre Épsilon. | Se preparan las opciones `3` y `8` con sus respectivas evidencias; Épsilon permanece no determinado, sin asignación negativa. La codificación de las opciones está validada, pero la incorporación de la selección parcial queda pendiente según la regla de DS-01. |
| `RCP-001-CA07` | DS-01, `alfa_presente`; dos entradas: negación explícita de Alfa y estado «no encontrado» sin candidato. | En la primera se prepara `0` y se conserva la negación y su evidencia. En la segunda el campo queda sin dato para preparar, conserva «no encontrado» y no recibe `0`. |
| `RCP-001-CA08` | DS-01, `alfa_estado`; cuatro entradas: «no encontrado», información ambigua, contenido no evaluable por ilegibilidad y variable no evaluable por definición insuficiente. | Solo la primera recibe `99`, con el estado y cobertura originales. Las otras quedan sin valor preparado y pendientes de resolución, con sus motivos diferenciados; no se utiliza `99` para ocultar insuficiencia de contenido o definición. |
| `RCP-001-CA09` | DS-01, `alfa_estado`; CLI-001 conserva afirmación y negación de Alfa en el mismo ámbito, con dos evidencias y estado contradictorio. | Se conservan el estado contradictorio y ambas evidencias; no se prepara `11`, `22` ni `99`. El campo queda pendiente de resolución. |
| `RCP-001-CA10` | DS-01, `gamma_valor`; CLI-001 aporta 5 u en 2024 y 8 u en 2025, con selección temporal pendiente. | Se conservan ambos candidatos y sus fechas, sin preparar un valor único. No se elige 8 por ser más reciente; se mantiene la selección temporal pendiente como motivo de resolución. |
| `RCP-001-CA11` | DS-01, `alfa_presente` y `alfa_detalle`; C1 confirma Alfa y C2 contiene el detalle «Detalle sintético». | Se prepara `alfa_presente` = `1` y `alfa_detalle` = «Detalle sintético»; la condición queda cumplida y ambos campos son proponibles según las reglas sintéticas suministradas, sin afirmar aprobación humana ni importación ejecutada. |
| `RCP-001-CA12` | Mismos campos y detalle que CA11; tres entradas para Alfa: negación explícita, no encontrado e información contradictoria. | Con negación se prepara `0` y se excluye el detalle de los valores propuestos para incorporación por la regla explícita, conservándolo en la representación intermedia. En las otras dos entradas la dependencia no es evaluable y la incorporación del detalle queda pendiente; no se convierte el valor ausente en `0`. |
| `RCP-001-CA13` | DS-01, `derivado_gamma` e `instrucciones` seleccionados; CLI-001 aporta Gamma = 5 u y un texto candidato. | Ambos figuran como no es campo de entrada. No se asigna 6 a `derivado_gamma` ni se transfiere el texto a `instrucciones`. |
| `RCP-001-CA14` | Se selecciona `gamma_valor` y se suministran sus restricciones de tipo, rango y unidad de DS-01, pero se omite la regla de correspondencia entre Gamma y el campo; solo se señala que sus nombres se parecen. C1 contiene 5 u. | Correspondencia pendiente, con C1 conservado para revisión y sin valor preparado. La coincidencia de nombres no sustituye la regla ausente. |
| `RCP-001-CA15` | DS-01; se seleccionan `fantasma` —inexistente—, `sin_tipo` y `nota_estudio`. C1 contiene «Control programado» para la nota. | Se informa campo desconocido para `fantasma` y definición insuficiente para `sin_tipo`, sin inventar configuración. La nota se prepara y valida de forma independiente. |
| `RCP-001-CA16` | DS-01, `fecha_hecho`; C1 aporta la fecha del hecho y depende de D1/página 2/B1 para identificarlo y D2/página 4/B2 para fecharlo el 6 de julio de 2020. | Se prepara `2020-07-06` y se conservan C1, ambas referencias documentales y la correspondencia aplicada. Ninguna evidencia se atribuye a un bloque distinto del que la sustenta. |
| `RCP-001-CA17` | DS-01; selección de `nota_estudio`, `gamma_valor` y `alfa_presente`. C1 = «Control programado», C2 = 5 u y C3 = negación explícita de Alfa, con evidencias. | La salida ofrece exactamente esas tres asignaciones validadas: texto «Control programado», número 5 y código `0`. Todas son proponibles según las reglas suministradas. Los estados, las evidencias y los motivos siguen vinculados como metadatos, sin crear campos de destino adicionales ni afirmar envío a REDCap. |
| `RCP-001-CA18` | DS-01, `alfa_presente`; C1 solo documenta sospecha de Alfa. | No se prepara `1` ni `0`. Se conserva la sospecha y se señala que no corresponde a las opciones del campo; queda pendiente de resolución, sin convertirla en diagnóstico confirmado ni negación. |
| `RCP-001-CA19` | DS-01, `nota_estudio`; C1 contiene 41 caracteres «A». En otra entrada, `gamma_valor` recibe 5 en una unidad distinta de `u`, sin conversión definida. | La primera indica incompatibilidad de longitud, sin truncar a 40 caracteres. La segunda indica incompatibilidad de unidad, sin convertir ni preparar 5 como si fueran `u`. |
| `RCP-001-CA20` | DS-01, `gamma_valor`; C1 = 5 u, sin referencias a evidencias. En otra entrada, C1 sí remite a un bloque legible de D1, pero otra página de D1 tiene un error de DOC-001. | La primera queda pendiente por trazabilidad insuficiente, sin valor validado. La segunda conserva el valor 5 validado y su evidencia, junto con la advertencia de cobertura; no declara completa la lectura del documento. |
| `RCP-001-CA21` | Variante de DS-01: `alfa_detalle` conserva únicamente la regla de visibilidad, sin regla de incorporación. Se seleccionan `alfa_presente` y `alfa_detalle`; hay negación explícita de Alfa y detalle textual válido. | Se prepara `0`, se evalúa la visibilidad como no cumplida y se conserva el detalle con su validación local. Su incorporación queda pendiente, sin inferir de la invisibilidad una prohibición, un borrado o una asignación negativa. |
| `RCP-001-CA22` | Dos solicitudes: diccionario ausente con selección no vacía; DS-01 disponible con selección vacía. | La primera comunica que falta el diccionario y no genera asignaciones de destino. La segunda comunica que no hay campos seleccionados y produce un resultado sin asignaciones; no selecciona campos automáticamente. |
| `RCP-001-CA23` | DS-01, `alfa_estado`; C1 confirma Alfa, pero la regla de correspondencia suministrada propone erróneamente el código `1`, que pertenece a `alfa_presente` y no es una opción de `alfa_estado`. | Se señala incompatibilidad del código con el campo y de la regla suministrada con DS-01. No se prepara `1` ni se sustituye silenciosamente por otro código; se conserva C1 para corregir la correspondencia. |

Cada escenario se comprueba sobre la representación intermedia, incluidos sus motivos y referencias. Superarlos no demuestra compatibilidad con una importación real hasta que se definan y verifiquen el diccionario definitivo y el mecanismo elegido. No se exige escribir en REDCap ni fijar porcentajes de rendimiento para aceptar este contrato funcional.

### Escenarios con definiciones del libro real y datos ficticios

Los casos siguientes complementan DS-01. Los nombres, tipos y códigos proceden exclusivamente de `data/redcap-codes-book.pdf`, en las páginas indicadas; los candidatos y sus evidencias son completamente ficticios. Las correspondencias se estipulan solo para cada prueba de codificación, sin establecer reglas clínicas del proyecto. No implican que los campos deban extraerse ni que exista autorización para importarlos. La trazabilidad clínica usa las mismas referencias sintéticas de los casos anteriores y añade la definición documental aplicada.

| Identificador | Entrada y definición verificada | Resultado observable exigido |
|---|---|---|
| `RCP-001-CA24` | Se selecciona `mes`, `dropdown` en p. 1; la correspondencia de prueba aporta una selección inequívoca de la etiqueta «01» y, en otra entrada, de «12». | Se preparan respectivamente los códigos `1` y `12`, no la etiqueta «01» como código. Se conserva la referencia a p. 1 y al resultado clínico sintético utilizado para la prueba. |
| `RCP-001-CA25` | Se seleccionan `panel_de_genes` y `tipo_panel_genes` según p. 9. Los datos ficticios estipulan respuesta «Sí» para el primero y opción «Comercial» para el segundo. | Se preparan `panel_de_genes` = `1` y `tipo_panel_genes` = `0`; se verifica la condición impresa. El segundo `0` conserva su significado «Comercial», sin convertirse en negación clínica. La visibilidad no se presenta como autorización de importación. |
| `RCP-001-CA26` | Se seleccionan `altura`, `text (number)` en p. 6, y `fecha_nacimiento`, `text (date_dmy)` en p. 1. Candidatos ficticios: 123 cm y fecha completa 29 de febrero de 2000; otra entrada da fecha 31 de febrero de 2000. | Se valida el número 123, sin imponer el rango de DS-01. La fecha preparada conserva día 29, mes 2 y año 2000 y su validación `date_dmy`; la fecha imposible se señala como incompatible y no se prepara. No se impone el formato sintético de DS-01 como máscara de transferencia del estudio. |
| `RCP-001-CA27` | Se seleccionan `entrada_por_proyecto_de_in` —p. 1— y `utilizado_en` —p. 4—. La respuesta ficticia del primero es «Sí» y se aportan las opciones «IMPaCT-Genómica» y «IMPaCT-Data» para el segundo; las demás opciones no están determinadas. | Se prepara `1` para la dependencia y las opciones `3` y `4` para `utilizado_en`, manteniendo los nombres asociados documentados `utilizado_en___3` y `utilizado_en___4`. No se deducen respuestas para otras opciones. La visibilidad es evaluable, pero la incorporación parcial queda pendiente de reglas no documentadas por esas filas. |
| `RCP-001-CA28` | Se seleccionan `edad_entrada_al_proyecto` —`calc`, p. 3—, `ano_nacimiento` —`descriptive`, p. 1— y `c_digo_ceic` —`text` con `@CALCTEXT`, p. 2—. Se ofrecen candidatos ficticios para los tres. | Los dos primeros no reciben valores como entradas ordinarias ni se ejecuta el cálculo. El tercero queda pendiente de una regla específica de tratamiento de la anotación, sin asignar el candidato como texto ordinario ni ejecutar la expresión por defecto. |
| `RCP-001-CA29` | Se selecciona `etnia`, cuyo `dropdown` contiene `999` = «No Disponible» —p. 6—. CLI-001 devuelve «no encontrado» y no se aporta regla de estudio que autorice su correspondencia con `999`. | Se conserva «no encontrado», sin dato para preparar y con la codificación de ausencia pendiente. No se asigna `999` por la mera existencia de la etiqueta ni se traslada el permiso sintético para `99` de DS-01. |

## 8. Cuestiones abiertas

Estas decisiones siguen pendientes; la lista no afirma que todas hayan sido consultadas ni atribuye respuestas a Ceres:

- **Campos prioritarios y diccionario aplicable:** selección sobre el libro consultado, confirmación de su vigencia y fuente inequívoca para identificadores o condiciones que las ligaduras y saltos de línea impidan leer con seguridad.
- **Correspondencias clínicas:** relación entre variables y campos, contextos y ámbitos admitidos, transformaciones y responsables de validar estas reglas.
- **Estados sin valor y selección múltiple:** códigos permitidos para cada estado, tratamiento de opciones no determinadas y condiciones para incorporar resultados parciales sin modificar información ajena.
- **Dependencias y campos especiales:** reglas de incorporación adicionales a la visibilidad y tratamiento acordado de campos calculados o descriptivos.
- **Anotaciones y datos operativos:** tratamiento de `@CALCTEXT`, `@SETVALUE`, `@DEFAULT`, obligatoriedad y estados de formulario; confirmar dependencias llamativas como la de `resultado_exoma`, sin corregir el diccionario por intuición.
- **Revisión humana:** obligatoriedad, responsables, información que deberán comprobar y condiciones para dar por resuelta una incidencia.
- **Incorporación posterior:** formato preferido, identificación de registros, eventos o repeticiones aplicables y mecanismo de transferencia; no se presupone API ni escritura automática.
- **Privacidad y validación:** entorno autorizado, acceso y conservación de evidencias, ejemplos de referencia y comprobaciones con el diccionario real antes de una integración.
