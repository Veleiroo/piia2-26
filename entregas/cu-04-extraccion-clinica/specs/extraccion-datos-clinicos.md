# CLI-001 — Extracción e interpretación de información clínica

## 1. Identificación y propósito

| Referencia | Descripción |
|---|---|
| Identificador | `CLI-001` |
| Proyecto | CU-04 — Extracción y estructuración de información clínica para REDCap |
| Propósito | Identificar información relevante para las variables solicitadas, interpretar su contexto y producir valores candidatos respaldados por evidencia documental. |
| Entrada documental | Representación intermedia de [DOC-001](ingesta-documentos.md), incluidas sus incidencias y limitaciones. |
| Destino funcional | Preparación posterior de resultados por RCP-001, sin anticipar su codificación en REDCap. |
| Marco de alcance | [README del proyecto](../README.md) |
| Referencia de evaluación | [Entrega 1](../../../evaluacion/entrega-1.md) |

Esta spec define la **propuesta funcional del equipo**. Las obligaciones descritas constituyen el contrato propuesto para su implementación, no decisiones clínicas ya validadas por Ceres Fernández Rozadilla. El subconjunto de variables, sus definiciones temporales y los protocolos de resolución de discrepancias siguen pendientes de confirmación.

## 2. Motivación y problema que resuelve

Una enfermedad puede aparecer en una historia clínica como diagnóstico, negación, sospecha, antecedente familiar u opción de un formulario. Detectar su nombre no basta para atribuírsela al paciente. Además, distintos informes pueden repetir un hecho o describir momentos diferentes de su evolución.

CLI-001 debe reducir la búsqueda e interpretación manual de la información solicitada, conservando las evidencias y los límites de cada extracción. Su resultado expresa lo que está documentado y con qué contexto; no establece por sí mismo la verdad clínica ni sustituye la revisión profesional.

## 3. Alcance funcional

**Incluido en la propuesta:**

- Localización de menciones y datos pertinentes para una selección explícita de variables de investigación.
- Interpretación de afirmaciones, negaciones, sospechas, antecedentes, sujeto de la información y contexto de formularios.
- Diferenciación de tratamientos prescritos, administrados y mencionados como antecedentes.
- Conservación de fechas, repeticiones, discrepancias y evidencias documentales.
- Generación de candidatos y estados de interpretación, con límites de cobertura y lectura heredados de DOC-001.

**Fuera del alcance:**

- Lectura de PDF, procesamiento documental y determinación visual del estado de casillas, responsabilidades de DOC-001. No se reconstruye contenido oculto o ilegible.
- Extracción indiscriminada de toda la historia clínica, identificación de pacientes o mezcla de entradas de personas distintas.
- Diagnóstico médico, recomendaciones terapéuticas o inferencias clínicas no justificadas por la documentación y la definición de la variable.
- Elección de una fuente por prestigio, fecha, frecuencia de repetición u otra prioridad no acordada.
- Asignación de nombres de campo, tipos, opciones o códigos del diccionario de REDCap, responsabilidad de RCP-001; acceso directo a IANUS o REDCap.

## 4. Entradas y resultados esperados

### Entradas

1. **Contenido preparado por DOC-001 para una entrada de un único paciente:** documentos, páginas, bloques textuales o elementos descritos, referencias de procedencia, estados e incidencias. Los estados «contenido disponible» o «procesado sin incidencias detectadas» no garantizan una lectura perfecta.
2. **Selección de variables de interés:** referencia y definición clínica suficiente para identificar qué dato se busca y a quién se refiere. Cuando exista, se aporta también el ámbito temporal, la información necesaria para reconocer el valor y cualquier regla de selección acordada para el estudio. Esta selección no exige que esté ya definido todo el libro de códigos ni convierte sus nombres en campos de salida de REDCap.

