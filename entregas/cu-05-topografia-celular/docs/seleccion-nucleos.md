# Seleccionar núcleos en las nuevas pilas con μSAM

El anotador abre los TIFF originales directamente, a resolución nativa, sin
necesitar un lote Cellpose. Se trabaja con un núcleo por vez y se conservan
sus revisiones por separado. Las sesiones V2 del lote anterior siguen disponibles.

## Campaña del 23 de noviembre

Los índices de la campaña se generan en el equipo, en estas rutas:

- Serie de 7 µm en `output/segmentacion/microsam/campana-2026-11-23/7-um/indice.html`.
- Serie HDF de 30 µm en `output/segmentacion/microsam/campana-2026-11-23/30-um/indice.html`.

Dentro de cada serie, `surcos/` y `controles/` contienen una carpeta por pila.

Dentro de μSAM, pulsa **Guardar y siguiente núcleo** para pasar a un ID libre
en la misma pila. Para retomar uno guardado, selecciona su ID en **Núcleo para
retomar** y pulsa **Guardar y abrir ese núcleo**. Los contornos en ámbar marcan
los otros núcleos guardados. La exportación de tramos usa las paradas guardadas
a ambos lados de cada núcleo.

Para cambiar de pila, guarda el núcleo actual, cierra la ventana y abre la pila
de destino desde la carpeta del proyecto:

```bash
conda activate topografia-microsam
python -m topografia_celular.anotacion3d --pila 'control 2 raw' --modelo vit_l_lm \
  --salida output/segmentacion/microsam/campana-2026-11-23/7-um/controles/control-2-raw
python -m topografia_celular.anotacion3d --pila '8 um surcos raw 2' --modelo vit_l_lm \
  --salida output/segmentacion/microsam/campana-2026-11-23/7-um/surcos/7-um-surcos-raw-2
```

Ejecuta solo el comando de la pila que quieras abrir. Para retomarla en un ID
concreto, añade por ejemplo `--nucleo 4`. El primer arranque del control
calcula los embeddings de sus 86 cortes.

Para retomar la serie HDF de 30 µm, usa el canal `ch00` y la carpeta de la pila
correspondiente:

```bash
python -m topografia_celular.anotacion3d --pila '30 um HDF' --modelo vit_l_lm \
  --salida output/segmentacion/microsam/campana-2026-11-23/30-um/surcos/30-um-hdf
python -m topografia_celular.anotacion3d --pila 'control 30 um HDF' --modelo vit_l_lm \
  --salida output/segmentacion/microsam/campana-2026-11-23/30-um/controles/control-30-um-hdf
```

## Medir una profundidad común

El exportador toma la última máscara guardada por núcleo. Busca dos cortes
de parada, es decir, cortes con un solo punto negativo y ninguna caja. Los
incluye como límites exteriores. El intervalo útil comienza un corte después
de la primera parada y acaba un corte antes de la segunda.

```bash
python -m topografia_celular.tramos \
  --serie output/segmentacion/microsam/campana-2026-11-23/7-um \
  --profundidad-um 7 \
  --salida output/revision-3d/tramos-campana-2026-11-23/volumen-tramos-7um.csv
```

La ventana se centra en el punto medio del intervalo y suma el área de cada
corte por el espesor que representa dentro de la ventana. Así se puede pedir
la misma profundidad física con distinto paso Z. Si faltan paradas, hay un
hueco, la ventana no cabe o la máscara toca un borde XY dentro de ella, el CSV
deja el volumen vacío y explica el motivo.

La profundidad de 7 µm es la propuesta del piloto. El CSV conserva el estado
de revisión original. Una fila pendiente sirve para comprobar el cálculo y
tiene que revisarse antes de construir los pares del predictor por muestra.
Las dos columnas de desplazamiento prueban un corte antes y uno después,
manteniendo la profundidad. Si la ventana desplazada rebasa los límites
fiables o toca un borde XY, esa columna queda vacía.

