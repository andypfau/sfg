from typing import Any



class Edge:
    
    def __init__(self, origin: Any, destination: Any, weight: Any = 1):
        self.origin, self.destination, self.weight = origin, destination, weight
    
    def __repr__(self) -> str:
        return f'Edge({self.origin},{self.destination},{self.weight})'


class Path:
    
    def __init__(self, nodes: list[Any], weights: list[Any], edges: list[Edge]):
        self.nodes, self.weights, self.edges = nodes, weights, edges
    
    def __repr__(self) -> str:
        return f'Path({self.nodes},{self.weights},{self.edges})'

    @property
    def gain(self) -> Any:
        product = 1
        for weight in self.weights:
            product *= weight
        return product
    
    def overlaps(self, other: Path) -> bool:
        for node in self.nodes:
            if node in other.nodes:
                return True
        return False
