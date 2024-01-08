import _env
from lib import SFG
import sympy
import math


A, ΓA, ΓL = sympy.symbols('A, ΓA, ΓL')

# create SFG of the scattering parameters of an attenuator, followed by a load termination
network = SFG(group_name_sep='.')
#network.add('Source.a', 'Source.b', ΓS)
network.add('Source.b', 'Att.1a')
network.add('Att.1b', 'Source.a')
network.add('Att.1a', 'Att.1b', ΓA)
network.add('Att.1a', 'Att.2b', A)
network.add('Att.2a', 'Att.1b', A)
network.add('Att.2a', 'Att.2b', ΓA)
network.add('Att.2b', 'Load.a')
network.add('Load.a', 'Load.b', ΓL)
network.add('Load.b', 'Att.2a')

# create plot
g = network.plot()
g.render(outfile='output/03_forced_match.pdf', view=True, cleanup=True)
for i,g in enumerate(network.plot_loops()):
    g.render(outfile=f'output/03_forced_match_loop{i}.pdf', view=True, cleanup=True)
for i,g in enumerate(network.plot_paths('Source.b', 'Source.a')):
    g.render(outfile=f'output/03_forced_match_s11-{i}.pdf', view=True, cleanup=True)

# calculate the scattering-parameter S11 (seen from the source into the attenuator)
s11 = network.calculate_gain('Source.b', 'Source.a')
print(f'S11, generic: {s11}')
print(f'S11, generic ideal attenuator: {s11.subs(ΓA,0)}')
print(f'S11, ideal 6 dB attenuator: {s11.subs(ΓA,0).subs(A,sympy.sympify("1/2"))}')