## Empezar por la segunda pila de surcos

Desde la carpeta del proyecto, usa el comando de surcos de la campaña.

La primera carga calcula los embeddings de los 61 cortes de 1464 × 1464; la
ventana aparece cuando termina. Las siguientes aperturas reutilizan esa caché.
Se propone Z=38 como inicio por su señal media, sin segmentar automáticamente
ningún núcleo. Cada candidato puede necesitar otro corte inicial.

Las entradas conservan su nombre original de carpeta. Las salidas y la
etiqueta del visor usan **7 µm**, según confirmó el usuario.

`--modelo vit_l_lm` selecciona ViT-Large especializado en microscopía óptica;
`vit_b_lm` permite elegir ViT-Base. Al retomar sin `--modelo` se conserva el del
manifiesto. No se cambia el modelo de una preparación existente: para comparar
con otro, usar una `--salida` distinta. Las cachés se separan por huella de la
señal y modelo en `tmp/modelos/micro-sam/volumenes/<huella>/<modelo>/`.

1. Seleccionar `point_prompts` y colocar un positivo dentro de un único núcleo.
2. Pulsar **S** para segmentar el corte visible. **T** alterna entre puntos
   positivos y negativos. Los negativos ayudan a separar vecinos o fondo.
3. Usar **Segment All Slices [Shift-S]** para propagar ese objeto en Z.
4. Recorrer los cortes, corregir donde falle y revisar los dos extremos.
   Cuando el núcleo ya no aparezca, situarse en ese corte y pulsar
   **Marcar parada en este corte**; repetir en el otro extremo y volver a
   **Segment All Slices**. El botón añade un único negativo, como requiere μSAM,
   y no sustituye puntos o cajas que ya existan en ese Z. Varios
   puntos positivos de distintos núcleos no representan varios objetos en este
   flujo; todos los puntos actuales deben referirse al núcleo que se está trabajando.
5. En el panel superior, elegir **Revisión** y añadir una nota si procede:
   `pendiente`, `admitida` o `excluida`. La admisión es una decisión de revisión
   visual del usuario, no una validación automática del modelo.
6. Pulsar **Guardar V2 y vista 3D** para conservar el núcleo actual. Para pasar
   a otro, **Guardar y siguiente núcleo** guarda y limpia sus puntos, cajas y
   máscara. El modelo y los embeddings permanecen cargados.

La capa **Núcleos guardados** muestra en ámbar los contornos de la última
revisión de los demás núcleos de la pila. Sirve como referencia al recorrer Z
y se puede ocultar con el icono del ojo. Los puntos positivos y negativos
siguen actuando sobre el núcleo activo.

El panel muestra el estado del guardado. Si la máscara no se puede guardar,
el cambio de núcleo se cancela y las capas se conservan. **Guardar y abrir ese
núcleo** también guarda cuando el número elegido coincide con el actual.
Si solo se han puesto puntos sin obtener una máscara, hay que segmentar antes
de cambiar. En este flujo **C** guarda el núcleo actual; el control nativo
`Commit` queda oculto para no enviar el trabajo a una capa que no se exporta.

La máscara guardada usa los píxeles nativos. Las medidas y superficies utilizan
el espaciado de cada eje: aproximadamente Z=1 µm y XY=0,12613 µm en esta pila.
La interfaz mantiene índices de corte y píxeles para respetar los controles de
μSAM. Las coordenadas físicas son relativas al campo, no a la platina.

## Retomar o cambiar de núcleo

El mismo comando retoma el núcleo 1. Para abrir otro directamente,
añade por ejemplo `--nucleo 2` al comando de la pila, incluido su `--salida`.

Dentro de la ventana, indicar el número en **Núcleo para retomar** y pulsar
**Guardar y abrir ese núcleo**. Primero se conserva el actual y luego se carga
la última revisión completa del elegido. Si todavía no existe, queda vacío.
La etiqueta **Núcleo actual** indica a cuál pertenecen las siguientes indicaciones.

