"""
This file holds the AST for .ato files and parsed elements
"""

from attrs import define
from typing import List, Tuple, Optional

@define
class ASTNode:
    source: str
    locn_start: int
    locn_end: int

@define
class Reference(ASTNode):
    path: List[str]

@define
class Pin(ASTNode):
    name: str
    connections: List[Reference]

@define
class Function(ASTNode):
    eqn: str

@define
class Assignment(ASTNode):
    asignee: str

@define
class Limit(ASTNode):
    eqn: str

@define
class State(ASTNode):
    name: str
    named_elements: List[ASTNode]
    elements: List[ASTNode]

@define
class Argument(ASTNode):
    name: str
    unit: str

@define
class Feature(ASTNode):
    name: str
    named_elements: List[ASTNode]
    elements: List[ASTNode]

@define
class Component(ASTNode):
    name: str
    named_elements: List[ASTNode]
    elements: List[ASTNode]

@define
class Connection(ASTNode):
    pins: List[Pin]

@define
class File(ASTNode):
    source: str
    named_elements: List[ASTNode]
    elements: List[ASTNode]
