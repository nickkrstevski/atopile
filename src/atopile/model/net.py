#%%
from typing import Iterable, Optional, AbstractSet, List

from atopile.model.model import  Model
from atopile.model.accessors import ModelVertexView, EdgeType, VertexType


#%%

class VertexViewGroup:
    def __init__(self, indicies: Iterable[int]) -> None:
        self.indicies = set(indicies)

def find_nets(model: Model) -> List[int]:
    # Create the nets
    electrical_graph = model.get_graph_view([EdgeType.connects_to])
    clusters = electrical_graph.connected_components(mode="weak")
    return [set(c) for c in clusters]

