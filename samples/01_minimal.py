import _env # ensure we can access the lib folder
from lib import SFG


# create a signal flow graph of a simple control loop
controller_p = 1e3
control_loop = SFG()
control_loop.add('Ref', 'Σ') # here the path gain is implicitly set to 1
control_loop.add('Σ', 'Ctrl')
control_loop.add('Ctrl', 'Sys', controller_p)
control_loop.add('Sys', 'Out')
control_loop.add('Sys', 'Σ', -1)

# plot it
g = control_loop.plot()
g.render(outfile='output/01_minimal.pdf', view=True, cleanup=True)

# calculate the gain from reference to output
total_gain = control_loop.calculate_gain('Ref', 'Out')
print(f'Total gain: {total_gain}')
