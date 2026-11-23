# DOC-001 — Ingesta y procesamiento de documentación clínica

## 1. Identificación y propósito

| Referencia | Descripción |
|---|---|
| Identificador | `DOC-001` |
| Proyecto | CU-04 — Extracción y estructuración de información clínica para REDCap |
| Propósito | Recibir documentación de un único paciente y producir contenido procesable con referencias de procedencia y limitaciones de lectura. |
| Consumidor del resultado | `CLI-001`, extracción e interpretación de información clínica. |
| Marco de alcance | [README del proyecto](../README.md) |
| Referencia de evaluación | [Entrega 1](../../../evaluacion/entrega-1.md) |

Esta spec desarrolla la **propuesta funcional del equipo**, pendiente de validación con la entidad. Las obligaciones expresadas como «debe» definen el comportamiento propuesto para su implementación y aceptación; no representan decisiones ya confirmadas por Ceres Fernández Rozadilla. La sección 6 distingue los hechos confirmados de las propuestas y los supuestos.

## 2. Motivación y problema que resuelve

La documentación clínica disponible combina texto digital, páginas escaneadas y elementos cuya lectura puede ser incompleta. Entregar esos archivos sin preparación obligaría al componente de extracción clínica a resolver también la lectura documental y dificultaría localizar el origen de los resultados.

DOC-001 concentra esa preparación: recupera contenido, conserva sus límites documentales y comunica qué partes presentan dificultades. Así, CLI-001 puede analizar la información disponible sin confundir la ausencia de texto recuperado con la ausencia de información clínica en el original. La recuperación documental no determina la validez clínica del contenido.

## 3. Alcance funcional

**Incluido en la propuesta:**

- Recepción de uno o varios PDF asociados a una entrada de un único paciente.
- Validación de las condiciones de admisión y de la posibilidad de abrir cada archivo.
- Recuperación de texto digital y tratamiento de contenido escaneado o mixto, incluso dentro de una misma página.
- Conservación de la separación, orden y procedencia de documentos, páginas y bloques recuperados.
- Señalización de contenido no recuperado, limitaciones y errores, manteniendo el contenido utilizable cuando el fallo sea parcial.
- Preparación de una representación intermedia para CLI-001, sin fijar su formato técnico.

**Fuera del alcance:**

- Identificación automática del paciente y comprobación clínica de que los documentos pertenecen a la misma persona.
- Admisión inicial de DOCX, portapapeles o carpetas como modalidad de entrada. Esto no impide recibir varios PDF mediante el mecanismo que se acuerde.
- Interpretación de diagnósticos, negaciones clínicas, vigencia temporal o contradicciones entre hechos, responsabilidad de CLI-001.
- Traducción, reconstrucción de texto ilegible o deducción de valores a partir de casillas o campos vacíos.
- Generación de variables, códigos o campos de REDCap, responsabilidad de RCP-001; acceso directo a IANUS o escritura en REDCap.

## 4. Entradas y resultados esperados

### Entrada

Una entrada comprende un conjunto no vacío de archivos PDF y una declaración de quien los aporta de que corresponden a un único paciente. **Exigir esa declaración es una propuesta del equipo**, no un procedimiento confirmado por la tutora. Puede transmitirse por el mecanismo de entrada que se acuerde y no requiere imponer una interfaz concreta ni aportar identificadores personales adicionales.

La extensión del archivo no basta para admitirlo: debe poder reconocerse y abrirse como PDF, con al menos una página. Los archivos de cero bytes, los PDF dañados, los formatos incompatibles y los PDF cuyo contenido no pueda abrirse por protección deben producir un resultado de validación explícito. No se propone gestionar contraseñas en este alcance.

### Representación intermedia

El resultado debe ofrecer funcionalmente, sin imponer un esquema de datos:

| Nivel | Información necesaria |
|---|---|
| Entrada | Referencia de la entrada, relación de documentos recibidos y resultado global del procesamiento. |
| Documento | Referencia inequívoca dentro de la entrada, correspondencia con el archivo recibido, posición en el conjunto, estado de validación y número de páginas si puede determinarse. |
| Página | Número de página física del PDF, comenzando por 1; naturaleza del contenido detectado —digital, escaneado, mixto o no determinada—; contenido recuperado y estado de recuperación. |
| Bloque recuperado | Texto o descripción documental del elemento, orden de lectura cuando pueda establecerse y referencias a documento y página. Para regiones diferenciadas, un localizador dentro de la página que permita distinguirlas, sin exigir coordenadas concretas. |
| Incidencia | Motivo de rechazo, error o limitación; documento, página y región afectados cuando puedan localizarse; efecto sobre la disponibilidad del contenido. |

Los textos y las descripciones de elementos deben distinguirse. Una descripción como «casilla de estado indeterminado» no puede presentarse como transcripción del original. No se exige conservar los archivos originales, imágenes o recortes en esta representación; su almacenamiento y acceso están pendientes de acuerdo.

Se proponen los siguientes estados de página:

- **Contenido disponible:** se ha recuperado contenido sin limitaciones detectadas; no certifica exactitud ni exhaustividad.
- **Recuperación limitada:** existe contenido recuperado y alguna limitación detectada o algún elemento que no se ha podido interpretar documentalmente.
- **Sin texto recuperado:** no se ha obtenido texto; debe acompañarse del motivo conocido o de la indicación de que no se ha podido determinar. No equivale a ausencia de datos clínicos.
- **Error de procesamiento:** un fallo impide procesar la página.

Los estados se asignan por este orden: error que impide procesar; sin texto recuperado si no hay transcripción, aunque existan descripciones de elementos; recuperación limitada si hay texto e incidencias de lectura; contenido disponible en los demás casos. Las descripciones y advertencias se conservan junto al estado, sin convertirlas en texto transcrito. Una página no procesada por un fallo del documento conserva su referencia y ese motivo como error de procesamiento.

El resultado global distingue **procesado sin incidencias detectadas**, **procesado con incidencias**, **sin contenido utilizable** y **entrada no admitida**, conforme a las reglas de la sección 5. Estos estados describen el procesamiento, no la fiabilidad clínica.

A efectos de estos estados, existe contenido utilizable si hay al menos un bloque con texto recuperado no vacío o un elemento documental descrito y localizado, como una casilla cuyo estado se ha distinguido. Las referencias, los estados y los mensajes de incidencia por sí solos no cuentan como contenido utilizable. Esta definición no prejuzga su relevancia para una variable clínica.

## 5. Comportamiento funcional

### 5.1. Recepción y validación

1. Comprobar que se han aportado archivos y la declaración de un único paciente. Una entrada vacía, sin esa declaración o declarada como correspondiente a varios pacientes no se admite ni se procesa; se comunica la condición incumplida.
2. Asignar referencias que distingan los documentos, incluso cuando tengan el mismo nombre, y conservar su orden de recepción.
3. Validar cada archivo por separado. Un archivo rechazado debe figurar en el resultado con su motivo, sin texto atribuido a él. Su rechazo no impide procesar otros PDF admitidos de la misma entrada.
4. No deducir la identidad del paciente ni dar por comprobada su pertenencia documental a partir de la declaración. Esta responsabilidad corresponde a quien prepara la entrada.

### 5.2. Recuperación y organización del contenido

1. Examinar las páginas para recuperar texto digital y tratar el contenido que requiera lectura de imágenes. La existencia de texto digital no permite omitir automáticamente las imágenes de la misma página.
2. Mantener el idioma y los caracteres recuperados, incluidos los acentos del francés, sin traducir ni normalizar terminología clínica.
3. Conservar los límites y el orden de documentos y páginas. Dentro de la página, preservar la separación de bloques, etiquetas y campos cuando pueda determinarse su relación; si el orden o la asociación son inciertos, comunicar esa limitación.
4. Evitar presentar dos veces el mismo contenido por haberlo obtenido de una imagen y de su capa textual superpuesta. Las repeticiones existentes en el original, incluidas las de páginas diferentes, deben conservarse; decidir su relevancia clínica corresponde a CLI-001.
5. Vincular cada bloque a su procedencia. No fusionar contenido de distintos documentos o páginas sin mantener las referencias de cada parte.

