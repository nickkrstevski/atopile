import logging
from contextlib import contextmanager
from pathlib import Path
from typing import List

from antlr4 import CommonTokenStream, FileStream

from atopile.model.model import EdgeType, Model, VertexType
from atopile.parser.AtopileLexer import AtopileLexer
from atopile.parser.AtopileParser import AtopileParser
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor

log = logging.getLogger(__name__)

def parse_file(path: Path) -> Model:
        input = FileStream(path)
        lexer = AtopileLexer(input)
        stream = CommonTokenStream(lexer)
        parser = AtopileParser(stream)
        tree = parser.file_input()
        return tree

class FromAtoBuilder(AtopileParserVisitor):
    def __init__(self, model: Model=None, path: List[Path]=None) -> None:
        super().__init__()

        if model is None:
            model = Model()
        self.model = model

        if path is None:
            path = []
        self._path = path

        self._parents = []

        # what we're currently building
        # use this to detect circular imports
        self._building_files = []

        # what we've already built
        # use this to ignore subsequent imports
        self._built_files = []

    @property
    def current_parent(self):
        return self._parents[-1]

    @contextmanager
    def parent(self, ref: str):
        self._parents.append(ref)
        yield
        self._parents.pop()

    @contextmanager
    def file_build(self, path: Path):
        if path.absolute() in self._building_files:
            raise RuntimeError(f"Circular import detected: {path}")
        path = path.absolute()
        self._parents.append(path)
        yield
        self._parents.pop()

    def find_file(self, filename: str) -> Tuple[str, Path]:
        ooscope_errors = []
        for path in self.path:
            full_path = path / filename
            if not full_path.is_relative_to(path):
                ooscope_errors.append(full_path)
                continue
            if full_path.exists():
                return full_path
        if ooscope_errors:
            raise FileNotFoundError(f"We could only find {filename} at {ooscope_errors}, which is above all search paths. The file must be within at least one search path.")
        raise FileNotFoundError(f"{filename}. this ")

    def build_from_filename(self, filename: str):
        """
        Start the build from the specified file expected within path.
        """
        path = self.find_file_in_path(filename)
        with self.file_build(path):
            tree = parse_file(path)

            self.model.new_vertex(VertexType.file, filename)
            self.model.data[ref] = {}

            self.current_parent = ref
            self.visit(tree)

    def visitImport_stmt(self, ctx: AtopileParser.Import_stmtContext):
        import_filename = ctx.STRING().getText().strip('"')

        path = self.build_root_path / import_filename
        if not path.exists():
            raise FileNotFoundError(path)

        if path in self.parsed_files:
            tree = self.parsed_files[path]
        else:
            tree = parse_file(path)
            self.parsed_files[path] = tree

            self.model.new_vertex(VertexType.file, import_filename)
            self.model.data[import_filename] = {}

        with self.parent(import_filename):
            import_ = super().visit(tree)

        to_import = ctx.name_or_attr().getText()
        graph_path, data_path = self.model.find_ref(to_import, import_filename)
        if data_path:
            raise RuntimeError(f"Cannot import data path {data_path}")

        self.model.new_edge(
            EdgeType.imported_to,
            graph_path,
            self.current_parent
        )

        return import_

    def define_block(self, ctx, block_type: VertexType):
        original_parent = self.current_parent
        name = ctx.name().getText()

        if ctx.OPTIONAL():
            block_path = self.model.new_vertex(
                block_type,
                name,
                option_of=self.current_parent
            )
        else:
            block_path = self.model.new_vertex(
                block_type,
                name,
                part_of=self.current_parent
            )

        self.model.data[block_path] = {}

        self.current_parent = block_path
        internals = super().visitChildren(ctx)
        self.current_parent = original_parent
        return internals

    def visitComponentdef(self, ctx: AtopileParser.ComponentdefContext):
        return self.define_block(ctx, VertexType.component)

    def visitModuledef(self, ctx: AtopileParser.ModuledefContext):
        return self.define_block(ctx, VertexType.module)

    def visitPindef_stmt(self, ctx: AtopileParser.Pindef_stmtContext):
        name = ctx.name().getText()
        pin_path = self.model.new_vertex(
            VertexType.pin,
            name,
            part_of=self.current_parent
        )
        self.model.data[pin_path] = {}

        return super().visitPindef_stmt(ctx)

    def visitSignaldef_stmt(self, ctx: AtopileParser.Signaldef_stmtContext):
        name = ctx.name().getText()
        signal_path = self.model.new_vertex(
            VertexType.signal,
            name,
            part_of=self.current_parent
        )
        self.model.data[signal_path] = {}

        return super().visitSignaldef_stmt(ctx)

    def visitConnect_stmt(self, ctx: AtopileParser.Connect_stmtContext):
        from_ref = ctx.name_or_attr(0).getText()
        to_ref = ctx.name_or_attr(1).getText()

        from_path, from_data_path = self.model.find_ref(from_ref, self.current_parent)
        to_path, to_data_path = self.model.find_ref(to_ref, self.current_parent)

        if from_data_path or to_data_path:
            raise AttributeError("Cannot connect to data object")

        self.model.new_edge(EdgeType.connects_to, from_path, to_path)

        return super().visitConnect_stmt(ctx)

    def visitWith_stmt(self, ctx: AtopileParser.With_stmtContext):
        with_ref = ctx.name_or_attr().getText()
        with_path, _ = self.model.find_ref(with_ref, self.current_parent)

        self.model.enable_option(with_path)

        return super().visitWith_stmt(ctx)

    def visitAssign_stmt(self, ctx:AtopileParser.Assign_stmtContext):
        assignee = ctx.name_or_attr(0).getText()
        if ctx.new_element():
            class_ref = ctx.new_element().name_or_attr().getText()
            class_path, _ = self.model.find_ref(class_ref, self.current_parent)
            # FIXME: this probably throws a dud error if the name is an attr
            instance_name = ctx.name_or_attr(0).name().getText()
            self.model.instantiate_block(class_path, instance_name, self.current_parent)
        else:
            if ctx.STRING():
                value = ctx.STRING().getText().strip("\"\'")

            elif ctx.NUMBER():
                value = float(ctx.NUMBER().getText())
            else:
                raise NotImplementedError("Only strings and numbers are supported")

            graph_path, existing_data_path, remaining_parts = self.model.find_ref(assignee, self.current_parent, return_unfound=True)
            data_path = existing_data_path + remaining_parts
            data = self.model.data[graph_path]
            for p in data_path[:-1]:
                data = data.setdefault(p, {})

            data[data_path[-1]] = value

        return super().visitAssign_stmt(ctx)
