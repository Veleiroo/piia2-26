# CU-17: Automatización de la Validación de Robustez en Sistemas DAA Mediante LLMs y Simulación 3D

## 1. Qué es el proyecto

Este proyecto desarrolla un framework para **automatizar la validación de la robustez de los sistemas Detect and Avoid (DAA)** basados en visión por computador.

---

## 2. Motivación

La integración de aeronaves no tripuladas en el espacio aéreo compartido no es seguro, por lo que se necesitan sistemas DAA que detecten aeronaves de ala fija (avionetas, ultraligeros). Validar estos sistemas en el mundo real tiene unas barreras importantes:
- **Coste y logística**: El despliegue de las aeronaves para campañas de vuelo resultan muy costosas, debido al combustible, alquiler de las aeronaves y los permisos correspondientes.
- **Riesgo operativo**: Simular trayectorias extremas para que los sistemas DAA sean capaces de detectar todas las situaciones posibles puede suponer un riesgo para las aeronaves. Estes riesgos son volar en condiciones meteorológicas extremas (mucha lluvia o niebla) o simular situaciones en las que la aeronave está muy cerca.

La idea es dejar de hacer pruebas a mano y usar un sistema automático que aprende de los resultados y puede repetir exactamente el mismo ensayo una y otra vez.

---

## 3. Alcance del proyecto

Para garantizar el foco y la viabilidad técnica, los límites del proyecto quedan definidos.

### ¿Qué entra en el proyecto? (Dentro del alcance)
- **Modelado paramétrico y renderizado 3D**: generación de escenas fotorrealistas en Blender mediante scripts de Python, parametrizando la posición y distancia relativa de la aeronave respecto al dron (para simular trayectorias de aproximación frontal o de cruce), meteorología (niebla, lluvia, iluminación solar).
- **Etiquetado automático**: extracción de las bounding boxes en formato COCO derivado directamente del escenario de Blender, eliminando el error humano del etiquetado manual.
- **Planificación de pruebas con LLM**: Uso de un modelo de lenguaje que crea archivos de configuración (en formato JSON) con las órdenes y valores exactos que debe simular Blender.
- **Exploración adaptativa (bucle cerrado)**: lógica de retroalimentación que analiza el desempeño del detector y analiza dónde emoieza a fallar. Ante esto genera automáticamente más ensayos en esas situaciones críticas para encontrar su límite exacto.
- **Evaluación y trazabilidad**: integración con el modelo detector provisto por Gradiant (YOLO-X) y generación automatizada de informes técnicos de robustez, detallando los resultados y los puntos débiles encontrados.



### ¿Qué queda explícitamente fuera? (Fuera del alcance)
- **Campañas de vuelo reales**: No se realizarán pruebas físicas con drones ni aeronaves reales en espacio aéreo.
- **Entrenamiento de nuevos detectores desde cero**: El objetivo es comprobar y encontrar los fallos de detectores que ya existen (como el YOLO-X de Gradiant), no programar una nueva IA de visión ni reentrenarla.
- **Instalar el sistema en el dron**: El software se ejecutará en ordenadores y servidores de prueba, no instalado directamente en el ordenador de a bordo del dron para funcionar en tiempo real.
- **Maniobras para esquivar obstáculos (evasión)**: El proyecto se enfoca solo en ver si el dron es capaz de detectar a tiempo la aeronave; no incluye programar las maniobras de giro o esquiva para apartarse del obstáculo.

---

## 4. Equipo del proyecto

| Integrante | Rol en el Proyecto | Correo Electrónico |
| :--- | :--- | :--- |
| *Paula Esmorís Rodríguez* | Arquitectura general, especificaciones funcionales y alcance del proyecto | *[paula.esmoris@rai.usc.es]* |
| *María Gómez Fernández* | Motor de simulación en Blender, parametrización de ensayos y etiquetado ground truth | *[maria.gomez6@rai.usc.es]* |
| *Alejandra Ares Rivas* | Orquestador de ensayos con LLM, bucle adaptativo de búsqueda de fallos y generación de informes | *[alejandra.ares@rai.usc.es]* |

* **Entidad colaboradora:** Fundación Centro Tecnolóxico de Telecomunicacións de Galicia (Gradiant).
* **Tutor profesional:** Daniel Jove Díaz (`djove@gradiant.org`).

## 5. Estructura del Repositorio

A continuación se detalla la organización de los directorios y archivos del proyecto. La documentación técnica se divide en el presente documento de visión global y las especificaciones funcionales independientes alojadas en la carpeta specs/:

```text
entregas/cu-17-validacion-daa-llm/
├── README.md      # Visión general, motivación y alcance del proyecto
└── specs/
    ├── motor-simulacion-blender.md   # Spec 1: Motor de simulación en Blender
    └── generador-informe-robustez.md    # Spec 2: Planificador adaptativo LLM, evaluación e informes
