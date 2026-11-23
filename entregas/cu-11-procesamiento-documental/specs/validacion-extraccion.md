---
description: Módulo de src/ que valida el JSON de extracción contra el esquema de su tipo y lista los campos ausentes.
state: Pendiente
---

# Spec — Validación del JSON de extracción

## Qué construir
Un módulo `src/procesamiento_documental/validacion.py` con una función:

```python
validate_extraction(document_type: str, content: str) -> ValidationResult
```

Recibe el texto en bruto que devuelve `ModelClient.extract()` (`ModelResponse.content`) y dice si es utilizable:

1. Parsea el texto como JSON.
2. Lo valida contra el esquema del tipo documental, leído con `load_extraction_schema()` de `cliente.py`, con JSON Schema Draft 2020-12 y comprobación de formatos (`"format": "date"` exige `AAAA-MM-DD`).
3. Lista los campos ausentes: la ruta de cada campo cuyo valor es `null` o una lista vacía, incluidos los anidados (`patient.dob`, `medications`, `procedures[2].cpt`) y los elementos `null` de una lista (`medications[0]`).

`ValidationResult` es una dataclass inmutable con:

| Campo | Tipo | Contenido |
|---|---|---|
| `is_valid` | `bool` | `True` si el JSON se parsea y cumple el esquema |
| `data` | `dict \| None` | El JSON parseado; `None` si el texto no es JSON o no es un objeto |
| `errors` | `list[str]` | Un mensaje por error; vacía si es válido |
| `missing_fields` | `list[str]` | Rutas de los campos ausentes, en el orden de las claves del JSON. Se calcula siempre que `data` no sea `None`, aunque el JSON sea inválido |

Cada mensaje de `errors` empieza por la ruta del campo, con la misma notación que `missing_fields`, seguida de `: ` y el motivo (`financials.total_charges: '1508' is not of type 'number'`). Si falta o sobra una clave, la ruta es la de esa clave (`insurance`, `notes`), no la del objeto que la contiene. Si el texto no es JSON o no es un objeto, el mensaje no lleva ruta.

## Por qué
`ARCHITECTURE.md` prevé un componente de validación y todavía no existe. Las primeras pruebas mostraron que el modo `json_schema` estricto de Groq no basta: el modelo genera salidas degeneradas, y una respuesta no debe darse por buena solo por haber pedido salida estructurada. Además, tres piezas necesitan la misma definición de «JSON válido» y de «campo ausente»: el script de `specs/prueba-modelo-groq.md`, la app de `specs/prototipo-streamlit.md` y la evaluación.

## Restricciones
- Aplica `decisions/esquemas-extraccion-documental.md`: todas las claves obligatorias, `null` si no hay dato y ninguna propiedad adicional. Una respuesta con propiedades no definidas es inválida.
- Los esquemas se leen con `load_extraction_schema()`; no se copian ni se modifican.
- Usa la librería `jsonschema` (`Draft202012Validator` con `FormatChecker`). Se añade a `dependencies` de `pyproject.toml` con su versión mínima.
- Solo informa: no corrige, no rellena ni elimina campos del JSON.
- Una respuesta mala del modelo nunca lanza una excepción: devuelve `is_valid=False` con el motivo en `errors`. Un `document_type` desconocido sí lanza `ValueError`, porque es un error de programación.
- Una lista vacía cuenta como campo ausente, pero no es un error: el modelo devuelve `[]` donde el ADR pide `null`. Unificarlo en el prompt queda fuera de esta spec.
- No llama a Groq ni cambia `cliente.py` ni `prompts.py`.

## Criterios de aceptación
- `tests/test_validacion.py` cubre, sin red y sin leer `data/raw/`, al menos estos casos con `bill`. Los JSON de ejemplo se escriben en el test a partir del esquema, no se copian del CSV de verdad de referencia: el de facturas trae `hospital_course`, que el esquema de `bill` no admite.
  1. Un JSON completo y correcto: `is_valid` es `True` y `errors` está vacía.
  2. Un texto que no es JSON, como la salida truncada `{"hospital_visit_phr":[{"hospital":[{"hospital":[`: `is_valid` es `False`, `data` es `None` y hay un error.
  3. Falta la clave `insurance`: inválido, y el error nombra `insurance`.
  4. Sobra una clave `notes`: inválido.
  5. `financials.total_charges` es `"1508"` (texto): inválido, y el error nombra `financials.total_charges`.
  6. `patient.dob` es `"03/11/1978"` o `"19781103"`: inválido por formato en los dos casos. El segundo detecta una versión de `jsonschema` que valida `date` solo con `date.fromisoformat`, que en Python 3.11 lo acepta.
  7. `patient.dob` es `null` y `medications` es `[]`: válido, y `missing_fields` contiene `patient.dob` y `medications`.
  8. `document_type="invoice"`: lanza `ValueError`.
- Con `discharge_summary`, un JSON sin `hospital_course` es inválido.
- `python -m pytest` en verde, con todas las pruebas del repositorio.
- `ruff check .` y `ruff format --check .` en verde.
- `README.md` describe el módulo en su sección de código.
