"""Pruebas de la calculadora.

Estructura pensada para crecer:
  - Una clase TestCase por operación (TestSuma, TestResta, ...).
  - Casos tabulados en listas CASOS y recorridos con subTest, así agregar
    un caso nuevo es solo añadir una tupla.
  - TestValidacionComun y TestCalcular se aplican a TODAS las operaciones
    registradas en Calculadora.OPERACIONES automáticamente: al añadir una
    operación nueva, ya queda cubierta por estas pruebas genéricas.

Ejecutar:  python3 -m unittest -v
"""

import math
import unittest

from calculadora import Calculadora


class BaseCalculadoraTest(unittest.TestCase):
    def setUp(self):
        self.calc = Calculadora()

    def verificar_casos(self, funcion, casos):
        for a, b, esperado in casos:
            with self.subTest(a=a, b=b, esperado=esperado):
                resultado = funcion(a, b)
                if isinstance(esperado, float):
                    self.assertAlmostEqual(resultado, esperado, places=9)
                else:
                    self.assertEqual(resultado, esperado)


class TestSuma(BaseCalculadoraTest):
    CASOS = [
        (2, 3, 5),
        (0, 0, 0),
        (-2, -3, -5),
        (-2, 3, 1),
        (5, 0, 5),                  # elemento neutro
        (0.1, 0.2, 0.3),            # precisión de punto flotante
        (1.5, 2, 3.5),              # int + float
        (10**18, 10**18, 2 * 10**18),  # enteros grandes
        (1e308, -1e308, 0.0),
    ]

    def test_casos(self):
        self.verificar_casos(self.calc.sumar, self.CASOS)

    def test_conmutativa(self):
        for a, b in [(2, 3), (-1.5, 4), (0, 7)]:
            with self.subTest(a=a, b=b):
                self.assertEqual(self.calc.sumar(a, b), self.calc.sumar(b, a))

    def test_asociativa(self):
        s = self.calc.sumar
        self.assertEqual(s(s(1, 2), 3), s(1, s(2, 3)))

    def test_infinito(self):
        self.assertEqual(self.calc.sumar(math.inf, 1), math.inf)
        self.assertTrue(math.isnan(self.calc.sumar(math.inf, -math.inf)))


class TestResta(BaseCalculadoraTest):
    CASOS = [
        (5, 3, 2),
        (3, 5, -2),
        (0, 0, 0),
        (-2, -3, 1),
        (5, 0, 5),
        (0, 5, -5),
        (0.3, 0.1, 0.2),
        (2.5, 1, 1.5),
        (10**18, 1, 10**18 - 1),
    ]

    def test_casos(self):
        self.verificar_casos(self.calc.restar, self.CASOS)

    def test_no_conmutativa(self):
        self.assertNotEqual(self.calc.restar(5, 3), self.calc.restar(3, 5))

    def test_restar_a_si_mismo_es_cero(self):
        for x in [0, 7, -3, 2.5]:
            with self.subTest(x=x):
                self.assertEqual(self.calc.restar(x, x), 0)

    def test_inversa_de_suma(self):
        for a, b in [(2, 3), (-4, 9), (1.5, 0.5)]:
            with self.subTest(a=a, b=b):
                self.assertAlmostEqual(
                    self.calc.restar(self.calc.sumar(a, b), b), a
                )


class TestValidacionComun(BaseCalculadoraTest):
    """Se aplica a todas las operaciones binarias registradas."""

    INVALIDOS = ["2", None, [1], {"a": 1}, True, object()]

    def test_tipos_invalidos_lanzan_typeerror(self):
        for nombre in Calculadora.OPERACIONES.values():
            metodo = getattr(self.calc, nombre)
            for invalido in self.INVALIDOS:
                with self.subTest(operacion=nombre, valor=invalido, posicion="a"):
                    with self.assertRaises(TypeError):
                        metodo(invalido, 1)
                with self.subTest(operacion=nombre, valor=invalido, posicion="b"):
                    with self.assertRaises(TypeError):
                        metodo(1, invalido)


class TestCalcular(BaseCalculadoraTest):
    def test_despacho_por_operador(self):
        casos = [(2, "+", 3, 5), (2, "-", 3, -1)]
        for a, op, b, esperado in casos:
            with self.subTest(op=op):
                self.assertEqual(self.calc.calcular(a, op, b), esperado)

    def test_todas_las_operaciones_registradas_existen(self):
        for simbolo, nombre in Calculadora.OPERACIONES.items():
            with self.subTest(simbolo=simbolo):
                self.assertTrue(callable(getattr(self.calc, nombre, None)))

    def test_operador_no_soportado(self):
        for op in ["*", "%", "", "suma", "//"]:
            with self.subTest(op=op):
                with self.assertRaises(ValueError):
                    self.calc.calcular(1, op, 2)


class TestDivision(BaseCalculadoraTest):
    CASOS = [
        (6, 3, 2),
        (1, 4, 0.25),
        (-6, 3, -2),
        (6, -3, -2),
        (-6, -3, 2),
        (0, 5, 0),
        (7, 1, 7),                 # elemento neutro
        (7, 2, 3.5),               # división real, no entera
        (1, 3, 0.333333333333),
        (2.5, 0.5, 5.0),
        (10**18, 10**9, 10**9),
    ]

    def test_casos(self):
        for a, b, esperado in self.CASOS:
            with self.subTest(a=a, b=b):
                self.assertAlmostEqual(self.calc.dividir(a, b), esperado, places=9)

    def test_division_por_cero(self):
        for a, b in [(1, 0), (0, 0), (-5, 0), (1, 0.0), (1.5, -0.0)]:
            with self.subTest(a=a, b=b):
                with self.assertRaises(ZeroDivisionError):
                    self.calc.dividir(a, b)

    def test_dividir_por_si_mismo_es_uno(self):
        for x in [1, 7, -3, 2.5]:
            with self.subTest(x=x):
                self.assertEqual(self.calc.dividir(x, x), 1)

    def test_inversa_de_multiplicar(self):
        for a, b in [(10, 4), (-9, 3), (1.5, 0.25)]:
            with self.subTest(a=a, b=b):
                self.assertAlmostEqual(self.calc.dividir(a, b) * b, a)

    def test_no_conmutativa(self):
        self.assertNotEqual(self.calc.dividir(6, 3), self.calc.dividir(3, 6))

    def test_infinito(self):
        self.assertEqual(self.calc.dividir(1, math.inf), 0)
        self.assertEqual(self.calc.dividir(math.inf, 2), math.inf)

    def test_via_calcular(self):
        self.assertEqual(self.calc.calcular(8, "/", 2), 4)
        with self.assertRaises(ZeroDivisionError):
            self.calc.calcular(8, "/", 0)


# --- Plantilla para futuras operaciones -------------------------------------
# class TestRaizCuadrada(BaseCalculadoraTest):
#     # Operación unaria: no usar verificar_casos de dos argumentos.
#     def test_negativo(self):
#         with self.assertRaises(ValueError):
#             self.calc.raiz_cuadrada(-1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
