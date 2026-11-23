# Sistema de clasificación basado en modelos fundacionales tabulares

## Qué es el proyecto

El objetivo es construir un prototipo interactivo con Streamlit para explorar y comparar modelos fundacionales tabulares en problemas industriales de clasificación binaria. La herramienta permitirá seleccionar un dataset de los facilitados para el proyecto, ejecutar los modelos disponibles y contrastar sus resultados con los baselines tradicionales proporcionados. Está dirigida a estudiantes y analistas que necesiten evaluar estos enfoques desde una interfaz común, sin reescribir el flujo de experimentación para cada caso.

Comenzamos usando distintos datasets para probar y comparar LightGBM, como baseline tradicional, y TabPFN, como modelo fundacional. También utilizamos MLflow para registrar las ejecuciones y comparar sus métricas y tiempos. Esta fase es un ensayo para aprender el flujo de trabajo; no representa por sí sola el alcance final, que contempla los distintos datasets incorporados al proyecto.

## Motivación

Los modelos fundacionales tabulares llegan preentrenados y permiten abordar nuevos datasets sin entrenar un modelo fundacional desde cero. Queremos estudiar si este enfoque proporciona resultados útiles y qué necesidades de preparación y recursos presenta frente a los métodos tradicionales.

Hemos escogido este proyecto por su aplicación a problemas industriales y por la oportunidad de evaluar estos modelos de forma práctica y rigurosa. Al finalizar, queremos disponer de un prototipo que facilite la ejecución e interpretación de experimentos y de un informe que documente las capacidades y limitaciones observadas. El equipo también aprenderá a evaluar modelos tabulares y construir prototipos analíticos.

## Alcance

**Incluye:**

- Un prototipo interactivo desarrollado con Streamlit.
- Selección entre los datasets de clasificación binaria y modelos previamente configurados y disponibles.
- Ejecución de modelos fundacionales tabulares sobre los datasets seleccionados, con un protocolo de evaluación registrado y reproducible para cada dataset.
- Comparación con los baselines tradicionales facilitados para cada caso, cuando sus condiciones de evaluación sean compatibles. Los baselines con un protocolo distinto o desconocido se identificarán como referencias externas.
- Presentación de métricas, gráficos, tiempos y detalles del experimento para facilitar la interpretación, indicando los resultados no disponibles y su motivo.
- Elaboración de un informe independiente en formato Markdown con la comparación de resultados, las limitaciones observadas y las conclusiones sobre el uso de los modelos en los casos evaluados.
- Uso de recursos cloud si hacen falta para ejecutar modelos que no puedan ejecutarse con los recursos locales.

**Queda fuera:**

- La clasificación multiclase y las tareas de regresión en esta primera versión.
- La carga libre de datasets o modelos no configurados previamente.
- Entrenar modelos fundacionales desde cero; el prototipo utilizará modelos preentrenados disponibles.
- Usar las predicciones para tomar decisiones automatizadas en procesos reales.
- Desplegar la herramienta como un sistema productivo; su propósito es la experimentación y comparación de modelos.

## Equipo y contacto

| Persona | Rol en el proyecto | Correo |
|---|---|---|
| Gonzalo Landeira Rodríguez | Ingeniero de ML | gonzalo.landeira@rai.usc.es |
| Álvaro Garnelo Luaces | Ingeniero de ML | alvaro.garnelo@rai.usc.gal |
| Rodrigo López Rego | Ingeniero de ML | rodrigo.lopez.rego@rai.usc.gal |

Los tres integrantes comparten las responsabilidades de preparación de datos, evaluación de modelos, desarrollo del prototipo y documentación de resultados.

- **Entidad:** SDG Group.
- **Tutor/a profesional:** Adriano Pezzi Fernández.
- **Correo de contacto:** [adrianoluis.pezzi@sdggroup.com](mailto:adrianoluis.pezzi@sdggroup.com).

## Estructura de esta entrega

- [README.md](./README.md): visión del proyecto, motivación, alcance, equipo y organización de la entrega.
- [specs/](./specs/): definiciones funcionales y criterios de aceptación de las funcionalidades del prototipo.
  - [comparar-modelos.md](./specs/comparar-modelos.md): selección de datasets y modelos y ejecución de experimentos con un protocolo de evaluación común.
  - [consultar-resultados.md](./specs/consultar-resultados.md): consulta e interpretación de resultados frente a baselines tradicionales y requisitos del informe comparativo.

Esta entrega contiene la definición del proyecto. La implementación del prototipo y el informe de resultados se desarrollarán en fases posteriores.

## Ensayo inicial

Para familiarizarnos con el flujo de trabajo, empezamos haciendo pruebas con tres datasets de ejemplo. Uno de ellos fue Default of Credit Card Clients, que contiene 30.000 clientes y cuyo objetivo es predecir el impago del mes siguiente. Con este dataset probamos LightGBM y TabPFN y exploramos la preparación y evaluación de los modelos. También usamos MLflow para registrar y comparar sus ejecuciones, métricas y tiempos.

Estas pruebas nos sirvieron para aprender y no determinan qué datasets formarán parte del prototipo final, que se centrará en los casos proporcionados para el proyecto.

Fuente: Yeh, I. (2009), Default of Credit Card Clients, UCI Machine Learning Repository.
