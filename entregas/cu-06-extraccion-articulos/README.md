# CU-06: extracción de información de artículos científicos mediante agentes

Entidad: iMATUS (Instituto de Materiais da USC)  
Tutores profesionales: Carmen Álvarez Lorenzo, Paola Carou Senra, María Viveiro López

## Qué es

Queremos desarrollar una aplicación en la que una investigadora suba un artículo sobre impresión de medicamentos por inyección de tinta (inkjet), marque qué datos necesita y reciba una tabla con ellos. Cada dato indica de qué parte del artículo sale, para que se pueda comprobar.

Por ejemplo, con un artículo que describe una tinta con cafeína impresa en una impresora Dimatix, el resultado sería algo así (el ejemplo es inventado):

| Dato | Valor | De dónde sale |
| --- | --- | --- |
| Fármaco | Cafeína | Sección 2.1 |
| Impresora | Dimatix DMP-2800 | Sección 2.2 |
| Viscosidad | 2,6 mPa·s | Tabla 1 |
| Número de Ohnesorge | 0,078 | Calculado con los datos anteriores |

En lugar de pedírselo todo a un LLM en un solo mensaje, repartimos el trabajo entre varios agentes, cada uno con sus propias instrucciones y encargado de un tipo de dato. El sistema se construye con CrewAI, una librería de Python para crear y coordinar agentes.

### El problema

Para entrenar modelos de IA en tecnología farmacéutica hacen falta tablas de datos, y esos datos están repartidos por los artículos: en el texto, en tablas, en gráficas o en el material suplementario. Extraerlos a mano es muy lento: a cuatro investigadoras les llevó cuatro meses hacerlo con 70 artículos.

### A quién va dirigido

Al grupo de investigación del iMATUS y a otros investigadores que necesiten recopilar datos de artículos sobre impresión inkjet de medicamentos.

## Motivación

Partimos de un estudio del propio iMATUS que hizo esta extracción con ChatGPT (GPT-4). Con 70 artículos y 23 datos por artículo acertó el 94 %, pero el proceso tenía dos problemas:

- Era manual: una persona tenía que pegar 8 prompts en ChatGPT, uno detrás de otro, para cada artículo.
- Los fallos se concentraban en puntos concretos, sobre todo al buscar en internet datos que el artículo no daba y al leer valores de gráficas.

Elegimos este proyecto porque responde a una necesidad real de un grupo de investigación y porque tenemos un resultado claro con el que compararnos. Nuestros objetivos son:

- Igualar o superar el 94 % en artículos que el sistema no haya visto durante el desarrollo.
- Procesar un artículo de principio a fin sin intervención humana.
- Mejorar lo que peor hizo ChatGPT: cálculos en Python, búsquedas que citan la fuente y un lector de gráficas.
- Aprender a construir y evaluar un sistema de agentes con datos reales.

## Alcance

### Qué entra

- Los 23 datos del estudio, en tres bloques:
  - Impresión (11): fármaco, impresora, boquilla, sustrato...
  - Propiedades de la tinta (9): viscosidad, tensión superficial, densidad y los números Oh y Z.
  - Dosis (3): cantidad de fármaco impresa, número de capas y superficie impresa.
- Los 70 artículos del estudio y su material suplementario. Usamos 20 para desarrollar y probar, y reservamos los otros 50 para la prueba final, para que el resultado no salga inflado.
- La conversión de los PDF a texto con Docling, para que los agentes trabajen con el texto y las tablas de cada artículo.
- Un corrector automático que compara las respuestas con las de las expertas (el Excel del estudio) y calcula el porcentaje de aciertos igual que el estudio.
- Un análisis de los errores de ChatGPT, para diseñar los agentes a partir de esos fallos.
- El sistema de agentes: un orquestador, un agente por bloque, tres ayudantes (calculadora de Oh y Z, buscador en internet y lector de gráficas) y un revisor final.
- Una comparación de 2 o 3 LLM disponibles en Databricks con los artículos de desarrollo, midiendo aciertos, tokens y tiempo, para elegir uno.
- Una interfaz sencilla para subir el artículo, elegir los datos y ver la tabla.

### Qué queda fuera

- Datos distintos de esos 23.
- Otras tecnologías de fabricación (impresión 3D por extrusión, estereolitografía...) u otros ámbitos.
- Ampliar la colección de 70 artículos o buscar artículos automáticamente.
- Entrenar modelos propios: usamos LLM existentes a través de su API.
- Interpretar los resultados: el sistema extrae y calcula datos, pero no valora si una formulación es buena.
- Desplegar la aplicación en producción, gestionar usuarios o guardar un histórico de artículos.
- Rehacer la anotación de las expertas: sus respuestas son nuestra referencia, salvo errores evidentes, que dejamos documentados.

## Equipo

