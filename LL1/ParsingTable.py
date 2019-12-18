import sys

def first_of_alpha(alpha,terminal,first_of_variables):
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

def parsing_table(production,terminal,first_of_variables,follow_of_variables):
    ans = dict()
    x = set(terminal) - {'^'}    # Terminals union '$'
    x = x.union('$')
    for var in production:
        ans[var] = dict()
        for t in x:
            ans[var][t] = 'Null'  # Denoting empty places by 'Null'
    flag = 0
    for var in production:
        for rhs in production[var]:
            tmp_set = first_of_alpha(rhs, terminal, first_of_variables)
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
#        sys.exit()
    return ans
