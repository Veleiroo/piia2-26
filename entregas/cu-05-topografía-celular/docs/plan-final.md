# Propuesta de planning hasta la entrega final

Fecha de inspección: 27 de octubre de 2026. Planning aprobado y aplicado en Trello.
Los enlaces a las tarjetas están en [trello.md](trello.md).

Todo el material del equipo está en `entregas/cu-05-topografía-celular/`,
dentro del fork de la asignatura. Las rutas y comandos de este documento son
relativos a esa carpeta, salvo las referencias a las guías de la asignatura.

## Hitos actualizados por el equipo

Fechas comunicadas por el usuario el 27 de octubre de 2026. Esta actualización
prevalece sobre las fechas anteriores de las guías locales.

| Hito | Fecha | Contenido y estado del plazo |
|---|---|---|
| Entrega 1 | 2 de noviembre de 2026 | README y al menos dos specs funcionales |
| Entrega 2 | 16 de noviembre de 2026 | Arquitectura y decisiones de implementación |
| Final | 11 de diciembre de 2026 | Hito final; fecha límite de entrega del material por confirmar |

La prioridad inmediata es dejar el README y las specs revisados el 1 de
noviembre, como objetivo interno, y presentar la Entrega 1 antes de su plazo.
Las specs describen el comportamiento y los criterios de aceptación previstos;
no dependen de tener ya implementado el piloto. Las incógnitas experimentales
se documentan como restricciones o supuestos pendientes de confirmar.

## Qué está comprobado

Se han localizado los ocho PDF y seis carpetas de pilas exportadas en
`data/`. No hay JSON de adquisición: hay dos XML por carpeta.
El inventario reproducible se genera en `tmp/inventario-metadatos.json` con
`python3 scripts/auditar_metadatos.py` (requiere `tifffile`). Una carpeta no equivale a una célula ni
a una réplica biológica.

| Carpeta | Planos Z | Dimensión Y × X | Canales científicos descritos |
|---|---:|---:|---|
| canales g10 | 49 | 485 × 107 | DAPI |
| canales g10 2 | 106 | 633 × 342 | DAPI y Alexa 488 |
| canales g10 3 | 111 | 1464 × 1464 | DAPI |
| control 1 | 49 | 381 × 492 | DAPI |
| control 2 | 46 | 585 × 395 | DAPI |
| control 3 | 46 | 331 × 395 | DAPI |

Las seis pilas tienen aproximadamente Δx = Δy = 0,0630635 µm y
Δz = 0,3333095 µm. Los Properties.xml redondean esos valores a 0,063 y
0,333 µm en `DimensionDescription/@Voxel`. El XML numérico contiene
`Length` en metros y `NumberOfElements`. En esta exportación Leica,
`Length / (NumberOfElements - 1)` recupera el espaciado y concuerda con
`Voxel` y con los ajustes de adquisición. El campo `Quantity` del hardware
tiene el valor 3.33309491452686E-07, coherente con el paso Z en metros,
pero su unidad está vacía: no se usa como única prueba de calibración.

No confundir el paso Z con el grosor óptico de una sección ni con la
resolución axial. El volumen se calculará con el espaciado de los tres ejes.

Se han comprobado los encabezados de los 619 TIFF: las dimensiones Y/X coinciden
con sus XML. Los índices Z son consecutivos, sin huecos en los grupos exportados.
Hay 407 planos DAPI; los otros 212 TIFF corresponden al canal 1 y a overlays de
`canales g10 2`. Los overlays no son muestras adicionales.

El microscopio figura como STELLARIS 8 y el tipo de adquisición como Confocal.
Los TIFF actuales son RGB uint8, incluso los del canal DAPI, y las imágenes
visualizadas contienen barras de escala y texto integrados en sus píxeles.
El RGB de visualización no equivale a tres canales biológicos. No se debe
segmentar la barra como si fuera señal nuclear. Solicitar el .lif de origen
o exportaciones monocanal sin anotaciones; el piloto puede avanzar con estas
imágenes si excluye las anotaciones y registra sus limitaciones.

`control 2` y `control 3` comparten los tiempos de inicio y fin, y el segundo
se denomina `Control 1d 63x2 02_Crop 2`. Son indicios de recortes de una misma
adquisición. La comparación directa no encontró que todo `control 3` fuera un
recorte vertical idéntico de `control 2` incluyendo anotaciones: no se afirma
duplicación exacta ni solapamiento. Agrupar provisionalmente ambos para la
evaluación y confirmar su procedencia con el grupo.

