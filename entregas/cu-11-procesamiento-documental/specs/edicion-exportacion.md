---
description: Edición y validación humana de las entidades en la app, y exportación del resultado a JSON, CSV y Excel.
state: Pendiente
---

# Spec — Edición, validación humana y exportación

## Qué construir
Dos ampliaciones de la app de `specs/prototipo-streamlit.md`, con su lógica en `src/`:

1. **Edición y validación humana.** Las tres tablas de resultados (`campos`, `procedimientos`, `medicamentos`) pasan a ser editables con `st.data_editor`. En `procedimientos` y `medicamentos` se pueden añadir y borrar filas. La columna `campo` no se edita. Tras cada cambio, la app reconstruye el JSON y lo vuelve a validar contra el esquema. Un botón «Marcar como validado» queda activo solo si el JSON editado es válido, y guarda en `st.session_state` que una persona lo ha revisado. Cualquier edición posterior vuelve a dejarlo como no validado.
2. **Exportación.** Tres `st.download_button`, activos solo si el JSON editado es válido, que descargan el resultado como se indica abajo. `<imagen>` es el nombre del fichero subido sin la extensión.
   - **JSON** (`<imagen>_entidades.json`): un objeto con `source_file`, `document_type`, `validated_by_human` (`true` o `false`) y `entities`, que es el JSON editado tal cual lo define el esquema.
   - **CSV** (`<imagen>_entidades.csv`): dos columnas, `campo` y `valor`, con una fila por valor del JSON y la notación de ruta de `missing_fields` (`patient.name`, `procedures[0].cpt`, `medications[1]`).
   - **Excel** (`<imagen>_entidades.xlsx`): una hoja por tabla (`campos`, `procedimientos`, `medicamentos`).

En `src/procesamiento_documental/` se añaden:
- en `tablas.py`, `tables_to_entities(document_type, tables) -> dict`, la inversa de `entities_to_tables()`. Convierte cada celda al tipo que pide el esquema: una celda vacía pasa a `null` y un número escrito como texto pasa a número. Una tabla de `procedimientos` o `medicamentos` sin filas vuelve como `null`, como pide el ADR de esquemas, nunca como `[]`. Si un valor no se puede convertir, se deja como texto para que la validación lo marque;
- un módulo `exportacion.py` con `to_json_bytes()`, `to_csv_bytes()` y `to_excel_bytes()`, que devuelven el contenido del fichero en bytes, sin escribir en disco.

## Por qué
Es uno de los objetivos fijados. El modelo se equivoca en algunos campos (por ejemplo, quitó el prefijo `MRN-` en la primera prueba). La persona usuaria tiene que poder corregirlo antes de exportar, y el fichero exportado tiene que decir si alguien lo ha revisado.

## Restricciones
- Aplica `decisions/interfaz-streamlit.md`: la conversión entre tablas y JSON, la validación y la generación de los ficheros viven en `src/`. `app.py` solo coloca los componentes.
- Aplica `decisions/esquemas-extraccion-documental.md`: lo exportado conserva los nombres de campo del esquema, todas sus claves obligatorias y `null` donde no hay dato.
- La validación es la de `validate_extraction()` de `specs/validacion-extraccion.md`; no se escribe otra.
- Los códigos como `cpt` o `npi` se tratan siempre como texto, para no perder los ceros a la izquierda (`"0260"`).
- Editar no vuelve a llamar a Groq.
- Queda fuera: las preguntas sobre el documento, exportar varios documentos en un mismo fichero y guardar los ficheros en el servidor.

## Criterios de aceptación
- `tests/test_tablas.py` comprueba, sin red, que:
  - `tables_to_entities(t, entities_to_tables(x)) == x` para una factura y un informe de alta de ejemplo, con `t` igual al tipo de cada uno. Los ejemplos usan `null`, no `[]`, para las listas sin datos;
  - una tabla de `medicamentos` sin filas vuelve como `medications: null`;
  - una celda vacía se convierte en `null`;
  - `financials.total_charges` escrito como `"1508"` se convierte en `1508`;
  - un `price` escrito como `"abc"` hace que la validación falle con un error que nombra `procedures[0].price`.
- `tests/test_exportacion.py` comprueba, sin red y sin escribir fuera de un directorio temporal, que:
  - el JSON exportado se parsea, `validated_by_human` refleja el estado y `entities` pasa `validate_extraction()`;
  - el CSV tiene la cabecera `campo,valor` y una fila `procedures[0].cpt` con el valor `0260`. El test lee el CSV con el módulo `csv` (o con `pandas.read_csv(..., dtype=str)`), para que el cero no se pierda al leer;
  - el Excel se abre con `pandas.read_excel` y tiene las hojas `campos`, `procedimientos` y `medicamentos` con el mismo número de filas que las tablas de origen.
- Prueba manual con la API real, anotada en el PR: con `med_doc_bill_100001_noisy.jpg`, corregir `patient.mrn` a `MRN-1039485`, marcar como validado, descargar los tres ficheros y comprobar que los tres llevan el valor corregido y que el JSON lleva `validated_by_human: true`. Después, editar otro campo y comprobar que el JSON descargado de nuevo lleva `validated_by_human: false`.
- `python -m pytest`, `ruff check .` y `ruff format --check .` en verde.
