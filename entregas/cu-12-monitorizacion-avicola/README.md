# Estimación automática del peso de pollos mediante visión artificial en entornos reales de granja

Proyecto asociado a la asignatura **Proyecto Integrador de IA II** del Grado en Inteligencia Artificial de la Universidade de Santiago de Compostela, en colaboración con **Balidea** y **Aviporto**.

## 1. Descripción del proyecto

El proyecto tiene como objetivo desarrollar y evaluar un sistema de **estimación del peso de pollos** mediante imágenes capturadas en las naves de Aviporto. Se busca estudiar cómo distintas técnicas de visión artificial pueden facilitar la monitorización del crecimiento de los animales, reduciendo la necesidad de pesados manuales frecuentes.

El sistema combinará dos funcionalidades: la detección o segmentación de pollos en imágenes con varios animales y la estimación del peso de cada individuo a partir de su imagen. Para desarrollar y evaluar esta solución, se construirá un **dataset propio** con grabaciones y pesajes de referencia obtenidos en la explotación de Portomarín.

Este proyecto da continuidad al [trabajo realizado el curso anterior](https://github.com/xiannovoa/poultry-vision-monitoring), en el que se exploró la estimación del peso de pollos utilizando un dataset público de imágenes individuales. En este proyecto se busca trasladar ese trabajo a un **entorno industrial real**.

El trabajo se plantea como un piloto experimental que permitirá comprobar la precisión del sistema en las condiciones de captura estudiadas y valorar su viabilidad para un futuro despliegue.

## 2. Motivación

Hemos escogido este proyecto para dar continuidad al trabajo del curso anterior y porque nos motivaba afrontar el reto de aplicar lo aprendido a un entorno industrial. Además, la colaboración con Balidea y Aviporto nos ofrece la oportunidad de participar activamente a lo largo todo el proceso, desde decidir cómo capturar y etiquetar los datos hasta desarrollar y evaluar los modelos.

Al finalizar, queremos disponer de un **dataset propio documentado** y de un **prototipo evaluado** que combine la extracción de pollos individuales con la estimación de su peso. La intención es obtener resultados que permitan identificar sus limitaciones y valorar, junto con las entidades colaboradoras, si merece la pena avanzar hacia un despliegue a mayor escala en la explotación. Para este despliegue se han estudiado ya alternativas de computación en el borde mediante *Raspberry* (procesamiento) y *LoRaWAN* (transmisión), con el objetivo de construir un mapa más completo del reto que se afronta.

## 3. Alcance

El alcance se ajusta al plazo de unas semanas disponible para el desarrollo del proyecto en **Proyecto Integrador de IA II**. Por ello, se prioriza la construcción y evaluación de un **piloto de estimación de peso mediante visión artificial**, utilizando datos obtenidos en la explotación de Aviporto. Los resultados se referirán a las condiciones de captura y a los animales incluidos en el estudio.

### Dentro del alcance

- **Preparación del sistema de captura:** configuración de la cámara PoE sobre una estructura móvil, grabación en microSD y recuperación de los vídeos para su procesamiento posterior. Se realizarán pruebas de encuadre, iluminación y calibración o referencia de escala para definir unas condiciones de adquisición documentadas.
- **Adquisición de datos propios:** grabación de pollos individuales con sus pesajes de referencia y captura de escenas con varios animales, en coordinación con Aviporto.
- **Construcción del dataset:** extracción y selección de fotogramas, asociación de imágenes individuales con sus pesos y anotación de escenas para la detección o segmentación. Se conservará la información necesaria para conocer el origen de los datos y separar entrenamiento, validación y test.
- **Estimación de peso individual:** entrenamiento y evaluación de un modelo que estime el peso de un pollo a partir de su imagen.
- **Extracción de individuos en escenas:** desarrollo y evaluación de un modelo de detección o segmentación que permita obtener imágenes individuales a partir de capturas con varios pollos.
- **Integración y evaluación del prototipo:** combinación de ambos modelos y análisis de los errores y limitaciones al estimar pesos a partir de escenas multi-ave reales.

### Fuera del alcance inicial

- El despliegue industrial permanente, con funcionamiento autónomo y monitorización continua en tiempo real.
- La ejecución de los modelos en dispositivos de borde, como Raspberry Pi, y la transmisión de resultados mediante LoRaWAN.
- La identificación y el seguimiento persistente de cada pollo a lo largo del tiempo.
- La monitorización de otras variables, como enfermedades o patrones de comportamiento.
- La validación general del sistema para cualquier nave, explotación o configuración de cámara.

Las alternativas de despliegue futuro podrán estudiarse y documentarse, pero su implementación quedará condicionada a los resultados del piloto y a una ampliación del alcance acordada con los tutores y las entidades colaboradoras.

## 4. Equipo

| Integrante | Responsabilidad principal | Correo de contacto |
| --- | --- | --- |
| Xián Novoa Gutiérrez | Preparación del dataset: organización de grabaciones y pesajes, extracción de fotogramas y asociación de etiquetas. | [xian.novoa@rai.usc.gal](mailto:xian.novoa@rai.usc.gal) |
| Iago Varela Rodríguez | Estimación de peso individual: entrenamiento y evaluación del modelo de predicción de peso. | [iago.varela@rai.usc.gal](mailto:iago.varela@rai.usc.gal) |
| Jesús Rodríguez Fernández | Extracción de pollos individuales: detección o segmentación de animales en escenas de la granja. | [jesus.rodriguez.fernandez@rai.usc.gal](mailto:jesus.rodriguez.fernandez@rai.usc.gal) |

Este reparto establece las responsabilidades iniciales de cada integrante. La adquisición de datos, las decisiones de diseño, la integración de las funcionalidades y la documentación se realizarán de forma colaborativa.

El proyecto cuenta con el acompañamiento técnico de **Balidea** y la colaboración de **Aviporto**, que facilita el acceso a la explotación y la coordinación de las jornadas de captura y pesaje.

## 5. Estructura

```text
entregas/
└── cu-12-monitorizacion-avicola/
    ├── README.md
    └── specs/
        ├── preparacion-dataset-peso.md
        ├── estimacion-peso-individual.md
        └── extraccion-pollos-individuales.md
```

- **`README.md`**: presenta el proyecto, su motivación, el alcance, el equipo y la estructura del repositorio.
- **`specs/`**: contiene las especificaciones funcionales. Cada documento describe qué construir, por qué, las restricciones y los criterios de aceptación:
  - **`preparacion-dataset-peso.md`**: define la transformación de las grabaciones individuales y los registros de pesaje en un dataset de imágenes etiquetadas, conservando su trazabilidad y estableciendo su división para entrenamiento, validación y test.
  - **`estimacion-peso-individual.md`**: define la estimación del peso de un pollo a partir de su imagen, incluyendo las condiciones de entrada, el resultado esperado y la evaluación del modelo.
  - **`extraccion-pollos-individuales.md`**: define la localización y extracción de animales en escenas con varios pollos, generando imágenes individuales que puedan utilizarse como entrada del estimador de peso.
  