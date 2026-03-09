from __future__ import annotations
from .trivial import Edge, Path
from .graphs_presets import GraphAttrPresets
from graphviz import Digraph
from typing import Any



class DirectedWeightedGraph:

    
    def __init__(self, group_name_sep: "str|None" = None):
        self._edges: list[Edge] = []
        self.group_name_sep = group_name_sep
        self.graph_attrs = GraphAttrPresets.SfgDefault


    @property
    def edges(self) -> list[Edge]:
        """ Returns all edges. """
        return list([e for e in self._edges])


    def add(self, origin: Any, destination: Any = None, weight: Any = 1):
        """ Add an edge from node <origin> to node <destination> with weight <weight>. """
        self._edges.append(Edge(origin, destination, weight))


    def remove_zeros(self):
        """ Remove all edges that have weight 0. """
        self._edges = list([edge for edge in self._edges if edge.weight != 0])


    def find_paths(self, origin: Any, destination: Any) -> list[Path]:
        """ Find all paths from node <origin> to node <destination>. """

        all_origins = [edge.origin for edge in self._edges]
        all_destinations = [edge.destination for edge in self._edges]
        
        if origin not in all_origins:
            raise ValueError(f'Origin node <{origin}> not found in graph')
        if destination not in all_destinations:
            raise ValueError(f'Destination node <{destination}> not found in graph')

        paths: list[Path] = []
        def find_paths(current_node, accumulated_path, accumulated_weights, accumulated_edges):
            nonlocal paths, destination
            if current_node == destination:
                paths.append(Path(accumulated_path, accumulated_weights, accumulated_edges))
                return
            elif current_node not in all_origins:
                return  # dead end
            for edge in [edge for edge in self._edges if edge.origin==current_node]:
                if edge.destination in accumulated_path:
                    continue  # loop
                find_paths(edge.destination, [*accumulated_path,edge.destination], [*accumulated_weights,edge.weight], [*accumulated_edges,edge])
        find_paths(origin, [origin], [], [])
        return paths


    def find_loops(self) -> list[Path]:
        """ Find all lopos in the graph. """
        
        all_origins = [edge.origin for edge in self._edges]
        
        loops: list[Path] = []
        def find_sub_loops(origin):
            nonlocal loops, all_origins
            def find_loop_paths(current_node, accumulated_path, accumulated_weights, accumulated_edges):
                nonlocal loops, all_origins
                if current_node not in all_origins:
                    return  # dead end
                for edge in [edge for edge in self._edges if edge.origin==current_node]:
                    if edge.destination in accumulated_path:  # a loop!
                        
                        # cut out the path that is the actual loop
                        idx = accumulated_path.index(edge.destination)
                        assert len(accumulated_path) > idx
                        loop_path = [*accumulated_path[idx+1:], edge.destination]
                        loop_edges = [*accumulated_edges[idx:], edge]
                        loop_weights = [*accumulated_weights[idx:], edge.weight]
                        assert len(loop_path) == len(loop_weights)
                        
                        if len(loop_path) >= 2:
                            # cycle the path until it starts with the lowest node
                            lowest_node = min(loop_path)
                            while loop_path[0] != lowest_node:
                                loop_path = [loop_path[-1], *loop_path[:-1]]
                                loop_edges = [loop_edges[-1], *loop_edges[:-1]]
                                loop_weights = [loop_weights[-1], *loop_weights[:-1]]

                        if loop_path not in [path.nodes for path in loops]:
                            loops.append(Path(loop_path, loop_weights, loop_edges))
                    else:
                        find_loop_paths(edge.destination, [*accumulated_path,edge.destination], [*accumulated_weights,edge.weight], [*accumulated_edges,edge])
            find_loop_paths(origin, [origin], [], [])
        for origin in all_origins:
            find_sub_loops(origin)
        
        return loops


    def print(self, show_trivial_weights: bool = False, return_str: bool = False) -> str|None:
        lines = []
        
        for edge in self._edges:
            if edge.weight == 0:
                if show_trivial_weights:
                    lines.append(f'[{edge.origin} -- 0 --> {edge.destination}]')
                else:
                    pass  # do not show at all
            elif (edge.weight == 1) and (not show_trivial_weights):
                lines.append(f'{edge.origin} ===> {edge.destination}')
            else:
                lines.append(f'{edge.origin} == {edge.weight} ==> {edge.destination}')
        
        s = '\n'.join(lines)
        if return_str:
            return s
        else:
            print(s)
            return None


    def _plot(self, edges: list[Edge], name: str, show_unity_weights: bool = True) -> Digraph:

        def split_name(name: "tuple[str,str]|str"):
            if isinstance(name, tuple) or isinstance(name, list):
                assert len(name)==2, 'Expecting name to be a 2-tuple'
                return tuple(name)  # already a tuple
            if self.group_name_sep is not None and isinstance(name, str) and self.group_name_sep in name:
                idx = name.index(self.group_name_sep)
                return (name[:idx], name[idx+1:])
            return (None, name)
        
        g = Digraph('G', filename=name)
        g.attr(**self.graph_attrs.graph)

        all_nodes = set()
        all_groups = set()
        for edge in edges:
            for node in [edge.origin, edge.destination]:
                (group, name) = split_name(node)
                all_nodes.add((group, name))
                all_groups.add(group)
        
        for i,graphed_group in enumerate(all_groups):
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

        
        for edge in edges:
            g.attr('edge', **self.graph_attrs.edge)
            
            if (not show_unity_weights) and (edge.weight == 0):
                continue
            elif (not show_unity_weights) and (edge.weight == 1):
                label = None
            else:
                label = str(edge.weight)
            g.edge(str(split_name(edge.origin)), str(split_name(edge.destination)), label=label)
        
        return g