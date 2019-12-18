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

def follow_fn(production,terminal,start_symbol,first_of_variables):
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
                        if '^' not in first_of_alpha(alpha,terminal,first_of_variables):
                            tmp_set = tmp_set.union(first_of_alpha(alpha,terminal,first_of_variables))
                        else:
                            tmp_set = tmp_set.union(first_of_alpha(alpha,terminal,first_of_variables))
                            tmp_set = tmp_set - {'^'}
                            tmp_set = tmp_set.union(ans[lhs])
                    else:
                        tmp_set = tmp_set.union(ans[lhs])
            if tmp_set != ans[var]:
                ans[var] = tmp_set
                change = 1
    return ans
