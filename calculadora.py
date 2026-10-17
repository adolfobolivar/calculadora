"""Calculadora simple con suma y resta, diseñada para extenderse fácilmente."""

from numbers import Number


def _validar(*valores):
    """Verifica que todos los operandos sean numéricos (excluye bool)."""
    for v in valores:
        if isinstance(v, bool) or not isinstance(v, Number):
            raise TypeError(f"Operando no numérico: {v!r}")


class Calculadora:
    """Agrega nuevas operaciones como métodos y regístralas en OPERACIONES."""

    def sumar(self, a, b):
        _validar(a, b)
        return a + b

    def restar(self, a, b):
        _validar(a, b)
        return a - b

    # Mapa símbolo -> nombre de método; añade aquí '/', 'sqrt', etc.
    OPERACIONES = {
        "+": "sumar",
        "-": "restar",
    }

    def calcular(self, a, operador, b):
        if operador not in self.OPERACIONES:
            raise ValueError(f"Operador no soportado: {operador!r}")
        return getattr(self, self.OPERACIONES[operador])(a, b)


def main():
    calc = Calculadora()
    print("Calculadora (+, -). Escribe 'salir' para terminar.")
    while True:
        entrada = input("> ").strip()
        if entrada.lower() == "salir":
            break
        try:
            a, op, b = entrada.split()
            print(calc.calcular(float(a), op, float(b)))
        except ValueError as e:
            print(f"Error: {e}. Formato esperado: 2 + 3")


if __name__ == "__main__":
    main()