Por nombres hay dos condiciones: control y G10. El conjunto disponible consta
de seis pilas; no se han detectado planos ausentes en sus secuencias exportadas.
No se han encontrado carpetas G80 o micropocillos. Falta conocer
el número de scaffolds independientes, lotes/donantes y las dimensiones reales
del patrón. El nombre `1d` sugiere un día, pendiente de confirmación experimental.
Alexa 488 identifica el fluoróforo, no por sí solo la estructura marcada.

## Alcance que propongo

Entregable principal: herramienta reproducible para cargar pilas calibradas,
segmentar instancias nucleares, revisar/corregir máscaras y exportar medidas
geométricas y controles de calidad. Predicción: experimento condicionado a que
se puedan construir pares topografía-respuesta y particiones independientes.
Con dos condiciones no se demuestra generalización a nuevas geometrías.

La primera versión medirá volumen, ejes de un elipsoide equivalente y sus
relaciones. Las definiciones y unidades deben quedar explícitas. Superficie y
esfericidad se incorporarán después de evaluar su sensibilidad al paso Z y al
contorno de segmentación. La orientación respecto al scaffold requiere conocer
su dirección/superficie: la orientación en la imagen no la sustituye.

## Trello: estructura y funcionamiento

Mantener Pendiente, En curso y Hecho. Cada tarjeta tendrá un responsable
principal y un revisor del equipo, resultado esperado, checklist corto,
dependencias y enlace a la evidencia. Los nombres se decidirán con el equipo;
no se infieren cuentas Trello a partir de usuarios GitHub.

Las áreas Datos, Segmentación, Medidas, Predicción y Entrega se indican en las
descripciones. Los bloqueos se registrarán con su causa y dependencia.
Limitar En curso a dos o tres tarjetas para todo el equipo.
Una tarjeta pasa a Hecho al cumplir su checklist y enlazar el resultado revisado;
marcarla completa y moverla son acciones distintas en Trello.

Estado del tablero: Primera reunión ya está completada en Hecho, junto
con Asignación de caso de uso, Primer contacto e Introducción al dominio.
Posesión de datos se ha completado y movido a Hecho tras verificar la recepción
de los archivos disponibles. La auditoría de calibración y procedencia tiene
su propia tarjeta en En curso; falta confirmar la procedencia experimental.

## Tarjetas propuestas

Fechas internas de seguimiento incluidas en el planning aprobado. Se revisarán
según la dedicación de cada integrante. La documentación se mantiene
durante el desarrollo; no se deja para la última semana.

| Tarjeta | Ventana propuesta | Resultado verificable | Dependencias |
|---|---|---|---|
| 1. Cerrar inventario, calibración y procedencia | 27-30 oct. | Seis pilas registradas, escalas por eje, dudas y grupos experimentales documentados | Archivos recibidos |
| 2. Acordar alcance y validación con la entidad | 27-30 oct. | Propuesta de objetivo, medidas, exclusiones y evaluación revisada; petición de datos preparada y dudas pendientes registradas | Hallazgos de 1 |
| E1. Preparar y entregar README y specs | 27 oct.-1 nov.; plazo 2 nov. | README y al menos dos specs revisados, con alcance, restricciones y criterios verificables; PR de entrega | Hallazgos disponibles de 1 y 2; las confirmaciones pendientes se documentan |
| 3. Cargar y visualizar una pila piloto | 30 oct.-5 nov. | Canal DAPI, desplazamiento Z, vistas XY/XZ/YZ y escala física correctos | 1 |
| 4. Segmentar y revisar el piloto | 4-11 nov. | Máscara 3D por instancias editable, correcciones guardadas y fallos identificados | 3 |
| 5. Mantener arquitectura y decisiones de implementación | 2-13 nov. | ARCHITECTURE, al menos dos ADR, README y specs coherentes; preparar entrega del 16 nov. | 2-4 |
| 6. Medir y procesar las seis pilas | 9-20 nov. | Tabla por núcleo con unidades, procedencia y estado de calidad; máscaras guardadas | 4 |
| 7. Validar la medición | 16-25 nov. | Referencia manual revisada, error por instancia y error geométrico, sensibilidad de medidas | 6 |
| 8. Decidir viabilidad del predictor y construir pares | 23-27 nov. | Tabla de entradas/salidas y particiones por grupo, o justificación de alcance descriptivo | 1, 2, 6 |
| 9. Comparar predictores si hay datos adecuados | 26 nov.-4 dic. | Media de entrenamiento, regresión regularizada y candidato para pocos datos con idénticas particiones | 7, 8 |
| 10. Cerrar demo, resultados y reproducibilidad | 30 nov.-7 dic. | Ejecución completa, exportaciones, dependencias y limitaciones; revisión con entidad | 6-9 según viabilidad |
| 11. Preparar presentación y entrega final | 1-9 dic.; final 11 dic. | Presentación, PDF, vídeo de respaldo y ensayo listos; confirmar plazo de entrega del material y preparar PR | Resultados disponibles; cierre tras 10 |

