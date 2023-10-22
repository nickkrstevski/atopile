"""
This datamodel represents the code in a clean, simple and traversable way, but doesn't resolve names of things
In building this datamodel, we check for name collisions, but we don't resolve them yet.
"""

import enum
import logging
import textwrap
import traceback
import typing
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Optional

from attrs import define, field

from atopile.model2 import errors, types
from atopile.model2.scope2 import Scope
from atopile.parser.AtopileParser import AtopileParser as ap
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.model2.parse import ParserRuleContext

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


Ref = tuple[str | int]


@define
class Link:
    source: Ref
    target: Ref


@define
class Replace:
    original: Ref
    replacement: Ref


@define
class Import:
    what: Ref
    from_: str


@define
class Object:
    supers: list[Ref] = field(factory=tuple)
    locals_: dict[Ref, Any] = field(factory=dict)


MODULE = Object()
COMPONENT = Object(supers=[("module",)])


PIN = Object()
SIGNAL = Object()
INTERFACE = Object()

## Usage Example

# file = Object(class_=MODULE, supers=[], locals_={})

# Resistor = Object(
#     supers=[COMPONENT],
#     locals_={
#         1: Object(class_=PIN),
#         2: Object(class_=PIN),
#         "test": 1,
#     },
# )

# in this data model we make everything by reference
# vdiv_named_link = Link(source=("r_top", 1), target=("top",))
# VDiv = Object(
#     supers=[MODULE],
#     links=[
#         Link(source=("r_top", 2), target=("out",)),
#         Link(source=("r_bottom", 1), target=("out",)),
#         Link(source=("r_bottom", 2), target=("bottom",)),
#         vdiv_named_link
#     ],
#     locals_={
#         "top": Object(class_=SIGNAL),
#         "out": Object(class_=SIGNAL),
#         "bottom": Object(class_=SIGNAL),
#         "r_top": Object(class_=("Resistor",)),
#         "r_bottom": Object(class_=("Resistor",)),
#         "top_link": vdiv_named_link,
#         ("r_top", "test"): 2,
#     },
# )


# Test = Object(
#     supers=[MODULE],
#     anon=[Replace(original=("vdiv", "r_top"), replacement=("Resistor2",))],
#     locals_={
#         "vdiv": Object(class_=("VDiv",)),
#     },
# )

## Return struct

class Type(enum.Enum):
    LINK = enum.auto()
    OBJECT = enum.auto()
    REPLACE = enum.auto()

## Builder


