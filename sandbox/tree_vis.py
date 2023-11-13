#%%
from atopile.dev.parse import parse_file
from atopile.model2.datamodel1 import Dizzy, Object, MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
from rich.tree import Tree
from rich import print

# %%
tree = parse_file(
    """
    module mod1:
        module comp1:
            module comp2:
                signal signal_a
    module mod_new:
        signal signal_b
    """
)
# %%
# dizzy = Dizzy("test.ato")
# dm1 = dizzy.visit(tree)

dm2 = Object(
        supers=MODULE,
        locals_=(
            (('comp1',), Object(
                supers=COMPONENT,
                locals_=((('comp1','comp2'), Object(
                supers=COMPONENT,
                locals_=(
                    (('signal_a',), Object(
                        supers=SIGNAL,
                        locals_=()
                    )),(('signal_b',), Object(
                        supers=SIGNAL,
                        locals_=()
                    ))
                )
            )),
                    (('signal_a',), Object(
                        supers=SIGNAL,
                        locals_=()
                    )),(('signal_b',), Object(
                        supers=SIGNAL,
                        locals_=()
                    ))
                )
            )),
            (('comp1',), Object(
                supers=COMPONENT,
                locals_=(
                    (('signal_a',), Object(
                        supers=SIGNAL,
                        locals_=()
                    )),(('signal_b',), Object(
                        supers=SIGNAL,
                        locals_=()
                    ))
                )
            )),
        )
)




# %%🦊
# rich visualizer
# prints out roughly in ato format, but with object types



class Wendy:
    def get_label(self, name, supers):
        # Check the type of the node and return the label
        if supers == MODULE:
            return f"🎁 {name} (module)"
        elif supers == COMPONENT:
            return f"⚙️ {name} (component)"
        elif supers == SIGNAL:
            return f"⚡️ {name} (signal)"
        elif supers == PIN:
            return f"📍 {name} (pin)"
        elif supers == INTERFACE:
            return f"🔌 {name} (interface)"
        else:
            return f"❓ {name} (unknown)"

    def visit(self, input_node: Object, rich_tree: Tree):
        for ref, obj in input_node.locals_:
            label = self.get_label(ref[0], obj.supers)
            subtree = rich_tree.add(label)
            self.visit(obj, subtree)
        return rich_tree

    def build_tree(self, dm1_tree: Object):
        # Create a tree structure using rich.tree
        tree = Tree("🌳 Project")
        return self.visit(dm1_tree, tree)

# Display the tree
tree_builder = Wendy()
tree = tree_builder.build_tree(dm2)
print(tree)


# %%
