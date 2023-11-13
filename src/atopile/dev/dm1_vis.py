from atopile.dev.parse import parse_file
from atopile.model2.datamodel1 import Object, Link, Import, Replace, MODULE, COMPONENT, PIN, SIGNAL, INTERFACE
from rich.tree import Tree
from rich import print

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

    def parse_object(self, name, obj, parent_tree):
        label = self.get_label(name, obj.supers)
        subtree = parent_tree.add(label)
        self.visit(obj, subtree)

    def parse_link(self,name, obj, parent_tree):
        parent_tree.add(obj.source + " 🔗 " + obj.target + " (Link)")

    def parse_replace(self,name, obj, parent_tree):
        parent_tree.add(obj.original + " 👈 " + obj.replacement + " (Replace)")

    def parse_import(self,name, obj, parent_tree):
        parent_tree.add(obj.what + " 📦 " + obj.from_ + " (Import)")

    def visit(self, input_node, rich_tree: Tree):
        # Check the input node type and call the appropriate function
        if isinstance(input_node, Link):
            self.parse_link(input_node.source, input_node, rich_tree)
        elif isinstance(input_node, Replace):
            self.parse_replace(input_node.original, input_node, rich_tree)
        elif isinstance(input_node, Import):
            self.parse_import(input_node.what, input_node, rich_tree)
        # objects have locals, which can be nested, so we need to recursively call visit
        elif isinstance(input_node, Object):
            for ref, obj in input_node.locals_:
                name = ref[0]
                self.parse_object(name, obj, rich_tree)
                label = self.get_label(name, obj.supers)
                subtree = rich_tree.add(label)
                self.visit(obj, subtree)
        else:
            raise TypeError(f"Unknown type {type(input_node)}")
        return rich_tree

    def build_tree(self, dm1_tree: Object):
        # Create a tree structure using rich.tree
        tree = Tree("🌳 Project")
        return self.visit(dm1_tree, tree)

# # Display the tree
# tree_builder = Wendy()
# tree = tree_builder.build_tree(dm2)
# print(tree)