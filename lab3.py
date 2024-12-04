import urllib.parse


class AVL:
    class Node:
        def __init__(self, parent, data, left=None, right=None, height=None):
            self.parent = parent
            self.left = left
            self.right = right
            self.data = data
            self.level = -1
            self.height = height


    def __init__(self, c, root_data):
        self.c = c
        self.root = AVL.Node(None, root_data)

        # def __calculate_subtree_size(self, node):
    def calculate_subtree_size(self, node):
        def _calc(node):
            if node is None:
                return 0

            return _calc(node.left) + _calc(node.right) + 1

        return _calc(node)
     #calculates height from node(not including node)
    def calculate_height(self, node):
        def _calc(node):
            if node is None:
                return 0
            height_left = _calc(node.left)
            height_right = _calc(node.right) 

            return max(height_left, height_right) + 1 
        return _calc(node) - 1  

    def insert(self, data):
        def _insert(parent):
            assert data != parent.data

            if data < parent.data:
                if parent.left is None:
                    parent.left = AVL.Node(parent, data)
                    return

                _insert(parent.left)
                return

            if parent.right is None:
                parent.right = AVL.Node(parent, data)
                return

            _insert(parent.right)

        _insert(self.root)


    def right_rot(self, node):
        root = node.left #left child becomes root
        node.left = root.right 
        root.right = node

        node.height = 1 + max(self.calculate_height(node.left), self.calculate_height(node.right))
        root.height = 1 + max(self.calculate_height(root.left), self.calculate_height(root.right))


        return root
        





class AVLGraphGenerator:
    def __init__(self):
        self.code = "digraph AVL {"

    def generate(self, tree: AVL):
        def _gen(node: AVL.Node):
            if node is None:
                return

            if node.parent is not None:
                self.code += f"{node.parent.data} -> {node.data};"

            _gen(node.left)
            _gen(node.right)

        self.code += f"{tree.root.data};"
        _gen(tree.root)
        self.code += "}"

        result = "https://dreampuf.github.io/GraphvizOnline/#" + urllib.parse.quote(self.code)

        return result  


# Create an AVL tree
tree = AVL(c=1, root_data=10)
tree.insert(5)
tree.insert(2)
tree.insert(3)
tree.insert(12)





generator = AVLGraphGenerator()
print(generator.generate(tree))
print(tree.calculate_subtree_size(tree.root))
print(tree.calculate_height(tree.root.left))