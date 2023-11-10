import logging
import typing
from itertools import chain

from atopile.model2 import errors
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.parser.AtopileParser import AtopileParser as ap
from atopile.model2.parse import ParserRuleContext
from pathlib import Path

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class ImportWalker(AtopileParserVisitor):
    def __init__(self) -> None:
        super().__init__()
        self._imports: set[str] = set()

    def visitString(self, ctx: ap.StringContext) -> str:
        return ctx.getText().strip("\"'")

    def visitImport_stmt(self, ctx: ap.Import_stmtContext):
        self._imports.add(self.visit(ctx.string()))

    @classmethod
    def find_deps(cls, ctx: ParserRuleContext):
        self = cls()
        self.visit(ctx)
        return self._imports


class PathFinder:
    def __init__(self, search_paths: typing.Iterable[Path]) -> None:
        self._search_paths: typing.Iterable[Path] = search_paths

    def find(self, cwd: Path, dep_name: str) -> Path:
        for search_path in chain([cwd], self._search_paths):
            candidate_path = search_path.joinpath(dep_name)
            if candidate_path.exists():
                return candidate_path.resolve().absolute()
        raise errors.AtoImportNotFoundError(f"Could not find import: {dep_name}")

    def glob(self, glob_str: str) -> typing.Iterable[Path]:
        for search_path in self._search_paths:
            for candidate_path in search_path.glob(glob_str):
                yield candidate_path.resolve().absolute()


T = typing.TypeVar("T")

class DependencySolver(typing.Generic[T]):
    def __init__(self) -> None:
        self._dependency_tree: dict[T, set[T]] = {}

    @classmethod
    def from_asts(
        cls, finder: typing.Callable[[T, str], T], asts: dict[T, ParserRuleContext]
    ) -> "DependencySolver":
        self = cls()
        self._dependency_tree = {}
        for path, ast in asts.items():
            self._dependency_tree[path] = set()
            for dep_name in ImportWalker.find_deps(ast):
                abs_path = finder(path, dep_name)
                self._dependency_tree[path].add(abs_path)
        self.check_for_cycles()
        return self

    @classmethod
    def from_dm_and_path(cls, dm: "DependencySolver", path: T) -> "DependencySolver":
        self = cls()
        self._dependency_tree = {}
        def visit(path):
            self._dependency_tree[path] = dm._dependency_tree[path]
            for dep in dm._dependency_tree[path]:
                visit(dep)
        visit(path)
        return self

    def check_for_cycles(self):
        """
        Check for cycles in the dependency tree.
        """
        checked = set()

        def visit(path: T, stack: typing.Optional[tuple[T]] = None):
            if path in checked:
                return

            if stack is None:
                stack = tuple()

            if path in stack:
                circle = stack[stack.index(path) :] + (path,)
                friendly_circle = " -> ".join(str(p) for p in circle)
                raise errors.AtoCircularDependencyError(
                    f"Circular dependency detected: {friendly_circle}"
                )

            for dep in self._dependency_tree.get(path, ()):
                visit(dep, stack + (path,))

            checked.add(path)

        for path in self._dependency_tree:
            visit(path)

    def buildable(self, complete: typing.Iterable[T]) -> typing.Iterable[T]:
        """
        Get the buildable paths from the dependency tree.
        """

        for candidate, candidate_deps in self._dependency_tree.items():
            if candidate in complete:
                continue
            residual_deps = candidate_deps - set(complete)
            if not residual_deps:
                yield candidate

    def build_order(self) -> typing.Iterable[T]:
        """
        Get the build order from the dependency tree.
        """
        complete = set()
        while len(complete) != len(self._dependency_tree):
            buildable = list(self.buildable(complete))
            if not buildable:
                leftovers = set(self._dependency_tree) - complete
                friendly_leftovers = ", ".join(map(str, leftovers))
                raise errors.AtoCompileError(
                    "We were unable to find a way to build everything."
                    f" {friendly_leftovers} remains un-built."
                )
            for path in buildable:
                yield path
                complete.add(path)