La configuración y el subconjunto definitivos están pendientes. Si la selección está vacía, se comunica que no hay variables sobre las que realizar extracción. Si una definición no permite saber qué dato se solicita, esa variable se devuelve como **no evaluable por definición insuficiente**, con el motivo; no se inventa su significado ni se impide analizar las demás variables definidas. Este resultado de validación se distingue de los estados clínicos descritos a continuación.

Si DOC-001 comunica **entrada no admitida**, CLI-001 conserva ese rechazo y su motivo, sin presentar la extracción como realizada. Si la entrada fue admitida pero quedó **sin contenido utilizable**, las variables definidas se devuelven con información insuficiente por falta de contenido evaluable. Ninguna de esas situaciones equivale a una búsqueda sin hallazgos ni a una negación clínica.

### Resultados

Cada variable solicitada debe tener un resultado, aunque no se obtenga un valor candidato. La representación funcional debe incluir:

| Información | Contenido exigido |
|---|---|
| Variable y ámbito | Referencia a la definición solicitada y al ámbito temporal aplicado, o indicación de que este no está definido. |
| Menciones y candidatos | Contenido extraído o valor candidato, distinguiendo menciones contextuales de afirmaciones aplicables a la variable. No se fuerza un único valor cuando faltan reglas para elegirlo. |
| Contexto | Afirmación, negación, sospecha o interpretación indeterminada; sujeto —paciente, familiar, otra persona o no determinado—; condición histórica o temporal cuando esté documentada. Para tratamientos, distinguir prescripción, administración y antecedente. |
| Fechas | Fecha documental y fecha o periodo del hecho, si constan, con su precisión original y sin confundirlas. Si no se conocen, indicarlo. |
| Evidencias | Referencias a documento, página y bloque o elemento de DOC-001; fragmento textual o descripción documental que sustenta la interpretación. Si intervienen varias evidencias, mantener las referencias relevantes a todas ellas. |
| Relaciones | Menciones repetidas del mismo hecho, hechos distintos y discrepancias detectadas, manteniendo sus respectivas procedencias. |
| Estado y limitaciones | Estado de interpretación, motivo, advertencias de lectura aplicables y cobertura documental disponible. |

La interpretación se expresa en dimensiones separadas: una mención puede ser a la vez **afirmada**, **histórica** y referida a un **familiar**. «Sospechada» no equivale a «afirmada» ni se convierte en diagnóstico confirmado.

Se proponen estos estados para el resultado en el ámbito evaluado:

| Estado | Significado |
|---|---|
| Respaldado por evidencia | Hay un valor o afirmación aplicable sustentado por documentación interpretable. Debe conservar si se trata de sospecha, antecedente o acción terapéutica; este estado no confirma un diagnóstico. |
| Negación explícita documentada | Existe una negación aplicable al dato y ámbito solicitados, con su evidencia. No se deduce de silencios ni de casillas vacías. |
| No encontrado en la documentación disponible | No se localiza un dato, afirmación, negación o sospecha aplicable en el contenido evaluable recibido. No demuestra ausencia clínica ni cobertura completa del original. |
| Información ambigua o insuficiente | Hay una mención relevante que no permite determinar el dato, o no existe contenido evaluable. Debe indicarse qué impide obtener el resultado. |
| Información contradictoria | Se conservan afirmaciones aparentemente incompatibles sobre el mismo dato y ámbito, sin una regla validada que permita resolverlas. Se muestran los candidatos y evidencias discrepantes. |

Cuando hay varios hechos o periodos diferenciados, se devuelven los candidatos con sus respectivos estados y contextos. Si falta una regla temporal, se indica **selección temporal pendiente** y no se fuerza un valor único. La falta de esa regla no obliga a descartar hechos que sí estén documentados.

## 5. Comportamiento funcional

### 5.1. Selección y evidencia

