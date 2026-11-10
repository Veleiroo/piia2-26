# Seguimiento de noviembre

Revisión documental y del tablero: 10 de noviembre de 2026. Esta revisión no
se presenta como reunión del equipo ni acredita asistencia a interactivas.

Rutina y registro continuo en Trello:
[Seguimiento de noviembre](https://trello.com/c/7SHwW2gD).

## Comentario y rúbrica recibidos

Comentario de octubre, comunicado por el equipo:

> Las tareas están bien dimensionadas y con DoR y DoD claros. Los bloqueos no
> se están identificando ni gestionando, y el tablero tiene algunos desajustes.
> Para noviembre: marcar los bloqueos en el tablero y actuar sobre cada uno,
> y actualizar el tablero en cada reunión.

La rúbrica recibida el 10 de noviembre valora definición de tareas, gestión de
bloqueos e higiene del tablero. Para MB exige alcance adecuado y DoR/DoD claros,
impedimentos señalados y gestionados, y columnas correctas con WIP contenido y
actualización en cada reunión. NP se asocia a no asistir a las reuniones
interactivas y no poder ser valorados. La mejora del tablero debe acompañarse
de participación real en esas reuniones.

## Funcionamiento del tablero

- **Pendiente:** trabajo aún no iniciado. Una dependencia futura no convierte
  automáticamente una tarea planificada en bloqueada.
- **En curso:** trabajo realmente iniciado, con evidencia y siguiente paso.
  Objetivo: dos tareas técnicas simultáneas; máximo tres tarjetas activas en
  total, contando el seguimiento. Antes de abrir otra, terminar, pausar o
  reorganizar una de las actuales y registrar el motivo.
- **Bloqueadas:** trabajo que no puede avanzar en su parte necesaria por un
  impedimento concreto. Registrar qué parte sí puede continuar.
- **Hecho:** DoD cumplida, checklist revisado y evidencia enlazada. Mover la
  tarjeta y marcarla completa son operaciones distintas.

Cada tarjeta debe indicar resultado, DoR (qué permite empezar), DoD (qué permite
cerrar), dependencias y evidencia. Se conservan los criterios existentes y se
explicitan los de las tarjetas nuevas o antes vacías.

Cada bloqueo debe incluir causa, fecha de detección o primera documentación,
alcance afectado, responsable del seguimiento, acción realizada, siguiente
acción, revisión, alternativa y criterio de desbloqueo. No atribuir al 10 de
noviembre el inicio de un bloqueo que ya figuraba el 3 de noviembre. Cuando
se resuelva, conservar la resolución y mover a Pendiente o En curso según
corresponda.

Pablo coordina provisionalmente el seguimiento. El reparto técnico y revisores
se concretan con el equipo en la próxima reunión; esta coordinación no presume
acuerdos con Alba o Franco. Próxima revisión interna: **13 de noviembre**, o
antes si hay reunión o nueva información. Es un objetivo de seguimiento, no una
reunión confirmada ni una fecha garantizada de recepción de archivos.

## Evidencia y acciones de esta revisión

| Hallazgo comprobado | Acción de gestión |
|---|---|
| `data/` contiene las seis carpetas de control/G10; no constan nuevas condiciones locales. | La integración adicional queda Bloqueada hasta confirmar recepción. Consulta preparada abajo. Se continúa con las pilas disponibles. |
| Hay notebook con carga, selección DAPI, orden Z, espaciado y pruebas exploratorias, y código Cellpose local. | Carga y segmentación pasan a En curso. No se cierran: faltan revisar sus criterios y continuidad/revisión 3D. |
| Las dos tarjetas de ampliación estaban Bloqueadas sin explicación. | Se documentan causas, dependencias, acciones, revisión y alternativas. |
| El título del predictor proponía inferir scaffold desde volumen, al revés de la spec entregada. | Se alinea con topografía → morfología nuclear y se vincula a medidas/viabilidad. |
| No constan `ARCHITECTURE.md` ni `decisions/` en la carpeta del equipo. | Entrega 2 sigue Pendiente y priorizada; puede redactarse sin esperar nuevos datos ni cerrar toda la segmentación. |

Las ejecuciones locales no demuestran que todos los cambios estén publicados
en GitHub. No se publican datos experimentales ni salidas de `tmp/`. Se conserva
el vencimiento interno del 5 de noviembre para cargar el piloto: el retraso se
revisa, no se oculta cambiando la fecha sin explicación.

## Consulta preparada para la entidad

**Borrador pendiente de envío por el equipo.** Primero comprobar si existen
archivos recibidos que todavía no se hayan incorporado al proyecto.

Hola, estamos avanzando con la segmentación y las medidas nucleares de las seis
pilas disponibles, correspondientes a control y G10. Para planificar la
ampliación y preparar los ejemplos topografía–morfología, necesitamos aclarar:

1. ¿Hay imágenes de otras condiciones disponibles? ¿Qué tipos de patrón y
   medidas nominales cubren y cuándo podríamos recibirlas?
2. Para cada carpeta, ¿qué adquisición y muestra experimental representa y
   cuáles son réplicas independientes? En particular, ¿`control 2` y `control 3`
   proceden de la misma adquisición o muestra?
3. ¿Podéis facilitar la correspondencia entre carpeta, tipo de patrón y medida
   nominal, incluyendo su unidad y la dimensión que describe?
4. Si hay nuevos archivos, ¿vendrán con canal nuclear y metadatos para calibrar
   X/Y/Z? Si existen originales sin anotaciones, serían útiles como mejora,
   aunque podemos continuar el piloto con las exportaciones actuales.

Si no hay más condiciones, adaptaremos la demostración y explicaremos los
límites de la evaluación con los datos actuales.

Pablo coordina el envío y el registro de respuesta. En la revisión del 13 de
noviembre, si no hay respuesta, decidir un seguimiento con la entidad y mantener
el avance con control/G10. Si no habrá datos nuevos, registrar la decisión de
alcance en las tarjetas afectadas. No consta ningún envío ni respuesta realizado
por esta revisión.

## En cada reunión

1. Revisar avances frente a DoD y enlazar evidencia; mover y completar solo lo
   realmente terminado.
2. Revisar cada bloqueo: acción desde la reunión anterior, resultado, siguiente
   acción, responsable, alternativa y próxima revisión.
3. Ajustar columnas, WIP y prioridades. Explicar retrasos y cambios de fechas;
   separar revisión interna de plazo oficial.
4. Registrar fecha real, asistentes reales, decisiones y tarjetas revisadas.
   Si no hay reunión, no crear un acta ficticia.

Plantilla para el registro de una reunión real:

```text
Fecha y asistentes:
Avances y evidencias:
Tarjetas movidas y motivo:
Bloqueos: acción → resultado → siguiente acción / responsable / revisión:
WIP y prioridades acordadas:
Próximos compromisos:
```

La Entrega 2 vence el 16 de noviembre antes de las 23:59 (Europe/Madrid), según
`evaluacion/entrega-2.md`; se mantiene el 13 como objetivo interno de revisión.
