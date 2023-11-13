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
from collections import ChainMap, defaultdict
from pathlib import Path
from typing import Any, Iterable, Optional, Mapping

from attrs import define, resolve_types, field

from atopile.model2 import datamodel1 as dm1
from atopile.model2 import errors

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@define
class Link:
    start_instance: "Object"
    start_node: "Object"  # FIXME: I'm not sure how this works with replacement operators being applied afterwards, particularly with nested links
    end_instance: "Object"
    end_node: "Object"


@define
class Replace:
    original: "Object"
    replacement: "Object"


@define
class Import:
    what: "Object"


ScopeMapping = Mapping[int | str, Any]

@define
class Frame:
    """
    The Frame type acts as an intermediate between dm1 and dm2 objects
    Specifically, it has a map of name-bindings and a lexical scope,
    which are both pointing back to dm1 objects.

    Frames are created for each dm1 tree, and are used to create the dm2 tree

    name_bindings provides a map from all the named locals in a dm1 object to their values
    lexical_scope provides the scope the dm1 object has. It's perhaps more accurately a closure
    """
    name_bindings: Mapping
    lexical_scope: Mapping

@define
class Object:
    # these are populated by Wendy
    locals_: Optional[Mapping] = None
    supers: Optional[tuple["Object"]] = None

    # these are created by Wendy, for the next guy
    name_bindings: Optional[Mapping] = None
    lexical_scope: Optional[Mapping] = None

for cls in [Object, Link, Replace, Import]:
    resolve_types(cls)


MODULE = Object()
COMPONENT = Object(supers=(Object))


PIN = Object()
SIGNAL = Object()
INTERFACE = Object()


BUILTINS = {
    dm1.MODULE[-1][0]: MODULE,
    dm1.COMPONENT[-1][0]: COMPONENT,
    dm1.PIN[-1][0]: PIN,
    dm1.SIGNAL[-1][0]: SIGNAL,
    dm1.INTERFACE[-1][0]: INTERFACE,
}


def create_name_binding_map(obj: Iterable[tuple[Optional[dm1.Ref], Any]]) -> Mapping:
    """
    Find all name-bindings, from a paired tuple of (name, obj)
    """
    name_bindings = {}
    for ref, value in obj:
        if ref is not None:
            subdict = name_bindings
            for name in ref[:-1]:
                subdict = subdict.setdefault(name, {})
            subdict[ref[-1]] = value
    return name_bindings


class Wendy:
    """
    Wendy's job is to walk the tree of dm1 objects, creating
    Frames and empty dm2 analog Objects for each dm1 object
    """
    def __init__(self) -> None:
        self.dm1_id_frame_map: dict[int, Frame] = {}
        self.dm1_id_object_map: dict[int, Object] = defaultdict(Object)
        self.collected_errors: list[errors.AtoError] = []

    def collect_error(self, error: errors.AtoError):
        self.collected_errors.append(error)

    def visit(self, obj: dm1.Object, dm1_lexical_scope: ChainMap) -> None:
        assert id(obj) not in self.dm1_id_object_map

        dm1_name_bindings = create_name_binding_map(obj.locals_)

        # create the name-bindings and lexical scope for this object
        self.dm1_id_frame_map[id(obj)] = Frame(dm1_name_bindings, dm1_lexical_scope)

        # create the hollow dm2 object
        self.dm1_id_object_map[id(obj)] = Object()

        # visit all of the children
        child_dm1_lexical_scope = dm1_lexical_scope.new_child(dm1_name_bindings)
        for _, local in obj.locals_:
            if isinstance(local, dm1.Object):
                self.visit(
                    local,
                    child_dm1_lexical_scope,
                )

    def visit_roots(self, objs: Iterable[dm1.Object]) -> None:
        """
        Expected to be called on an iterable of file objects, which are generally the roots of these trees
        """
        for obj in objs:
            self.visit(obj, BUILTINS)


class Lofty:
    """
    Lofty's job is to walk the tree, filling in the dm2 objects
    """
    def __init__(
        self,
        dm1_id_frame_map: dict[int, Frame],
        dm1_id_object_map: dict[int, Object],
        search_paths: Iterable[Path],
        path_dm1_map: dict[Path, dm1.Object],
    ) -> None:
        # these name-bindings and lexical scopes are created by Wendy
        # their keys are the names for the given scope, and the values
        # are the dm1 objects
        self.dm1_id_frame_map = dm1_id_frame_map
        self.dm1_id_object_map = dm1_id_object_map
        self.search_paths = search_paths
        self.path_dm1_map = path_dm1_map

        self.dm1_id_dm2_map: dict[int, Object] = {}
        self.errors: list[errors.AtoError] = []

    def collect_error(self, error: errors.AtoError) -> errors.AtoError:
        self.errors.append(error)
        return error

    def search_file_path(self, dep_name: str) -> Path:
        for search_path in self.search_paths:
            candidate_path = search_path.joinpath(dep_name)
            if candidate_path.exists():
                return candidate_path.resolve().absolute()
        raise errors.AtoImportNotFoundError(f"Could not find import: {dep_name}")

    def visit_generic(self, thing: Any) -> Any:
        """
        Handle visiting something - it'll work out where to dispatch the call.
        """
        match thing:
            case dm1.Object:
                return self.visit_dm1_Object(thing)
            case dm1.Link:
                return self.visit_dm1_Link(thing)
            case dm1.Replace:
                return self.visit_dm1_Replace(thing)
            case dm1.Import:
                return self.visit_dm1_Import(thing)
            case _:
                return thing

    def map_dm1_ref_to_dm2(self, name: dm1.Ref, dm1_frame: Frame, raise_exceptions = False) -> Object:
        """
        Map a name to a dm2 object via the dm1 object and the frame
        """
        try:
            return self.dm1_id_dm2_map[dm1_frame.lexical_scope[name]]
        except KeyError as ex:
            ex2 = self.collect_error(
                errors.AtoKeyError(
                    f"Name not found: {name}",
                    None,
                    None,
                    None,
                )
            )
            if raise_exceptions:
                raise ex2 from ex

    def visit_dm1_Object(self, dm1_obj: dm1.Object) -> Object:
        frame = self.dm1_id_frame_map[id(dm1_obj)]
        dm2_obj = self.dm1_id_dm2_map[id(dm1_obj)]

        dm2_obj.locals_ = tuple((name, self.visit_generic(obj)) for name, obj in dm1_obj.locals_)
        dm2_obj.supers = tuple(self.map_dm1_ref_to_dm2(super_, frame) for super_ in dm1_obj.supers)
