# Interfaz de subida y selección de variables

## Qué construir

Una aplicación web sencilla (Streamlit) que es la puerta de entrada del usuario
final al sistema. Permite:

1. **Subir un artículo:** un PDF obligatorio y, opcionalmente, uno o varios
   ficheros de material suplementario (PDF o DOCX).
2. **Elegir las variables:** una lista con las 23 variables agrupadas en sus tres
   bloques (impresión, tinta, dosis), con casillas para marcarlas una a una y un
   botón por bloque para marcar o desmarcar todo el bloque. Cada variable muestra
   su nombre legible y una descripción corta (por ejemplo, *"Diámetro de
   boquilla: diámetro del orificio por donde sale la gota, en µm"*).
3. **Lanzar la extracción:** un botón que envía los ficheros y las variables al
   orquestador (spec `extraccion-por-agentes-especialistas`) y muestra en qué
   punto está (enviando los ficheros, agente de impresión, agente de tinta, agente
   de dosis, terminado).
4. **Ver el resultado:** una tabla con una fila por caso (formulación o
   montaje de impresión) y estas columnas por variable: dato, valor,
   unidad, origen (artículo, suplementario, calculado) y de dónde sale
   (la frase literal del artículo y su sección o tabla). Los valores `"NR"` se
   muestran como "No reportado" y en un color distinto.
5. **Descargar:** el resultado en CSV y en JSON.

**Dónde encaja.** Es la última pieza de la cadena (fase 5): no extrae nada por
sí misma, solo recoge la entrada del usuario, llama al orquestador y presenta su
salida. Corresponde exactamente al ejemplo del documento de planteamiento: "subo
un artículo, marco qué datos quiero y recibo una tabla con cada dato y la frase
de donde sale".

## Por qué

- Las personas que van a usar el sistema son investigadoras de farmacia, no
  programadoras. Sin interfaz, usarlo exige abrir una terminal y editar
  ficheros, que es justo el trabajo manual que queremos quitar.
- No siempre hacen falta las 23 variables. Elegir solo las necesarias ahorra
  tiempo y coste, porque el orquestador solo lanza los agentes de los bloques
  marcados.
- Mostrar la frase de origen junto a cada valor permite a la investigadora
  validar o descartar un dato sin volver a leer el artículo entero. Es lo que
  hace que se pueda confiar en la tabla.
- Exportar a CSV permite pegar los resultados directamente en la hoja con la que
  se entrenan los modelos, que es el fin último del proyecto.

## Restricciones

- **Tecnología:** Streamlit, en Python, para compartir lenguaje con el resto del
  sistema. Se ejecuta en local con `streamlit run app.py`; el despliegue en un
  servidor público queda fuera del alcance.
- **Ficheros aceptados:** artículo en PDF de como máximo 50 MB; suplementarios
  en PDF o DOCX, como máximo 5 ficheros y 50 MB cada uno. Cualquier otro formato
  o tamaño se rechaza antes de llamar al orquestador, con un mensaje que dice
  qué fichero falla y por qué.
- **PDF sin texto:** si el PDF es una imagen escaneada y no se puede extraer texto
  (menos de 500 caracteres extraídos), se avisa al usuario y no se lanza la
  extracción. El OCR queda fuera del alcance.
- **Al menos una variable:** el botón de extraer está desactivado mientras no haya
  ninguna variable marcada. Por defecto vienen marcadas las 23.
- **Sin lógica de extracción en la interfaz:** la interfaz no llama al LLM ni hace
  cálculos; todo pasa por el orquestador. Así, cambiar los agentes no obliga a
  tocar la interfaz.
- **Privacidad:** los ficheros subidos se guardan en una carpeta temporal de la
  sesión y se borran al cerrarla; no se guardan en el repositorio.
- **Idioma:** la interfaz está en español; los nombres internos de las variables
  (`Nozzle_diameter`...) se muestran junto al nombre legible para que coincidan
  con el Excel del estudio.
- **Fuera del alcance:** cuentas de usuario, procesar varios artículos a la vez
  desde la interfaz y editar los valores en la tabla.

## Criterios de aceptación

1. **Subida válida:** al subir el PDF del artículo 1 (Genina) la aplicación
   muestra su nombre y número de páginas y activa la selección de variables.
2. **Rechazo de formatos:** al subir un `.xlsx` como artículo, o un PDF de más de
   50 MB, aparece un mensaje de error que nombra el fichero y el motivo, y el
   orquestador no recibe ninguna llamada (se comprueba en el log).
3. **PDF sin texto:** al subir un PDF escaneado de prueba (incluido en
   `tests/datos/`) aparece el aviso de "no se ha podido leer texto" y no se lanza
   la extracción.
4. **Selección por bloque:** pulsar "desmarcar bloque" en impresión deja
   desmarcadas exactamente sus 11 variables y el contador muestra 12/23
   seleccionadas.
5. **Botón bloqueado:** con 0 variables marcadas, el botón "Extraer" está
   desactivado.
6. **Solo lo pedido:** si se marca solo `Printed_drug_dose`, la tabla de resultado
   contiene solo esa variable y el log muestra que solo se ejecutó el agente de
   dosis.
7. **Tabla completa:** para el artículo 1 con las 23 variables, cada valor que no
   es "No reportado" tiene relleno el campo "de dónde sale" (100 % de las celdas).
8. **Coherencia con el backend:** el CSV descargado contiene exactamente los
   mismos valores que el JSON que devuelve el orquestador para esa ejecución
   (comparación automática en un test: 0 diferencias).
9. **CSV utilizable:** el CSV se abre en Excel y en pandas
   (`pd.read_csv`) sin errores, con una fila por caso y columnas
   `variable_valor`, `variable_unidad`, `variable_origen`, `variable_evidencia`.
10. **Progreso visible:** durante la extracción la pantalla muestra en todo
    momento el paso actual, y al terminar muestra el tiempo total y el coste de esa
    ejecución.
11. **Tiempo propio de la interfaz:** sin contar lo que tarda el orquestador, la
    interfaz tarda menos de 2 segundos en mostrar la tabla una vez recibida la
    respuesta (medido con un orquestador simulado que responde al instante).
12. **Limpieza:** después de cerrar la sesión, la carpeta temporal de esa sesión
    ya no existe.
