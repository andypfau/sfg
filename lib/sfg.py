from .trivial import Edge, Path
from .dir_weight_graph import DirectedWeightedGraph
from graphviz import Digraph
from types import SimpleNamespace
from typing import Any
import itertools


class SFG(DirectedWeightedGraph):


    def __init__(self, group_name_sep: "str|None" = None):
        """
        Args:
            group_name_sep: any node names provided as string will be split at this separator into (group,node).
                If you do not want to  get automatic splitting, leave it as None.
        """
        super().__init__(group_name_sep=group_name_sep)


    def plot(self, name: str = 'SFG', show_unity_weights: bool = True) -> Digraph:
        """
        Return a graphviz.Digraph of the SFG.
        
        Args:
            name:               name of the graphviz Digraph; only relevant if you want to export this later.
            show_unity_weights: if False, edge labels for weights of 1 are hidden.
        """
        return self._plot(self._edges, name, show_unity_weights)


    def plot_loops(self, name_prefix: str = 'SFG', find_kwargs: dict = {}, plot_kwargs: dict = {}) -> list[Digraph]:
        """
        Return a list graphviz.Digraph, one for each closed loop in the SFG.
        
        Args:
            name_prefix: name prefix for the graphviz Digraphs (suffix is just an int starting at 0);
                only relevant if you want to export them later.
            find_kwargs: keyword arguments for the find_loops() method.
            plot_kwargs: keyword arguments for the plot() method.
        """
        paths = self.find_loops()
        return [self._plot(path.edges, f'{name_prefix}{i}', **plot_kwargs) for i,path in enumerate(paths)]


    def plot_paths(self, origin: Any, destination: Any, name_prefix: str = 'SFG', find_kwargs: dict = {}, plot_kwargs: dict = {}) -> list[Digraph]:
        """
        Return a list graphviz.Digraph, one for each forward path between two specified nodes in the SFG.
        
        Args:
            origin:      node name where the path starts.
            destination: node name where the path ends.
            name_prefix: name prefix for the graphviz Digraphs (suffix is just an int starting at 0);
                           only relevant if you want to export them later.
            find_kwargs: keyword arguments for the find_loops() method.
            plot_kwargs: keyword arguments for the plot() method.
        
        Names can be provided the same way as for the `add()` method.
        """
        paths = self.find_paths(origin=origin, destination=destination)
        return [self._plot(path.edges, f'{name_prefix}{i}', **plot_kwargs) for i,path in enumerate(paths)]


    def add(self, origin: Any, destination: Any = None, weight: Any = 1):
        """ Add an edge from node <origin> to node <destination> with weight <weight>. """
        super().add(origin=origin, destination=destination, weight=weight)


    def remove_zeros(self):
        """ Remove all edges that have weight 0. """
        super().remove_zeros()


    def find_paths(self, origin: Any, destination: Any) -> list[Path]:
        """ Find all paths from node <origin> to node <destination>. """
        return super().find_paths(origin=origin, destination=destination)


    def find_loops(self) -> list[Path]:
        """ Find all lopos in the graph. """
        return super().find_loops()


    def print(self, show_trivial_weights: bool = False, return_str: bool = False) -> str|None:
        return super().print(show_trivial_weights=show_trivial_weights, return_str=return_str)


    def gain(self, origin: any, destination: any) -> any:
        """
        Calculate the gain from one node to another node in the SFG.

        Args:
            origin:      node name where the path starts.
            destination: node name where the path ends.

        Names can be provided the same way as for the `add()` method.

        Returns:
            The calculated gain, i.e. the appropriate sums and products of the weights along
                the path. Thus, the return type is determined by the types of the weights.
                E.g. if all weights are floats, this method returns a float. If any of them
                are sympy expressions, the return type is also a sympy expression.
        """
        
        forward_path = self.find_paths(origin, destination)
        if len(forward_path) < 1:
            raise ValueError(f'No path from <{origin}> to <{destination}>')
        all_loops = self.find_loops()
        
        numerator = 0
        for path in forward_path:
            gain = 1
            for weight in path.weights:
                gain *= weight
            cofactor = self._get_determinant(all_loops, excluded_nodes=path.nodes)
            numerator += gain * cofactor
        
        determinant = self._get_determinant(all_loops)
        
        return numerator / determinant
    
    
    def _get_nontouching_loops(self, loops: list[Path], tuple_size: int) -> list[list[Path]]:
        assert tuple_size >= 1
        if tuple_size == 1:
            return [[loop] for loop in loops]
        result = []
        for loop_tuple in itertools.combinations(loops, tuple_size):
            overlapping = False
            for i in range(0, tuple_size-1):
                for j in range(i+1, tuple_size):
                    if loop_tuple[i].overlaps(loop_tuple[j]):
                        overlapping = True
                        break
            if not overlapping:
                result.append(loop_tuple)
        return result


    def _get_determinant(self, loops: list[Path], excluded_nodes: list[any] = []) -> any:
        determinant = 1
        for n in range(1, len(loops)+1):
            accu = 0
            for nontouching_loops in self._get_nontouching_loops(loops, n):
                product = 1
                for path in nontouching_loops:
                    for node in path.nodes:
                        if node in excluded_nodes:
                            product = 0  # loop touches -> ignore
                            break
                    for weight in path.weights:
                        product *= weight
                accu += product
            sign = +1 if (n % 2 == 0) else -1
            determinant += accu * sign
        return determinant
