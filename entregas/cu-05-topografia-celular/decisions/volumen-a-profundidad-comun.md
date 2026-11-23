# Medir volumen a una profundidad física común

**Estado:** aplicada en el piloto de medidas. La profundidad del piloto es de 7 µm.

## Decisión

Medir el volumen de una ventana central con el mismo espesor físico en cada
núcleo, dentro del intervalo señalado por dos marcas de parada de μSAM. El
centro de la ventana se sitúa en el punto medio del intervalo fiable. El
exportador suma el área de cada corte multiplicada por el espesor que ese
corte representa dentro de la ventana, incluido el peso parcial de los planos
de los extremos. Guardar ese resultado como `volumen_tramo_um3`, con su
profundidad, la procedencia y el estado de revisión.

## Motivación

Las máscaras de la campaña pueden tener extremos difusos o terminar en el
último plano de la pila. El tramo central permite aprovechar cortes que sí
tienen contorno visible. Una ventana de 7 µm tampoco implica el mismo número de
planos en RAW y HDF, que tienen pasos Z de aproximadamente 1 y 2 µm. La
calibración y los pesos por plano resuelven esa diferencia de muestreo en el
cálculo del volumen. La comparabilidad biológica se revisa por separado.

El piloto midió 28 de los 30 núcleos guardados. Dos máscaras tenían paradas
incompletas o ambiguas y quedaron señaladas para revisar. Entre los 26 núcleos
que admitían mover la ventana un plano en ambos sentidos, el cambio máximo fue
2,2 % en RAW y 5,3 % en HDF. Estas cifras comprueban el comportamiento del
recorte en el piloto. La validación de contornos requiere revisión visual.

## Alternativas

| Alternativa | Resultado o coste para este proyecto |
|---|---|
| Medir toda la máscara | Es apropiado para máscaras completas revisadas. Si faltan extremos, el resultado depende de cuánto se segmentó. |
| Conservar el mismo número de cortes | Con pasos Z distintos, el espesor físico cambia de una pila a otra. |
| Completar extremos por interpolación | Puede ser útil para explorar la forma, pero añadiría vóxeles estimados donde el contorno observado es ambiguo. |

## Referencias

- [Exportador de tramos](../src/topografia_celular/tramos.py)
- [Pruebas con geometría y pasos Z conocidos](../tests/test_tramos.py)
- [Guía y comando de medición](../docs/seleccion-nucleos.md#medir-una-profundidad-común)
