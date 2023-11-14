"""
Walk the dm1 tree and create dm2 analogs.

Step 1 is to create hollow dm2 objects that have the same structure as dm1

Step 2 requires name resolution, which is a smidge tricky.
If we pass-down lexical scoping information as we walk the tree,
we can resolve all lexically scoped names, including references to supers.

However, we need this information for all objects in order to be able to "hop"
between scopes. For example, "a.b.c" is a reference to "c" in the scope of
"a.b", but from within a scope containing "a", we don't necessarily know that
"b" or "c" exist, we just (after step 1), know what "a" is.
"""

import logging
import collections
from pathlib import Path
from typing import Any, Iterable, Optional, Mapping

from attrs import define, resolve_types, field

from atopile.model2 import datamodel1 as dm1
from atopile.model2 import errors

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@define
class Base:
    src: Optional[dm1.Base] = field(default=None, kw_only=True, eq=False)


@define
class Link(Base):
    start_instance: "Object"
    start_node: "Object"
    end_instance: "Object"
    end_node: "Object"


@define
class Replace(Base):
    original: "Object"
    replacement: "Object"


@define
class Import(Base):
    what: "Object"


@define
class Object(Base):
    # these are populated by Scoop
    locals_: Optional[Mapping] = None
    supers: Optional[tuple["Object"]] = None

    # these are created by Scoop, for the next guy
    name_bindings: Optional[Mapping] = None
    closure: Optional[Mapping] = None


for cls in [Object, Link, Replace, Import]:
    resolve_types(cls)


MODULE = Object()
COMPONENT = Object(supers=(Object))


PIN = Object()
SIGNAL = Object()
INTERFACE = Object()


BUILTINS = {
    dm1.MODULE[-1]: MODULE,
    dm1.COMPONENT[-1]: COMPONENT,
    dm1.PIN[-1]: PIN,
    dm1.SIGNAL[-1]: SIGNAL,
    dm1.INTERFACE[-1]: INTERFACE,
}


class Scoop:
    """
    Scoop's job is to walk the tree of dm1 objects, creating
    Frames and empty dm2 analog Objects for each dm1 object
    """

    def __init__(self) -> None:
        self.builtins_map = collections.ChainMap(BUILTINS)

        self.dm1_id_object_map: dict[int, Object] = {
            id(obj): obj for obj in self.builtins_map.values()
        }
        self.dm1_id_name_binding_map: dict[int, dict[str, Any]] = {}
        self.dm1_id_closure_map: dict[int, collections.ChainMap[dm1.Ref, Any]] = {}
        self.collected_errors: list[errors.AtoError] = []

    def collect_error(self, error: errors.AtoError):
        self.collected_errors.append(error)

    def visit(self, dm1_obj: dm1.Object, closure: collections.ChainMap) -> None:
        assert id(dm1_obj) not in self.dm1_id_object_map

        self.dm1_id_object_map[id(dm1_obj)] = Object(src=dm1_obj)
        binding_map = self.dm1_id_name_binding_map[id(dm1_obj)] = dict(
            filter(lambda x: x[0] is not None, dm1_obj.locals_)
        )
        self.dm1_id_closure_map[id(dm1_obj)] = closure

        child_closure = closure.new_child(binding_map)
        for _, child in dm1_obj.locals_:
            if isinstance(child, dm1.Object):
                self.visit(child, child_closure)

    def visit_roots(self, objs: Iterable[dm1.Object]) -> None:
        """
        Expected to be called on an iterable of file objects, which are generally the roots of these trees
        """
        for obj in objs:
            self.visit(obj, self.builtins_map)
        if self.collected_errors:
            raise ExceptionGroup(
                "Errors occurred while visiting roots", self.collected_errors
            )


