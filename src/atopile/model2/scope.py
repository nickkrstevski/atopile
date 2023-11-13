import logging
import typing
from contextlib import contextmanager

from atopile.model2 import types
from atopile.parser.AtopileParserVisitor import AtopileParserVisitor
from atopile.model2.parse import ParserRuleContext

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class Scope:
    def __init__(
        self,
        current: types.Class | types.Object,
        parent: typing.Optional["Scope"] = None,
    ) -> None:
        self._current = current
        self._parent = parent

    def __getitem__(self, key: str):
        """
        Get an item from:
        1. The current scope
        2. The current scope's supers (eg. super classes)
        3. The parent scope (eg. outer scope, same file)
        4. Parent's parent etc...

        # FIXME: do we really want this implicit? "this"/"self" might be more appropriate
        """

        scopes = self._current.internal

        if isinstance(self._current, types.Object):
            # the reason for the two "s"s is because it's a list of lists
            superss = self._current.type_.supers
        else:
            superss = self._current.supers

        for supers in superss:
            for super_ in supers:
                scopes += super_.internal

        if self._parent:
            scopes += self._parent._current.internal

        for scope in scopes:
            if key in scope:
                return scope[key]
        raise KeyError(f"'{key}' not found")

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def set(self, key: str, value) -> typing.Any:
        old = self._current.internal.get(key)
        self._current.internal[key] = value
        return old