`--nueva` permite empezar de cero sobre el ID elegido conservando sus propuestas
anteriores; para un núcleo distinto, usar otro ID o el botón siguiente. No hay
autoguardado al cerrar: guardar antes de salir.

## Primera pila de surcos: solo overlay

```bash
python -m topografia_celular.anotacion3d --pila '8 um surcos raw' --senal azul-overlay --modelo vit_l_lm \
  --salida output/segmentacion/microsam/campana-2026-11-23/7-um/surcos/7-um-surcos-raw
```

Esta elección extrae explícitamente la componente azul del RGB. No combina
los otros colores ni los interpreta como señal nuclear. Se propone Z=13 y se
excluye la anotación inferior detectada: en los archivos actuales, la región
Y=998:1024, X=0:147. Comprobar que ningún núcleo elegido toque esa exclusión.

La pila tiene 49 cortes de 1024 × 1024, con XY≈0,18038 µm y Z≈1 µm. Su XML
identifica ALEXA 405 en azul; se conserva esa etiqueta, pendiente de confirmar
la tinción. El canal separado sería preferible para análisis posteriores.

La opción predeterminada `ch00` exige TIFF monocromos separados; si no existen,
se informa del problema y no se usa el overlay silenciosamente.

## Qué se guarda

```text
output/segmentacion/microsam/campana-2026-11-23/7-um/surcos/7-um-surcos-raw-2/
├── version-2.json                 # Fuentes, huellas y calibración
├── senal.tif                      # Copia nativa de la señal de trabajo
├── exclusion.tif
├── indice-3d.html                 # Última revisión de cada núcleo
├── medidas-nucleos.csv            # Una fila por ID, incluida revisión pendiente
├── medidas-admitidas.csv          # Solo revisión explícitamente admitida
└── nucleos/
    ├── nucleo-001/
    │   ├── propuesta-001/
    │   │   ├── mascara.tif        # Binaria y comprimida sin pérdida
    │   │   ├── medidas.json       # Volumen, diámetros equivalentes y procedencia
    │   │   ├── sesion.json        # Puntos, cajas, configuración y revisión
    │   │   ├── indice-3d.html
    │   │   └── superficie-3d.html
    │   └── propuesta-002/         # Corrección del mismo núcleo
    └── nucleo-002/                # Otro objeto
```

Las tablas se generan tras guardar el primer núcleo. Cada guardado crea una
propuesta nueva. Primero se conservan la máscara, las indicaciones y las
medidas; después se generan las vistas y el suavizado opcional. Si falla esa
segunda fase, el núcleo sigue siendo reanudable y su sesión indica la
exportación pendiente o el error, sin perder el original.
Las revisiones no se cuentan como nuevos objetos. Las medidas se calculan sobre
la máscara sin suavizar; la comparación suavizada, si se solicita, queda aparte.

En la prueba técnica real, un único positivo produjo una máscara que llegaba
a los 61 cortes. Ese resultado se conservó excluido en `tmp/experimentos/`,
sin incorporarlo a las medidas del proyecto. Las paradas y la revisión de los
extremos son necesarias; que la propagación termine no demuestra exactitud.

No se admite un objeto de un solo plano, con huecos Z o que toque los bordes del
volumen. También se impide admitir dos IDs con máscaras solapadas, para reducir
el riesgo de duplicar un núcleo. Estos controles no comprueban que el contorno
sea correcto: sigue siendo necesaria la revisión visual de toda la máscara.
Se puede guardar pendiente o excluido para conservar los casos problemáticos.