1. Validar la selección y buscar información únicamente para las variables definidas. El contexto necesario puede contener otros términos, pero no genera resultados adicionales de variables no solicitadas.
2. Obtener candidatos a partir de texto o elementos documentales aportados por DOC-001. Cada afirmación y cada transformación de una mención en candidato deben poder justificarse mediante evidencia identificable.
3. Conservar el texto de las abreviaturas. Si su significado está definido inequívocamente en el contexto documental, puede utilizarse esa equivalencia conservando ambas evidencias; si sigue siendo ambiguo, no elegir una expansión por suposición. Una abreviatura sin resolver no constituye por sí sola evidencia de ambigüedad sobre una variable: debe existir evidencia adicional que las relacione. Si no existe esa relación ni otras menciones aplicables, devolver **no encontrado en la documentación disponible** para la variable, conservando la abreviatura sin resolver en su contexto documental. La cobertura terminológica clínica deberá validarse.
4. No generar candidatos sin procedencia. Si falta una referencia necesaria, comunicar la limitación de trazabilidad; no inventar documento, página o fragmento.

### 5.2. Interpretación contextual

- Una afirmación explícita sobre el paciente produce una afirmación documentada, sin convertirla en un diagnóstico emitido por el sistema.
- Una negación conserva el concepto negado y su alcance. Por ejemplo, «no se descarta» expresa incertidumbre, no una negación de la enfermedad.
- Las sospechas e hipótesis se conservan como tales. La mera mención de una prueba solicitada no confirma el diagnóstico investigado.
- Los antecedentes históricos se distinguen de la situación actual; un hecho pasado no se presenta como vigente sin evidencia que lo sustente.
- Las menciones sobre familiares u otras personas no se atribuyen al paciente. Si el sujeto no puede determinarse, se indica la ambigüedad.
- Una opción de formulario sin marcar no se interpreta como enfermedad presente ni como negación. Un estado de casilla indeterminado o no soportado por DOC-001 no se resuelve mediante conjeturas. Una casilla marcada solo se relaciona con su etiqueta si DOC-001 conserva esa asociación y la definición permite interpretarla; no equivale por sí sola a diagnóstico confirmado.
- «Prescrito», «administrado» y «tratamiento previo» describen situaciones distintas. Una prescripción no demuestra administración ni cumplimiento del tratamiento.

### 5.3. Contexto temporal

- Conservar separadamente la fecha del informe y las fechas de los hechos. Una fecha documental no sustituye una fecha clínica ausente.
- Mantener la precisión disponible: un año no se transforma en día y mes concretos. Las expresiones relativas se conservan y solo se vinculan a una fecha si su referencia es inequívoca; cualquier resolución debe conservar la expresión y su justificación.
- Aplicar una selección temporal únicamente si está definida para la variable. No adoptar como regla general «el informe más reciente» ni «el valor más repetido».
- Dos valores de momentos diferentes pueden reflejar evolución; no se consideran contradictorios solo por diferir. Si faltan fechas o no puede compararse su ámbito, se conserva la discrepancia y se indica esa incertidumbre.

### 5.4. Repeticiones y discrepancias

- Agrupar como menciones del mismo hecho las referencias que lo identifiquen inequívocamente, conservando todas sus evidencias. No contar menciones como acontecimientos independientes ni equiparar repetición con corroboración independiente.
- Si no puede determinarse si dos menciones describen el mismo hecho, mantener la relación como incierta; no fusionarlas ni afirmar que hubo dos acontecimientos.
- Ante afirmaciones aparentemente incompatibles para el mismo sujeto, variable y ámbito temporal, mostrar ambas, señalar la discrepancia y no seleccionar arbitrariamente una. Si no hay evidencia suficiente para establecer que comparten ámbito, indicar **posible discrepancia con ámbito incierto**.
- La ausencia de un dato en un informe no contradice por sí sola una afirmación en otro. Resolver contradicciones exige el protocolo que se acuerde con la tutora.

### 5.5. Ausencia, lectura limitada y trazabilidad

