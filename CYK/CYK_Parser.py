from collections import defaultdict

class ParseTree:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None

    def __str__(self):
        if self.is_leaf():
            return str(self.data)
        else:
            return '{}({},{})'.format(self.data, self.left, self.right)

class CYKParser:
    def __init__(self, grammar, dictionary):
        self.grammar = grammar
        self.dictionary = dictionary
        self.chart = []
        self.pred = True

    def from_files(grammar_file, dict_file):
        grammar = CYKParser.create_dict(grammar_file)
        dictionary = CYKParser.create_dict(dict_file)
        return CYKParser(grammar, dictionary)

    def create_dict(file):
        d = defaultdict(set)
        with open(file) as infile:
            for line in infile:
                arr = line.split('->')
                left = arr[0].strip()
                right = arr[1].strip()
                # Bottom-up parsing
                d[right].add(left)
        return d

    def parse(self, sentence):
        words = sentence.split(' ')
        self.chart = self.create_chart(len(words))
        self.fill_chart_with_dictionary(words)
        self.complete_chart(words)
        res_tree = self.create_parse_trees(self.chart)
        try :
            res_tree[1]
        except :
            self.pred = False
            return
        return res_tree

    def create_chart(self, length):
        chart = []
        for i in range(length):
            column = [None] * (i + 1)
            chart.append(column)
        return chart

    def fill_chart_with_dictionary(self, words):
        for i in range(len(self.chart)):
            self.chart[i][i] = {CYKParser.ChartNode(x) for x in self.dictionary[words[i]]}

    def complete_chart(self, words):
        for offset in range(1, len(words), 1):
            for i in range(len(words) - offset):
                self.complete_chart_field(i + offset, i)

    def complete_chart_field(self, x, y):
        left = x - 1
        down = len(self.chart[x]) - 1
        count = len(self.chart[x]) - (y + 1)
        chart_field = set()
        for i in range(count):
            left_set = self.chart[left][y]
            down_set = self.chart[x][down]
            combinations = self.set_combinations(left_set, down_set)
            result = set()
            for c1, c2 in combinations:
                parsed = self.grammar['{} {}'.format(c1.data, c2.data)]
                if len(parsed) != 0:
                    data = list(parsed)[0]
                    same_data = [x for x in result if x.data == data]
                    if len(same_data) > 0:
                        same_data[0].append_pointers(c1, c2)
                    else:
                        result.add(CYKParser.ChartNode(data, c1, c2))
            for c in result:
                same_data = [x for x in chart_field if x.data == c.data]
                if len(same_data) > 0:
                    same_data[0].extend_pointers(c.pointers)
                else:
                    chart_field.add(c)
            left -= 1
            down -= 1
        self.chart[x][y] = chart_field

    def set_combinations(self, set1, set2):
        result = set()
        for x in set1:
            for y in set2:
                result.add((x, y))
        return result

    class ChartNode:
        def __init__(self, data, left=None, right=None):
            self.data = data
            self.pointers = []
            if left is not None and right is not None:
                self.pointers.append((left, right))

        def append_pointers(self, left, right):
            self.pointers.append((left, right))

        def extend_pointers(self, new_pointers):
            self.pointers.extend(new_pointers)

        def __str__(self):
            return str(self.data)

    def print_chart(self):
        line_start = 0
        for row in range(len(self.chart)):
            s = ' ' * line_start
            for column in range(row, len(self.chart), 1):
                string_set = {str(c) for c in self.chart[column][row]}
                tmp = '{}' if len(string_set) == 0 else str(string_set)
                s += tmp + ' ' * (15 - len(tmp))
                if column == row:
                    line_start = len(s)
            print(s)

    def create_parse_trees(self, chart, start=None):
        if start is None:
            try :
                start = list(chart[len(chart) - 1][0])[0]
            except :
                self.pred = False
                return
        if len(start.pointers) == 0:
            return [ParseTree(start.data)]
        parse_trees = []
        for l, r in start.pointers:
            left_tree = self.create_parse_trees(chart, l)
            right_tree = self.create_parse_trees(chart, r)
            for x in left_tree:
                for y in right_tree:
                    parse_trees.append(ParseTree(start.data, x, y))
        return parse_trees


if __name__ == '__main__':
    print("CYK Parser")
    parser = CYKParser.from_files('CFGrammar.txt', 'dictionary.txt')
    string = "conmeo nhin nhu  mot cucbong"
    trees = parser.parse(string)
    print("\n Parsing Table")
    parser.print_chart()
    if parser.pred :
        print("\n String Accepted!!")
        print("\n Parse Tree : ")
        print(trees[1])
    else :
        print("\n String iRejects!!")