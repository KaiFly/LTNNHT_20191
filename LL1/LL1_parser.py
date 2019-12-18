import re
from prettytable import PrettyTable
from First import first_fn
from Follow import follow_fn
from ParsingTable import parsing_table
import Stack as st
from anytree import Node, RenderTree

def input_string_printer(input_list,input_pointer):
    str = ''
    for i in input_list[input_pointer:]:
        str = str + i + " "
    return str

class production:
    def __init__(self, left_side = None, right_side = None):
        self.ls = left_side
        self.rs = right_side

    def toStr(self):
        s = self.ls + "->" + self.rs
        return s

    def right_token(self):
        return self.rs.split(" ")

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

if __name__ == '__main__':
    print("LL1 - Parser")
    L = []
    production_dict = dict()     # Productions for each variable as a dictionary with key as variable
    Grammar_file = open("Grammar3.txt","r")   # file containing production rules
    for line in Grammar_file:
        line = line.rstrip()
        l = re.split("->|\|| ", line)
        l = list(filter(None,l))
        if l:
            L.append(l)
    Grammar_file.close()
    start_symbol = L[0][0]
    terminal = L[2]
    for i in range(3, len(L), 1):
        production_dict[L[i][0]] = [j for j in L[i][1:]]

#    print('\nTerminal Symbols =',terminal)
    #print(production)
    first_of_variables = first_fn(production_dict,terminal)
    follow_of_variables = follow_fn(production_dict,terminal,start_symbol,first_of_variables)
    ###############################################################
    print('\nFirst of Variables : ')
    for var in first_of_variables:
        print(var,'-',first_of_variables[var])
    print('\nFollow of Variables : ')
    for var in follow_of_variables:
        print(var,'-',follow_of_variables[var])
    ###############################################################
    table = parsing_table(production_dict,terminal,first_of_variables,follow_of_variables)
    #print(table)
    print('\nParsing Table')
    ########### TABLE FORMATTING #############
    tmp_table = table
    x = terminal
    if '^' in x:
        x.remove('^')
    x.append('$') ; x.sort()
    l1 = ['Var/Term']
    x = ['Var/Term'] + x
    obj = PrettyTable(x)
    for var in tmp_table:
        tmp_list = list(var)
        ddd = tmp_table[var]
        for key in sorted(ddd):
            tmp_list.append(ddd[key])
        obj.add_row(tmp_list)
    print(obj)
    ##########################################
    ######### PARSING OF INPUT STRING ########
    input_file = open("input2.txt","r");
    for line in input_file:
        input_string = line.rstrip()

    input_string = input_string + '$'
    #print(input_string)
    input_list = []

    tmp_input_string = ''
    #print(terminal)
    for i in input_string:
        if i != ' ':
            tmp_input_string = tmp_input_string + i
        #print(tmp_input_string)
        if tmp_input_string in terminal:
            input_list.append(tmp_input_string)
            tmp_input_string = ''
    #input_list.append('$')
    print()
    print(input_list,'\n')
    ################# STACK #####################
    valid = 1
    input_pointer = 0
    stack = st.Stack()
    stack.push('$')
    stack.push(start_symbol)
    print(stack.print_bottom_up() + "        " + input_string_printer(input_list,input_pointer))
    deri_list = []
    while stack.top() != '$':
        top_sym = stack.top()
        next_input = input_list[input_pointer]
        #### table[top_sym][next_input]=',TD'                 ## Testing purpose
        if top_sym.isupper():
            ls = top_sym
            if table[top_sym][next_input]=='Null':
                valid = 0
                break;
            else:
                tmp_list_2 = []
                char = ''
                length = len(table[top_sym][next_input])

                for i in range(length):
                    char_ = table[top_sym][next_input][i]
                    char = char + table[top_sym][next_input][i]
                    if(char_.isupper()):
                        char = ''
                        tmp_list_2.append(char_)
                    else:
                        if char in terminal:
                            tmp_list_2.append(char)
                            char = ''
#                print("tmp list_2 : ", tmp_list_2)
                rs = " ".join(tmp_list_2)
                deri_list.append(production(ls, rs))
                stack.pop()
                tmp_list_2.reverse()
                for i in tmp_list_2:
                    stack.push(i)
                print(stack.print_bottom_up() + "        " + input_string_printer(input_list,input_pointer))
        else:
            if top_sym == input_list[input_pointer]:
                stack.pop()
                input_pointer = input_pointer + 1
                print(stack.print_bottom_up() + "        " + input_string_printer(input_list,input_pointer))
            else:
                valid = 0
                break
    if input_pointer != len(input_list)-1:
        valid = 0
    if valid == 1:
        print("\nString Accepted!!")
        print("\n1. LM Derivation :")
        for d in deri_list:
            print(d)
        print("\n2. Parse Tree")
        root = LMD_PTree(start_symbol, deri_list)
        print(RenderTree(root))

    else:
        print("\nString Rejects!!")