Checklist 1: comprobar TIFF/XML e índices Z; registrar escalas y canal; vincular
recortes a adquisición/scaffold; pedir originales de las seis pilas sin
anotaciones. La calibración y la integridad dimensional iniciales ya están
comprobadas, pero la procedencia experimental sigue abierta.

Checklist 2: acordar objetivo de análisis nuclear; confirmar célula/tiempo/patrón;
solicitar tablas LAS X y datos existentes; dejar anotado qué condiciones permiten
evaluar predicción. No enviar mensajes a la entidad sin autorización del usuario.

Checklist E1: redactar README (problema, motivación, alcance, equipo y estructura);
redactar al menos dos specs para carga/visualización y segmentación/medición;
definir criterios observables, unidades y exclusiones; dejar la predicción
condicionada a los datos; revisar coherencia y preparar el PR para el 2 nov.

Checklist 3: ordenar Z numéricamente; leer canales desde metadatos; visualizar
anisotropía sin deformar proporciones; excluir texto/barra y guardar configuración.
Primera candidata: control 1, sujeto a revisar contención nuclear en Z.

Checklist 4: probar un método clásico; comparar un preentrenado si aporta valor;
revisar instancias en los tres planos; guardar máscara automática y corregida,
parámetros y versión. El suavizado o reescalado debe preservar la calibración.

Checklist 5: documentar carga/segmentación/medidas y la rama condicional de
predicción; justificar dos decisiones reales; revisar criterios de aceptación;
preparar el PR de la entrega intermedia sin inventar resultados.

Checklist 6: calcular volumen y ejes en coordenadas físicas; señalar truncados,
uniones y artefactos; exportar una fila por núcleo con identificadores de campo,
adquisición y scaffold cuando se conozcan; no contar cada plano como ejemplo.

Checklist 7: delimitar referencia manual de evaluación; medir detección/unión/
separación además del solapamiento; comparar geometría automática y revisada;
separar el conjunto usado para ajustar parámetros del que se usa para evaluarlos
en la medida que permitan los grupos disponibles.

Checklist 8: confirmar pares reales; agrupar recortes de una adquisición;
registrar réplicas por condición; decidir antes de elegir el modelo. Si no hay
independencia suficiente, entregar análisis descriptivo y prototipo experimental,
sin una afirmación de generalización predictiva.

Checklist 9: definir pocas entradas y salidas; elegir métricas como MAE por
variable; ajustar transformaciones usando solo entrenamiento; comparar en las
mismas particiones, guardar predicciones y explicar límites. TabPFN o LLM son
candidatos, no decisiones ya tomadas. Si no se cumple 8, esta tarjeta se cierra
como no viable con justificación, sin fabricar evaluación.

Checklist 10: reproducir una ejecución desde instalación limpia; comprobar
salidas y mensajes de error; preparar una demo breve; revisar utilidad y
conclusiones con la entidad y recoger su visto bueno.

Checklist 11: confirmar el plazo de entrega del material del hito final del
11 de diciembre; redactar motivación, solución, evidencia y límites; ensayar
diez minutos; comprobar compatibilidad y vídeo; preparar y subir el PR dentro
del plazo que se confirme. El cierre interno del 9 dic. es un objetivo de
preparación, no una fecha oficial de entrega. No se presupone una antelación
mínima de dos días mientras el plazo actualizado siga pendiente.

## Fechas de la asignatura usadas

Se usan las fechas actualizadas por el usuario: Entrega 1 el 2 nov., Entrega 2
el 16 nov. y final el 11 dic. de 2026. La fecha límite para entregar el material
final sigue pendiente de confirmación; no se deduce del día del hito final.

Las fechas anteriores de `evaluacion/entrega-1.md`, `evaluacion/entrega-3.md`
y README están desactualizadas respecto a esta comunicación. Esas guías se
conservan como documentación de la asignatura, sin reescribirlas como si el
profesorado ya hubiese publicado versiones corregidas. El contenido de la
Entrega 2 sigue siendo arquitectura y decisiones de implementación, el 16 nov.

Tablero consultado: https://trello.com/b/19titMFj/proyecto-ii-scaffolds
