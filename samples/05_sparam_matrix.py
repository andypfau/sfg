import _env
from lib import SFG
import sympy


S11a, S21a, S12a, S22a = sympy.symbols('S_11a, S_21a, S_12a, S_22a')
S11b, S21b, S12b, S22b = sympy.symbols('S_11b, S_21b, S_12b, S_22b')

# create SFG of the scattering parameters of two cascaded networks
network = SFG(group_name_sep='.')
network.add('1a', 'A.1a')
network.add('A.1b', '1b')

network.add('A.1a', 'A.1b', S11a)
network.add('A.2a', 'A.1b', S21a)
network.add('A.1a', 'A.2b', S12a)
network.add('A.2a', 'A.2b', S22a)

network.add('A.2b', 'B.1a')
network.add('B.1b', 'A.2a')

network.add('B.1a', 'B.1b', S11b)
network.add('B.2a', 'B.1b', S21b)
network.add('B.1a', 'B.2b', S12b)
network.add('B.2a', 'B.2b', S22b)

network.add('2a', 'B.2a')
network.add('B.2b', '2b')

# create plot
g = network.plot(show_unity_weights=False)
g.render(outfile='output/05_sparam_matrix.pdf', view=True, cleanup=True)

# calculate the four S-parameters of the cascade network
s11 = network.calculate_gain('1a', '1b')
s21 = network.calculate_gain('1a', '2b')
s12 = network.calculate_gain('2a', '1b')
s22 = network.calculate_gain('2a', '2b')
s = sympy.Matrix([[s11,s21],[s12,s22]])
sympy.init_printing() 
sympy.pprint(s)

# sanity check: if we set network B to unity, the S-parameters of the cascade should
#   equal the S-parameters of the first network only; same for the other network
s_only_a = s.subs([(S11b,0), (S21b,1), (S12b,1), (S22b,0)])
sympy.pprint(s_only_a)
s_only_b = s.subs([(S11a,0), (S21a,1), (S12a,1), (S22a,0)])
sympy.pprint(s_only_b)
