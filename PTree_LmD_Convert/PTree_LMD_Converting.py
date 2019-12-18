# -*- coding: utf-8 -*-
from gen_PTree import PTree
import re


class production:

        def __init__(self, left_side = None, right_side = None):
                self.ls = left_side
                self.rs = right_side

        def toStr(self):
                s = self.ls + "->" + self.rs
                return s

        def right_token(self):
                return list(self.rs)

        def left_token(self):
                return list(self.ls)

        def check_CFG(self):
                if len(self.ls) == 1:
                        return True
                else :
                        return False

        def get_len_rs(self):
                return len(self.rs)

        def __str__(self):
                return self.toStr()


def genString_fromTree(root):
        result = []
        def traversalTree(root):
                if root.is_leaf:
                        result.append(root.name[0])
                if root :
                        for child in root.children:
                                traversalTree(child)
                return result
        traversalTree(root)
        string_yeilded = "".join(result)
        return string_yeilded


#### Extract information of Context - Free Grammar text file
CFG = open("CFGrammar.txt", "r")
L = []
for line in CFG:
        line = line.rstrip()
        l = re.split(" |->|\n|", line)
        l = list(filter(None,l))
        if l:
                L.append(l)

CFG.close()
start_sym, terminal_syms, nterminal_syms = L[0], L[2], L[1]
derivation_dict = {}

for i in range(3, len(L), 1):
        deri = production(L[i][0], "".join(L[i][1:]))
        derivation_dict[deri.toStr()] = i-2

#### Algorithms
def Algorithm1(is_print = True):
        # Parse Tree Input
        T = PTree()
        T.gen_PTree()

        # Pseudo1 in report
        """
        root = Dtree.root
        Dtree_to_Lmd(root):
        	derivations = {}
        	# Đọc từ trái sang phải các node con của node đang xét
        	S = root.children
        	derivations.add( root.val + ‘->’ + ‘’.join(S) )
        	Tn = S.nonTerminals()
        	if Tn :
        	# Đệ quy để duyệt các dẫn xuất, một DX ứng với node là kí tự KKT
        		for q in Tn :
        			Dtree_to_Lmd(q)
        	# Một vòng ĐQ thực hiện cho đến khi duyệt hết các node KKT
        return derivations

        """

        root = T.root
        derivation_result = []
        def extract_LDM(root):
                S = root.children
                deri = production(root.name, "".join([s.name for s in S]))
                derivation_result.append(deri)
                Tn = []
                for node in S :
                        if node.name in nterminal_syms:
                                Tn.append(node)
                if Tn :
                        for node in Tn:
                                extract_LDM(node)
        extract_LDM(root)
        if is_print :
                print("Algorithm 1 : Parse Tree -> LM Derivation")
                print("- Input : Parse Tree")
                T.Render_Tree()
                print("\n- Output : Derivation order :")
                s = ""
                for deri in derivation_result:
                        s += " " + str(derivation_dict[deri.toStr()])
                print(s)
                for deri in derivation_result:
                        print(deri)
        return derivation_result



def Algorithm2(is_print = True):
        # Parse Tree Input
        derivation_input = Algorithm1(is_print = False)

        # Pseudo2 in report
        """
        Lmd_to_Dtree(derivations : set):
        	dTree = Tree()
        	tStack = Stack()
        	Dtree.root = Node(G.start_state)	# Khởi tạo gốc = trạng thái bắt đầu S
        	current_node = Dtree.root	# Đặt trỏ tới gốc cây
        	for deri in derivation :	# Duyệt lần lượt các DX theo thứ tự trái -> phải
        		R = get_right(deri)
                check_most_left = False
			    check_having_nTerminal = False
			    # Chú ý đến kí tự KKT đầu tiên bên trái để đặt trỏ
        		for s in list(R):	# Duyệt các kí tự VP của DX
        			childNode = parent_node.addChild(Node(s))#Thêm các node con
        			if s is non terminal :
        				check_having_nTerminal = True
        				if not check_most_left:
        					current_node = childNode
        					check_most_left = True
        				else :
        					# Thêm các kí thự KKT còn lại vào stack
        					pStack.push(childNode)
        		if not check_having_nTerminal :
        			# Khi xog một nhánh(bên trái) Duyệt tiếp nhánh có gốc trên stack
        			current_node = pStack.pop()
        	return dTree
        """
        from Stack import Stack
        from anytree import Node, RenderTree
        def extract_PTree():
                stack = Stack()
                root = Node(start_sym)
                current_node = root
                for deri in derivation_input :
                        R = deri.right_token()
                        check_most_left = False
                        check_having_nTerminal = False
                        parent_node = current_node
                        for s in R:
                                child_node = Node(s, parent = parent_node)
                                if s in nterminal_syms:
                                        check_having_nTerminal = True
                                        if not check_most_left:
                                                current_node = child_node
                                                check_most_left = True
                                        else :
                                                stack.push(child_node)

                        if not check_having_nTerminal:
                                try :
                                        current_node = stack.pop()
                                except :
                                        if deri == derivation_input[-1]:
                                                pass
                                        else :
                                                raise("Error")
                return root
        root = extract_PTree()
        if is_print :
                print("Algorithm 2 : Derivation -> Parse Tree")
                print("- Input : LM Derivation")
                for deri in derivation_input:
                        print(deri)
                print("\n- Output : Parse Tree :")
                print(RenderTree(root))
                print("Yeild : ", genString_fromTree(root))
        return root


#### Main
if __name__ == "__main__":
        print("Running algorihms :")
        # Parse Tree -> Derivation
        Algorithm1()
        print('--------------------------------------------------------')
        # Derivation -> Parse Tree
        r = Algorithm2()