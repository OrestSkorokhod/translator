

class Relation:

    def __init__(self):
        # self.grammar = {'<program>': [['<declaration list>', '<operators block>']],
        #                 '<declaration list>': [['<declaration>'], ['<declaration list>', '<declaration>']],
        #                 '<declaration>': [['<type>', '<variables list>', '\\n']],
        #                 '<type>': [['int'], ['float']],
        #                 '<variables list>': [['id'], ['id', '<variables list>']],
        #                 '<operators list>': [['<operator>', '\\n'], ['<operators list>', '<operator>', '\\n']],
        #                 '<operators block>': [['{', '\\n', '<operators list>', '}']],
        #                 '<operator>': [['<loop>'], ['<condition>'], ['<assigning>'], ['<input>'], ['<output>']],
        #                 '<loop>': [['while', '<LE>', 'do', '<operators block>']],
        #                 '<condition>': [['if', '<LE>', '?', '<operators block>']],
        #                 '<assigning>': [['id', '=', '<E>']],
        #                 '<input>': [['cin', '>>', 'id'], ['<input>', '>>', 'id']],
        #                 '<output>': [['cout', '<<', 'id'], ['<output>', '<<', 'id']],
        #                 '<E>': [['<E>', '+', '<T>'], ['<E>', '-', '<T>'], ['<T>']],
        #                 '<T>': [['<T>', '*', '<F>'], ['<T>', '/', '<F>'], ['<sign>', '<F>']],
        #                 '<F>': [['id'], ['con'], ['(', '<E>', ')']],
        #                 '<sign>': [['-'], ['+']],
        #                 '<LE>': [['<LT>'], ['<LE>', 'or', '<LT>']],
        #                 '<LT>': [['<LF>'], ['<LF>', 'and', '<LT>']],
        #                 '<LF>': [['<R>'], ['(', '<LE>', ')'], ['!', '<LF>']],
        #                 '<R>': [['<E>', '<LS>', '<E>']],
        #                 '<LS>': [['<'], ['>'], ['<='], ['>='], ['!='], ['==']]
        #                 }
        self.grammar = {'<program>': [['<declaration list>', '<operators block>']],

                        # '<declaration list1>': [['declaration list']],
                        '<declaration list>': [['<declaration1>', '\\n'], ['<declaration list>', '<declaration1>', '\\n']],

                        '<declaration1>': [['<declaration>']],
                        '<declaration>': [['<type>', 'id'], ['<declaration>', ',', 'id']],


                        '<type>': [['int'], ['float']],

                        # '<operators block1>': [['<operators block>']],
                        '<operators block>': [['{', '<operators list1>', '}']],

                        '<operators list1>': [['<operators list>']],
                        '<operators list>': [['<operator1>', '\\n'], ['<operators list>', '<operator1>', '\\n']],



                        '<operator1>': [['<operator>']],
                        '<operator>': [['<loop>'], ['<condition>'], ['<assigning>'], ['<input>'], ['<output>']],

                        # '<N>': [['\\n']],


                        # '<loop1>': [['<loop>']],
                        '<loop>': [['while', '<LE1>', 'do', '<operators block>']],
                        # '<condition1>': [['<condition>']],
                        '<condition>': [['if', '<LE1>', '?', '<operators block>', ':', '<operators block>']],
                        '<assigning>': [['id', '=', '<E1>']],
                        '<input>': [['cin', '>>', 'id'], ['<input>', '>>', 'id']],
                        '<output>': [['cout', '<<', 'id'], ['<output>', '<<', 'id']],


                        '<E1>': [['<E>']],
                        '<E>': [['<E>', '+', '<T1>'],
                                ['<E>', '-', '<T1>'],
                                ['<T1>'],
                                ['-', '<T1>']], #змінено

                        '<T1>': [['<T>']],
                        '<T>': [['<T>', '*', '<F1>'], ['<T>', '/', '<F1>'], ['<F1>']],

                        '<F1>': [['<F>']],
                        # '<F>': [['id'], ['-', 'id'], ['+', 'id'], ['con'], ['-', 'con'], ['(', '<E1>', ')']],
                        '<F>': [['id'],  ['con'], ['(', '<E1>', ')']],    #змінено

                        # '<sign1>': [['<sign>']],
                        # '<sign>': [['-'], ['+']],

                        '<LE1>': [['<LE>']],
                        '<LE>': [['<LT1>'], ['<LE>', 'or', '<LT1>']],

                        '<LT1>': [['<LT>']],
                        '<LT>': [['<LF1>'], ['<LT>', 'and', '<LF1>']],

                        '<LF1>': [['<LF>']],
                        '<LF>': [['[', '<R>', ']'], ['(', '<LE1>', ')'], ['!', '<LF>']],
                        '<R>': [['<E1>', '<LS1>', '<E1>']],

                        '<LS1>': [['<LS>']],
                        '<LS>': [['<'], ['>'], ['<='], ['>='], ['!='], ['==']]
                        }
        # self.grammar = {'<Z>': [['b', '<M>', 'b']],
        #                 '<M>': [['(', '<L>'], ['a']],
        #                 '<L>': [['<M>', 'a', ')']]}
        #
        self.terminals = set()
        self.not_terminals = set()
        self.set_terminals()
        self.last_pluses = {}
        self.first_pluses = {}
        self.r_table = dict()
        self.count_of_conflicts = 0
        # self.r_table['dec'] = dict()
        # self.r_table['dec']['kek'] = 'lola'
        # print(self.r_table)
        self.set_relation()
        # print(self.r_table)
        # print(self.last_plus('<LF>'))
        # print(self.first_plus('<LE>'))

    def set_terminals(self):
        for rule, variants in self.grammar.items():
            for variant in variants:
                for word in variant:
                    if word[0] == '<' and word[-1] == '>':
                        self.not_terminals.add(word)
                    else:
                        self.terminals.add(word)

    def last_plus(self, word):
        last_set = set()

        def last_p(word_):
            if word_ in self.terminals:
                last_set.add(word_)
            else:
                for variant in self.grammar[word_]:
                    last_set.add(variant[-1])
                    if variant[-1] in self.not_terminals:
                        if variant[-1] == word_:
                            last_set.add(word_)
                        else:
                            last_p(variant[-1])
        last_p(word)

        return last_set

    def first_plus(self, word):
        first_set = set()

        def first_p(word_):
            if word_ in self.terminals:
                first_set.add(word_)
            else:
                for variant in self.grammar[word_]:
                    first_set.add(variant[0])
                    if variant[0] in self.not_terminals:
                        if variant[0] == word_:
                            first_set.add(word_)
                        else:
                            first_p(variant[0])

        first_p(word)

        return first_set

    def set_relation(self):
        rozdilnik = '.'
        for word in self.not_terminals:
            self.r_table[word] = dict()
            for word2 in self.not_terminals:
                self.r_table[word][word2] = '{:5s}'.format(rozdilnik)
            for word2 in self.terminals:
                self.r_table[word][word2] = '{:5s}'.format(rozdilnik)
        for word in self.terminals:
            self.r_table[word] = dict()
            for word2 in self.not_terminals:
                self.r_table[word][word2] = '{:5s}'.format(rozdilnik)
            for word2 in self.terminals:
                self.r_table[word][word2] = '{:5s}'.format(rozdilnik)

        for rule, variants in self.grammar.items():
            for variant in variants:
                if len(variant) >= 2:
                    for i in range(len(variant) - 1):
                        # print(variant)
                        # self.r_table[variant[i]] = dict()
                        self.r_table[variant[i]][variant[i + 1]] = '='
                        self.first_rule(variant[i], variant[i + 1])
                        self.second_rule(variant[i], variant[i + 1])

    def make_table(self):
        str_to = ' ' * 30
        for key in self.r_table:
            str_to += '{:5s}'.format(key[:5])
        addition = ''
        count = 0
        str_to += '\n'
        for key, value in self.r_table.items():
            str_to += '{:30s}'.format(key)
            # addition += key + ' '
            for k, v in value.items():
                # print(v)
                if not v == '.    ':
                    addition += key + ' ' + k + ' ' + v + '\n'
                    count += 1
                # print(key,k,v)
                # print(len(v))
                str_to += '{:5s}'.format(v)
                # str_to += v
            str_to += '\n'
        str_to += 'Count of conflicts is {}\n'.format(self.count_of_conflicts)
        # print(self.first_plus('<sign>'))
        return str_to + addition + '\nNumber of signs:{}'.format(count)

    def first_rule(self, word1, word2):
        if word2 in self.not_terminals:
            firsts = self.first_plus(word2)
            for one in firsts:
                # print(word1, one)
                if self.r_table[word1][one] == '.    ' or self.r_table[word1][one] == '<':
                    self.r_table[word1][one] = '<'
                else:
                    self.count_of_conflicts += 1
                    self.r_table[word1][one] += '<'

    def second_rule(self, word1, word2):
        if word1 in self.not_terminals:
            lasts = self.last_plus(word1)
            # firsts = self.first_plus(word2)
            if word2 in self.terminals:
                for one in lasts:
                    # print(one, word2)
                    if self.r_table[one][word2] == '.    ' or self.r_table[one][word2] == '>':
                        self.r_table[one][word2] = '>'
                    else:
                        self.count_of_conflicts += 1
                        self.r_table[one][word2] += '>'
            else:
                firsts = self.first_plus(word2)
                for one in lasts:
                    for one_f in firsts:
                        # print('kek')
                        if self.r_table[one][one_f] == '.    ' or self.r_table[one][one_f] == '>':
                            self.r_table[one][one_f] = '>'
                        else:
                            self.count_of_conflicts += 1
                            self.r_table[one][one_f] += '>'
