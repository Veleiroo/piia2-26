# Generador informe de robustez

## 1. Qué hay que construir

Un módulo basado en un LLM que opera en la etapa final de la arquitectura de validación, tomando todos los resultados (la configuración de cada escenario y las detecciones del modelo YOLO, en formato JSON) para generar de forma automática un informe detallado de robustez del detector DAA. El informe muestra qué requisitos se cumplen, dónde se degrada el detector, qué pruebas han fallado y qué parte del espacio operacional se ha cubierto. 

Se realiza un análisis de los resultados de forma automática (métricas, zonas críticas y cobertura) y un LLM lo redacta como un documento de evidencia estructurado y útil.

## 2. Por qué
En nuestro proyecto anterior, el análisis caso a caso y la redacción del informe de evidencia eran procesos manuales que generaban un cuello de botella en la validación. El propósito de este componente es automatizar la creación de informes para aumentar la cobertura de pruebas reduciendo el trabajo manual y garantizando que se visibilicen rápidamente las zonas críticas donde el sistema falla.

## 3. Restricciones

- **Trazabilidad**: toda afirmación del informe debe poder rastrearse hasta los ensayos que la respaldan.

- **Sin conclusiones inventadas**: el LLM no produce cifras propias. Solo puede citar valores presentes en los datos que se le pasan, es decir, las conclusiones que saca deben tener base en los datos de prueba.

- **Sin acceso a imágenes**: el módulo trabaja solo con archivos de resultados.

- **Determinismo**: con los mismos resultados, el análisis y sus conclusiones deben ser siempre los mismos.

- **Dependencia de datos:** El sistema recibirá un input estructurado de los ensayos, donde cada uno cuenta con su propia configuración y resultado.


## 4. Criterios de aceptación

- **Identificador en cada fallo y zona crítica**: el 100% de los fallos y zonas críticas del informe incluyen el identificador de los ensayos que los originan, de forma que se puedan reproducir.

- **Identificación de zonas críticas**: el informe señala explícitamente las zonas críticas con su intervalo numérico de degradación (por ejemplo, "caída de rendimiento entre los niveles 2 y 4 de niebla").

-  **Cifras respaldadas por los datos**: ninguna cifra del informe aparece sin respaldo en los resultados, y así se comprueba automáticamente.

- **Cobertura del espacio operacional**: el informe indica la cobertura alcanzada sobre el espacio operacional y qué zonas quedan sin probar.

- **Tratamiento de ensayos incompletos**: los ensayos que no se pudieron completar aparecen en el informe con su motivo y no se cuentan como éxitos ni como fallos.

- **Formato y tiempo de generación**: el informe se genera en un formato legible y en un tiempo razonable (menos de un minuto).

- **Reproducibilidad del análisis**: al procesar los mismos datos se obtienen las mismas conclusiones.