### 5.3. Elementos complejos y dificultades de lectura

| Elemento | Comportamiento propuesto |
|---|---|
| Formularios y tablas | Conservar etiquetas, contenido y relaciones reconocibles. Si no puede determinarse qué contenido corresponde a cada campo o celda, señalarlo y no inventar la asociación. |
| Casillas | Distinguir, cuando pueda determinarse visualmente, marcada, sin marcar y estado indeterminado. Si esta capacidad no está soportada, indicar la limitación. Una casilla sin marcar no se convierte en un valor clínico negativo. |
| Manuscritos | Recuperar el texto que sea posible y señalar las regiones detectadas no recuperadas o no soportadas. No completar palabras por plausibilidad clínica. |
| Tachaduras y zonas ocultas | Conservar el texto tachado que siga siendo visualmente legible, con advertencia, sin decidir su vigencia clínica. En una zona tapada por una ocultación opaca, no propagar texto de capas subyacentes aunque sea extraíble: señalar la región y su limitación, sin reconstruir su contenido. Esta distinción es una propuesta de tratamiento, no una garantía de detectar todas las ocultaciones. |
| Contenido ilegible o estructura incierta | Localizar la dificultad a nivel de página o región, conservar las partes recuperadas y comunicar la limitación sin generar texto sustitutivo. |

Estas obligaciones no presuponen detección infalible de todas las dificultades. La cobertura sobre manuscritos, idiomas, casillas y alteraciones requiere evaluación específica; cuando una capacidad no esté soportada debe constar en el resultado de los documentos a los que pueda afectar, sin presentarlos como completamente interpretados.

### 5.4. Resultado y fallos parciales

- Cada documento admitido conserva una referencia a todas sus páginas, incluidas las vacías y las que fallen. Una página sin texto no debe desaparecer ni alterar la numeración de las restantes.
- Un error localizado no debe eliminar el contenido recuperado de otras páginas o documentos. Si un fallo impide continuar con un documento, se indica qué páginas han quedado sin procesar; se continúa con los demás documentos admitidos.
- Una página legítimamente vacía no constituye por sí sola una incidencia, pero debe aparecer como **sin texto recuperado**.

El estado global se asigna aplicando estas reglas en orden:

1. Si se incumplen las condiciones generales de 5.1, el resultado es **entrada no admitida**.
2. Si se cumplen, pero ningún archivo o página aporta contenido utilizable, el resultado es **sin contenido utilizable**, con los motivos correspondientes. Esto incluye el caso en que todos los archivos sean rechazados o todas las páginas estén vacías.
3. Si existe contenido utilizable y hay algún rechazo, error, limitación o página pendiente de procesamiento, el resultado es **procesado con incidencias**.
4. En los demás casos, todas las páginas se han procesado, existe contenido utilizable y el resultado es **procesado sin incidencias detectadas**.

## 6. Restricciones y supuestos

### Requisitos y contexto confirmados

- La unidad de entrada corresponde a un único paciente.
- Se dispone de PDF heterogéneos con texto digital, escaneos, formularios, casillas, manuscritos, tachaduras y texto parcialmente oculto; hay documentos en distintos idiomas, incluido el francés.
- La lectura completa no está garantizada y no se ha seleccionado una tecnología de procesamiento documental.

### Características verificadas en los materiales locales

Referencias a páginas físicas de los PDF de `data/`, sin reproducir su contenido clínico:

| Observación | Referencia local | Límite de la comprobación |
|---|---|---|
| Páginas con imagen y sin texto extraíble; otras con texto extraíble y sin imágenes. | `M1.pdf`, p. 1; `M2.pdf`, p. 1, respectivamente. | La falta de texto extraíble no demuestra que la imagen sea ilegible. |
| Coexistencia de objetos de texto e imagen en una página. | `M3.pdf`, p. 1. | Una imagen puede ser un logotipo; esta estructura no prueba por sí sola que haya texto clínico escaneado junto al digital. |
| Contenido textual en francés. | `M1.pdf`, p. 14. | No acredita cobertura de lectura de todas las páginas o idiomas. |
| Páginas con el mismo texto extraíble. | `M3.pdf`, pp. 45 y 47. | No demuestra que sean dos acontecimientos ni permite decidir su relevancia clínica. |
| Página sin objetos de texto, imagen ni dibujo. | `M4.pdf`, p. 99. | Es un caso de vacío documental, distinto de una página de imagen sin transcripción. |

La inspección se ha limitado a la estructura y al texto extraíble; no se han verificado visualmente formularios, estados de casillas, manuscritos, tachaduras ni legibilidad de imágenes. Esas dificultades se mantienen como contexto comunicado por el equipo y capacidades pendientes de evaluación. Tampoco se equipara un rectángulo oscuro que se solape geométricamente con texto a una ocultación: puede ser un fondo y requiere comprobar su presentación visual.

### Decisiones de alcance propuestas por el equipo

- Admisión inicial de PDF, declaración de un único paciente y validación por archivo.
- Representación intermedia con trazabilidad, estados e incidencias, y conservación de los resultados ante fallos parciales.
- Separación entre recuperación documental, interpretación clínica y estructuración para REDCap.
- Los criterios de la sección 7 verifican este contrato propuesto; no equivalen a umbrales de calidad aprobados por la tutora.

### Supuestos de funcionamiento

- Quien aporta la documentación conoce su procedencia y prepara el conjunto de un único paciente. La declaración no permite detectar automáticamente una mezcla accidental.
- CLI-001 tendrá acceso al contenido y a sus limitaciones de forma conjunta. Una página sin texto recuperado no podrá tratarse como prueba de ausencia de una variable clínica.
- Los documentos sintéticos de aceptación podrán contar con un resultado de referencia explícito, independiente de la salida del sistema.

### Privacidad y decisiones técnicas pendientes

No se incorporarán historias clínicas ni fragmentos reales a esta spec, al repositorio o a las pruebas de aceptación descritas. Los ejemplos serán sintéticos y no derivados de pacientes identificables. Los mensajes de error deben permitir localizar la incidencia mediante referencias, sin reproducir contenido clínico como diagnóstico técnico.

El entorno autorizado, los accesos, la conservación o eliminación de originales y resultados, el tratamiento de archivos temporales y la posible utilización de servicios externos deben acordarse con la entidad. Esta spec no autoriza el envío de documentación sanitaria a proveedores ni fija políticas de almacenamiento. Tampoco fija modelos, herramientas, arquitectura, tamaños máximos, tiempos de respuesta o niveles de precisión no acordados.

## 7. Criterios de aceptación

Todos los escenarios utilizan archivos **sintéticos**, preparados para la verificación; esta spec describe sus características, sin crear los archivos ni implementar pruebas. Cada escenario registra la entrada y la salida de referencia antes de ejecutar el sistema. Salvo indicación contraria, se aporta la declaración de un único paciente y el resultado se comprueba en la representación intermedia, sin depender de una interfaz concreta.

En las comprobaciones textuales de CA01 a CA03 y CA05 solo se permite normalizar espacios y saltos de línea; deben conservarse palabras, acentos, números y orden. Son verificaciones de casos controlados, no porcentajes de precisión aplicables a documentación clínica real.