- Sin una mención aplicable, usar **no encontrado en la documentación disponible**, indicando la cobertura recibida. Si todo el contenido está ausente o no es evaluable por errores de lectura, usar **información ambigua o insuficiente**, no un negativo clínico.
- Una región ilegible relevante para el dato impide completar ese dato por suposición. Una advertencia localizada no obliga a descartar otra evidencia legible e independiente; se conserva el candidato y se informa de la limitación de cobertura.
- Si solo hay menciones familiares u opciones sin seleccionar, conservar su contexto y señalar que no se ha encontrado una afirmación aplicable al paciente. Si la selección de una opción es indeterminada, comunicar información insuficiente para ese elemento.
- Cada candidato, negación o discrepancia debe remitir a sus evidencias y advertencias de DOC-001. Los estados sin candidato deben expresar el motivo y el conjunto de documentos evaluados, sin inventar un fragmento probatorio de la ausencia.
- Una conclusión que combine un valor, una fecha o una explicación de bloques distintos debe conservar las referencias que justifican cada parte. El formato técnico se acordará posteriormente; no se exige un esquema JSON ni una estructura de clases.

## 6. Restricciones y supuestos

### Requisitos y contexto conocidos

- La entrada corresponde a un único paciente y el contenido documental procede de DOC-001, con sus límites de recuperación.
- Existen repeticiones, fechas distintas, negaciones, sospechas, antecedentes, tratamientos, resultados de pruebas, abreviaturas y formularios con opciones que pueden no corresponder al paciente.
- Hay información contradictoria o insuficiente. No se dispone de un protocolo validado por Ceres para resolver contradicciones o elegir el momento temporal de cada variable.
- El subconjunto de variables prioritarias sigue pendiente de confirmación.

En la consulta local se ha verificado texto extraíble idéntico en `data/M3.pdf`, pp. 45 y 47, y presencia de varias expresiones de fecha en ambas páginas, sin deducir de ello episodios independientes ni resolver su relación temporal. `data/M1.pdf`, p. 14, confirma contenido en francés. La clasificación estructural y sus límites están en la sección 6 de DOC-001. Los demás fenómenos contextuales comunicados por el equipo no se consideran comprobados exhaustivamente por esta inspección ni constituyen compromisos de interpretación perfecta.

### Propuestas del equipo

- Selección explícita de variables, candidatos con dimensiones contextuales separadas y los estados de interpretación definidos en esta spec.
- Conservación de alternativas y selección temporal pendiente cuando no hay criterios acordados para obtener un único valor.
- Agrupación de repeticiones inequívocas sin perder evidencias ni convertirlas en una regla de prioridad.
- Los criterios de aceptación siguientes verifican este contrato propuesto; no constituyen un protocolo clínico aprobado ni umbrales de calidad para historias reales.

### Supuestos de funcionamiento

- La selección aportada permite identificar al menos las variables que sí estén suficientemente definidas. Su configuración concreta no está decidida.
- DOC-001 entrega conjuntamente contenido, referencias y limitaciones, sin que se presuponga que su lectura o detección de incidencias sea perfecta.
- No se presupone un conjunto clínico etiquetado ni una capacidad universal para interpretar menciones. Las referencias de los escenarios sintéticos se definen expresamente para su futura verificación.

### Restricciones de tratamiento y tecnología

No se utilizarán historias clínicas reales ni fragmentos de pacientes en esta documentación o sus ejemplos de aceptación. Las evidencias descritas para el funcionamiento real son información sanitaria y su acceso, conservación, revisión y tratamiento deben acordarse con la entidad; esta spec no autoriza su publicación en el repositorio ni el envío a servicios externos.

No se fijan modelos, frameworks, herramientas, arquitectura, acceso a plataformas externas ni métricas o umbrales de rendimiento. La validación clínica y la definición de un conjunto de referencia quedan pendientes.

## 7. Criterios de aceptación

