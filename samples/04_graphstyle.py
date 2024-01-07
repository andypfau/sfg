import _env
from lib import SFG


control_loop = SFG(group_name_sep='.')
control_loop.add('Ref', 'Loop.Σ')
control_loop.add('Loop.Σ', 'Loop.Ctrl')
control_loop.add('Loop.Ctrl', 'Loop.Sys', 100)
control_loop.add('Loop.Sys', 'Out')
control_loop.add('Loop.Sys', 'Loop.Σ', -1)


# optional: reset to graphviz defaults (i.e. remove all custom attributes)
control_loop.graph_attrs = SFG.GraphAttrPresets.GraphvizDefault

# change graph direction to top-down
control_loop.graph_attrs.graph['rankdir'] = 'TB'

# change shapes and colors
control_loop.graph_attrs.group['shape'] = 'rectangle'
control_loop.graph_attrs.group['style'] = 'rounded,filled'
control_loop.graph_attrs.group['color'] = 'Cornsilk'
control_loop.graph_attrs.node['shape'] = 'square'
control_loop.graph_attrs.node['style'] = 'rounded,filled'
control_loop.graph_attrs.node['fillcolor'] = 'SpringGreen'
control_loop.graph_attrs.node['pencolor'] = 'Black'
control_loop.graph_attrs.edge['color'] = 'Maroon'


g = control_loop.plot()
g.render(outfile='output/04_graphstyle.pdf', view=True, cleanup=True)
