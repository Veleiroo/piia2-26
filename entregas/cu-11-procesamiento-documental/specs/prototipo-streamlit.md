---
description: Primera versión de app.py en Streamlit que carga una imagen JPEG, la procesa con la tubería de src/ y muestra el tipo y las entidades extraídas.
state: Pendiente
---

# Spec — Prototipo base en Streamlit

## Qué construir
La primera versión de la app, `app.py` en la raíz del repositorio, con una sola página:

1. **Barra lateral:** el modelo en uso (valor de `GROQ_MODEL`).
2. **Carga:** un `st.file_uploader` que acepta un único fichero `.jpg` o `.jpeg`.
3. **Inspección:** la imagen cargada, a ancho completo de la columna.
4. **Procesamiento:** un botón «Procesar» que llama a `process_document()` de `specs/prueba-modelo-groq.md` con un spinner mientras espera.
5. **Resultados:**
   - el tipo de documento predicho;
   - si el JSON es válido (`st.success`) o no (`st.warning`, con los errores de la validación);
   - la lista de campos ausentes;
   - tres tablas: campos (`campo`, `valor`), procedimientos (`desc`, `cpt`, `price`) y medicamentos (`medicamento`);
   - la latencia y los tokens de cada llamada;
   - el JSON en bruto, dentro de un `st.expander`.

La conversión del JSON a tablas vive en `src/procesamiento_documental/tablas.py`, en una función `entities_to_tables(data: dict) -> dict[str, pandas.DataFrame]` que devuelve las tablas `campos`, `procedimientos` y `medicamentos`. La de campos tiene una fila por cada valor que no está en `procedures` ni en `medications`, con la misma notación de ruta que `missing_fields` (`patient.name`, `financials.total_charges`). Los campos `null` también tienen fila, con el valor vacío, para que la edición de `specs/edicion-exportacion.md` pueda rellenarlos. Las otras dos tienen una fila por elemento de su lista.

Si la validación devuelve `data` igual a `None`, no se muestran tablas: solo los errores y el JSON en bruto. Si `data` es un objeto pero no cumple el esquema, las tablas se muestran igual, junto con los errores. La edición y la exportación de `specs/edicion-exportacion.md` reutilizarán esta función.

## Por qué
Es uno de los objetivos impuestos: crear la interfaz principal, el componente de carga e inspección de imágenes y conectarla con la API para mostrar los resultados. SDG pidió ver los resultados en tabla. Sobre esta app se construyen después la edición, la exportación y las preguntas sobre el documento.

## Restricciones
- Aplica `decisions/interfaz-streamlit.md`: `app.py` solo contiene presentación. No importa `groq` ni `jsonschema`, y no construye prompts ni valida JSON: todo eso lo hace a través de `procesamiento_documental`.
- La app carga `.env` con `python-dotenv` y crea el cliente con `ModelClient.from_env()` una sola vez (`st.cache_resource`).
- La imagen subida pasa a `image_to_data_url()` con sus bytes y no se guarda en disco.
- El resultado se guarda en `st.session_state` para que no se pierda al repetirse el script. Subir otra imagen borra el resultado anterior.
- Ningún error muestra una traza de Python en pantalla:
  - si faltan `GROQ_API_KEY` o `GROQ_MODEL`, un `st.error` dice qué variable configurar y la carga queda desactivada;
  - si el fichero no es un JPEG, un `st.error` lo dice. Se comprueba por el contenido, no por la extensión: los tres primeros bytes deben ser `FF D8 FF`. La comprobación es una función `is_jpeg(image: bytes) -> bool` de `ingesta.py`;
  - si la tubería devuelve un error, se muestra con su etapa (clasificación o extracción).
- Queda fuera de esta spec: editar los resultados, exportarlos, las preguntas sobre el documento, procesar varias imágenes a la vez y aceptar formatos distintos de JPEG.

## Criterios de aceptación
- `streamlit run app.py` arranca la app sin errores en la consola.
- `tests/test_tablas.py` comprueba, sin red, que `entities_to_tables()` con una factura de ejemplo de 3 procedimientos y 2 medicamentos devuelve 3 filas en `procedimientos`, 2 en `medicamentos`, y una tabla `campos` que incluye `patient.name` y `financials.total_charges` pero ninguna fila de `procedures` ni de `medications`. Con `procedures: null`, la tabla de procedimientos está vacía y conserva sus tres columnas.
- `tests/test_ingesta.py` comprueba que `is_jpeg()` acepta los bytes de un JPEG y rechaza los de un PNG y un fichero vacío.
- `tests/test_app.py` usa `streamlit.testing.v1.AppTest` sin red y comprueba que la app arranca sin excepciones y que, sin `GROQ_API_KEY`, muestra un `st.error` que nombra la variable. Para que no lea el `.env` de la máquina, el test parchea `dotenv.load_dotenv` y borra `GROQ_API_KEY` y `GROQ_MODEL` con `monkeypatch`.
- `app.py` no contiene `import groq` ni `import jsonschema` (comprobable con `ruff check` y una búsqueda en el fichero).
- Prueba manual con la API real, anotada en el PR:
  - con `data/raw/Data/bills/med_doc_bill_100001_noisy.jpg`, la app muestra el tipo `bill`, el hospital «Lilavati Hospital», el nombre de paciente «Amit Singh» y 5 procedimientos;
  - con cualquier informe de `data/raw/Data/discharge_summaries/`, muestra el tipo `discharge_summary` y una fila `hospital_course` en la tabla de campos;
  - con `GROQ_MODEL` apuntando a un modelo que no existe, la app muestra el error con la etapa «clasificación» y sin traza de Python;
  - un fichero PNG renombrado a `.jpg` muestra el `st.error` de «no es un JPEG».
- `README.md` documenta cómo lanzar la app.
- `python -m pytest`, `ruff check .` y `ruff format --check .` en verde.
