# Predicción de cierres de bateas de mejillón en las rías gallegas

## Qué es

Una herramienta que, para cada polígono de bateas de mejillón, estima la probabilidad de que siga en su estado actual (abierto o cerrado) durante los próximos 1, 3, 7 y 14 días. El proyecto continúa el trabajo de PIIA 1, que predecía el cierre del día siguiente solo en la ría de Arousa, y lo amplía en tres direcciones: más rías, más datos y un modelo de supervivencia.

Este proyecto va dirigido a productores de mejillón, que deciden cuándo cosechar y cómo planificar el trabajo y las ventas. La herramienta orienta esas decisiones, pero no sustituye a la decisión oficial de apertura o cierre, que corresponde a INTECMAR.

## Motivación

**Por qué este proyecto.** Galicia es una de las principales regiones productoras de mejillón del mundo, y un cierre inesperado deja a los productores sin poder vender. Es un problema real y cercano, con datos públicos, en el que ya tenemos experiencia tras PIIA 1.

**Por qué cambiar de modelo.** En PIIA 1 obtuvimos un F1 de 0,93 en el test de 2024-2025, pero al revisarlo descubrimos que copiar el estado de hoy da un F1 de 0,942. El motivo es que solo 143 de las 19.136 filas de test cambian de estado. Es decir, nuestro modelo no aportaba más que esa regla, justo en el caso que importa: anticipar los cambios.

El análisis de supervivencia evita ese problema. Trata a cada polígono como un ser que "vive" mientras está abierto y "muere" al cerrarse, y predice cuánto tiempo seguirá así. Solo evalúa a los polígonos que todavía pueden cerrarse, y responde a una pregunta más útil: "¿podré seguir cosechando la semana que viene?".

**Qué queremos conseguir al terminar:**

1. Un modelo que anticipe los cierres mejor que una regla simple basada en la última analítica.
2. Comprobar con datos reales si el modelo funciona en una ría que no ha visto durante el entrenamiento.
3. Saber qué datos son imprescindibles para predecir y cuáles aportan poco.

## Alcance

### Dentro del alcance

- **Datos:** la ría de Arousa (2015-2025) y las demás rías que recibamos de INTECMAR.
- **Cultivo:** solo mejillón.
- **Preparación de datos:** validar, limpiar y unificar los datos de cada ría (spec 1).
- **Predicción:** un único modelo de supervivencia para todas las rías, que estima la permanencia de un polígono abierto y de uno cerrado a 1, 3, 7 y 14 días (spec 2).
- **Evaluación:** por años y dejando fuera una ría, siempre comparando con dos referencias simples (spec 2).
- **Informe de dependencia de datos:** un documento breve que recoge qué fuentes necesita el modelo y cuánto aporta cada una (spec 3).

### Fuera del alcance

| Fuera de alcance | Motivo |
|---|---|
| Otras especies (ostra, almeja, vieira...) | Acumulan y eliminan las toxinas a otro ritmo. Además, hay muy pocos muestreos en Galicia. |
| Nuevas fuentes de datos (fitoplancton, afloramiento, satélite) | Podrían mejorar el modelo, pero no las tenemos y conseguirlas ampliaría demasiado el tiempo del proyecto. |
| Aplicación web desplegada, API o ejecución en tiempo real | Requieren infraestructura y mantenimiento que no son el objetivo del proyecto. |
| Modelos más avanzados (Cox, Random Survival Forest, multiestado, riesgos competitivos) | Usamos un solo método que el equipo pueda entender y defender. |
| Un modelo distinto para cada ría | Queremos un modelo general, aplicable a una ría nueva. |

## Funcionalidades

```
CSV de cada ría  ->  Spec 1: preparación de datos  ->  Tabla diaria con el estado de cada polígono
                                                                       |
                      Probabilidades y evaluación  <-  Spec 2: predicción de supervivencia
                                     |
Spec 3: informe de dependencia de datos (usa también los resultados de la spec 1)
```

| Spec | Qué hace | Por qué hace falta |
|---|---|---|
| Preparación de datos multi-ría | Comprueba cada CSV, limpia los valores y genera una fila por polígono y día con su estado. | El modelo necesita datos comparables entre rías. |
| Predicción de supervivencia | Entrena y evalúa el modelo, y responde a consultas sobre un polígono y una fecha. | Es el resultado que usa el productor y la respuesta a nuestros dos primeros objetivos. |
| Informe de dependencia de datos | Reúne los resultados de las otras dos specs, clasifica cada fuente de datos y fija qué debe aportar una ría nueva. | Responde a nuestro tercer objetivo y permite decidir si una ría se puede usar. |

## Supuestos y riesgos

| Supuesto o riesgo | Qué implica | Qué haremos |
|---|---|---|
| Los datos nuevos todavía no han llegado | No sabemos qué rías ni qué periodo tendremos. | Exigimos el mismo formato que Arousa. Si no llegan a tiempo, evaluaremos dejando fuera zonas de Arousa e indicaremos que esa prueba es menos exigente. |
| No tenemos el histórico oficial de aperturas y cierres | Estimamos el estado a partir de las toxinas y el límite legal, sin ver cierres preventivos ni reglas de reapertura. | Lo dejamos claro en los resultados. |
| Suponemos que el resultado del laboratorio se conoce el mismo día | Los resultados pueden ser algo optimistas. | Lo indicamos como limitación. |

## Equipo


| Persona | Rol | Correo |
|---|---|---|
| Hugo Penas Pazos | Datos: preparación y validación | hugo.penas@rai.usc.es |
| Alejandro Romano Vizcaya | Modelo: entrenamiento de supervivencia | alejandro.romano@rai.usc.es |
| Marcos Suárez Sertal | Evaluación: métricas y comparación por ría | marcos.suarez.sertal@rai.usc.es |
| Martín Otero Tourís | Documentación y coordinación | martin.otero.touris@rai.usc.es |

## Estructura

En esta primera entrega solo hay documentación, todavía no hay código.

```
entregas/cu-xx-cierres-bateas/
  README.md                            Este documento: qué es el proyecto, alcance y equipo
  specs/
    preparacion-datos-multi-ria.md     Qué debe hacer la preparación de datos y cómo se comprueba
    prediccion-supervivencia.md        Qué debe hacer el modelo y cómo se comprueba
    informe-dependencia-datos.md       Qué debe contener el informe de dependencia de datos y cómo se comprueba
```

## Glosario

| Término | Significado |
|---|---|
| **Batea** | Plataforma flotante de la que cuelgan las cuerdas donde se cultiva el mejillón. |
| **Polígono** | Zona delimitada de una ría que agrupa bateas. Es la unidad que se abre o se cierra. |
| **Biotoxinas** | Toxinas producidas por microalgas que se acumulan en el mejillón. |
| **INTECMAR** | Organismo gallego que analiza las toxinas y decide las aperturas y los cierres. |
| **Censura** | Dejar de observar un polígono antes de saber cuándo cambia su estado. Sabemos que siguió igual "al menos" hasta ese día. |
| **AUC** | Mide si el modelo da más riesgo a los polígonos que cierran que a los que no. 0,5 equivale al azar y 1 es perfecto. |
