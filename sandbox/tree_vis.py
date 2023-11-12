#%%
from atopile.dev.parse import parse_file
from atopile.model2.datamodel1 import Dizzy, Object, MODULE, COMPONENT, PIN, SIGNAL, INTERFACE


# %%
tree = parse_file(
    """
    module mod1:
        component comp1:
            signal signal_a
            signal signal_a
    module mod2:
        component comp1:
            signal signal_a
            signal signal_a
    """
)
# %%
dizzy = Dizzy("test.ato")
dm1 = dizzy.visit(tree)

dm1

# %%🦊
# rich visualizer
# prints out roughly in ato format, but with object types
from rich.tree import Tree
from rich import print

# Create a tree structure using rich.tree
# Function to build the tree using rich.tree

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
            if isinstance(obj, Object):
                subtree = rich_tree.add(self.get_label(ref[0], obj.supers))
                self.visit(obj, subtree)

    def build_tree(self, dm1_tree: Object):
        # Create a tree structure using rich.tree
        tree = Tree("🌳 Project")
        self.visit(dm1_tree, tree)
        return self.tree

# Assuming dm1 is defined somewhere above with the correct structure


# Display the tree
tree_builder = Wendy()
tree = tree_builder.build_tree(dm1[0][1])
print(tree)


# %%
