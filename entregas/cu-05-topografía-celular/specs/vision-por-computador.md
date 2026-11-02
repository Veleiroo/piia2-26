# Visión por computador: segmentación y medición nuclear

## Qué construir y para qué

Un flujo reproducible que reciba una pila de microscopía con señal nuclear DAPI,
obtenga máscaras por instancia que puedan revisarse y exporte medidas geométricas
de los núcleos. Estas medidas permitirán describir las muestras y construir las
respuestas observadas de los ejemplos del [módulo LLM](integracion-llm-few-shot.md).

Medir el núcleo que aparece en una imagen es un paso previo a predecir su forma
desde la topografía. La funcionalidad debe conservar la relación entre imagen,
máscara, medida y muestra para poder revisar incidencias o medidas dudosas.

## Entradas y salidas

**Entradas:** carpeta de una pila TIFF, XML de adquisición, identificador de pila
y configuración de procesamiento. La configuración recoge el canal, los planos
seleccionados, el muestreo, la normalización, las zonas excluidas y los parámetros
de segmentación. Se admiten las exportaciones actuales, aunque incluyan anotaciones.

**Salidas:**

- Máscaras de etiquetas enteras: `0` para fondo e identificadores positivos para
  las instancias. Se conserva la propuesta automática y, si se modifica, una
  versión revisada diferenciada.
- Una tabla con una fila por núcleo medido, con identificador de pila e instancia, volumen en
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
   regiones de planos sucesivos pertenecen al mismo núcleo y asignarles un
   identificador común para toda la pila. Revisar las asociaciones dudosas,
   especialmente cuando aparecen uniones, fragmentaciones o señal tenue.
6. **Medir y exportar.** Calcular las medidas usando coordenadas físicas y una
   máscara con identidad coherente en Z. Exportar las incidencias junto a cada
   instancia y distinguir las medidas admitidas para análisis de las que
   requieren revisión.

## Restricciones y supuestos

- Los archivos originales se leen sin modificarse. Las máscaras y resultados
  derivados se guardan separados de ellos.
- El espaciado entre planos se obtiene del XML; la barra visible y el DPI del
  TIFF no bastan para calcular volumen. Se respeta la anisotropía X/Y/Z.
- La segmentación no requiere conocer la posición o la geometría completa del
  scaffold. Su tipo de patrón y medida nominal se conservan como metadatos para
  asociarlos después con las medidas nucleares y construir los ejemplos del LLM.
- Las exportaciones RGB de 8 bits limitan la información de intensidad disponible.
  Aumentar contraste puede amplificar ruido; cada transformación debe registrarse.
- Las zonas con anotaciones no contienen señal recuperable mediante exclusión.
  Un núcleo que las toque se marca para revisión.
- Actualmente no hay máscaras de referencia. La calidad de la segmentación se
  revisará visualmente y se registrarán los fallos observables. Esa revisión no
  permite cuantificar la exactitud ni convertir las máscaras en ground truth.
  Si más adelante se dispone de anotaciones de referencia adecuadas, podrá
  plantearse una evaluación cuantitativa; no es un requisito del alcance actual.
- Las capas de una pila y varios núcleos de una misma adquisición no se contarán
  automáticamente como réplicas experimentales independientes.

## Del piloto por capas a las medidas del núcleo completo

El piloto actual usa Cellpose para segmentar cada plano XY de forma independiente.
Produce una máscara por capa, con identificadores locales: el objeto con ID `1`
en una capa no tiene por qué ser el mismo núcleo que el objeto con ID `1` en la
siguiente. Apilar esas máscaras sin asociar sus objetos no permite identificar
qué vóxeles pertenecen a cada núcleo completo.

El siguiente paso consiste en relacionar las regiones que corresponden al mismo
núcleo a lo largo de Z y reunirlas bajo un único identificador. Con esa máscara
por núcleo y la calibración X/Y/Z se podrán calcular el volumen y los ejes.
La asociación y esas medidas están previstas en esta spec, pero todavía no están
resueltas en el piloto. Se puede partir de las máscaras 2D de Cellpose; este paso
no exige utilizar un modelo de segmentación 3D.

## Criterios de aceptación

Para comprobar que esta parte funciona, revisaremos lo siguiente:

1. **Las capas se cargan en el orden correcto.** Se ordenan por su posición Z,
   aunque los nombres de archivo no aparezcan ordenados. Si falta una capa, está
   duplicada o hay problemas con las dimensiones o la escala física, el programa
   avisa antes de calcular medidas.

2. **Se utiliza la señal del núcleo.** Los metadatos permiten identificar el canal
   DAPI y se guarda qué archivos se han utilizado. Las imágenes que combinan
   varios canales y el segundo canal de `canales g10 2` no se cuentan como nuevas
   muestras nucleares.

3. **Las máscaras encajan con las imágenes.** Tienen las mismas dimensiones que
   la imagen procesada y usan `0` para el fondo y números distintos para los
   objetos detectados. Las zonas de texto y barras de escala que hayamos excluido
   quedan fuera de las máscaras. Si reducimos la resolución, se conserva la
   información necesaria para relacionar el resultado con la imagen original.

4. **Podemos revisar y corregir el resultado.** En una pila piloto se muestran
   los contornos sobre las imágenes, tanto en las capas centrales como en los
   extremos con menos señal. Se puede guardar una corrección sin perder la
   máscara automática y dejar anotados los problemas encontrados.

5. **Cada núcleo mantiene su identidad entre capas antes de medir su volumen.**
   Las regiones asociadas al mismo núcleo comparten un identificador en toda la
   pila. Mientras solo tengamos máscaras independientes por capa, el resultado
   se presenta como segmentación 2D y no se exportan volúmenes por núcleo.

6. **Los cálculos respetan las dimensiones físicas.** Con una máscara de prueba
   y una escala conocidas, comprobamos que el volumen coincide con el número de
   vóxeles multiplicado por `Δx × Δy × Δz`. Los ejes se expresan en µm, se ordenan
   de mayor a menor y sus relaciones coinciden con `a/b` y `b/c`. Esto comprueba
   los cálculos; no demuestra que las máscaras de las imágenes reales sean exactas.

7. **Cada medida se puede relacionar con su núcleo de origen.** La tabla contiene
   una fila por núcleo, con su pila, identificador, máscara y medidas con unidades.
   Se señalan los núcleos cortados por el borde y los que necesitan revisión,
   para poder excluirlos de los ejemplos del predictor.

8. **Queda guardado cómo se obtuvo el resultado.** Se conservan el modelo y su
   versión, los parámetros, la escala, las zonas excluidas y las correcciones.
   La revisión indica qué imágenes se han inspeccionado y qué fallos se han
   observado. Al no disponer de ground truth, no se calculan Dice, IoU ni una
   tasa de error de segmentación.

## Decisiones pendientes

Antes de completar esta parte tenemos que decidir:

- **Cómo relacionar las máscaras entre capas:** elegir cómo reconocer que dos
  regiones de capas sucesivas pertenecen al mismo núcleo y cómo revisar los
  casos dudosos.
- **Qué ajustes de imagen y de Cellpose usaremos:** comparar las opciones de
  contraste y los parámetros de segmentación, especialmente en las capas con
  poca señal, y guardar la configuración elegida.
- **Cómo haremos las correcciones:** elegir una forma de editar las máscaras,
  guardar los cambios y marcar los núcleos que sigan siendo dudosos.