Los escenarios usan contenido **completamente sintético**, ya preparado como salida de DOC-001; no dependen de ejecutar la lectura de PDF para comprobar CLI-001. «Afección Alfa», «afección Delta», «fármaco Beta» y «marcador Gamma» son denominaciones ficticias sin reglas médicas implícitas. No representan variables aprobadas para el estudio ni campos de REDCap.

Cada bloque cuenta con referencia de documento, página y fragmento o elemento. Salvo indicación contraria, está legible, no tiene advertencias y se refiere al paciente. Cada escenario solicita solo las variables indicadas, cuya definición se limita a la afirmación documental expresada y a su contexto. Las fechas de los ejemplos son sintéticas. Los resultados se comprueban por su contenido y referencias, sin imponer un formato de serialización.

En escenarios inequívocos se exigen los valores, estados y contextos indicados: devolver siempre «desconocido» o «información insuficiente» no permite superar estos criterios. Los estados mencionados son los definidos en la sección 4.

| Identificador | Entrada y selección sintéticas | Resultado observable exigido |
|---|---|---|
| `CLI-001-CA01` | D1, página 1: «Diagnóstico confirmado de afección Alfa en el paciente». Se solicita la afirmación diagnóstica documentada de Alfa. | Candidato «afección Alfa», afirmado y referido al paciente, respaldado por evidencia en D1/página 1. No se devuelve solo desconocido ni se presenta como diagnóstico emitido por el sistema. |
| `CLI-001-CA02` | D1, página 1: «El paciente no presenta afección Alfa». Se solicita la presencia documentada de Alfa en ese contexto. | Negación explícita documentada de Alfa, con la frase como evidencia; no se produce un candidato afirmativo. |
| `CLI-001-CA03` | Dos entradas independientes: «Sospecha de afección Alfa; pendiente de estudio» y «No se descarta afección Alfa». Se solicita la afirmación diagnóstica documentada de Alfa. | En ambas se conserva Alfa como sospecha o hipótesis respaldada por la mención, sin diagnóstico confirmado ni negación explícita. |
| `CLI-001-CA04` | D1: «Antecedente de afección Alfa en 2019. En la valoración de 2026 no presenta afección Alfa». Se solicita Alfa con sus contextos temporales. | Se conserva una afirmación histórica en 2019 y una negación explícita en la valoración de 2026, con sus evidencias. No se fusionan en un único valor ni se declaran contradictorias solo por corresponder a estados distintos en el tiempo. |
| `CLI-001-CA05` | D1: «Antecedentes familiares: la madre presenta afección Alfa». Se solicita la presencia documentada de Alfa en el paciente. | La mención se atribuye a un familiar, no al paciente. Para el paciente se indica no encontrado en la documentación disponible; no se informa una negación documentada. Se conserva la referencia que explica la exclusión. |
| `CLI-001-CA06` | DOC-001 aporta la etiqueta «afección Alfa» asociada inequívocamente a una casilla sin marcar, sin otras menciones. Se solicita Alfa en el paciente. | La opción queda identificada como no seleccionada; no se genera presencia ni negación clínica. El resultado para Alfa es no encontrado en la documentación disponible, con el contexto de formulario. |
| `CLI-001-CA07` | La etiqueta «afección Alfa» tiene una casilla de estado indeterminado y advertencia de DOC-001 de lectura no soportada. Se solicita Alfa. | Información ambigua o insuficiente para esa opción, conservando la advertencia y la referencia. No se deduce marcada, sin marcar, presencia o ausencia clínica. |
| `CLI-001-CA08` | D1, página 1, y D2, página 3, contienen «El 12 de febrero de 2025 se administró una dosis de fármaco Beta»; D2 añade «Se reproduce el mismo episodio descrito en D1». Se solicitan las administraciones documentadas de Beta. | Se representa un único hecho con dos menciones y ambas referencias, conservando su fecha. No se informa que hubo dos administraciones ni que la repetición demuestra una corroboración independiente. |
| `CLI-001-CA09` | D1: «En la valoración del 3 de marzo de 2026 se confirma afección Alfa». D2: «En la valoración del 3 de marzo de 2026 se descarta afección Alfa». Se solicita Alfa en esa misma valoración, sin regla de prioridad. | Información contradictoria, con la afirmación, la negación, la fecha común y ambas evidencias. No se elige una fuente ni se convierte la discrepancia en un simple no encontrado. |
| `CLI-001-CA10` | Informe fechado el 10 de junio de 2026: «Diagnóstico de afección Alfa realizado el 4 de abril de 2021». Se solicita el diagnóstico documentado y su fecha. | Se recupera Alfa y se distingue fecha del documento —10 de junio de 2026— de fecha del hecho —4 de abril de 2021—. No se infiere que el diagnóstico ocurrió en 2026 ni que su estado siga vigente. |
| `CLI-001-CA11` | D1: «El 1 de mayo de 2024, marcador Gamma: 5 unidades». D2: «El 1 de mayo de 2025, marcador Gamma: 8 unidades». Se solicita Gamma sin regla temporal. | Se conservan los valores 5 y 8, sus unidades, fechas y referencias, con selección temporal pendiente. No se elige automáticamente 8 ni se considera contradicción la diferencia entre fechas. |
| `CLI-001-CA12` | Mismo contenido que CA11; la definición solicitada exige el valor de Gamma documentado el 1 de mayo de 2024. | Candidato 5 unidades, asociado a esa fecha y a D1, por aplicación explícita del ámbito solicitado. No se sustituye por el valor del informe posterior. |
| `CLI-001-CA13` | Dos entradas: una contiene solo «Marcador Gamma: 5 unidades» y otra «Se descarta afección Alfa». En ambas se solicita Alfa. | En la primera: no encontrado en la documentación disponible y ningún negativo clínico. En la segunda: negación explícita documentada con su evidencia. Los resultados no se equiparan. |
| `CLI-001-CA14` | D1, página 1, legible: «Diagnóstico confirmado de afección Alfa». Página 2 sin texto recuperado por un error de DOC-001. Se solicita Alfa. | Se conserva el candidato afirmado de la página 1 y su evidencia, junto con la limitación de cobertura de la página 2. No se descarta el dato legible ni se declara revisado el contenido de la página fallida. |
| `CLI-001-CA15` | Dos entradas: una solo contiene páginas sin texto recuperado por errores de DOC-001; otra contiene «Marcador Gamma: [región ilegible] unidades», con advertencia localizada. Se solicita Gamma. | En ambas, información ambigua o insuficiente con el motivo y las referencias disponibles. En la segunda no se inventa un valor numérico; en ninguna se devuelve una negación clínica ni un resultado de búsqueda sin advertencias. |
| `CLI-001-CA16` | D1, página 2, bloque B1: «Diagnóstico confirmado de afección Alfa. Fecha del diagnóstico indicada en D2». D2, página 4, bloque B2: «Fecha del diagnóstico de afección Alfa: 6 de julio de 2020». Se solicita diagnóstico y fecha. | Candidato Alfa con fecha 6 de julio de 2020. La afirmación remite a D1/página 2/B1 y la fecha a D2/página 4/B2; la conclusión conserva ambas evidencias y no atribuye la fecha a un fragmento que no la contiene. |
| `CLI-001-CA17` | D1: «Diagnóstico confirmado de afección Alfa y afección Delta. Marcador Gamma: 5 unidades». Se solicita exclusivamente Alfa. | Hay resultado para Alfa con su evidencia y no se crean resultados de variables Delta o Gamma. El fragmento de evidencia puede conservar el contexto original sin convertirlo en extracciones adicionales. |
| `CLI-001-CA18` | D1 contiene tres bloques: «Se prescribe fármaco Beta el 1 de enero de 2025»; «Se administra fármaco Beta el 2 de enero de 2025»; «Antecedente de tratamiento con fármaco Beta en 2020». Se solicitan las menciones de tratamiento con Beta y sus contextos. | Se distinguen prescripción, administración y antecedente, con sus fechas y evidencias. No se informa que la prescripción demuestra administración ni que el antecedente implica tratamiento actual. |
| `CLI-001-CA19` | Dos entradas: una contiene únicamente «AX consta en antecedentes», sin definir AX ni relacionarla con Alfa; otra contiene «En este informe, AX significa afección Alfa» y «Diagnóstico confirmado de AX». Se solicita Alfa. | En la primera se conserva AX como abreviatura sin resolver, con su contexto y procedencia, y se devuelve no encontrado en la documentación disponible para Alfa, sin atribuirle presencia, negación ni ambigüedad por esa sola mención. En la segunda se recupera Alfa como afirmación, conservando tanto la definición de AX como la mención diagnóstica. |
| `CLI-001-CA20` | D1: «En 2025 se registró afección Alfa». D2: «En 2026 se registró afección Alfa». No se indica si describen un hecho persistente o episodios distintos. Se solicitan hechos documentados de Alfa. | Se conservan ambas menciones y fechas con relación incierta. No se afirma que hubo dos episodios ni se fusionan como un único acontecimiento demostrado. |
| `CLI-001-CA21` | Tres solicitudes: selección vacía; variable con solo una referencia sin definición interpretable; selección de esa variable junto con Alfa bien definida y el texto de CA01. | La primera informa que no hay variables para extraer; la segunda identifica la definición insuficiente sin inventarla; la tercera conserva ese aviso y devuelve además el candidato afirmado de Alfa. |
| `CLI-001-CA22` | Se solicita Alfa bien definida. En una entrada DOC-001 comunica entrada no admitida; en otra comunica entrada admitida sin contenido utilizable. | En la primera se conserva el rechazo y su motivo sin generar resultado de búsqueda clínica. En la segunda se informa de insuficiencia por falta de contenido evaluable. Ninguna produce un candidato, una negación o «no encontrado» como si se hubiese inspeccionado contenido legible. |

