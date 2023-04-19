"""
This datamodel represents the lowest level of the circuit compilation chain, closest to the hardware.

"""

from typing import List, Optional

import igraph as ig
from attrs import define, field

@define
class GraphNode:
    """
    Represents a node(/vertex) in a graph
    """
    graph: ig.Graph
    id: str

@define
class EtherealPin:
    """
    Represents a pin that is not physically present on the board, any feature or component
    """
    name: str
    type: GraphNode
    electrical_node: GraphNode

@define
class Pin(EtherealPin):
    """
    Represents a pin that is phyically present on a device or circuit module

    :param pad: the reference the pad on the package's footprint
    """
    pad: str

@define
class Package:
    """
    Represents a package a component physically comes in.
    eg. QFN-48, SOIC-8, etc...
    """
    name: str
    footprint: str
    pins: List[Pin] = field(factory=list)

@define
class Block:
    """
    Represent a logical block of the circuit, whether that's a component, a feature of a component or a circuit module
    If a package is specified for a block, subblocks cannot have packages
    """
    name: str
    type: GraphNode
    heirarchy_node: GraphNode
    ethereal_pins: List[EtherealPin] = field(factory=list)
    blocks: List['Block'] = field(factory=list)
    package: Optional[Package] = field(default=None)
