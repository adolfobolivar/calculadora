# Calculadora

Calculadora sencilla en Python que suma, resta y divide. Está pensada como base para
agregar más operaciones (raíz cuadrada, potencia, etc.) con una suite de pruebas
que crece junto con el código.

## Requisitos

- Python 3.8 o superior
- No necesita dependencias externas (las pruebas usan `unittest`, incluido en Python)

## Uso

### Modo interactivo

```bash
python3 calculadora.py
```

```
Calculadora (+, -, /). Escribe 'salir' para terminar.
> 2 + 3
5.0
> 10 - 4
6.0
> salir
```

### Como librería

```python
from calculadora import Calculadora

calc = Calculadora()
calc.sumar(2, 3)          # 5
calc.restar(10, 4)        # 6
calc.dividir(7, 2)        # 3.5
calc.calcular(2, "+", 3)  # 5
```

Si un operando no es numérico se lanza `TypeError`. Dividir entre cero lanza
`ZeroDivisionError`. Si el operador no es
soportado se lanza `ValueError`.

## Pruebas

```bash
python3 -m unittest -v
```

Las pruebas (`test_calculadora.py`) incluyen:

- **Casos tabulados** por operación: enteros, negativos, decimales y números grandes.
- **Propiedades matemáticas**: conmutatividad, asociatividad, `x - x = 0`, resta como inversa de la suma.
- **Validación genérica**: toda operación registrada en `Calculadora.OPERACIONES` se prueba automáticamente contra entradas inválidas.
- **Plantillas** comentadas para futuras pruebas de raíz cuadrada.

## Cómo agregar una operación

1. Crea el método en `Calculadora` (por ejemplo `dividir`).
2. Regístralo en `OPERACIONES` (`"/": "dividir"`).
3. Agrega su clase de pruebas en `test_calculadora.py` (hay plantillas al final del archivo).
4. Ejecuta `python3 -m unittest -v`.

> Nota: las operaciones de un solo operando (como la raíz cuadrada) requieren
> adaptar `calcular` y las pruebas genéricas, que hoy asumen dos operandos.

## Estructura

```
calculadora.py        # Lógica de la calculadora y modo interactivo
test_calculadora.py   # Suite de pruebas
README.md
```
