# Few-shot estructurado por muestra

**Estado:** diseño propuesto para el primer prototipo.

## Decisión

Preparar ejemplos por muestra experimental y usar un adaptador independiente
del proveedor. El primer candidato es `openai/gpt-oss-20b` mediante Groq,
solicitando una respuesta con esquema JSON estricto. La consulta describe
la topografía y el protocolo de medida. Los ejemplos aportan sus descriptores
y la mediana observada de la respuesta nuclear de su muestra.

La prueba inicial usa como objetivo el volumen del tramo a 7 µm de
profundidad. La salida completa de volumen y ejes de la spec requiere máscaras
completas revisadas. El contrato identifica el tipo de objetivo, declara sus
unidades y reserva un estado de abstención cuando faltan datos. La validación
de código comprueba que la respuesta tiene sentido para ese objetivo.

## Motivación

El predictor recibe descriptores y medidas tabulares. Un esquema estricto
facilita comprobar y registrar la respuesta. Un servicio remoto evita que el
LLM compita con μSAM por la GPU del equipo. La evaluación del prototipo medirá
si los ejemplos en contexto mejoran respecto a la media del entrenamiento,
con los mismos grupos reservados para ambos métodos.

La unidad del ejemplo es la muestra, porque varios núcleos de una captura
comparten condiciones y procedencia. La preparación de ejemplos requiere
confirmar grupos y descriptores. La demo del contrato puede hacerse antes
con datos sintéticos y un adaptador simulado.

## Alternativas

| Alternativa | Resultado o coste para este proyecto |
|---|---|
| LLM local cuantizado | Evita depender de una API. Requiere comprobar memoria, velocidad y compatibilidad del esquema en el equipo que ejecuta μSAM. |
| Respuesta libre del LLM | Permite una explicación narrativa, pero complica validar campos, unidades, errores y abstenciones. |
| Media de entrenamiento como único predictor | Es sencilla y reproducible. Forma la referencia de comparación para decidir si el few-shot aporta algo con estos datos. |

## Verificación y referencias

La demo local prepara la misma consulta sintética con `k=1` y `k=2`, comprueba
el contrato con una respuesta simulada y registra las dos trazas en
`tmp/experimentos/few-shot-demo/`.

```bash
python -m topografia_celular.few_shot
```

En la conexión con el proveedor se registrarán las respuestas inválidas como
fallos. Si se alcanza el mínimo previsto de grupos, se usarán las mismas
particiones para el LLM y la media base y se calculará el MAE.

- [Implementación local del prompt y de la validación](../src/topografia_celular/few_shot.py)
- [Pruebas de separación por grupo y del contrato](../tests/test_few_shot.py)
- [Spec de integración few-shot](../specs/integracion-llm-few-shot.md)
- [Modelos y esquema estricto de Groq](https://console.groq.com/docs/structured-outputs)
