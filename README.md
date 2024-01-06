SFG
===

[Signal flow graph](https://en.wikipedia.org/wiki/Signal-flow_graph) calculation and plotting in Python.


## Requirements

Run `python -m pip install -r requirements.txt` to install the required packages.

Tested with Python 3.12.


## How To Use

### Demos

For a simple demo, just run any of the Python files in the `samples` folder.

### Basic Concept

1. Create a SFG object.
2. Add all paths of the system:
    - Each path consists of a source node, a destination node, and a weight (gain).
        - If not specified, the weight is implicitly set to 1.
        - A weight may be a numeric value, or e.g. a [sympy](https://pypi.org/project/sympy/) symbol.
    - A node name may be a string, or a tuple `(group,name)` if you want to group nodes in groups.
        - Alternatively, you can specify a separator in the constructor; then every name is split into group and name by the seprator.
        - See demo `samples/02_control_loop.py` for an example.
3. Create a plot of the SFG by calling the `plot()` function, using the [graphviz](https://pypi.org/project/graphviz/) package.
    - The function will return the graph as a `graphviz.Digraph` object, which you can save or display.
        - See demo `samples/01_minimal.py.py` for an example.
    - You can also plot all loops in the system, by calling the `plot_loops()` function.
        - See demo `samples/02_control_loop.py` for an example.
    - You can also plot all forward paths of a specified path in the system, by calling the `plot_paths()` function, with the names of the source and destination nodes as arguments.
        - See demo `samples/02_control_loop.py` for an example.
4. Calculate the path gain by calling the `calculate_gain()` method.
    - The gain is calculated using [Mason's gain formula](https://en.wikipedia.org/wiki/Mason's_gain_formula).
    - See demo `samples/01_minimal.py.py` for an example.

##### Example

Example code; see also `samples/01_minimal.py.py`:

    from lib import SFG

    # create SFG
    controller_p = 1e3
    control_loop = SFG()
    control_loop.add('Ref', 'Δ')set to 1
    control_loop.add('Σ', 'Ctrl')
    control_loop.add('Ctrl', 'Sys', controller_p)
    control_loop.add('Sys', 'Out')
    control_loop.add('Sys', 'Σ', -1)

    # plot it
    g = control_loop.plot()
    ...

    # calculate the gain from reference to output
    total_gain = control_loop.calculate_gain('Ref', 'Out')
    ...

The resulting graph is:
<img src="./doc/demo_sfg_controlloop.svg" height="100" />

The resulting gain is `0.999` ≈ 1.


### Applications

- [Control loops](https://en.wikipedia.org/wiki/Control_loop) (see demo `samples/01_minimal.py.py`)
- [Scattering Parameters](https://en.wikipedia.org/wiki/) (see `samples/03_forced_match.py` )
