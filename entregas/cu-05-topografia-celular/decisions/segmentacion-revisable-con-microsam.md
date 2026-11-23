# Segmentación revisable con μSAM

**Estado:** aplicada en la campaña de selección de núcleos.

## Decisión

Procesar las pilas nuevas con el anotador 3D de μSAM y ViT-Large
(`vit_l_lm`). Abrir cada pila con su calibración y canal registrado. Revisar un
núcleo por vez y conservar máscaras, puntos, cajas y parámetros en propuestas
numeradas por pila e ID. Reutilizar los embeddings de una misma señal y modelo.
El lote previo de Cellpose queda disponible como referencia del piloto inicial.

## Motivación

La propagación da una primera máscara coherente a través de Z, mientras que la
interfaz permite corregir cortes en los que el contorno pierde señal o se junta
con otro objeto. En el piloto, varios núcleos tenían un centro medible y
extremos inciertos. Guardar las indicaciones permite retomar la revisión y
seguir el origen de cada medida. ViT-Large procesó las pilas seleccionadas en
la RTX 3060 del equipo. La calidad aún se revisa visualmente por núcleo.

## Alternativas

| Alternativa | Resultado o coste para este proyecto |
|---|---|
| Cellpose por plano y asociación automática | Útil para procesar el lote inicial, pero la identidad entre cortes se tiene que reconstruir y algunos casos conservan huecos o fragmentación. |
| μSAM ViT-Base | Tiene menor coste de memoria y permite un piloto rápido. ViT-Large cabe en el equipo para estas pilas y queda como modelo de la campaña. Se puede retomar ViT-Base en otro destino si el lote exige menos memoria. |
| Etiquetar todos los cortes a mano | Aporta una referencia pequeña de validación. Resulta costoso como procedimiento para todas las pilas. |

## Referencias

- [Guía de selección y guardado](../docs/seleccion-nucleos.md)
- [Preparación TIFF directa](../src/topografia_celular/entrada_microsam.py)
- [Anotador y almacenamiento de las revisiones](../src/topografia_celular/anotacion3d.py)
- [Documentación de μSAM](https://computational-cell-analytics.github.io/micro-sam/micro_sam.html)
