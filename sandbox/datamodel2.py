from attrs import define, field
from typing import Any


@define
class Object:
    supers: list["Object"] = field(factory=list)
    class_: tuple[str] = field(factory=tuple)


@define
class TypeDef:
    supers: list["TypeDef"] = field(factory=list)


@define
class Interface:
    supers: list["TypeDef"] = field(factory=list)


@define
class Link:
    source_object: Interface
    source_interface: Interface
    target_object: Interface
    target_interface: Interface


MODULE = TypeDef()
COMPONENT = TypeDef(supers=[MODULE])

file = Object(type_=MODULE, supers=[], locals_={})

PIN = TypeDef()
SIGNAL = TypeDef()


Resistor = TypeDef(
    supers=[COMPONENT],
    locals_={
        1: Interface(type_=PIN),
        2: Interface(type_=PIN),
        "test": 1,
    },
)

# in this data model we make everything by reference

VDiv = TypeDef(
    supers=[MODULE],
    anon=[
        Link(
            source = ("r_top", 2),
            target = ("out",)
        ),
        Link(
            source = ("r_bottom", 1),
            target = ("out",)
        ),
        Link(
            source = ("r_bottom", 2),
            target = ("bottom",)
        ),
    ],
    locals_={
        "top": Interface(type_=SIGNAL),
        "out": Interface(type_=SIGNAL),
        "bottom": Interface(type_=SIGNAL),
        "r_top": Object(class_=("Resistor",)),
        "r_bottom": Object(class_=("Resistor",)),
        "top_link": Link(
            source = ("r_top", 1),
            target = ("top",)
        ),
        ("r_top", "test"): 2,
    },
)


@define
class Replace:
    original: tuple[str]
    replacement: tuple[str]


Test = TypeDef(
    supers=[MODULE],
    anon=[
        Replace(
            original = ("vdiv", "r_top"),
            replacement = ("Resistor2",)
        )
    ],
    locals_={
        "vdiv": Object(
            class_=("VDiv",)
        ),
    }
)
