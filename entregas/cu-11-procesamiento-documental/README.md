# Sistema de procesamiento documental mediante IA

> Proyecto Integrador de IA II · Grado en Inteligencia Artificial · USC · Curso 2026/27
> Caso de uso CU-11, propuesto por SDG Group

> **Estado (29-10-2026):** semana 2 de la planificación. Están hechos la ingesta del dataset, los prompts y el cliente de Groq, con sus pruebas. Falta confirmar el modelo ([`specs/prueba-modelo-groq.md`](specs/prueba-modelo-groq.md)), y la app todavía no existe.

## Qué es

Una herramienta web en Streamlit que procesa imágenes de documentos médicos con un modelo de IA multimodal, sin entrenarlo para esta tarea. Resuelve dos casos de uso sobre los mismos documentos:

- **Clasificación documental:** identificar si el documento es una factura médica o un informe de alta hospitalaria.
- **Detección de entidades:** extraer sus datos (hospital, paciente, diagnóstico, procedimientos, medicación, importes…) a un JSON estructurado.

La persona usuaria carga un documento, ve el resultado, puede corregirlo y lo exporta.

## Motivación

Las organizaciones dedican mucho trabajo manual a leer, clasificar y transcribir los datos de sus documentos. Es una tarea lenta, cara y propensa a errores. Los modelos multimodales actuales prometen automatizarla sin entrenar un modelo para cada tipo de documento. Este proyecto quiere comprobar hasta dónde llega esa promesa: medir la precisión de un modelo de propósito general al clasificar y extraer datos de documentos con ruido realista, y demostrar en una herramienta interactiva, con una persona que valida los resultados, cuánto trabajo puede ahorrar.

## Alcance

### Dentro del proyecto

- Ingesta de las imágenes JPEG del dataset.
- Clasificación documental y extracción de entidades a JSON estructurado mediante un modelo multimodal servido por la API de Groq.
- Interfaz en Streamlit: carga e inspección de la imagen, ejecución del procesamiento y visualización de los resultados.
- Preguntas en lenguaje natural sobre el documento cargado (Visual QA).
- Edición y validación humana de las entidades extraídas.
- Exportación de los resultados a Excel, CSV y JSON.
- Control de errores: respuestas JSON malformadas, campos ausentes y fallos de conexión.
- Evaluación de la precisión en clasificación y extracción, y de los tiempos de respuesta de la API.

### Fuera del proyecto

- Entrenar o ajustar (*fine-tuning*) modelos propios.
- De momento, las ampliaciones de la planificación. Se abordarán, todas o en parte, solo si el alcance anterior se termina a tiempo:
  - Detección de anomalías y reglas de negocio sobre los datos extraídos.
  - Indicador de evidencia: el fragmento de texto literal en el que se basa cada dato.
  - Inferencia local con vLLM y un modelo abierto, en lugar de la API online.
  - Resaltado en la imagen (*bounding boxes*) de dónde está cada dato.

## Equipo

| Nombre | Rol | Contacto |
|---|---|---|
| Héctor Barro | Estudiante | hector.barro@rai.usc.es |
| Alejandro Barros | Estudiante | alejandro.barros0@rai.usc.es |
| Rodrigo Boquete | Estudiante | rodrigo.boquete@rai.usc.es |

**Tutores profesionales (SDG Group):** Adriano Pezzi Fernández · adrianoluis.pezzi@sdggroup.com 
Esteban Fabello Gonzalez · esteban.fabello@sdggroup.com
Pablo Hervada Presedo · pablo.hervada@sdggroup.com
**Tutor académico (USC):** Ismael Rodríguez Fernández · ismael.rodriguez@usc.es

## Datos

1000 imágenes JPEG de documentos médicos en inglés, con ruido añadido (marcas de agua, brillos, sombras), cada una con su JSON de referencia:

| Tipo | Imágenes | Carpeta | Verdad de referencia |
|---|---|---|---|
| Factura médica (`bill`) | 500 | `data/raw/Data/bills/` | `data/raw/Data/medical_bills_ground_truth.csv` |
| Informe de alta (`discharge_summary`) | 500 | `data/raw/Data/discharge_summaries/` | `data/raw/Data/discharge_summaries_ground_truth.csv` |

