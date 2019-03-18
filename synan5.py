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
    def __init__(self):
        self.stack = [self.reshitka]
        rel = Relation()
        self.rel_table = dict(rel.r_table)
        self.rel_table['#'] = dict()
        for k in rel.r_table:
            # print(k)
            self.rel_table['#'][k] = '<'
            # print(self.rel_table['#'][k])
            self.rel_table[k]['#'] = '>'
        # self.rel_table['<=']['('] = '>'
        # print(self.rel_table['#'])


        # print(rel_table)
        self.from_table_to_list(lexan.lexems_out)
        # print(self.lexemes)
        self.lexemes.append(Lexem(lexem='#'))
        # self.analyse()

    def from_table_to_list(self, lexems_out):
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
        # self.copy_lexemes = list(self.lexemes)


    def compare(self, lex):
        def id_or_con_check(element):
            #   str(self.stack[len(self.stack) - 1]) if self.stack[len(self.stack) - 1].idn_code == '' else 'id'
            # print(element)
            # print(type(element))
            if element.idn_code != '':
                return 'id'
            elif element.con_code != '':
                return 'con'
            else:
                return element

        # print('peak: {}'.format(self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 1]))]))
        # print(str(id_or_con_check(lex)))
        # print(self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 1]))]['float'])
        if str(self.stack[len(self.stack) - 1]) == '<program>':
            print('all is ok')
        else:
            if self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 1]))][str(id_or_con_check(lex))] in ('=', '<'):
                self.stack.append(lex)
                print('appended')
                print('Stack: {}'.format(self.stack))
                self.rozbir_table += '{}'.format(','.join([str(i) for i in self.stack])).ljust(100)
                self.rozbir_table += '|'.ljust(60)
                self.rozbir_table += '|'.ljust(60) + '\n'
            elif self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 1]))][str(id_or_con_check(lex))] == '>':
                rule = []
                # print('peak: {}'.format(self.stack[len(self.stack) - 1]))

                # if self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 2]))][str(id_or_con_check(self.stack[len(self.stack) - 1]))] == '<':
                #     rule.insert(0, str(self.stack.pop()))
                # else:
                #     if len(self.stack) > 1:
                #         while self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 2]))][str(id_or_con_check(self.stack[len(self.stack) - 1]))] != '<':
                #             print('lol')
                #             rule.insert(0, str(self.stack.pop()))
                while self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 2]))][str(id_or_con_check(self.stack[len(self.stack) - 1]))] != '<':
                    # print('lol')
                    rule.insert(0, str(self.stack.pop()))
                rule.insert(0, str(self.stack.pop()))

                self.rozbir_table += '{}'.format(','.join([str(i) for i in self.stack])).ljust(100)
                print('rule: {}'.format(rule))
                self.rozbir_table += '|{}'.format(''.join([str(i) for i in rule])).ljust(60)
                for grammar_rule, description in Relation().grammar.items():
                    if rule in description:
                        self.stack.append(Lexem(lexem=grammar_rule, idn_code='', con_code=''))
                        self.rozbir_table += '|{}'.format(grammar_rule).ljust(60) + '\n'
                        print('Stack: {}'.format(self.stack))
                        self.compare(lex)
                        # self.stack.append(lex)

                        break
                else:
                    raise Warning('Syntax error in line {} after {}'.format(lex.line, self.get_line(lex)));
            else:
                raise Warning('Syntax error in line {} after {}'.format(lex.line, self.get_line(lex)));

    def get_line(self, lexem):
        line = []
        for lex in self.copy_lexemes:
            # print(lex)
            if lex.line == lexem.line and lex.number < lexem.number:
                line.append(lex.lexem)
            elif lex.line > lexem.line:
                break
        return ' '.join(line)


    def analyse(self):
        self.stack = []
        self.stack.append(self.reshitka)
        self.lexemes = []
        self.from_table_to_list(lexan.lexems_out)
        for lex in self.lexemes:
            print('------------')
            print('Lexem: {}'.format(lex.lexem))
            print('Stack: {}'.format(self.stack))
            # print(lex.idn_code)
            # new_lex = Lexem()

            if lex.idn_code != '':
                lex.lexem = 'id'
            elif lex.con_code != '':
                lex.lexem = 'con'

            # self.rozbir_table += '{}'.format(lex)

            self.compare(lex)


            # if self.stack[len(self.stack) - 1] == '#' or \
            #  self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 1]))][str(id_or_con_check(lex))] in ('=', '<'):
            #     self.stack.append(lex)
            #     print('appended')
            # elif self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 1]))][str(id_or_con_check(lex))] == '>':
            #     rule = []
            #
            #     while self.stack[len(self.stack) - 2] == '#' or \
            #     self.rel_table[str(id_or_con_check(self.stack[len(self.stack) - 2]))][str(id_or_con_check(self.stack[len(self.stack) - 1]))] != '<':
            #         # print(self.stack)
            #         rule.insert(0, str(self.stack.pop()))
            #         if self.stack[len(self.stack) - 1] == '#':
            #             break
            #
            #     print('rule: {}'.format(rule))
            #     for grammar_rule, description in Relation().grammar.items():
            #         if rule in description:
            #             self.stack.append(Lexem(lexem=grammar_rule, idn_code='', con_code=''))
            #
            #             self.compare(lex)
            #
            #
            #             self.stack.append(lex)
            #
            #             break
