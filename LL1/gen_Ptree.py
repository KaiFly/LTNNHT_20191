from anytree import Node
import Stack as st


def LMD_PTree(start_sym, derivation):
    derivation_input = derivation
    def extract_PTree():
        stack = st.Stack()
        root = Node(start_sym)
        current_node = root
        for deri in derivation_input :
            R = deri.right_token()
            check_most_left = False
            check_having_nTerminal = False
            parent_node = current_node
            for s in R:
                child_node = Node(s, parent = parent_node)
                if s.isupper():
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
    return extract_PTree()

