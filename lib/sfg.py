from typing import TypeVar, Union
import itertools
from graphviz import Digraph
from types import SimpleNamespace
from collections import defaultdict


class SFG:

    class GraphAttrPresets:
        
        GraphvizDefault = SimpleNamespace(graph=dict(), group=dict(), node=dict(), edge=dict())
        
        SfgDefault = SimpleNamespace(
            graph=dict(
                rankdir='LR',
            ),
            group=dict(
                shape='rectangle',
                style='filled,rounded',
                color='GreenYellow',
            ),
            node=dict(
                shape='circle',
                style='filled,solid',
                fillcolor='HotPink',
                pencolor='Black',
            ),
            edge=dict(
            ),
        )

        Monochrome = SimpleNamespace(
            graph=dict(
                rankdir='LR',
            ),
            group=dict(
                shape='rectangle',
                style='dashed',
            ),
            node=dict(
                shape='circle',
            ),
            edge=dict(
            ),
        )


    def __init__(self, group_name_sep: "str|None" = None):
        def lf():
            return []
        self._list_factory = lf
        self.graph: dict[str,list]
        self.graph = defaultdict(self._list_factory)
        self.group_name_separator = group_name_sep
        self.graph_attrs = SFG.GraphAttrPresets.SfgDefault
    

    def add(self, from_node: "tuple[str,str]|str", to_node: "tuple[str,str]|str", weight = 1):
        """
        Add a new node.

        args:
            from_node: name of the 
        """
        self.graph[self._split_name(from_node)].append((self._split_name(to_node),weight))


    def plot(self, name: str = 'SFG') -> Digraph:
        """ Return a graphviz.Digraph of the SFG """
        return self._plot(self.graph, name)


    def plot_loops(self, name_prefix: str = 'SFG', *args, **kwargs) -> list[Digraph]:
        """ Return a list graphviz.Digraph, one for each loop in the SFG """
        loops = self.find_loops(*args, **kwargs)
        result = []
        for i,loop in enumerate(loops):
            graph = defaultdict(self._list_factory)
            for i in range(len(loop.path)):
                j = (i+1)%len(loop.path)
                sn, dn = loop.path[i], loop.path[j]
                w = loop.weights[j]
                graph[sn].append((dn,w))
            result.append(self._plot(graph, f'{name_prefix}{i}'))
        return result


    def plot_paths(self, from_node, to_node, name_prefix: str = 'SFG', *args, **kwargs) -> list[Digraph]:
        """ Return a list graphviz.Digraph, one for each forward path between the specified nodes in the SFG """
        paths = self.find_paths(from_node, to_node, *args, **kwargs)
        result = []
        for i,path in enumerate(paths):
            graph = defaultdict(self._list_factory)
            for i in range(len(path.path)-1):
                sn, dn = path.path[i], path.path[i+1]
                w = path.weights[i+1]
                graph[sn].append((dn,w))
            result.append(self._plot(graph, f'{name_prefix}{i}'))
        return result


    def find_loops(self, include_zero_gain: bool = False):
        loops = []
        def sort_loop(path, weights):
            i_start = 0
            for i,elem in enumerate(path):
                if elem < path[i_start]:
                    i_start = i
            for _ in range(i_start):
                path = path[1:] + [path[0]]
                weights = weights[1:] + [weights[0]]
            return path, weights
        def find_sub_loops(start):
            def find_paths(origin, path, weights):
                if origin not in self.graph:
                    return # dead end
                for (destination,weight) in self.graph[origin]:
                    if destination in path:
                        weights[0] = weight # there may be multieple paths leading here, make sure we use the correct weight
                        loop = path[path.index(destination):]
                        loop, weights = sort_loop(loop, weights)
                        if loop not in [l.path for l in loops]:
                            loops.append(SimpleNamespace(path=loop, weights=weights))
                        break
                    else:
                        if weight == 0 and not include_zero_gain:
                            continue
                        find_paths(destination, path+[destination], weights+[weight])
            find_paths(start, [], [])
        for start in self.graph.keys():
            find_sub_loops(start)
        return loops


    def find_paths(self, from_node, to_node, include_zero_gain: bool = False):
        from_node = self._split_name(from_node)
        to_node = self._split_name(to_node)
        paths = []
        def find_paths(graph, origin, path, weights):
            if origin == to_node:
                paths.append(SimpleNamespace(path=path, weights=weights))
                return
            elif origin not in self.graph:
                return # dead end
            for (destination,weight) in graph[origin]:
                if destination in path:
                    continue # loop
                else:
                    if weight == 0 and not include_zero_gain:
                        continue
                    find_paths(graph, destination, path+[destination], weights+[weight])
        find_paths(self.graph, from_node, [from_node], [1])
        return paths


    def calculate_gain(self, from_node, to_node):
        
        def product(factors):
            p = 1
            for f in factors:
                p *= f
            return p

        def get_cofactor(excluded_nodes=[]):
            loops = self.find_loops(include_zero_gain=False)
            loop_count = len(loops)
            denom = 1
            sign = -1
            for order in range(1, loop_count+1):
                # calculate all possible n-tuples
                for loop_tuple_indices in itertools.combinations([i for i in range(loop_count)], order):
                    include = True
                    for li1 in range(len(loop_tuple_indices)):
                        # check if we have to exclude this loop due to unwanted nodes
                        for node in loops[loop_tuple_indices[li1]].path:
                            if node in excluded_nodes:
                                include = False
                        # check if we have to exclude this due to touching loops
                        for li2 in range(li1+1, len(loop_tuple_indices)):
                            for node in loops[loop_tuple_indices[li1]].path:
                                if node in loops[loop_tuple_indices[li2]].path:
                                    include = False
                    if include:
                        # calculate product of all loops in the tuple
                        gain = 1
                        for li1 in range(len(loop_tuple_indices)):
                            gain *= product(loops[loop_tuple_indices[li1]].weights)
                        denom += sign * gain
                sign = -sign
            return denom
        
        paths = self.find_paths(from_node, to_node, include_zero_gain=False)

        gain = 0
        for path in paths:
            gain += product(path.weights) / get_cofactor(path.path)
        gain /= get_cofactor()
        return gain


    def _split_name(self, name: "tuple[str,str]|str"):
        """
        Ensures the name is a tuple (group,name). If a string is given, it is interpreted
        group and name separated by group_name_separator; if group_name_separator is None,
        then the group is assumed to be None.
        """
        if isinstance(name, tuple) or isinstance(name, list):
            assert len(name)==2, 'Expecting name to be a 2-tuple'
            return name
        if self.group_name_separator is not None and isinstance(name, str) and self.group_name_separator in name:
            idx = name.index(self.group_name_separator)
            return (name[:idx], name[idx+1:])
        return (None, name)

    
    def _plot(self, graph: dict[tuple[str,str],list], name) -> Digraph:
        """ Create a graphviz Digraph """
        g = Digraph('G', filename=name)
        g.attr(**self.graph_attrs.graph)

        all_nodes = []
        all_groups = []
        for (src_group,src_name),dw in graph.items():
            all_nodes.append((src_group,src_name))
            all_groups.append(src_group)
            for ((dest_group,dest_name),_) in dw:
                all_nodes.append((dest_group,dest_name))
                all_groups.append(dest_group)
        
        for i,graphed_group in enumerate(set(all_groups)):
            if graphed_group is None:
                continue
            with g.subgraph(name=f'cluster_{i}') as gsub:
                gsub.attr(label=str(graphed_group), **self.graph_attrs.group)
                for (group,name) in all_nodes:
                    if group!=graphed_group:
                        continue
                    gsub.attr('node', **self.graph_attrs.node)
                    gsub.node(str((group,name)), label=name)
        
        for (group,name) in all_nodes:
            if group is not None:
                continue
            g.attr('node', **self.graph_attrs.node)
            g.node(str((group,name)), label=name)

        
        for source,destinations in graph.items():
            for (dest,weight) in destinations:
                g.attr('edge', **self.graph_attrs.edge)
                g.edge(str(source), str(dest), label=str(weight))
        
        return g