| Nombre | Rol | Correo |
| --- | --- | --- |
| Noa Diz Fernández | Organización de los artículos y conversión de PDF a texto | noa.diz@rai.usc.es |
| Pablo Rigueiro Vázquez | Corrector automático y repositorio | pablo.rigueiro@rai.usc.es |
| Xiana Oliveira Allo | Repetición del estudio por código y elección del LLM | xiana.oliveira@rai.usc.es |
| Eva Graña Cordeiro | Análisis de errores de ChatGPT | eva.grana.cordeiro@rai.usc.es |

## Estructura

Esta entrega está en el repositorio de la asignatura:

```
entregas/
  cu-06-extraccion-articulos/
    README.md                                  este documento
    specs/
      extraccion-por-agentes-especialistas.md  los agentes de impresión, tinta y dosis
      interfaz-subida-y-seleccion.md           subir el artículo, elegir los datos y ver la tabla
```

En `specs/` hay una especificación por funcionalidad: qué se construye, por qué, con qué restricciones y cómo se comprueba que funciona.

El código está aparte, en nuestro repositorio de trabajo, `piia2-extraccion`, que es privado porque usamos datos que no se pueden publicar:

```
piia2-extraccion/
  README.md                      cómo instalarlo y cómo trabajamos
  CLAUDE.md                      reglas del repositorio
  docs/
    decisiones.md                qué está decidido y qué falta por decidir
    variables.md                 las 23 variables, sus bloques y unidades
    formato_datos.md             formato común de los datos
    contexto/introduccion.md     fases y reparto
  src/piia/
    datos/                       formato común y conversión del Excel
    evaluacion/                  corrector automático y emparejamiento de casos
    lector_pdf/                  conversión de PDF a texto con Docling
    config_llm.py                configuración del LLM
  scripts/                       scripts numerados (01 a 05) para ejecutar cada paso
  tests/                         pruebas, solo con datos inventados
  data/                          datos locales: no se suben a GitHub, salvo desarrollo.txt y su README
```

### Cómo funcionará el sistema

```
Artículo (PDF) + suplementario + datos elegidos
                  |
     Docling (convierte el PDF a texto)
                  |
             Orquestador
   (decide qué agentes actúan y en qué orden)
                  |
   +--------------+--------------+
   |              |              |
Impresión       Tinta          Dosis
   |              |              |
   +--------------+--------------+
                  |
Ayudantes, solo si hacen falta:
calculadora, buscador, lector de gráficas
                  |
   Revisor (unidades, rangos y citas)
                  |
  Tabla con cada dato y de dónde sale
```

El corrector queda fuera de este flujo: es la herramienta con la que medimos los aciertos del sistema en cada fase.

### Fases

| Fase | Duración orientativa | Resultado |
| --- | --- | --- |
| 1. Entender dónde falla el LLM | 2 semanas | Análisis de errores de ChatGPT, corrector y estudio repetido por código |
| 2. Primeros agentes | 2-3 semanas | Un agente por bloque con CrewAI |
| 3. Sistema completo | 3 semanas | Orquestador y ayudantes, sin intervención humana |
| 4. Mejorar | 2-3 semanas | Corrección de fallos hasta igualar o superar el estudio |
| 5. Aplicación y entrega | 2 semanas | Interfaz, prueba final con los 50 artículos reservados y memoria |

### Estado actual

Estamos en la fase 1. Ya hemos seleccionado los 20 artículos de desarrollo, convertido el Excel del estudio a un formato de trabajo común y pasado esos 20 artículos a texto con Docling. El corrector también funciona: con las respuestas de GPT-4 da 0,9355 en los 70 artículos, a un dato de la cifra de referencia de 0,9357 (validado el 24/10/2026).

También hemos decidido cómo emparejar los casos de las expertas con los del sistema: por similitud, comparando los campos que identifican cada caso (por ejemplo, fármaco y sustrato), porque nuestro sistema no dará los casos en el orden del Excel. El código de este emparejamiento ya está escrito y lo estamos revisando.

Los siguientes pasos son repetir el estudio por código y empezar con los agentes.

## Glosario

| Término | Qué significa |
| --- | --- |
| Impresión inkjet | Imprimir medicamentos como en una impresora de papel, con una "tinta" que lleva el fármaco |
| Formulación (tinta) | La mezcla que se imprime: fármaco, disolventes y otros ingredientes. Un artículo puede probar varias |
| Cabezal / boquilla | La pieza por donde sale la tinta |
| Sustrato | El material sobre el que se imprime (papel comestible, plástico...) |
| Viscosidad | Lo espesa que es la tinta |
| Tensión superficial | Lo que le cuesta a la tinta formar gotas |
| Oh y Z | Números que indican si una tinta se imprimirá bien. Oh = η / √(ρ·σ·d) y Z = 1/Oh |
| Suplementario | Archivos extra que acompañan al artículo. A veces un dato solo aparece ahí |
| LLM | Modelo de lenguaje, como ChatGPT, Claude o Gemini |
| Agente | Un LLM con un papel, unas instrucciones y, si hace falta, herramientas |
| CrewAI | Librería de Python para crear y coordinar agentes |
| Orquestador | La parte que decide qué agente actúa y en qué orden |
