import _env
from lib import SFG
import sympy
import re


def parse_sfg_script(script) -> tuple[SFG,list[tuple[str,str]]]:
    sfg = SFG(group_name_sep='.')
    paths = []
    for line in script.splitlines():
        line = line.strip()
        if len(line) < 1 or line.startswith('#'):
            continue
        if m := re.fullmatch(r'([a-zA-Z0-9\._]+)\s*->\s*([a-zA-Z0-9\._]+)(\s*:\s*([a-zA-Z0-9\._+-]+))?', line):
            src, dst, weight = m.group(1), m.group(2), m.group(4)
            if weight is None:
                weight = 1
            elif re.fullmatch(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?', weight):
                weight = float(weight)
            else:
                weight = sympy.symbols(weight)
            sfg.add(src, dst, weight)
        elif m := re.fullmatch(r'([a-zA-Z0-9\._]+)\s*=>\s*([a-zA-Z0-9\._]+)', line):
            src, dst = m.group(1), m.group(2)
            paths.append((src,dst))
        else:
            raise ValueError(f'Unable to parse "{line}"')
    return sfg, paths


sfg, paths = parse_sfg_script('''
    # SFG
    Port1.a -> A.1a
    A.1b -> Port1.b
    A.1a -> A.1b: S11a
    A.2a -> A.1b: S21a
    A.1a -> A.2b: S12a
    A.2a -> A.2b: S22a
    A.2b -> B.1a
    B.1b -> A.2a
    B.1a -> B.1b: S11b
    B.2a -> B.1b: S21b
    B.1a -> B.2b: S12b
    B.2a -> B.2b: S22b
    Port2.2a -> B.2a
    B.2b -> Port2.b

    # paths to calculate
    Port1.a => Port1.b
    Port1.a => Port2.b''')


g = sfg.plot(show_unity_weights=False)
g.render(outfile='output/06_parser.pdf', view=True, cleanup=True)


sympy.init_printing() 
for (src,dst) in paths:
    path = sympy.simplify(sfg.calculate_gain(src, dst))

    print()
    print(f'Path {src} -> {dst}:')
    sympy.pprint(path)
