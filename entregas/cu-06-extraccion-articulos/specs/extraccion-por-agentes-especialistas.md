# Extracción por agentes especialistas

## Qué construir

Un equipo de tres agentes hechos con CrewAI, cada uno especialista en uno de los
tres bloques de datos del estudio del iMATUS, coordinados por un orquestador:

| Agente | Bloque | Variables |
|---|---|---|
| Agente de impresión | Impresión (11) | `Drug`, `Drug_supplier`, `Inkjet_printer`, `Inkjet_printer_supplier`, `Inkjet_technology`, `Nozzle`, `Nozzle_supplier`, `Nozzle_diameter`, `Substrate`, `Substrate_supplier`, `Printed_object` |
| Agente de tinta | Propiedades de la tinta (9) | `Viscosity`, `Kinematic_viscosity`, `Surface_tension`, `Density_reported`, `Density_calculated`, `Z_reported`, `Z_calculated`, `Oh_reported`, `Oh_calculated` |
| Agente de dosis | Dosis (3) | `Printed_drug_dose`, `Number_of_layers`, `Printed_area` |

**Funcionamiento.**

1. El orquestador recibe el PDF del artículo (y los de su material
   suplementario, si los hay) junto con las variables pedidas, los pasa a texto
   con Docling, decide qué agentes hacen falta según las variables pedidas y
   los lanza. Si no se pide ninguna variable de un bloque,
   ese agente no se ejecuta.
2. Cada agente identifica primero las formulaciones (tintas) y casos de
   impresión distintos que describe el artículo, porque un artículo puede
   probar varias tintas, impresoras o sustratos, y devuelve una fila por caso.
3. Para cada variable, el agente devuelve el valor, la unidad, el origen y la
   evidencia (ver formato más abajo). Si el dato no aparece, devuelve
   `"NR"` (no reportado) en lugar de inventarlo.
4. Cuando una variable se obtiene por cálculo (por ejemplo Oh o Z a partir de
   viscosidad, tensión superficial, densidad y diámetro de boquilla), el agente
   de tinta no hace la cuenta él mismo: llama a la herramienta calculadora
   y anota que el valor es calculado.
5. El orquestador junta las salidas de los tres agentes en un único JSON por
   artículo.

**Formato de salida** (un fichero `art_NNN.json` por artículo, con la misma
estructura que el `ground_truth/` del corrector para que se pueda corregir sin
conversión), añadiendo el campo `evidencia`:

```json
"Inkjet_printer": {
  "valor": "Dimatix DMP-2800",
  "unidad": null,
  "fuente": "articulo",          // articulo | suplementario | calculado | internet
  "evidencia": "...printed using a Dimatix DMP-2800 materials printer...",
  "ubicacion": "Sección 2.2",
  "nota": null
}
```

**Dónde encaja.** Es el núcleo del sistema (fases 2 y 3 del proyecto). Recibe
los PDF desde la interfaz, los pasa a texto con Docling, usa la calculadora como herramienta, su salida la
mide el corrector automático y la interfaz la muestra al usuario.

## Por qué

- El estudio del iMATUS pegaba a mano 8 prompts enormes en ChatGPT, uno tras
  otro. Queremos el mismo resultado sin intervención humana.
- Repartir el trabajo en especialistas permite dar a cada agente instrucciones
  cortas y dirigidas a los fallos concretos que encontramos en la fase 1. Según
  el corrector sobre las respuestas de GPT-4, el bloque de impresión es el peor
  (exactitud 0,909) y dentro de él fallan sobre todo `Nozzle_diameter` (0,766),
  `Inkjet_printer` (0,825, se confunde impresora con cabezal) y
  `Nozzle_supplier` (0,825, se inventa el fabricante). En dosis, el número de
  capas (0,898) casi nunca está escrito tal cual.
- Exigir la frase de origen (`evidencia`) hace que cada dato sea comprobable por
  una persona en segundos y reduce los valores inventados: si el agente no puede
  citar, no debería afirmar.

## Restricciones

- **Entrada en texto:** los agentes leen el texto que produce Docling a partir
  del PDF, con las tablas reconstruidas; no leen el PDF original.