| Identificador | Escenario sintético | Resultado observable exigido |
|---|---|---|
| `DOC-001-CA01` | PDF digital de dos páginas, con una sola línea por página: «DOCUMENTO ALFA 001» y «DOCUMENTO ALFA 002». | Se recuperan ambas líneas, cada una en su página y en ese orden; hay dos páginas registradas y ningún texto adicional atribuido al original. |
| `DOC-001-CA02` | PDF de una página que contiene únicamente una imagen nítida de la línea impresa «DOCUMENTO BETA 003», horizontal sobre fondo blanco, sin capa textual. | La línea aparece en el contenido recuperado con referencia a la página 1. Devolver solo una advertencia o un resultado vacío no satisface este criterio. |
| `DOC-001-CA03` | PDF mixto: página 1 con texto digital «BLOQUE DIGITAL 004»; página 2 con imagen de «BLOQUE ESCANEADO 005»; página 3 con texto digital «CABECERA 006» y una imagen no superpuesta de «ANEXO 007». | Se recuperan las cuatro líneas en sus páginas y en el orden descrito. La página 3 conserva ambos bloques y se identifica como mixta. |
| `DOC-001-CA04` | Dos PDF llamados `informe.pdf`, cada uno con dos páginas y un marcador por página; uno de los marcadores se repite deliberadamente en ambos documentos. | Los documentos tienen referencias distintas; cada bloque remite al documento y página esperados. Se conserva el marcador repetido en ambos orígenes, sin fusionarlos. |
| `DOC-001-CA05` | PDF digital con la línea «Texte synthétique : été, garçon, cœur.» y otra con «SIN TRADUCCIÓN». | Ambas líneas se recuperan en el idioma original, conservando los caracteres indicados y sin traducción ni sustitución de términos. |
| `DOC-001-CA06` | PDF con una página legible, una página de imagen con los fragmentos legibles «INICIO» y «FIN» y una franja opaca que corta otros renglones dejando trazos interrumpidos visibles a ambos lados, y otra página legible. La parte tapada no tiene texto subyacente recuperable. | Se conserva el contenido de las páginas 1 y 3 con su numeración original. En la página 2 se recuperan «INICIO» y «FIN», se localiza la región con ocultación visible y se señala su limitación de lectura, sin reconstruir la parte tapada. Esa página figura con recuperación limitada y el resultado global es procesado con incidencias. |
| `DOC-001-CA07` | Archivo de cero bytes y, en una entrada independiente, un PDF truncado que no puede abrirse. | Cada archivo queda rechazado con motivo distinguible —vacío o no abrible/dañado—, sin texto recuperado. Ambas entradas terminan sin contenido utilizable y no provocan un fallo sin resultado comunicado. |
| `DOC-001-CA08` | Un archivo de texto renombrado con extensión `.pdf`, acompañado de un PDF digital legible. | El falso PDF se rechaza por incompatibilidad; el PDF admitido conserva su contenido y procedencia. El resultado global es procesado con incidencias. |
| `DOC-001-CA09` | Tres entradas independientes: sin archivos; con PDF pero sin declaración de un único paciente; con PDF y declaración de que contiene varios pacientes. | Cada entrada queda no admitida, indica la condición incumplida y no ofrece contenido procesado. No se solicita al sistema identificar a los pacientes para decidir. |
| `DOC-001-CA10` | PDF protegido que no permite abrir el contenido sin contraseña. | Se comunica la imposibilidad de apertura por protección, sin texto atribuido al documento ni intento de presentarlo como procesado. Si es el único archivo, el resultado es sin contenido utilizable. |
| `DOC-001-CA11` | PDF con una página legible y otra realmente vacía, sin texto ni imágenes; en una entrada independiente, PDF con una única página vacía. | En el primer caso hay dos páginas registradas: la segunda figura sin texto recuperado, sin valores clínicos deducidos y sin desplazar la numeración; su vacío, por sí solo, no origina un error. En el segundo, el resultado es sin contenido utilizable, con la página vacía registrada. |
| `DOC-001-CA12` | PDF con imagen de «MARCADOR SUPERPUESTO 008» y una capa textual que reproduce esa misma línea en la misma posición. | La representación ofrece una única transcripción de esa línea en la página; no la duplica por sus dos formas de recuperación. |
| `DOC-001-CA13` | Formulario sintético con etiquetas impresas legibles, una casilla marcada, otra sin marcar, un campo vacío, un trazo manuscrito sin significado textual y un bloque de texto parcialmente oculto con trazos interrumpidos visibles en los bordes de la ocultación. Las regiones están identificadas en la referencia del escenario. | Se conservan las etiquetas. Para cada región compleja se ofrece su estado documental o una limitación localizada; no se rellenan el campo vacío ni la parte oculta del texto. Si se distinguen las casillas, sus estados coinciden con la referencia; si no se soporta esa lectura, se indica como limitación provisional. No se generan valores clínicos afirmativos o negativos a partir de ellas. |
| `DOC-001-CA14` | PDF digital con «MARCADOR ANTIGUO» tachado, pero todavía recuperable como texto, seguido de «MARCADOR POSTERIOR». | Si se recupera el texto tachado, aparece asociado a la advertencia de alteración o a una limitación de esa lectura. Se conserva el texto posterior. DOC-001 no elige uno de los dos como hecho clínico vigente. |
| `DOC-001-CA15` | PDF de tres páginas y un fallo de procesamiento provocado de forma controlada solo en la página 2; páginas 1 y 3 recuperables. | Las páginas 1 y 3 conservan su contenido y referencias. La página 2 figura con error y motivo, sin contenido inventado; el resultado global es procesado con incidencias. |
| `DOC-001-CA16` | PDF sintético con «INICIO» y «FIN» visibles y otra línea parcialmente cubierta por una franja opaca, con trazos interrumpidos que hacen visible la ocultación. El texto tapado permanece extraíble en la capa textual del PDF. | Se recuperan los segmentos visibles y se localiza la limitación; la representación no expone el texto tapado ni lo envía como evidencia a CLI-001. La página figura con recuperación limitada. El caso exige respetar una ocultación observable, no adivinar contenido oculto sin indicios. |

