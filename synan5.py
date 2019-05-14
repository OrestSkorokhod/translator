# from lexan import lexems_out
import lexan

from lexem import Lexem
from relation import Relation

lexems_in = ['int', 'float', 'while', 'do', 'if', 'cin',
             'cout', '{', '}', ',', '.', ':', '=', '<<',
             '>>', '<', '>', '<=', '>=', '==', '!=', '+', '-', '*',
             '(', ')', '/', '?', '\n', 'or', 'and', '!']

class SyntaxAnalyser5:
    lexemes = []
    reshitka = Lexem(lexem='#', idn_code='', con_code='')
    stack = [reshitka]
    rel_table = None
    copy_lexemes = []

    rozbir_table = ''
    poliz = []
    def __init__(self):
        self.stack = [self.reshitka]
        rel = Relation()
        self.rel_table = dict(rel.r_table)
        self.rel_table['#'] = dict()
        for k in rel.r_table:
            self.rel_table['#'][k] = '<'
            self.rel_table[k]['#'] = '>'

        self.from_table_to_list(lexan.lexems_out)

        self.lexemes.append(Lexem(lexem='#'))


    def from_table_to_list(self, lexems_out):
        kek_lexemes = []

        for string in lexems_out:
            lex = Lexem()
            lex.number = string['number']
            lex.lexem = str(string['lex'])
            lex.code = string['code']
            lex.line = string['line']
            lex.idn_code = string['idn_code']
            lex.con_code = string['con_code']
            self.lexemes.append(lex)
            self.copy_lexemes.append(lex)
            kek_lexemes.append(lex)

        return kek_lexemes



    def compare(self, lex):
        def id_or_con_check(element):
            if element.idn_code != '':
                return 'id'
            elif element.con_code != '':
                return 'con'
            else:
                return element

        if str(self.stack[len(self.stack) - 1]) == '<program>':
            # print('all is ok')
            pass
        else:

            relation = self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 1]))][str(id_or_con_check(lex))]

            self.rozbir_table += '| {} '.format(relation)

            self.rozbir_table += '| {}'.format(','.join([str(self.copy_lexemes[i - 1]) for i in range(self.number_of_lexems_out, len(self.lexemes))])).ljust(100)

            if relation in ('=', '<'):
                self.stack.append(lex)
                # print('appended')
                # print('Stack: {}'.format(self.stack))
                self.rozbir_table += '|'.ljust(60)
                self.rozbir_table += '|{}'.format(','.join([str(i) for i in self.poliz])) + '\n'
                self.write_stack()

            elif relation == '>':
                rule = []

                while self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 2]))][str(id_or_con_check(self.stack[len(self.stack) - 1]))] != '<':
                    rule.insert(0, str(self.stack.pop()))
                rule.insert(0, str(self.stack.pop()))

                # print('rule: {}'.format(rule))

                self.rozbir_table += '| {}'.format(''.join([str(i) for i in rule])).ljust(60)

                for grammar_rule, description in Relation().grammar.items():
                    if rule in description:
                        # print('desc', description)
                        if len(rule) >= 2 and str(rule[0]) == '-':
                            # print('\n\n\n\n')
                            self.poliz.append('@')
                        if len(rule) >= 3 and str(rule[1]) in ('-', '+', '*', '/'):
                            # print('\n\n\n\n')
                            self.poliz.append(str(rule[1]))
                        self.rozbir_table += '|{}'.format(','.join([str(i) for i in self.poliz])) + '\n'
                        self.stack.append(Lexem(lexem=grammar_rule, idn_code='', con_code=''))
                        self.write_stack()
                        # self.rozbir_table += '|{}'.format(grammar_rule).ljust(60) + '\n'
                        # print('Stack: {}'.format(self.stack))
                        self.compare(lex)
                        break
                else:
                    raise Warning('Syntax error in line {} after {}'.format(lex.line, self.get_line(lex)));

            else:
                raise Warning('Syntax error in line {} after {}'.format(lex.line, self.get_line(lex)));


    def get_line(self, lexem):
        line = []
        for lex in self.copy_lexemes:
            if lex.line == lexem.line and lex.number < lexem.number:
                line.append(lex.lexem)
            elif lex.line > lexem.line:
                break
        return ' '.join(line)

    def write_stack(self):
        self.rozbir_table += '{}'.format(','.join([str(i) for i in self.stack])).ljust(100) # + '\n'

    def count_poliz(self):
        def summa(a, b):
            return float(a) + float(b)
        def vidnim(a, b):
            return float(a) - float(b)
        def mnoj(a, b):
            return float(a) * float(b)
        def dil(a, b):
            # print(type(a), type(b))
            # print(a, b)
            # print(float(a) / float(b))
            return float(a) / float(b)
        def un_min(a):
            return - float(a)



        opers = {'+': summa,
                 '-': vidnim,
                 '*': mnoj,
                 '/': dil,
                 '@': un_min}

        self.rozbir_poliz_table = ''

        self.poliz_stack = []
        number = 0
        # print('keke', dil(225, 25))
        for j in self.poliz:
            # print(j)
            number += 1
            # print(number)
            self.rozbir_poliz_table += '{}'.format(','.join([str(i) for i in self.poliz_stack])).ljust(70)
            self.rozbir_poliz_table += '| {}'.format(','.join([str(self.poliz[i-1]) for i in range(number, len(self.poliz)+1)])).ljust(70) + '\n'
            if j.isdigit():


                self.poliz_stack.append(j)

            elif j in ('+', '-', '*', '/'):
                r2 = self.poliz_stack.pop()
                r1 = self.poliz_stack.pop()
                self.poliz_stack.append(opers.get(j)(r1, r2))
            elif j == '@':
                r1 = self.poliz_stack.pop()
                self.poliz_stack.append(opers.get(j)(r1))
        self.rozbir_poliz_table += '{}'.format(','.join([str(i) for i in self.poliz_stack])).ljust(70)
        return self.poliz_stack[0]





    def analyse(self):
        self.stack = []
        is_declaration = True
        self.stack.append(self.reshitka)
        self.lexemes = []
        self.poliz = []
        self.from_table_to_list(lexan.lexems_out)

        self.write_stack()

        self.number_of_lexems_out = 0

        for lex in self.lexemes:
            self.number_of_lexems_out += 1
            if lex.lexem == '{':
                is_declaration = False
            # print('------------')
            # print('Lexem: {}'.format(lex.lexem))
            # print('Stack: {}'.format(self.stack))

            if lex.idn_code != '':
                # if not is_declaration:
                    # self.poliz.append(lex.lexem)
                lex.lexem = 'id'
            elif lex.con_code != '':
                if not is_declaration:
                    self.poliz.append(lex.lexem)
                lex.lexem = 'con'

            self.compare(lex)
        print(self.poliz)
        # print(self.count_poliz())
