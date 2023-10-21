from attrs import define, field
from typing import Any


@define
class Object:
    attrs: dict[str, Any] = field(factory=dict)
    supers: list["Object"] = field(factory=list)

@define
class Interface(Object):
    pass

@define
class Link(Object):
    obj: Object
    interface: Interface


MODULE = Object()

COMPONENT = Object(supers=[MODULE])

rp2040 = Object(supers=[COMPONENT])

rp2040_kit = Object(supers=[rp2040])

NaraGuy = Object(supers=[MODULE], attrs={"rp2040": rp2040_kit})

rp2041 = Object(supers=[rp2040])

rp2041_kit = Object(supers=[rp2041])

ThingUsingNaraGuy = Object(supers=[MODULE], attrs={"nara_guy": NaraGuy,
                                                   "nara_guy.rp2040": rp2041_kit
                                                   })
