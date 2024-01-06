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
        - A weight may be a numeric value, or e.g. a `sympy` symbol.
    - A node name may be a string, or a tuple `(group,name)` if you want to group nodes in groups.
        - Alternatively, you can specify a separator in the constructor; then every name is split into group and name by the seprator.
        - See demo `02_control_loop.py` for an example.
3. Plot the SFG by calling the `plot()` function.
    - The function will return the graph as a `graphviz.Digraph` object, which you can save or display.
        - See demo `01_minimal.py.py` for an example.
    - You can also plot all loops in the system, by calling the `plot_loops()` function.
        - See demo `02_control_loop.py` for an example.
    - You can also plot all forward paths of a specified path in the system, by calling the `plot_paths()` function, with the names of the source and destination nodes as arguments.
        - See demo `02_control_loop.py` for an example.
4. Calculate the path gain by calling the `calculate_gain()` method.
    - The gain is calculated using [Mason's gain formula](https://en.wikipedia.org/wiki/Mason's_gain_formula).
        - See demo `01_minimal.py.py` for an example.
