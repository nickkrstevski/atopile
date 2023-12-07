# %%
from pathlib import Path
from textwrap import dedent

import rich
import rich.tree

from atopile.address import AddrStr
from atopile.model2.build import Spud
from atopile.model2.datamodel import Instance
from atopile.model2.errors import ErrorHandler, HandlerMode
from atopile.model2.flatten import get_ref_from_instance, get_ref_data_from_instance, data_bubbler
from atopile.model2.datatypes import Ref

# %%

def make_tree(instance: Instance, tree: rich.tree.Tree = None) -> rich.tree.Tree:
    if tree is None:
        addr_str = AddrStr.from_parts(node=instance.ref)
        tree = rich.tree.Tree(addr_str)

    for child_name, child in instance.children.items():
        if isinstance(child, Instance):
            make_tree(child, tree.add(child_name))
            print(child_name)
            print(child.children)
        else:
            tree.add(f"{child_name} == {str(child)}")

    for link in instance.joints:
        tree.add(f"{AddrStr.from_parts(node=link.source.ref)} ~ {AddrStr.from_parts(node=link.target.ref)}")

    return tree

def print_tree(tree: rich.tree.Tree) -> None:
    rich.print(tree)


#%%
src_code = """
    interface Power:
        signal vcc
        signal gnd

    component Resistor:
        pin p1
        pin p2
        value = 312
        hi = 1

    module ARoot:
        r1 = new Resistor
        power = new Power
        r1.p1 ~ power.vcc
        r1.p2 ~ power.gnd

        vdiv = new VDiv

    module VDiv:
        r_top = new Resistor
        r_bottom = new Resistor

        signal top ~ r_top.p1
        signal output ~ r_top.p2
        output ~ r_bottom.p1
        signal bottom ~ r_bottom.p2

        r_top.test = 1000
        r_top.test2 = 2000
        r_bottom.smth = 66
        r_bottom.value = 666

    module Root:
        a = new ARoot
        a.vdiv.r_top.value = 2
        a.vdiv.r_bottom.value = 4

"""

# %%
error_handler = ErrorHandler(handel_mode=HandlerMode.RAISE_ALL)
spud = Spud(error_handler, (Path("."),))

#%%
flat = spud.build_instance_from_text(dedent(src_code).strip(), ("Root",))
print_tree(make_tree(flat))

# %%

#print(get_ref_from_instance(Ref(('a','vdiv','r_top')), flat))

#print(get_ref_data_from_instance(Ref(('a','vdiv','r_top',)), flat))

print(data_bubbler(flat, Ref(('Root',))))


# %%
