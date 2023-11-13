#%%
from atopile.dev.parse import parse_file
from atopile.model2.datamodel1 import Dizzy, Object, Link, Import, Replace, MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
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
                    (('interface1',), Object(
                        supers=INTERFACE,
                        locals_=()
                    )),(('pin1',), Object(
                        supers=PIN,
                        locals_=()
                    ))
                )
            )),
        )
)

dm3 = Link(source="signal_a", target="signal_b")




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

    def parse_module(self, name, obj, parent_tree):
        label = self.get_label(name, MODULE)
        subtree = parent_tree.add(label)
        self.visit(obj, subtree)

    def parse_component(self, name, obj, parent_tree):
        label = self.get_label(name, COMPONENT)
        subtree = parent_tree.add(label)
        self.visit(obj, subtree)

    def parse_signal(self, name, obj, parent_tree):
        label = self.get_label(name, SIGNAL)
        subtree = parent_tree.add(label)
        self.visit(obj, subtree)

    def parse_pin(self, name, obj, parent_tree):
        label = self.get_label(name, PIN)
        subtree = parent_tree.add(label)
        self.visit(obj, subtree)

    def parse_interface(self, name, obj, parent_tree):
        label = self.get_label(name, INTERFACE)
        subtree = parent_tree.add(label)
        self.visit(obj, subtree)

    def parse_link(self, name, obj, parent_tree):
        parent_tree.add(obj.source + " 🔗 " + obj.target + " (Link)")

    def parse_replace(self, name, obj, parent_tree):
        parent_tree.add(obj.source + " 👈 " + obj.target + " (Replace)")

    def visit(self, input_node, rich_tree: Tree):
        if isinstance(input_node, Link):
            self.parse_link(input_node.source, input_node, rich_tree)
        else:
            for ref, obj in input_node.locals_:
                name = ref[0]
                if obj.supers == MODULE:
                    self.parse_module(name, obj, rich_tree)
                elif obj.supers == COMPONENT:
                    self.parse_component(name, obj, rich_tree)
                elif obj.supers == SIGNAL:
                    self.parse_signal(name, obj, rich_tree)
                # Add conditions for Link, Replace, Import, etc.
                else:
                    label = self.get_label(name, obj.supers)
                    subtree = rich_tree.add(label)
                    self.visit(obj, subtree)
        return rich_tree

    def build_tree(self, dm1_tree: Object):
        # Create a tree structure using rich.tree
        tree = Tree("🌳 Project")
        return self.visit(dm1_tree, tree)

# Display the tree
tree_builder = Wendy()
tree = tree_builder.build_tree(dm3)
print(tree)


# %%
