import logging
import typing
import traceback
from contextlib import contextmanager
import textwrap

from atopile.model2 import types, errors
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.parser.AtopileParser import AtopileParser as ap
from atopile.parser.parser2 import ParserRuleContext
from atopile.model2.scope2 import Scope
from pathlib import Path

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class DependencyFinder(AtopileParserVisitor):
    def visitImport_stmt(self, ctx: ap.Import_stmtContext):
        return ctx.string().strip("\"'")

    def aggregateResult(self, aggregate, nextResult):
        return aggregate + [nextResult]


class Compiler(AtopileParserVisitor):
    def __init__(self, name: str, logger: logging.Logger) -> None:
        self.name = name
        self.logger = logger
        self.deps: dict[str, types.Class] = []
        self._scope_stack: list[Scope] = []
        super().__init__()

    @contextmanager
    def new_scope(self, current: types.Class | types.Object):
        yield Scope(current, self._scope_stack[-1] if self._scope_stack else None)

    @property
    def scope(self) -> Scope:
        return self._scope_stack[-1]

    def visitTotally_an_integer(self, ctx: ap.Totally_an_integerContext) -> types.Class:
        try:
            return str(int(ctx.getText()))
        except ValueError:
            raise errors.AtoCompileError("Expected an integer")

    def visitFile_input(self, ctx: ParserRuleContext) -> types.Class:
        file = types.Class(name=self.name)
        with self.new_scope(file):
            self.visitChildren(ctx)
            return file

    def visitBlocktype(self, ctx: ap.BlocktypeContext):
        block_type_name = ctx.getText()
        if block_type_name == "module":
            default_super = types.BLOCK
            allowed_supers = [types.BLOCK]
        elif block_type_name == "component":
            default_super = types.COMPONENT
            allowed_supers = [types.COMPONENT, types.BLOCK]
        else:
            raise errors.AtoCompileError(f"Unknown block type '{block_type_name}'")
        return default_super, allowed_supers

    def visitName(self, ctx: ap.NameContext) -> str:
        return ctx.getText()

    def visitAttr(self, ctx: ap.AttrContext) -> tuple[str]:
        return tuple(ctx.name())

    def visitName_or_attr(self, ctx: ap.Name_or_attrContext) -> tuple[Scope, str]:
        if ctx.name():
            return self.scope, self.visitName(ctx.name())
        elif ctx.attr():
            scope = self.scope
            path = self.visitAttr(ctx.attr())
            for attr in path[:-1]:
                scope = scope[attr]
            return scope, path[-1]

        raise errors.AtoCompileError("Expected a name or attribute")

    def visitBlockdef(self, ctx: ap.BlockdefContext) -> types.Class:
        new_class_name = self.visit(ctx.name())
        if new_class_name in self.scope:
            raise errors.AtoNameConflictError(
                f"Cannot redefine '{new_class_name}' in the same scope"
            )

        default_super, allowed_supers = self.visitBlocktype(ctx.blocktype())

        if ctx.FROM():
            if not ctx.name_or_attr():
                raise errors.AtoCompileError(
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

    def visitPindef_stmt(self, ctx: ap.Pindef_stmtContext):
        name = self.visit(ctx.totally_an_integer() or ctx.name())
        if not name:
            raise errors.AtoCompileError("Pins must have a name")

        if name in self.scope:
            raise errors.AtoNameConflictError(
                f"Cannot redefine '{name}' in the same scope"
            )

        pin = types.PIN.make_instance()
        self.scope[name] = pin

        return pin

    def visitSignaldef_stmt(self, ctx: ap.Signaldef_stmtContext):
        name = self.visit(ctx.name())
        if not name:
            raise errors.AtoCompileError("Signals must have a name")

        if name in self.scope:
            raise errors.AtoNameConflictError(
                f"Cannot redefine '{name}' in the same scope"
            )

        signal = types.INTERFACE.make_instance()
        self.scope[name] = signal

        return signal

    def visitImport_stmt(self, ctx: ap.Import_stmtContext):
        from_file: str = self.visitString(ctx.string())
        scope, to_import = self.visitName_or_attr(ctx.name_or_attr())

        if not from_file:
            raise errors.AtoCompileError("Expected a 'from <file-path>' after 'import'")
        if not to_import:
            raise errors.AtoCompileError(
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

    def visitConnectable(self, ctx: ap.ConnectableContext) -> types.InterfaceObject:
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
                f"Cannot connect to '{name}' because it is not an interface"
            )

        return connectable

    def visitConnect_stmt(self, ctx: ap.Connect_stmtContext) -> types.LinkObject:
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

    def visitWith_stmt(self, ctx: ap.With_stmtContext):
        """
        FIXME: I'm not entirely sure what this is for
        Remove it soon if we don't figure it out
        """
        raise NotImplementedError

    def visitNew_stmt(self, ctx: ap.New_stmtContext) -> types.Object:
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

    def visitAssignable(self, ctx: ap.AssignableContext) -> types.Object | types.Class | types.Attribute | int | float | str:
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

    def visitAssign_stmt(self, ctx: ap.Assign_stmtContext) -> tuple[typing.Optional[str], typing.Any]:
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

    def visitRetype_stmt(self, ctx: ap.Retype_stmtContext):
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


def get_ctx_from_exception(ex: Exception) -> typing.Optional[ParserRuleContext]:
    for tb, _ in list(traceback.walk_tb(ex.__traceback__))[::-1]:
        if tb.f_locals.get("ctx"):
            if isinstance(tb.f_locals.get("self"), Compiler):
                return tb.f_locals["ctx"]


def compile_file(
    file_path: Path,
    tree: ParserRuleContext,
    logger: typing.Optional[logging.Logger] = None,
) -> types.Class:
    """
    Compile the given tree into an atopile core representation
    """

    if logger is None:
        logger = log

    try:
        return Compiler(file_path, logger=logger).visit(tree)

    except Exception as ex:
        if ctx := get_ctx_from_exception(ex):
            if isinstance(ex, errors.AtoCompileError):
                message = ex.user_facing_name + ": " + ex.message
            else:
                message = f"Unprocessed '{repr(ex)}' occurred during compilation"

            logger.error(
                textwrap.dedent(
                    f"""
                {file_path}:{ctx.start.line}:{ctx.start.column}:
                {message}
                """
                ).strip()
            )

        raise