El usuario confirmó el 23 de noviembre de 2026 que ambas pilas de surcos son de
**7 µm**; los nombres originales `8 um surcos raw` y `8 um surcos raw 2` se
conservan para localizar los archivos. Falta precisar qué dimensión del patrón
describe ese valor. Los manifiestos existentes mantienen la medida nominal sin
asignar; la calibración del microscopio para medir los núcleos es independiente.

Más núcleos de un campo mejoran su descripción, pero no establecen independencia
experimental. Antes del few-shot habrá que agrupar por muestra y confirmar las
condiciones; esta fase guarda máscaras y medidas, no evalúa el predictor.

## Preparar sin abrir la ventana

Añade `--solo-preparar` al comando de la pila para validar y preparar la salida
sin cargar el visor.

`--z` elige un corte inicial, `--salida` una ubicación separada y `--cpu` permite
trabajar sin GPU. Las huellas de fuentes y preparados se verifican al reutilizar.
Los controles y la propagación corresponden al [anotador 3D oficial de μSAM](https://computational-cell-analytics.github.io/micro-sam/micro_sam/sam_annotator/annotator_3d.html).

## Organización de output

```text
output/
├── indice.html
├── LEEME.txt
├── inventarios/                   # Metadatos, importación e historial de traslados
├── notebooks/                     # Copias ejecutadas
├── revision-3d/cellpose-umbral-1-1/ # Vistas y medidas asociadas anteriores
└── segmentacion/
    ├── cellpose/                  # Lotes umbral-0-5 y umbral-1-1
    └── microsam/
        ├── v2/                    # Sesiones anteriores, sin alterar sus manifiestos
        ├── seleccion/             # Piloto anterior de selección de núcleos
        └── campana-2026-11-23/
            └── 7-um/              # Surcos y controles de la serie
```

Los tres accesos antiguos `segmentacion/umbral-0-5`, `umbral-1-1` y
`version-2-microsam` son enlaces de compatibilidad. Se conservan porque hay
sesiones anteriores que contienen esas rutas. El registro local
`output/inventarios/organizacion-2026-11-17.json` comprueba con SHA-256 que los
942 archivos previos conservan su contenido tras ordenarlos. `output/indice.html`
reúne los accesos a las vistas. Los ensayos técnicos permanecen en `tmp/experimentos/`.

## Si la ventana falla al iniciar OpenGL

En esta sesión, el entorno de ejecución heredaba `QT_XCB_GL_INTEGRATION=none`.
Para abrir la ventana se utilizó esta configuración solo para el proceso:

```bash
QT_QPA_PLATFORM=xcb QT_XCB_GL_INTEGRATION=xcb_glx PYOPENGL_PLATFORM=glx \
  python -m topografia_celular.anotacion3d --pila '8 um surcos raw 2' \
  --salida output/segmentacion/microsam/campana-2026-11-23/7-um/surcos/7-um-surcos-raw-2
```

No modifica la configuración global del equipo. La documentación de
[μSAM](https://computational-cell-analytics.github.io/micro-sam/)
describe también los problemas de contexto OpenGL al usar XWayland.

## Memoria y recuperación

El suavizado mantiene el método, sigma, espaciado y resolución nativa. Calcula
las distancias en un recorte del núcleo con margen para todo el soporte del
filtro, y devuelve la máscara en la rejilla completa. Se comprobó sobre el primer
núcleo guardado que el resultado coincide vóxel a vóxel con el cálculo anterior.
Las superficies también evitan ordenar una copia de todo el volumen para
identificar etiquetas. Las máscaras suavizadas nuevas se comprimen sin pérdida.

Antes de reservar las matrices del suavizado se estima su memoria de trabajo.
Si no hay margen suficiente, se conserva el original y se registra que no se
pudo completar ese derivado. No se baja la resolución ni se cambia sigma para
hacerlo caber silenciosamente.

La ventana recuperada se lanzó en una sesión de proceso independiente, con
entrada estándar desconectada y registro en `tmp/experimentos/`, para que no
dependa de mantener un comando de terminal esperando en el chat.
