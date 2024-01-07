import _env
from lib import SFG
import sympy


# define a symbol, so that we can get the gain as an algebraic expression
ctrl_p = sympy.symbols('P')

# create SFG, with the control loop grouped as "Loop"
control_loop = SFG(group_name_sep='.')
control_loop.add('Ref', 'Loop.Σ') # note that you could also define node names as a tuple (group_name,node_name)
control_loop.add('Loop.Σ', 'Loop.Ctrl')
control_loop.add('Loop.Ctrl', 'Loop.Sys', ctrl_p)
control_loop.add('Loop.Sys', 'Out')
control_loop.add('Loop.Sys', 'Loop.Σ', -1)

# create plot
g = control_loop.plot()
g.render(outfile='output/02_control_loop.pdf', view=True, cleanup=True)

# calculate the gain from reference to output
total_gain = control_loop.calculate_gain('Ref', 'Out')
total_gain_1k = total_gain.subs(ctrl_p, 1e3)
print(f'Total gain, generic: {total_gain}')
print(f'Total gain, with P = 1k: {total_gain_1k}')
