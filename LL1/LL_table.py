from prettytable import PrettyTable

class gen_table :

    def first_fn(self, production,terminal):
        ans = dict()
        for var in production:
            ans[var] = set()
        change = 1
        while change:
            change = 0
            for var in production:
                tmp_set = ans[var]
                for p in production[var]:
                    length = len(p)
                    char = ''
                    for i in range(length):
                        char_ = p[i]
                        char = char + p[i]
                        # print(char)
                        if (char_.isupper()):
                            char = ''
                            tmp_set = tmp_set.union(ans[char_])
                            # ^ is epsilon, checking variable have epsilon in left most positon
                            if ('^' in ans[char_]) and (i != length-1):
                                tmp_set = tmp_set - {'^'}
                            else:
                                break
                        else:
                            if (char in terminal):
                                set_terminal = set([char])
                                tmp_set = tmp_set.union(set_terminal)
                                break
                if tmp_set != ans[var]:
                    ans[var] = tmp_set
                    change = 1
        return ans

    def first_of_alpha(self, alpha,terminal,first_of_variables):
        ans = set()
        char = ''
        for i in range(len(alpha)):
            char_ = alpha[i]
            char = char + alpha[i]
            if(char_.isupper()):
                char = ''
                ans = ans.union(first_of_variables[char_])
                if ('^' in first_of_variables[char_]) and (i!=len(alpha)-1):
                    ans = ans - {'^'}
                else:
                    break
            else:
                if char in terminal:
                    set_terminal = set([char])
                    ans = ans.union(set_terminal)
                    break
        return ans

    def follow_fn(self, production,terminal,start_symbol,first_of_variables):
        ans = dict()
        for var in production:
            ans[var] = set()
        change = 1
        while change:
            change = 0
            for var in production:
                tmp_set = ans[var]
                if(var == start_symbol):
                    tmp_set = tmp_set.union({'$'})
                for lhs in production:
                    for p in production[lhs]:
                        if p.find(var)<0:
                            continue
                        elif p.find(var)<len(p)-1:
                            alpha = p[p.find(var)+1]
                            if '^' not in self.first_of_alpha(alpha,terminal,first_of_variables):
                                tmp_set = tmp_set.union(self.first_of_alpha(alpha,terminal,first_of_variables))
                            else:
                                tmp_set = tmp_set.union(self.first_of_alpha(alpha,terminal,first_of_variables))
                                tmp_set = tmp_set - {'^'}
                                tmp_set = tmp_set.union(ans[lhs])
                        else:
                            tmp_set = tmp_set.union(ans[lhs])
                if tmp_set != ans[var]:
                    ans[var] = tmp_set
                    change = 1
        return ans

    def parsing_table(self, production,terminal,first_of_variables,follow_of_variables):
        ans = dict()
        x = set(terminal) - {'^'}
        x = x.union('$')
        for var in production:
            ans[var] = dict()
            for t in x:
                ans[var][t] = 'Null'
        flag = 0
        for var in production:
            for rhs in production[var]:
                tmp_set = self.first_of_alpha(rhs, terminal, first_of_variables)
                for each in tmp_set:
                    if each == '^':
                        tmp_set_2 = follow_of_variables[var]
                        for some in tmp_set_2:
                            if(ans[var][some] != 'Null'):
                                flag = 1
                                break
                            else:
                                ans[var][some] = rhs
                    else:
                        if (ans[var][each] != 'Null'):
                            flag = 1
                            break
                        else:
                            ans[var][each] = rhs
                if flag:break
            if flag:break
        if flag:
            print("\nGiven grammar is not LL(1)")
            pass
        # sys.exit()
        return ans

    def print_Table(self, table, terminal):
        print('\nParsing Table')
        tmp_table = table
        x = terminal
        if '^' in x:
            x.remove('^')
        x.append('$') ; x.sort()
        x = ['Var/Term'] + x
        obj = PrettyTable(x)
        for var in tmp_table:
            tmp_list = list(var)
            ddd = tmp_table[var]
            for key in sorted(ddd):
                tmp_list.append(ddd[key])
            obj.add_row(tmp_list)
        print(obj)
