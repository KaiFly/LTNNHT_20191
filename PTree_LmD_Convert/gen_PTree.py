from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import pydot



class PTree():
        def __init__(self):
                self.root = None
                self.nodes= []

        def gen_PTree(self):
                N0 = Node('E')
                N1 = Node('E', parent = N0)
                N2 = Node('*', parent = N0)
                N3 = Node('E', parent = N0)
                N4 = Node('I', parent = N1)
                N5 = Node('(', parent = N3)
                N6 = Node('E', parent = N3)
                N7 = Node(')', parent = N3)
                N8 = Node('a', parent = N4)
                N9 = Node('E', parent = N6)
                N10 = Node('+', parent = N6)
                N11 = Node('E', parent = N6)
                N12 = Node('I', parent = N9)
                N13 = Node('I', parent = N11)
                N14 = Node('a', parent = N12)
                N15 = Node('I', parent = N13)
                N16 = Node('0', parent = N13)
                N17 = Node('I', parent = N15)
                N18 = Node('0', parent = N15)
                N19 = Node('b', parent = N17)
                self.root = N0

        def PTree_png(self):
                DotExporter(self.root).to_dotfile("PTree_input")
                (graph,) = pydot.graph_from_dot_file("PTree_input")
                graph.write_png('PTree_input.png')

        def Render_Tree(self):
                print(RenderTree(self.root))


#M = PTree()
#M.gen_PTree()
#M.Render_Tree()