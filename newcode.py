import urllib.parse


class AVL:
    class Node:
        def __init__(self, parent, key, left=None, right=None):
            self.parent = parent
            self.left = left
            self.right = right
            self.key = key

    def __init__(self, c, root_data):
        self.root = AVL.Node(None, root_data)
        self.c = c

    # calculate subtree size from node including node
    def calculate_subtree_size(self, node):
        if node is None:
            return 0

        return self.calculate_subtree_size(node.left) + self.calculate_subtree_size(node.right) + 1

    def calculate_height(self, node):
        if node is None:
            return 0
        return max(self.calculate_height(node.left), self.calculate_height(node.right)) + 1

    def update_bf(self, node):
        if node is None:
            return 0
        return self.calculate_height(node.right) - self.calculate_height(node.left)
    def insert(self, data):
        def _insert(parent):
            assert data != parent.key

            if data < parent.key:
                if parent.left is None:
                    parent.left = AVL.Node(parent, data)
                    return

                _insert(parent.left)
                return

            if parent.right is None:
                parent.right = AVL.Node(parent, data)
                return

            _insert(parent.right)
            balanced_left = self.calculate_subtree_size(parent.left) > self.c * self.calculate_subtree_size(parent)
            balanced_right = self.calculate_subtree_size(parent.right) > self.c * self.calculate_subtree_size(parent)
            if balanced_left or balanced_right:
                # Update height of the current node
                parent.height = 1 + max(self.calculate_height(parent.left), self.calculate_height(parent.right))

                # Check balance factor
                bf = self.update_bf(parent)

                # If unbalanced, perform rotation
                if bf < -1 and data < parent.left.key:  # Left-Left case
                    return self.right_rot(parent)
                if bf > 1 and data > parent.right.key:  # Right-Right case
                    return self.left_rot(parent)
                if bf < -1 and data > parent.left.key:  # Left-Right case
                    parent.left = self.left_rot(parent.left)
                    return self.right_rot(parent)
                if bf > 1 and data < parent.right.key:  # Right-Left case
                    parent.right = self.right_rot(parent.right)
                    return self.left_rot(parent)

        _insert(self.root)

    def right_rot(self, node):
        root = node.left
        node.left = root.right
        if root.right:
            root.right.parent = node
        root.right = node

        # Update parent pointers
        root.parent = node.parent
        if node.parent:
            if node.parent.left == node:
                node.parent.left = root
            else:
                node.parent.right = root
        node.parent = root

        # If the rotated node was the root, update the tree root
        if self.root == node:
            self.root = root

        return root

    def left_rot(self, node):
        root = node.right
        node.right = root.left
        if root.left:
            root.left.parent = node
        root.left = node

        # Update parent pointers
        root.parent = node.parent
        if node.parent:
            if node.parent.right == node:
                node.parent.right = root
            else:
                node.parent.left = root
        node.parent = root

        # If the rotated node was the root, update the tree root
        if self.root == node:
            self.root = root

        return root

class AVLGraphGenerator:
    def __init__(self):
        self.code = "digraph AVL {"

    def generate(self, tree: AVL):
        def _gen(node: AVL.Node):
            if node is None:
                return

            if node.parent is not None:
                self.code += f"{node.parent.key} -> {node.key};"

            _gen(node.left)
            _gen(node.right)

        self.code += f"{tree.root.key};"
        _gen(tree.root)
        self.code += "}"

        result = "https://dreampuf.github.io/GraphvizOnline/#" + urllib.parse.quote(self.code)

        return result


# Create an AVL tree
tree = AVL(c=0.55, root_data=4)
tree.insert(6)
tree.insert(5)
tree.insert(7)
tree.insert(8)

generator = AVLGraphGenerator()
print(generator.generate(tree))

tree.insert(10)
tree.insert(20)
tree.insert(15)
tree.insert(1)
tree.insert(2)
tree.insert(3)
tree.insert(2.5)


generator = AVLGraphGenerator()
print(generator.generate(tree))