class Dizzy(AtopileParserVisitor):
    def __init__(
        self,
        name: str,
        # logger: logging.Logger,
    ) -> None:
        self.name = name
        # self.logger = logger
        super().__init__()

    def visitTotally_an_integer(self, ctx: ap.Totally_an_integerContext) -> int:
        text = ctx.getText()
        try:
            return int(text)
        except ValueError:
            raise errors.AtoTypeError(f"Expected an integer, but got {text}")

    def visitFile_input(self, ctx: ap.File_inputContext) -> tuple[Type, Optional[Ref], Object]:
        results: list[tuple[Type, Optional[Ref], Object]] = [self.visit(c) for c in ctx.getChildren()]
        return results

    def visitBlocktype(self, ctx: ap.BlocktypeContext) -> tuple[Type, Optional[Ref], Object]:
        block_type_name = ctx.getText()
        match block_type_name:
            case "module":
                return MODULE
            case "component":
                return COMPONENT
            case _:
                raise errors.AtoError(f"Unknown block type '{block_type_name}'")

    def visitName(self, ctx: ap.NameContext) -> str | int:
        """
        If this is an int, convert it to one (for pins), else return the name as a string.
        """
        try:
            return int(ctx.getText())
        except ValueError:
            return ctx.getText()

    def visitAttr(self, ctx: ap.AttrContext) -> tuple[str]:
        return tuple(self.visitName(name) for name in ctx.name()) # Comprehension

    # TODO: reimplement that function
    def visitName_or_attr(self, ctx: ap.Name_or_attrContext) -> tuple[str]:
        if ctx.name():
            return self.visitName(ctx.name())
        elif ctx.attr():
            print("should not get here")
            scope = self.scope
            path = self.visitAttr(ctx.attr())
            for attr in path[:-1]:
                if isinstance(scope[attr], Scope):
                    scope = scope[attr]
                    continue

                if isinstance(scope[attr], (types.Class, types.Object)):
                    # create custom scopes for classes and objects
                    scope = Scope(scope[attr])
                    continue

                if isinstance(scope[attr], types.Attribute):
                    if isinstance(scope[attr].type_, (types.Class, types.Object)):
                        scope = Scope(scope[attr].value)
                        continue

                raise errors.AtoTypeError(
                    f"{attr} in scope {scope} isn't an object or class"
                )
            return scope, path[-1]

        raise errors.AtoError("Expected a name or attribute")

    #TODO: reimplement
    def visitBlockdef(self, ctx: ap.BlockdefContext) -> tuple[Type, Optional[Ref], Object]:
        new_class_name = self.visit(ctx.name())
        if new_class_name in self.scope:
            raise errors.AtoNameConflictError(
                f"Cannot redefine '{new_class_name}' in the same scope"
            )

        default_super, allowed_supers = self.visitBlocktype(ctx.blocktype())

        if ctx.FROM():
            if not ctx.name_or_attr():
                raise errors.AtoError(
                    "Expected a name or attribute after 'from'"
                )
            super_name, super_scope = self.visitName_or_attr(ctx.name_or_attr())
            actual_super = super_scope[super_name]
            if not isinstance(actual_super, types.Class):
                raise errors.AtoTypeError(
                    f"Can only subclass classes, which '{super_name}' is not"
                )
            if actual_super not in allowed_supers:
                allowed_supers_friendly = ", ".join([s.name for s in allowed_supers])
                raise errors.AtoTypeError(
                    f"Can only subclass {allowed_supers_friendly}, which '{super_name}' is not"
                )
        else:
            actual_super = default_super

        new_class = types.Class.make_subclass(new_class_name, actual_super)
        with self.new_scope(new_class):
            self.visitChildren(ctx)

        return new_class

    #TODO: reimplement
    def visitPindef_stmt(self, ctx: ap.Pindef_stmtContext) -> tuple[Type, Optional[Ref], Object]:
        name = self.visit(ctx.totally_an_integer() or ctx.name())

        #TODO: provide context of where this error was found within the file
        if not name:
            raise errors.AtoError("Pins must have a name")
        #TODO: reimplement this error handling at the above level
        # if name in self.scope:
        #     raise errors.AtoNameConflictError(
        #         f"Cannot redefine '{name}' in the same scope"
        #     )
        created_pin = Object(
            supers=[PIN],
        )

        return (Type.OBJECT, name, created_pin)

    #TODO: reimplement
    def visitSignaldef_stmt(self, ctx: ap.Signaldef_stmtContext) -> tuple[Type, Optional[Ref], Object]:
        name = self.visit(ctx.name())

        #TODO: provide context of where this error was found within the file
        if not name:
            raise errors.AtoError("Signals must have a name")

        created_signal = Object(
            supers=[SIGNAL],
        )

        #TODO: reimplement this error handling at the above level
        # if name in self.scope:
        #     raise errors.AtoNameConflictError(
        #         f"Cannot redefine '{name}' in the same scope"
        #     )
        return (Type.OBJECT, name, created_signal)

    #TODO: reimplement
    def visitImport_stmt(self, ctx: ap.Import_stmtContext) -> tuple[Type, Optional[Ref], Object]:
        from_file: str = self.visitString(ctx.string())
        scope, to_import = self.visitName_or_attr(ctx.name_or_attr())

        if not from_file:
            raise errors.AtoError("Expected a 'from <file-path>' after 'import'")
        if not to_import:
            raise errors.AtoError(
                "Expected a name or attribute to import after 'import'"
            )

        if to_import == "*":
            # import everything
            raise NotImplementedError("import *")

        if to_import in self.scope:
            raise errors.AtoNameConflictError(
                f"Cannot redefine '{to_import}' in the same scope"
            )

        self.scope[to_import] = scope[to_import]

    #TODO: reimplement
    def visitConnectable(self, ctx: ap.ConnectableContext) -> tuple[Type, Optional[Ref], Object]:
        if ctx.name_or_attr():
            scope, name = self.visitName_or_attr(ctx.name_or_attr())
            connectable = scope[name]
        elif ctx.numerical_pin_ref():
            pin_ref = self.visit(ctx.numerical_pin_ref())
            connectable = self.scope[pin_ref]
        elif ctx.pindef_stmt() or ctx.signaldef_stmt():
            connectable = self.visitChildren(ctx)

        if isinstance(connectable, types.Attribute):
            connectable = connectable.value

        if not isinstance(connectable, types.InterfaceObject):
            raise errors.AtoTypeError(
                f"Cannot connect to '{ctx.getText()}' because it is not an interface"
            )

        return connectable

    #TODO: Reimplement
    def visitConnect_stmt(self, ctx: ap.Connect_stmtContext) -> tuple[Type, Optional[Ref], Object]:
        """
        Connect interfaces together
        """
        start = self.visitConnectable(ctx.connectable(0))
        end = self.visitConnectable(ctx.connectable(1))
        link = types.LINK.make_instance()
        if not isinstance(link, types.LinkObject):
            raise errors.AtoTypeError("Unknown error")
        link.start = start
        link.end = end
        self.scope.append_anon(link)
        return link

    # Tricky, not sure what to do about this guy. I guess that's a super?
    def visitWith_stmt(self, ctx: ap.With_stmtContext) -> tuple[Type, Optional[Ref], Object]:
        """
        FIXME: I'm not entirely sure what this is for
        Remove it soon if we don't figure it out
        """
        raise NotImplementedError

    def visitNew_stmt(self, ctx: ap.New_stmtContext) -> tuple[Type, Optional[Ref], Object]:
        scope, name_to_init = self.visit(ctx.name_or_attr())
        to_init = scope[name_to_init]
        if not isinstance(to_init, types.Class):
            raise errors.AtoTypeError(
                f"Can only initialise classes, which '{name_to_init}' is not"
            )
        return to_init.make_instance()

    def visitString(self, ctx: ap.StringContext) -> str:
        return ctx.getText().strip("\"'")

    def visitBoolean_(self, ctx: ap.Boolean_Context) -> bool:
        return ctx.getText().lower() == "true"

    def visitAssignable(
        self, ctx: ap.AssignableContext
    ) -> tuple[Type, Optional[Ref], Object] | int | float | str:
        if ctx.name_or_attr():
            scope, name = self.visitName_or_attr(ctx.name_or_attr())
            return scope[name]

        if ctx.new_stmt():
            return self.visit(ctx.new_stmt())

        if ctx.NUMBER():
            value = float(ctx.NUMBER().getText())
            return int(value) if value.is_integer() else value

        if ctx.string():
            return self.visitChildren(ctx)

        if ctx.boolean_():
            return self.visitBoolean_(ctx.boolean_())

    def visitAssign_stmt(
        self, ctx: ap.Assign_stmtContext
    ) -> tuple[Type, Optional[Ref], Object]:
        scope, name = self.visitName_or_attr(ctx.name_or_attr())
        assignable = self.visitAssignable(ctx.assignable())

        match assignable:
            case types.Object() as x:
                attr = types.Attribute(type_=x.type_, value=x)
            case types.Class() as x:
                attr = types.Attribute(type_=types.Class, value=x)
            case types.Attribute() as x:
                attr = types.Attribute(type_=x.type_, value=x.value)
            case int() | float() | str() as x:
                attr = types.Attribute(type_=type(x), value=x)

        scope[name] = attr

    def visitRetype_stmt(self, ctx: ap.Retype_stmtContext) -> tuple[Type, Optional[Ref], Object]:
        """
        This statement type will replace an existing block with a new one of a subclassed type

        Since there's no way to delete elements, we can be sure that the subclass is
        a superset of the superclass (confusing linguistically, makes sense logically)
        """
        obj_scope, obj_name = self.visitName_or_attr(ctx.name_or_attr(0))
        target_scope, target_name = self.visitName_or_attr(ctx.name_or_attr(1))

        obj = obj_scope[obj_name]
        if not isinstance(obj, types.Object):
            raise errors.AtoTypeError(
                f"Can only retype objects, which '{obj_name}' is not"
            )

        target = target_scope[target_name]
        if not isinstance(target, types.Class):
            raise errors.AtoTypeError(
                f"Can only retype to classes, which '{target_name}' is not"
            )
        if not target.is_subclass_of(obj.type_):
            raise errors.AtoTypeError(
                f"Cannot retype '{obj_name}' to '{target_name}' because '{target_name}' is not a subclass of '{obj.type_.name}'"
            )

        obj.type_ = target


def compile_file(
    tree: ParserRuleContext,
    logger: typing.Optional[logging.Logger] = None,
) -> types.Class:
    """
    Compile the given tree into an atopile core representation
    """

    if logger is None:
        logger = log

    return Dizzy(
        'test',
        # logger=logger
    ).visit(tree)

