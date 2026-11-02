# Visión por computador: segmentación y medición nuclear

## Qué construir y para qué

Un flujo reproducible que reciba una pila de microscopía con señal nuclear DAPI,
obtenga máscaras por instancia que puedan revisarse y exporte medidas geométricas
de los núcleos. Estas medidas permitirán describir las muestras y construir las
respuestas observadas de los ejemplos del [módulo LLM](integracion-llm-few-shot.md).

Medir el núcleo que aparece en una imagen es un paso previo a predecir su forma
desde la topografía. La funcionalidad debe conservar la relación entre imagen,
máscara, medida y muestra para poder identificar el origen de un error.

## Entradas y salidas

**Entradas:** carpeta de una pila TIFF, XML de adquisición, identificador de pila
y configuración de procesamiento. La configuración recoge el canal, los planos
seleccionados, el muestreo, la normalización, las zonas excluidas y los parámetros
de segmentación. Se admiten las exportaciones actuales, aunque incluyan anotaciones.

**Salidas:**

- Máscaras de etiquetas enteras: `0` para fondo e identificadores positivos para
  las instancias. Se conserva la propuesta automática y, si se modifica, una
  versión revisada diferenciada.
- Una tabla por núcleo medido con identificador de pila e instancia, volumen en
  µm³, ejes `a ≥ b ≥ c` en µm y relaciones `a/b` y `b/c`. Los ejes corresponden a
  un elipsoide equivalente; sus relaciones describen forma sin asumir la
  orientación de la superficie del scaffold.
- Un registro de procedencia con archivos de entrada, calibración, transformaciones,
  modelo y versión, parámetros, exclusiones y estado de revisión.
- Figuras de la imagen y las máscaras superpuestas para inspeccionar los resultados.

## Comportamiento esperado

1. **Validar y cargar.** Identificar el canal DAPI desde los metadatos, ordenar los
   planos por su índice Z y comprobar dimensiones, planos ausentes o duplicados
   y calibración X/Y/Z. Los overlays y otros canales se mantienen fuera de la
   señal nuclear utilizada.
2. **Preparar la señal.** En las exportaciones RGB actuales, extraer la señal azul
   de visualización. Proponer y permitir corregir la exclusión del texto y la
   barra de escala. Mostrar el efecto de normalizar o submuestrear y actualizar
   la calibración cuando cambie la resolución de trabajo.
3. **Segmentar.** Producir propuestas por instancia y mostrar sus contornos sobre
   los planos de origen. El piloto parte de Cellpose en 2D; el modelo y sus
   parámetros podrán cambiar tras comparar resultados. La prueba de contraste
   debe incluir planos centrales y extremos tenues.
4. **Revisar.** Permitir guardar máscaras corregidas e incidencias: núcleos unidos,
   fragmentados, truncados por los bordes o afectados por una zona excluida.
   Una máscara automática queda identificada como propuesta hasta su revisión.
5. **Asociar entre capas.** Antes de medir un núcleo completo, establecer qué
   regiones de planos sucesivos pertenecen a la misma instancia. El piloto 2D
   puede ejecutarse por separado; sus IDs locales no se interpretan como
   identidades persistentes ni habilitan por sí solos medidas volumétricas.
6. **Medir y exportar.** Calcular las medidas usando coordenadas físicas y una
   máscara con identidad coherente en Z. Exportar las incidencias junto a cada
   instancia y distinguir las medidas admitidas para análisis de las que
   requieren revisión.

## Restricciones y supuestos

- Los archivos originales se leen sin modificarse. Las máscaras y resultados
  derivados se guardan separados de ellos.
- El espaciado entre planos se obtiene del XML; la barra visible y el DPI del
  TIFF no bastan para calcular volumen. Se respeta la anisotropía X/Y/Z.
- La geometría del scaffold no es necesaria para segmentar el núcleo. `G10`
  funciona como etiqueta mientras sus descriptores físicos no estén confirmados.
- Las exportaciones RGB de 8 bits limitan la información de intensidad disponible.
  Aumentar contraste puede amplificar ruido; cada transformación debe registrarse.
- Las zonas con anotaciones no contienen señal recuperable mediante exclusión.
  Un núcleo que las toque se marca para revisión.
- Actualmente no hay máscaras de referencia. Se preparará una selección manual
  revisada para evaluar segmentación y medición. No se atribuirán valores de
  Dice, IoU o exactitud a las propuestas sin esa referencia.
- Las capas de una pila y varios núcleos de una misma adquisición no se contarán
  automáticamente como réplicas experimentales independientes.
- Esta spec define el resultado funcional completo. La asociación entre capas y
  las medidas volumétricas son pasos pendientes posteriores al piloto 2D actual.

## Criterios de aceptación

| ID | Condición verificable |
|---|---|
| CV-01 | Una pila con índices Z desordenados por nombre se carga en orden numérico. Ante un plano ausente, duplicado, dimensiones incompatibles o calibración inválida, el flujo identifica el problema antes de exportar medidas físicas. |
| CV-02 | El registro identifica el canal nuclear y los archivos empleados. Los overlays y el segundo canal de `canales g10 2` no se contabilizan como muestras nucleares adicionales. |
| CV-03 | Cada máscara coincide con la forma de su imagen de trabajo, contiene etiquetas enteras y mantiene a cero las zonas excluidas. Si existe submuestreo, el registro permite localizarla en las coordenadas originales y recuperar su escala física. |
| CV-04 | Para una pila piloto se pueden inspeccionar la señal y los contornos en planos centrales y extremos, guardar una corrección y distinguir el resultado revisado de la propuesta automática. Las incidencias quedan vinculadas a la instancia afectada. |
| CV-05 | Un resultado de segmentación 2D independiente se identifica como tal. La exportación de volumen por núcleo solo se habilita al disponer de una máscara con asociación revisada entre capas. |
| CV-06 | Para una máscara de prueba con `N` vóxeles y calibración conocida, el volumen exportado coincide con `N × Δx × Δy × Δz`, salvo redondeo de presentación. Los ejes están ordenados, expresados en µm y las relaciones exportadas coinciden con los cocientes definidos. |
| CV-07 | La tabla permite recuperar para cada fila su pila, instancia, máscara, unidades y estado de calidad. Los núcleos truncados o pendientes de revisión aparecen señalados y pueden excluirse de los ejemplos destinados al predictor. |
| CV-08 | Cada ejecución guarda la configuración y la procedencia necesarias para repetirla. La evaluación sobre la futura referencia manual identifica los casos usados para ajustar parámetros y los usados para comprobarlos, y registra los errores observados sin presentar la revisión visual como una métrica de exactitud. |

## Decisiones pendientes

Concretar el método de asociación entre capas, cerrar los parámetros de contraste
y segmentación tras revisar los extremos tenues y seleccionar la referencia
manual. El piloto actual sirve para tomar estas decisiones; esta entrega no
presupone que ya estén implementadas o validadas.