Estos criterios verifican resultados concretos en escenarios controlados. No acreditan por sí solos cobertura clínica, interpretación completa de formularios ni calidad suficiente sobre documentación real. En particular, CA06 y CA07 comprueban el uso del estado de casilla que entrega DOC-001, no su reconocimiento visual.

La evaluación posterior requiere un conjunto de referencia autorizado, definiciones clínicas y temporales validadas y criterios de anotación. Las métricas y los umbrales de precisión, exhaustividad u otras medidas se acordarán con la tutora; no se establecen valores arbitrarios en esta spec.

## 8. Cuestiones abiertas

La lista distingue decisiones pendientes, sin afirmar que todas hayan sido consultadas ni atribuir a Ceres respuestas todavía no recibidas.

- **Variables prioritarias:** subconjunto, definiciones clínicas, sujeto de interés y forma de facilitar la selección al sistema.
- **Ámbito temporal:** momento o periodo que corresponde a cada variable y reglas para distinguir antecedentes, persistencia y episodios independientes.
- **Discrepancias:** protocolo para comparar fuentes, resolver contradicciones y expresar resultados pendientes de revisión.
- **Cobertura contextual y terminológica:** idiomas, abreviaturas, tratamientos y capacidad imprescindible de interpretación de formularios, condicionada por la salida de DOC-001.
- **Evaluación:** disponibilidad de ejemplos de referencia, construcción de un conjunto etiquetado autorizado, criterios de anotación, métricas y umbrales de aceptación.
- **Revisión y tratamiento de resultados:** intervención humana, responsables de validar candidatos, acceso a evidencias y condiciones de almacenamiento y procesamiento de información sanitaria.
- **Relación con RCP-001:** información clínica y estados que deberá conservar la preparación para REDCap, sin fijar aquí nombres de campos, códigos ni mecanismos de incorporación.
