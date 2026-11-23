# Spec: seleccionar y ejecutar un experimento

## Qué construir

Una funcionalidad del prototipo Streamlit que permita elegir un dataset registrado y uno o varios modelos fundacionales tabulares disponibles, y lanzar una evaluación de clasificación binaria. Para el dataset seleccionado, la herramienta asociará los metadatos necesarios —fichero, variable objetivo, clases positiva y negativa y configuración de evaluación— y mostrará el estado de la ejecución. Los resultados de las ejecuciones completadas se podrán consultar en la vista definida en [consultar-resultados.md](./consultar-resultados.md).

Cada caso podrá vincularse con el baseline tradicional proporcionado por SDG Group. Cuando sus datos, partición y protocolo sean compatibles con los del experimento, se utilizará como comparación directa. Si su protocolo es distinto o desconocido, se identificará como referencia externa y se indicarán las diferencias o la información que falta.

## Por qué

El caso de uso busca estudiar el potencial de los modelos fundacionales en distintos problemas industriales tabulares. Una interfaz común permitirá probar los datasets y modelos disponibles sin reescribir el flujo de evaluación en cada experimento. Mantener un protocolo registrado para cada dataset permitirá interpretar las diferencias entre modelos y reproducir las evaluaciones.

## Restricciones y supuestos

- La primera versión ofrece únicamente datasets de clasificación binaria y modelos previamente configurados y disponibles; no admite ficheros o modelos arbitrarios.
- Cada dataset registrado identifica su variable objetivo, clases positiva y negativa, fuente y tratamiento básico requerido.
- Antes de ejecutar, cada dataset tendrá un protocolo registrado que identifique los conjuntos de entrenamiento y evaluación y, si se utiliza, el de validación. La partición se conservará mediante los identificadores de sus filas o mediante un procedimiento reproducible que especifique el método, sus parámetros y la semilla cuando exista aleatoriedad.
- Los modelos comparados se evaluarán sobre las mismas filas, con las mismas etiquetas y definiciones de métricas. El preprocesado específico de cada modelo quedará registrado.
- Los datos de evaluación no se utilizarán para ajustar el modelo, aprender el preprocesado, seleccionar hiperparámetros o elegir el umbral de decisión. Estas decisiones se tomarán con los datos de entrenamiento o validación y se registrarán antes de la evaluación.
- Un baseline solo se presenta como comparación directa si utiliza el mismo conjunto de evaluación, objetivo y protocolo compatible; si no, se etiqueta como referencia externa y se muestran sus limitaciones.
- La herramienta muestra errores de carga, incompatibilidad o falta de recursos, y no marca una ejecución fallida como completada.
- Las ejecuciones son experimentales y no se usan para decisiones reales sobre personas.

## Criterios de aceptación

1. El usuario puede ver y seleccionar los datasets registrados y uno o varios modelos disponibles en la interfaz.
2. Al seleccionar un dataset, la interfaz identifica el problema, la variable objetivo y las clases positiva y negativa antes de ejecutar.
3. El usuario puede iniciar una evaluación y ve si está en curso, completada o fallida para cada modelo seleccionado.
4. Para cada ejecución completada quedan registrados el dataset, el modelo, la configuración, el preprocesado y el protocolo que permite reproducir la partición. Los modelos comparados utilizan las mismas filas de evaluación.
5. El registro del experimento permite comprobar que el ajuste, el preprocesado aprendido y la selección de hiperparámetros o umbral utilizan exclusivamente los conjuntos de entrenamiento o validación.
6. Cuando existe un baseline asociado, la interfaz distingue una comparación directa de una referencia externa e indica las diferencias conocidas o la información necesaria para verificar su compatibilidad.
7. Si el modelo no puede ejecutarse por falta de datos, dependencias o recursos, se informa del motivo de forma visible y la ejecución figura como fallida. No se presentan métricas como si la evaluación hubiera terminado.
8. Los resultados de una ejecución completada están disponibles en la vista de consulta, aunque no exista un baseline compatible.
