import sys
sys.path.insert(0, '.')

from lib import SFG
import sympy
import unittest



class TestCalculatedGains(unittest.TestCase):


    def test_trivial(self):
        sfg = SFG()
        sfg.add('A', 'B')
        sfg.add('B', 'C', 10)
        sfg.add('C', 'D')
        self.assertEqual(sfg.gain('A', 'D'), 10)


    def test_simple_loop(self):
        sfg = SFG()
        sfg.add('A', 'B')
        sfg.add('B', 'C', 10)
        sfg.add('C', 'B', 1)
        sfg.add('C', 'D')
        self.assertAlmostEqual(sfg.gain('A', 'D'), 10/(1-10*1))


    def test_double_loop(self):
        sfg = SFG()
        sfg.add('A', 'B')
        sfg.add('B', 'C', 1)
        sfg.add('C', 'B', 0.1)
        sfg.add('C', 'D')
        sfg.add('D', 'E', 1)
        sfg.add('E', 'D', 0.2)
        sfg.add('E', 'F')
        self.assertAlmostEqual(sfg.gain('A', 'F'), (1/(1-1*0.1)) * (1/(1-1*0.2)))


    def test_nested_loops(self):
        sfg = SFG()
        sfg.add('A', 'B')
        sfg.add('B', 'C', 1)
        sfg.add('C', 'B', 0.1)
        sfg.add('C', 'D')
        sfg.add('D', 'E', 1)
        sfg.add('E', 'D', 0.1)
        sfg.add('E', 'F')
        sfg.add('E', 'G')
        sfg.add('G', 'H')
        sfg.add('H', 'I')
        sfg.add('I', 'H', 0.1)
        sfg.add('I', 'J', 0.2)
        sfg.add('J', 'H', 0.1)
        sfg.add('J', 'B')
        self.assertAlmostEqual(sfg.gain('A', 'F') , 1.7160686)
        self.assertNotAlmostEqual(sfg.gain('B', 'C') , 1/(1-1*0.1))  # this node is part of a bigger loop, so the simple loop gain must be incorrect



class TestClassBehavior(unittest.TestCase):


    def test_allows_strings_as_names(self):
        sfg = SFG()
        sfg.add('A', 'B', 10)
        self.assertEqual(sfg.gain('A', 'B'), 10)


    def test_allows_ints_as_names(self):
        sfg = SFG()
        sfg.add(1, 2, 10)
        self.assertEqual(sfg.gain(1, 2), 10)


    def test_allows_tuples_as_names(self):
        sfg = SFG()
        sfg.add(('Group 1','A'), ('Group 2','B'), 10)
        self.assertEqual(sfg.gain(('Group 1','A'), ('Group 2','B')), 10)


    def test_empty_graph_fails(self):
        sfg = SFG()
        with self.assertRaises(ValueError):
            sfg.gain('A', 'B')


    def test_invalid_node_fails(self):
        sfg = SFG()
        sfg.add('A', 'B')
        with self.assertRaises(ValueError):
            sfg.gain('A', 'D')


    def test_no_path_fails(self):
        sfg = SFG()
        sfg.add('A', 'B')
        sfg.add('C', 'D')
        with self.assertRaises(ValueError):
            sfg.gain('A', 'D')


    def test_works_with_float(self):
        sfg = SFG()
        sfg.add('A', 'B', 1.0)
        sfg.add('B', 'C', 2.0)
        g = sfg.gain('A', 'C')
        self.assertIsInstance(g, float)
        self.assertAlmostEqual(g, 1.0*2.0)


    def test_works_with_sympy(self):
        ab, bc = sympy.symbols('ab bc')
        sfg = SFG()
        sfg.add('A', 'B', ab)
        sfg.add('B', 'C', bc)
        g = sfg.gain('A', 'C')
        self.assertIsInstance(g, sympy.Expr)
        self.assertAlmostEqual(g.subs(ab,1).subs(bc,2), 1*2)


    def test_works_with_some_custom_type(self):
        class MyNumericClass:
            @staticmethod
            def _cast(obj):
                if isinstance(obj,MyNumericClass):
                    return obj.value
                return obj
            def __init__(self, value):
                self.value = value
            def __add__(self, other):
                return MyNumericClass(self.value + MyNumericClass._cast(other))
            def __radd__(self, other):
                return MyNumericClass(self.value + MyNumericClass._cast(other))
            def __mul__(self, other):
                return MyNumericClass(self.value * MyNumericClass._cast(other))
            def __rmul__(self, other):
                return MyNumericClass(self.value * MyNumericClass._cast(other))
            def __truediv__(self, other):
                return MyNumericClass(self.value / MyNumericClass._cast(other))
            def __rtruediv__(self, other):
                return MyNumericClass(self.value / MyNumericClass._cast(other))
        sfg = SFG()
        sfg.add('A', 'B', MyNumericClass(1))
        sfg.add('B', 'C', MyNumericClass(2))
        g = sfg.gain('A', 'C')
        self.assertIsInstance(g, MyNumericClass)
        self.assertAlmostEqual(g.value, 1*2)



if __name__ == '__main__':
    unittest.main()