Origen: [Noisy Medical Document Images (Kaggle)](https://www.kaggle.com/datasets/devp1866/noisy-medical-document-images-ocr).

La verdad de referencia incluye valores que no aparecen en todas las imágenes (por ejemplo, `medications` en las facturas). Cómo puntuarlos en la evaluación está pendiente de un ADR.

## Tecnologías

- Python 3.11 o superior.
- Streamlit para la interfaz ([ADR](decisions/interfaz-streamlit.md)).
- API de Groq para el modelo multimodal ([ADR](decisions/modelo-via-api-groq.md)). Modelo candidato: `qwen/qwen3.8-27b`, que acepta imágenes y salida JSON con esquema. **Sin confirmar:** en la primera prueba, con una sola factura, clasificó bien 5 de 5 veces, pero la extracción solo devolvió un JSON válido 2 de 5 veces. La confirmación o el descarte se anotarán aquí al cerrar [`specs/prueba-modelo-groq.md`](specs/prueba-modelo-groq.md). Es un modelo en *preview* en Groq y puede retirarse sin aviso.
- Ruff como linter y formateador ([ADR](decisions/linter-ruff.md)), y pytest para las pruebas.

## Estructura del repositorio

````
PIIA-2-cu-11/
├── .claude/       # Configuración de asistentes de IA para el proyecto
│   ├── agents/    # Definiciones de agentes especializados
│   └── skills/    # Instrucciones y habilidades reutilizables para los agentes
├── .github/       # Configuración de GitHub, como flujos de integración continua
├── .vscode/       # Configuración recomendada para trabajar en VS Code
├── data/          # Datos del proyecto
│   ├── processed/ # Datos derivados o transformados durante el procesamiento
│   └── raw/       # Dataset original y datos de referencia
├── decisions/     # Decisiones de arquitectura y diseño (ADR)
├── docs/          # Documentación general, materiales y actas del proyecto
├── Notebooks/     # Cuadernos para exploración y experimentación con los datos
├── output/        # Resultados generados, métricas y exportaciones
├── script/        # Scripts auxiliares, incluida la evaluación del modelo
├── specs/         # Especificaciones de las tareas y funcionalidades pendientes
├── src/           # Código fuente de la aplicación y del procesamiento documental
├── tests/         # Pruebas automatizadas del proyecto
├── .gitignore
├── AGENTS.md
├── ARCHITECTURE.md
└── README.md
````

### Especificaciones

En orden de ejecución; cada una depende de las anteriores.

| Spec | Encargo | Semana | Estado |
|---|---|---|---|
| [`validacion-extraccion.md`](specs/validacion-extraccion.md) | Validar el JSON de extracción contra su esquema y listar los campos ausentes | 2 | Pendiente |
| [`prueba-modelo-groq.md`](specs/prueba-modelo-groq.md) | Medir el modelo con 40 imágenes y confirmarlo o descartarlo | 2 → 3 | Pendiente |
| [`prototipo-streamlit.md`](specs/prototipo-streamlit.md) | Primera versión de la app: cargar, procesar y ver resultados | 3 | Pendiente |
| [`edicion-exportacion.md`](specs/edicion-exportacion.md) | Editar y validar los resultados, y exportarlos a JSON, CSV y Excel | 4 | Pendiente |

Por escribir: preguntas sobre el documento (semana 4) y evaluación de la precisión (semana 5; antes hace falta el ADR sobre los campos no observables).

## Instalación y uso

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate · Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
```

`-e` instala en modo editable el paquete `procesamiento_documental` de `src/`, así que la app, los scripts y las pruebas lo importan sin más. Es obligatorio: los esquemas JSON están en `src/`, fuera del paquete, y solo se encuentran con la instalación editable. El extra `dev` añade Ruff y pytest.

Crea en la raíz un fichero `.env` (no se sube a git) con tu clave de Groq y el modelo:

```
GROQ_API_KEY=tu_clave
GROQ_MODEL=qwen/qwen3.8-27b
```

> **Privacidad:** las imágenes se envían completas, codificadas en Base64, a la API online de Groq. No proceses documentos que no estés autorizado a compartir con ese servicio.

### Cómo funciona el procesamiento

Cada documento se procesa con **dos llamadas** consecutivas a Groq, con la misma imagen:

1. **Clasificación:** el modelo devuelve `{"document_type": ...}` con `bill` o `discharge_summary`. Si la respuesta no es válida, no se hace la extracción.
2. **Extracción:** con el esquema del tipo devuelto, el modelo devuelve las entidades en JSON. Se mantienen todas las claves del esquema; los datos no visibles o ilegibles van como `null`.

Las dos llamadas piden salida estructurada con `response_format` de tipo `json_schema` en modo estricto.

### Código

| Módulo | Qué hace |
|---|---|
| `ingesta.py` | `load_dataset()` lee los CSV de verdad de referencia y enlaza cada fila con su imagen; falla ante la primera incoherencia. `sample_documents()` elige una muestra equilibrada por tipo con semilla fija. `image_to_data_url()` codifica un JPEG para enviarlo a Groq. |
| `prompts.py` | Prompts, tipos documentales y esquema de clasificación. Construye los mensajes multimodales y el `response_format` de cada llamada. |
| `cliente.py` | La única pieza que habla con Groq. `ModelClient.from_env()` lee `GROQ_API_KEY` y `GROQ_MODEL`; `classify()` devuelve el tipo validado y `extract()` el JSON en bruto. Cada respuesta incluye latencia, tokens e intentos. Reintenta los 429, los fallos de conexión y los 5xx, hasta 5 veces; cualquier otro fallo lanza `ModelError`. |

### Pruebas

```bash
python -m pytest     # pruebas unitarias, sin red ni cuota de Groq
ruff check .         # obligatorio antes de subir cambios
ruff format --check .
```

Prueba de extremo a extremo con la API real: clasifica y extrae el primer JPEG de `data/raw/` e imprime las dos respuestas, sin guardar nada.

```bash
python tests/envio_imagenes_groq.py
```

### Interfaz Streamlit

La interfaz permite elegir primero la categoría (`bills` o
`discharge_summaries`) y después una imagen de esa carpeta, o subir documentos
propios. También permite inspeccionar la imagen, editar la tabla de entidades y
descargar los resultados en JSON o CSV. Incluye el espacio de consulta en
lenguaje natural. La clasificación, extracción, anotación de bounding boxes y
respuestas del LLM se mostrarán cuando se conecten sus servicios al backend; la
interfaz no genera resultados de ejemplo.

La pestaña **Reporte de métricas** resume los 1000 documentos del dataset, indica
cuántos se han procesado en la sesión y muestra clasificación, confianza y
tiempos por documento. Cuando haya resultados, compara la clasificación con la
categoría de la carpeta y los campos extraídos con los CSV de referencia
(coincidencia exacta, ignorando mayúsculas y diferencias de espacios). Los
resultados se mantienen en la sesión actual de Streamlit y no se procesan
documentos en lote automáticamente.

#### Integración frontend-backend

Para conectar la interfaz hacen falta **2 puntos de integración**. Son funciones
de Python en `src/procesamiento_documental/integraciones.py`; no hace falta crear
dos servidores o dos APIs independientes. El backend puede implementar ambas
funciones usando los módulos del proyecto, Groq u otros servicios:

| Punto de integración | Entrada del frontend | Respuesta que espera la interfaz | Uso |
|---|---|---|---|
| `procesar_documento(imagen)` | Bytes de una imagen | `ResultadoProcesamiento` | Clasificación, entidades extraídas, confianza, duración y, opcionalmente, imagen anotada. |
| `responder_pregunta(imagen, pregunta, resultado)` | Bytes de la imagen, texto de la pregunta y resultado del procesamiento (o `None`) | Texto de respuesta | Consulta en lenguaje natural sobre el documento. |

El contrato de `ResultadoProcesamiento` incluye `document_type` (`bill` o
`discharge_summary`), `classification_confidence` (0–1 o `None`),
`processing_seconds` (o `None`), `entities` (objeto con el esquema documental
correspondiente) y `annotated_image` (bytes de imagen anotada o `None`). Para
mostrar bounding boxes, el backend puede devolver la imagen ya anotada en ese
campo; la interfaz todavía no consume coordenadas de cajas como estructura
separada.

Las métricas agregadas del reporte **no requieren un tercer servicio**: la app
las calcula con los resultados de procesamiento de la sesión y compara contra
las etiquetas de las carpetas y los CSV locales de referencia. La navegación
por las imágenes, la carga de ficheros, la edición y la exportación también son
funcionalidades del frontend. Actualmente los resultados solo se conservan en
la sesión activa de Streamlit; si se necesita historial entre sesiones o
usuarios, habría que añadir persistencia (por ejemplo, una base de datos), que
no forma parte de estos dos puntos mínimos.

Ambas funciones lanzan `IntegracionPendienteError` mientras no esté conectado
el backend, para que la interfaz indique explícitamente qué integración falta.

Lanza la aplicación desde la raíz del repositorio:

```bash
.\.venv\Scripts\python.exe -m streamlit run src/app.py
```
