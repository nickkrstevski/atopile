from attrs import define, field
from pathlib import Path
import typing


class _Sentinel:
    """
    Used to create internal singletons for the types module.
    """


UNDEFINED = _Sentinel()


class Base:
    src_path: Path
    src_line: int
    src_col: int


@define
class Physical(Base):
    # TODO:
    pass


@define
class Equation(Base):
    # TODO:
    pass


@define
class MapType(Base):
    type_: "Class"


@define
class Map(Base):
    type_: MapType
    _map = {}


@define
class Attribute(Base):
    type_: typing.Type[Physical] | typing.Type[int] | typing.Type[float] | typing.Type[
        str
    ] | typing.Type[bool] | typing.Type[Equation] | "Class" | MapType
    value: typing.Union[
        Physical, int, float, str, bool, Equation, "Object", Map
    ] = UNDEFINED


@define
class Object(Base):
    type_: "Class"
    internal: dict[str, Attribute] = field(factory=dict)

    def is_instance_of(self, cls: "Class") -> bool:
        for classes in self.type_.supers:
            if cls in classes:
                return True
        return False



@define
class Class(Base):
    name: str
    supers: list[list["Class"]] = field(factory=list)
    internal: dict[str, typing.Union[Attribute, Equation, "Class", "Object"]] = field(
        factory=dict
    )
    anon: list[typing.Union[Attribute, Equation, "Class", "Object"]] = field(
        factory=list
    )
    object_type: typing.Optional[typing.Type[Object]] = None

    def get_object_type(self) -> typing.Type[Object]:
        if self.object_type:
            return self.object_type
        for supers in self.supers:
            for super_ in supers:
                if super_.object_type:
                    return super_.object_type
        return Object

    def make_instance(self) -> Object:
        return self.get_object_type()(type_=self)

    @classmethod
    def make_subclass(cls_, name: str, super_: "Class") -> "Class":
        if super_:
            supers = [super_]
        else:
            supers = []
        return cls_(name, supers=[supers, *super_.supers])

    @classmethod
    def is_subclass_of(self, cls: "Class") -> bool:
        for supers in self.supers:
            if cls in supers:
                return True
        return False



# Object Seeds

@define
class InterfaceObject(Object):
    links: list["LinkObject"] = field(factory=list)


INTERFACE = Class(
    "Interface",
    object_type=InterfaceObject,
)


@define
class LinkObject(Object):
    start: typing.Optional[InterfaceObject] = None
    end: typing.Optional[InterfaceObject] = None


LINK = Class(
    "link",
    object_type=LinkObject,
)


BLOCK = Class("block")


COMPONENT = Class("component", supers=[[BLOCK]])


PIN = Class("pin", supers=[[INTERFACE]])
