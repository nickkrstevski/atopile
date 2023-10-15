from attrs import define
from pathlib import Path
import typing


class _Sentinel:
    """
    Used to create internal singletons for the types module.
    """


UNDEFINED = _Sentinel()


class Base:
    def __init__(self, src_path: Path, src_line: int, src_col: int):
        self.src_path = src_path
        self.src_line = src_line
        self.src_col = src_col


class Physical(Base):
    # TODO:
    pass


class Equation(Base):
    # TODO:
    pass


class Map(Base):
    def __init__(self, type_: "AttributeTypes"):
        self.type_ = type_
        self._map = {}


AttributeTypes = typing.Union[
    _Sentinel,
    typing.Type[Physical],
    typing.Type[int],
    typing.Type[float],
    typing.Type[str],
    typing.Type[bool],
    typing.Type[Equation],
    "Class",
    "Object",
    Map,
]


class Attribute(Base):
    def __init__(
        self, name: str, type_: AttributeTypes, value: AttributeTypes = UNDEFINED
    ):
        self.name = name
        self.type = type_
        self.value = value


class Class(Base):
    def __init__(
        self,
        name: str,
        supers: list[list["Class"]] = None,
        internal: dict[str, Attribute | Equation | "Class" | "Object"] = None,
        anon: list[Attribute | Equation | "Class" | "Object"] = None,
    ):
        self.name = name
        self.supers = supers or []
        self.internal = internal or {}
        self.anon = anon or []

    def init(self) -> "Object":
        return Object(self)

    def subclass(self, name: str, ) -> "Class":
        return Class(name, supers=(self.supers + [[self]]))


class Object(Base):
    def __init__(
        self,
        type_: Class,
        internal: dict[str, Attribute] = None,
    ):
        self.type_ = type_
        self.internal = internal or {}


# Object Seeds


INTERFACE = Class("Interface")


class InterfaceObject(Object):
    def __init__(self, *args, links: list["LinkObject"] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.links = links or []


LINK = Class()


class LinkObject(Object):
    def __init__(self, *args, start: InterfaceObject = UNDEFINED, end: InterfaceObject = UNDEFINED, **kwargs):
        super().__init__(*args, **kwargs)
        self.start = start
        self.end = end


BLOCK = Class()


COMPONENT = Class(supers=[BLOCK])


def is_instance_of(obj: Object, cls: Class) -> bool:
    return cls in obj.type_.supers