Los casos de escaneo legible verifican que existe recuperación efectiva de imágenes; no basta con marcar todos los escaneos como no recuperables. CA06, CA13 y CA14 comprueban el tratamiento explícito de límites y alteraciones, sin acreditar una capacidad universal para detectarlos. CA15 requiere poder provocar un fallo localizado en el entorno de verificación, sin imponer cómo se implementa ese entorno.

CA13 admite provisionalmente declarar la lectura de casillas como no soportada. Su cumplimiento no demuestra capacidad de interpretación de formularios. Si esa capacidad resulta imprescindible para el proyecto, necesitará una evaluación específica con ejemplos de referencia y criterios de aceptación acordados que exijan reconocer los elementos y sus relaciones; declarar la limitación no bastará para superarla.

La aceptación de estos escenarios no demuestra calidad suficiente sobre manuscritos reales, documentos degradados, estructuras complejas o todos los idiomas. Esa evaluación requiere muestras autorizadas, referencias, métricas y umbrales acordados con la tutora. No se establecen aquí porcentajes arbitrarios de recuperación ni compromisos de rendimiento.

## 8. Cuestiones abiertas

La relación de consultas ya realizadas está recogida en el README; la lista siguiente no implica que todas estas cuestiones se hayan trasladado a Ceres o cuenten con su aprobación.

- **Entrada real desde IANUS:** formatos exportables, composición de cada conjunto documental y disponibilidad de ejemplos de referencia.
- **Declaración de un único paciente:** validación del mecanismo propuesto y procedimiento operativo para preparar los conjuntos y corregir mezclas detectadas por sus responsables.
- **Cobertura documental:** idiomas exigidos, incluido el francés, y nivel esperado de recuperación de manuscritos, casillas, tablas, tachaduras y texto oculto.
- **Calidad y aceptación:** referencias autorizadas, criterios para considerar recuperable un contenido, métricas y umbrales; los estados de procesamiento no sustituyen esta evaluación.
- **Uso de resultados limitados:** revisión humana y condiciones para trasladar a CLI-001 contenido incompleto o de lectura incierta.
- **Tratamiento de datos:** entorno, permisos de acceso, servicios permitidos, conservación, eliminación y acceso a originales para comprobar la procedencia.
- **Límites operativos:** volumen y tamaño de documentos, restricciones por protección, tiempos esperados y prioridad de otros formatos. No se consideran condiciones de admisión confirmadas mientras no se acuerden.
