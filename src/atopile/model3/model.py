from typing import Union
from atopile.parser.AtopileParser import AtopileParser


class BaseView:
    def __init__(self, source, parent: "BlockView") -> None:
        self._source = source
        self._parent = parent

    @property
    def parent(self) -> "BlockView":
        return self._parent

    @property
    def parents(self) -> list["BlockView"]:
        if self.parent is None:
            return []
        return [self.parent] + self.parent.parents


class DeclarationView(BaseView):
    VariableSrcTypes = AtopileParser.Assign_stmtContext
    _source: VariableSrcTypes


class BlockView(BaseView):
    BlockSrcTypes = Union[
        AtopileParser.ComponentdefContext,
        AtopileParser.ModuledefContext,
        AtopileParser.File_inputContext
    ]
    _source: BlockSrcTypes

    @property
    def name(self) -> str:
        return self._source.name().getText()

    @property
    def is_optional(self) -> bool:
        return bool(self._source.OPTIONAL())

    @property
    def parent(self) -> "BlockView":
        return self._parent

    @property
    def parents(self) -> list["BlockView"]:
        if self.parent is None:
            return []
        return [self.parent] + self.parent.parents

    @property
    def path_as_views(self) -> list[BaseView]:
        return self.parents + [self]

    @property
    def path(self) -> str:
        return "/".join(p.name for p in self.path_as_views)

    def is_instance_of(self, block: "BlockView") -> bool:
        return self in block.parents


class ElectricalNodeView(BaseView):
    ElectricalNodeSrcTypes = Union[
        AtopileParser.Pindef_stmtContext,
        AtopileParser.Signaldef_stmtContext
    ]
    _source: ElectricalNodeSrcTypes

    def find_connected_nodes(self) -> list["ElectricalNodeView"]:
        raise NotImplementedError()
