---
description: Script que procesa 40 imágenes del dataset con el modelo de GROQ_MODEL y mide acierto en clasificación, JSON válidos, latencia y coste para confirmar o descartar el modelo.
state: Pendiente
---

# Spec — Prueba del modelo de Groq

## Qué construir
Tres piezas, en este orden:

1. **Temperatura fija en el cliente.** `ModelClient` envía `temperature=0` en todas sus llamadas.
2. **Tubería de un documento** en `src/procesamiento_documental/pipeline.py`: `process_document(client, image_data_url) -> DocumentResult`. Hace dos llamadas en serie:
   1. **Clasificación** con `client.classify()`: tipo `bill` o `discharge_summary`.
   2. **Extracción** con `client.extract()` y el tipo obtenido, que elige el esquema (`src/Hospital_Bill.json` o `src/Discharge_Summary.json`). La respuesta se valida con `validate_extraction()` de `specs/validacion-extraccion.md`.

   `DocumentResult` guarda el tipo predicho, las dos `ModelResponse` (o `None` si la llamada no se hizo o falló), el `ValidationResult` (o `None` si la extracción no se hizo o falló) y, si algo falló, el error y la etapa (`classification` o `extraction`). Ningún fallo del modelo sale como excepción. La app de `specs/prototipo-streamlit.md` reutiliza esta función.
3. **Script** `script/prueba_modelo.py`, que elige la muestra, llama a `process_document()` por cada imagen, guarda un CSV en `output/` e imprime un resumen.

Lo que ya existe y se reutiliza sin cambios: `load_dataset()`, `sample_documents()` e `image_to_data_url()` de `ingesta.py`, los prompts de `prompts.py` y los reintentos de `cliente.py`.

## Por qué
El modelo candidato (`qwen/qwen3.8-27b`) está en *preview* y solo se ha probado con una imagen. En esa prueba clasificó bien 5 de 5 veces, pero la extracción solo devolvió un JSON válido 2 de 5 veces. Antes de construir la app sobre él hay que medir, con una muestra, si lee nuestros documentos y devuelve un JSON utilizable en un tiempo y con un coste razonables.

## Restricciones
- Muestra: `sample_documents(load_dataset(), per_type=20, seed=42)`, es decir, 20 imágenes de cada tipo.
- El script solo orquesta y escribe resultados. Las llamadas, la tubería y la validación viven en `src/`.
- La clave y el modelo se leen de `GROQ_API_KEY` y `GROQ_MODEL`. El script carga `.env` con `python-dotenv`. El nombre del modelo no aparece en el código.
- Los 429, los fallos de conexión y los 5xx los reintenta el cliente, como ya hace. Un 400 `json_validate_failed` no se reintenta: cuenta como JSON no válido, porque es justo lo que se mide. Reintentarlo una vez queda descartado para esta medición, porque ocultaría la tasa de fallos del modelo; si las cifras lo justifican, se planteará después, con `temperature=0` ya fijada.
- Si la clasificación falla (error de la API o tipo inválido), no se hace la extracción y la fila queda marcada con el error.
- Un error en una imagen no detiene el script: se anota en su fila y se sigue con la siguiente. Solo se detiene si faltan las variables de entorno.
- El precio por millón de tokens de entrada y de salida, en USD, se pasa como argumento (`--precio-entrada`, `--precio-salida`), porque depende del modelo y Groq lo cambia.
- Solo lee de `data/raw/`.
- Queda fuera comparar los valores extraídos con la verdad de referencia: depende de cómo se puntúen los campos que no aparecen en la imagen, que se decidirá en un ADR aparte.

## Criterios de aceptación
- `_client()` y `_completion()` pasan de `tests/test_cliente.py` a `tests/conftest.py`, y los dos ficheros de test los usan desde ahí.
- `tests/test_pipeline.py`, sin red (con ese transporte simulado), comprueba que:
  - las peticiones a Groq llevan `temperature` 0;
  - una clasificación inválida devuelve un `DocumentResult` con el error en la etapa `classification` y sin llamada de extracción;
  - un 400 `json_validate_failed` en la extracción devuelve un `DocumentResult` con el error en la etapa `extraction`, sin lanzar excepción;
  - una extracción correcta devuelve el tipo, las dos respuestas y una validación con `is_valid` verdadero.
- El script se ejecuta con un solo comando, documentado al principio del fichero y en `README.md`:
  `python script/prueba_modelo.py --precio-entrada <USD/M> --precio-salida <USD/M>`.
- Deja en `output/prueba_modelo_<AAAAMMDD-HHMM>.csv` 40 filas, una por imagen, con estas columnas: `filename`, `real_type`, `predicted_type`, `json_valid`, `error_stage`, `error`, `classification_latency_s`, `extraction_latency_s`, `input_tokens` y `output_tokens` (suma de las dos llamadas), `attempts` (suma de las dos llamadas), `missing_fields` (rutas separadas por `;`) y `extraction_raw` (el texto de la extracción o, si Groq la rechazó con un 400 que trae `failed_generation`, ese texto). `json_valid` es el `is_valid` de la validación contra el esquema del tipo predicho, aunque la clasificación se haya equivocado; si no hubo validación, `False`.
- Imprime un resumen con: el modelo de `GROQ_MODEL` y `PROMPT_VERSION`; el acierto en clasificación (aciertos/40 y %); el porcentaje de JSON válidos sobre 40; la latencia media y p95 por imagen (suma de las dos llamadas, solo imágenes con las dos llamadas correctas); el número de errores por etapa; y el coste estimado en USD de la muestra y extrapolado a las 1000 imágenes.
- El modelo se da por **confirmado** si el acierto en clasificación es ≥ 95 % (38/40), los JSON válidos son ≥ 90 % (36/40) y la latencia p95 por imagen es ≤ 10 s. Si no, queda **descartado** para la app.
- El resultado, con las cifras del resumen, la fecha y el nombre del modelo, queda anotado en la sección «Tecnologías» de `README.md`.
- `python -m pytest`, `ruff check .` y `ruff format --check .` en verde.
