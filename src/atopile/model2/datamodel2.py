"""
This datamodel performs:
    - name resolution
    - type checking
    - linking both between objects and files

This happens as a two step process:
    1. Create all the objects of the datamodel
    2. Link the objects together datamodel
"""

import logging
import typing
from pathlib import Path
from typing import Any, Iterable, Optional

from attrs import define, field, resolve_types

from atopile.model2 import datamodel1 as dm1
from atopile.model2 import errors

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@define
class Link:
    start_instance: "Object"
    start_node: "Object"
    end_instance: "Object"
    end_node: "Object"


@define
class Replace:
    original: "Object"
    replacement: "Object"


@define
class Import:
    what: "Object"


@define
class Object:
    supers: tuple["Object"] = field(factory=list)
    locals_: tuple[tuple[dm1.Type, Optional[tuple[str]], Any]] = field(factory=tuple)


for cls in [Object, Link, Replace, Import]:
    resolve_types(cls)


MODULE = Object()
COMPONENT = Object(supers=(Object))


PIN = Object()
SIGNAL = Object()
INTERFACE = Object()


def create_objects(dm1_trees: Iterable[dm1.Object]) -> dict[int, Object]:
    """
    Create a superset of all the objects possibly in the datamodel, but leaves them empty.
    Linking will happen in another pass.
    """
    objs = {}
    for src in dm1_trees:
        objs.update(
            {
                id(src): Object(),
                **create_objects(
                    filter(lambda x: isinstance(x[2], dm1.Object), src.locals_)
                ),
            }
        )
    return objs


BUILTINS = {
    dm1.MODULE[-1][0]: MODULE,
    dm1.COMPONENT[-1][0]: COMPONENT,
    dm1.PIN[-1][0]: PIN,
    dm1.SIGNAL[-1][0]: SIGNAL,
    dm1.INTERFACE[-1][0]: INTERFACE,
}


NULL_OBJECT = Object()


class Lofty:
    """
    Builds the dm2 trees import and and objects
    """

    def __init__(self) -> None:
        self._search_paths = typing.Iterable[Path] = []
        self.dm1_files: dict[Path, dm1.Object] = {}
        self.dm2_objs: dict[int, Object] = {}
        self.errors: list[errors.AtoError] = []

    def collect_error(self, error: errors.AtoError):
        self.errors.append(error)

    def search_file_path(self, dep_name: str) -> Path:
        for search_path in self._search_paths:
            candidate_path = search_path.joinpath(dep_name)
            if candidate_path.exists():
                return candidate_path.resolve().absolute()
        raise errors.AtoImportNotFoundError(f"Could not find import: {dep_name}")

    def get_name_in_scope(self, scope: tuple[dm1.Object], name: str) -> Optional[Object]:
        for obj in scope:
            if name in obj.locals_:
                return obj.locals_[name]

    def get_name_in_supers(self, obj: dm1.Object, name: str) -> Optional[Object]:
        for super_ref in obj.supers:
            super_ = self.
            if name in super_.locals_:
                return super_.locals_[name]

    def resolve_name(self, scope: tuple[dm1.Object], name: str) -> tuple[Object, bool]:
        """
        Takes a name and resolves it to a pointer to the Object that represents it.
        Returns that points and a bool indicating whether it was found in the current scope or super's scopes
        """
        for obj in scope:
            if name in obj.locals_:
                return obj.locals_[name], True
        for super_ in obj.supers:
            pass
        raise errors.AtoKeyError(f"'{name}' not in scope")

    def resolve_reference(
        self, scope: tuple[dm1.Object], reference: dm1.Ref
    ) -> tuple[Object, Optional[Object], Optional[Object]]:
        """
        Takes a reference as a tuple of (attr, attr, attr, ...)
        and resolves it to pointer to the Objects that represent:
            - the thing
            - the object that thing is in (if applicable)
            - the super of that object which defines the thing (if applicable)
        """

        return self.resolve_references(scope, reference)[-1]

    def visit_import(self, scope: tuple[dm1.Object], ctx: dm1.Import) -> Import:
        path = self.search_file_path(ctx.from_)
        _scope = (self.dm1_files[path],)
        return Import(
            what=self.resolve_reference(_scope, ctx.what)[0],
        )

    def visit_replace(self, scope: tuple[dm1.Object], ctx: dm1.Replace) -> Replace:
        return Replace(
            original=self.resolve_reference(scope, ctx.original)[0],
            replacement=self.resolve_reference(scope, ctx.replacement)[0],
        )

    def visit_link(self, scope: tuple[dm1.Object], ctx: dm1.Link) -> Link:
        start_node, start_obj, _ = self.resolve_reference(scope, ctx.source)
        end_node, end_obj, _ = self.resolve_reference(scope, ctx.source)
        return Link(
            start_obj=start_obj,
            start_node=start_node,
            end_obj=end_obj,
            end_node=end_node,
        )

    def visit_object(self, scope: tuple[dm1.Object], ctx: dm1.Object) -> Object:
        internal_scope = scope + (ctx,)
        obj = self.dm2_objs[id(ctx)]
        obj.supers = (tuple(self.resolve_reference(ref)[0] for ref in ctx.supers),)
        obj.locals_ = (
            tuple(
                (
                    type_,
                    name,
                    self.visit(internal_scope, value),
                )
                for type_, name, value in ctx.locals_
            ),
        )
        return obj

    def visit(self, scope: tuple[dm1.Object], ctx) -> Object:
        match ctx:
            case dm1.Object:
                return self.visit_object(scope, ctx)
            case dm1.Import:
                return self.visit_import(scope, ctx)
            case dm1.Replace:
                return self.visit_replace(scope, ctx)
            case dm1.Link:
                return self.visit_link(scope, ctx)
            case _:
                raise TypeError(f"Unknown type: {type(ctx)}")


class Wendy:
    """
    Wendy can perform in-scope name resolution, but has no concept of supers.
    She's responsible for creating dm2 import objects and placing dm2 references
    """
    def __init__(self) -> None:
        self.dm1_files: dict[Path, dm1.Object] = {}
        self.dm2_objs: dict[int, Object] = {}
        self.errors: list[errors.AtoError] = []


def build(srcs: dict[Path, dm1.Object]) -> Object:
    objs = create_objects(srcs.values())
    link()