class Lofty:
    """
    Lofty's job is to walk the tree, filling in the dm2 objects
    """

    def __init__(
        self,
        dm1_id_object_map: dict[int, Object],
        dm1_id_name_binding_map: dict[int, dict[str, Any]],
        dm1_id_closure_map: dict[int, collections.ChainMap[dm1.Ref, Any]],
        search_paths: Iterable[Path],
        path_dm1_map: dict[Path, dm1.Object],
    ) -> None:
        # these name-bindings and lexical scopes are created by Scoop
        # their keys are the names for the given scope, and the values
        # are the dm1 objects
        self.dm1_id_object_map = dm1_id_object_map
        self.dm1_id_name_binding_map = dm1_id_name_binding_map
        self.dm1_id_closure_map = dm1_id_closure_map
        self.search_paths = search_paths
        self.path_dm1_map = path_dm1_map

        self.errors: list[errors.AtoError] = []

    def collect_error(self, error: errors.AtoError) -> errors.AtoError:
        """
        Collect up the errors so non-fatal errors can be reported collectively, reducing noise
        This also returns the error, so it can be raised on the spot if desired
        """
        self.errors.append(error)
        return error

    def search_file_path(self, dep_name: str) -> Path:
        for search_path in self.search_paths:
            candidate_path = search_path.joinpath(dep_name)
            if candidate_path.exists():
                return candidate_path.resolve().absolute()
        raise errors.AtoImportNotFoundError(f"Could not find import: {dep_name}")

    def find_inside_mapping_dm1(self, ref: dm1.Ref, dm1_obj: dm1.Object, mapping: Mapping) -> Any:
        if not ref:
            return dm1_obj

        try:
            return mapping[ref]
        except KeyError:
            pass

        for i in range(1, len(ref)):
            ref_fragment = ref[:-i]
            remaining_ref = ref[-i:]
            try:
                matched_obj = mapping[ref_fragment]
                if not isinstance(matched_obj, dm1.Object):
                    raise TypeError

                return self.find_inside_dm1(
                    remaining_ref,
                    matched_obj,
                )
            except KeyError:
                continue
        raise KeyError

    def find_inside_dm1(self, ref: dm1.Ref, dm1_obj: dm1.Object) -> Any:
        if not ref:
            return dm1_obj

        dm1_name_binding_map = self.dm1_id_name_binding_map[id(dm1_obj)]
        return self.find_inside_mapping_dm1(ref, dm1_obj, dm1_name_binding_map)

    def find_in_scope_dm1(self, ref: dm1.Ref, dm1_obj: dm1.Object) -> Any:
        if not ref:
            return dm1_obj

        dm1_closure = self.dm1_id_closure_map[id(dm1_obj)]
        dm1_name_binding_map = self.dm1_id_name_binding_map[id(dm1_obj)]
        internal_name_map = dm1_closure.new_child(dm1_name_binding_map)

        return self.find_inside_mapping_dm1(ref, dm1_obj, internal_name_map)

    def visit_roots(self, dm1_objs: Iterable[dm1.Object]) -> Iterable[Object]:
        builtins_closure = collections.ChainMap(BUILTINS)
        for dm1_obj in dm1_objs:
            yield self.visit_dm1_Object(dm1_obj, builtins_closure)

    def visit_generic(self, thing: Any, dm2_closure: collections.ChainMap) -> Any:
        """
        Handle visiting something - it'll work out where to dispatch the call.
        """
        match type(thing):
            case dm1.Object:
                return self.visit_dm1_Object(thing, dm2_closure)
            case dm1.Link:
                return self.visit_dm1_Link(thing, dm2_closure)
            case dm1.Replace:
                return self.visit_dm1_Replace(thing, dm2_closure)
            case dm1.Import:
                return self.visit_dm1_Import(thing, dm2_closure)
            case _:
                return self.visit_default(thing, dm2_closure)

    def visit_default(self, thing: Any, dm2_closure: collections.ChainMap) -> Any:
        """
        Do this if nothing else
        """
        return thing

    def visit_dm1_Object(
        self, dm1_obj: dm1.Object, dm2_closure: collections.ChainMap
    ) -> Object:
        """
        Handle visiting a dm1.Object
        """
        dm2_obj = self.dm1_id_object_map[id(dm1_obj)]

        # find the objects representing the supers
        # FIXME: this should do an actual lookup, not just a flat/dumb ref-based one
        # this should only be an issue with multi-part refs
        dm2_obj.supers = tuple(
            self.lookup_dm2_obj_by_ref(dm1_obj, super_ref)
            for super_ref in dm1_obj.supers
        )
        dm2_obj.name_bindings = {}
        dm2_obj.closure = dm2_closure.new_child(dm2_obj.name_bindings)
        dm2_obj.locals_ = tuple(
            (name, self.visit_generic(obj, dm2_obj.closure)) for name, obj in dm1_obj.locals_
        )
        dm2_obj.name_bindings.update(
            dict(
                filter(lambda x: x[0] is not None, dm2_obj.locals_)
            )
        )
        return dm2_obj

    def visit_dm1_Link(
        self, dm1_thing: dm1.Link, dm2_closure: collections.ChainMap
    ) -> Link:
        """
        Handle visiting a dm1.Link
        """
        raise NotImplementedError

    def visit_dm1_Replace(
        self, dm1_thing: dm1.Replace, dm2_closure: collections.ChainMap
    ) -> Replace:
        """
        Handle visiting a dm1.Replace
        """
        raise NotImplementedError

    def visit_dm1_Import(
        self, dm1_thing: dm1.Import, dm2_closure: collections.ChainMap
    ) -> Import:
        """
        Handle visiting a dm1.Import
        """
        raise NotImplementedError