- **Framework:** CrewAI en Python. El LLM concreto es el que se elija en el paso 3
  de la fase 1; el código no debe depender de un proveedor concreto (se cambia
  con configuración, no editando los agentes).
- **Separación de artículos:** durante el desarrollo solo se usan los 20 artículos
  de `desarrollo.txt`. Los otros 50 no se procesan hasta la prueba final.
- **No inventar:** un valor con `fuente = "articulo"` o `"suplementario"` debe
  llevar una `evidencia` que sea texto literal del documento. Si no hay frase que
  lo respalde, el valor es `"NR"`.
- **Sin cálculos dentro del LLM:** todo valor numérico derivado (Oh, Z, densidad
  calculada a partir de proporciones de disolventes, viscosidad cinemática) pasa
  por la calculadora.
- **Fuera de esta spec:** la búsqueda en internet y la lectura de gráficas. Si un
  dato solo está en una gráfica o requiere buscarlo fuera, el agente devuelve
  `"NR"` con `nota` indicando dónde podría estar (por ejemplo
  `"posible en Fig. 3"`), para que los ayudantes de la fase 3 lo recojan después.
- **Unidades:** se respetan las del artículo y se rellena el campo `unidad`; no se
  convierten salvo que la variable lo exija en la plantilla de las expertas.
- **Salida válida siempre:** si un agente falla (error de API, respuesta mal
  formada), se reintenta como máximo 2 veces; si sigue fallando, sus variables se
  devuelven como `"NR"` con `nota = "error_agente"` y el resto del artículo se
  entrega igual.
- **Coste y tiempo:** se registra por artículo el número de tokens, el coste en
  dólares y el tiempo total.

## Criterios de aceptación

Todos se miden sobre los 20 artículos de desarrollo, con el corrector automático
y la misma tolerancia que se usó para reproducir el 94 % del estudio.

1. **Ejecución sin intervención:** el comando
   `python -m extraccion --articulos desarrollo.txt` procesa los 20 artículos y
   deja 20 ficheros `art_NNN.json` sin que nadie toque nada a mitad.
2. **Formato:** los 20 JSON se validan contra el esquema del `ground_truth/` (más
   los campos `evidencia` y `ubicacion`) sin errores, y el corrector los lee sin
   conversión previa.
3. **Exactitud global:** la exactitud global es ≥ 0,936, la de GPT-4 en el
   estudio.
4. **Exactitud por bloque:** impresión ≥ 0,909, tinta ≥ 0,991 y dosis ≥ 0,919
   (las cifras de GPT-4 por bloque).
5. **Mejora en los puntos débiles:** `Nozzle_diameter`, `Inkjet_printer` y
   `Nozzle_supplier` superan cada una la exactitud de GPT-4 (0,766, 0,825 y
   0,825).
6. **Evidencia literal:** en el 100 % de los valores con `fuente` igual a
   `articulo` o `suplementario`, la `evidencia` aparece literalmente en el texto de origen
   (comprobado por un script de test que busca la frase en el texto convertido
   con Docling tras normalizar espacios, saltos de línea y guiones de corte).
7. **Valores inventados:** el número de casos FP2 (el sistema da un valor donde
   las expertas pusieron "no reportado") es menor que el de GPT-4 en esos
   mismos 20 artículos.
8. **Cálculos trazables:** el 100 % de los valores con `fuente = "calculado"`
   tienen en la traza de ejecución una llamada a la calculadora.
9. **Selección de variables:** si se piden solo variables de un bloque (por
   ejemplo, solo `Printed_drug_dose`), los otros dos agentes no se ejecutan (se ve
   en la traza) y el JSON solo contiene las variables pedidas.
10. **Robustez:** si se simula un error de API en un agente, el artículo se
    entrega igual con las variables de ese agente como `"NR"` y
    `nota = "error_agente"`.
11. **Coste y tiempo:** existe un CSV con una fila por artículo con tokens, coste
    y tiempo, y la media por artículo no supera 0,50 $ y 5 minutos.
