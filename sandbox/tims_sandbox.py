# %%
import logging
from pathlib import Path
from textwrap import dedent
from atopile.address import AddrStr
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from atopile.model2.build import Spud
from atopile.model2.designators import make_designators
from atopile.model2.solve_vdiv import solve_vdivs
from atopile.model2.errors import ErrorHandler, HandlerMode
from atopile.targets.netlist.kicad6_m2 import Builder

from atopile.model2.datamodel import Object, Instance
from atopile.model2.datatypes import KeyOptMap

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler())


#%%
src_code = """
    interface Power:
        signal vcc
        signal gnd

    component Resistor:
        pin p1
        pin p2
        footprint = "Resistor_SMD:R_0603_1608Metric"
        ratio = 2

    module VDiv:
        r_top = new Resistor
        r_bottom = new Resistor

        signal in ~ r_top.p1
        signal out ~ r_top.p2
        out ~ r_bottom.p1
        signal bottom ~ r_bottom.p2

        r_total = 10
        in.current = 1
        in.voltage = 10
        out.voltage = 8

    module Root:
        power = new Power

        vdiv = new VDiv

"""

# %%
error_handler = ErrorHandler(handel_mode=HandlerMode.RAISE_ALL)
spud = Spud(error_handler, (Path("."),))
flat = spud.build_instance_from_text(dedent(src_code).strip(), ("Root",))


# VDiv = Object(supers_refs=(), locals_=KeyOptMap(()))

# vdiv = Instance(ref=())

# flat = spud.build_instance_from_text(dedent(src_code).strip(), ("Root",))

#%%
solve_vdivs(flat)

# %%

# %%
