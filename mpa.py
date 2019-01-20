import lexan
import synan


class MPA:
    def __init__(self):
        self.i = 0
        self.last_state = 5
        self.stack = []
        self.state = 1
        self.is_end = False
        self.op_bl = 'operators_block'
        self.op = 'operator'
        self.exp = 'expression'
        self.log_e = 'logical expression'
        self.lexemes = lexan.lexems_out
        self.idns = lexan.idn_out
        self.cons = lexan.con_out
        self.analys_table = []
        self.avtomat_stanes = {
            '1': [['int', '', 2, 'error'],
                  ['float', '', 2, 'error']],
            '2': [['id', '', 3, 'error']],
            '3': [[',', '', 2, 'error'],
                  ['\\n', '', 4, 'error']],
            '4': [['int', '', 2, self.op_bl, 5],
                  ['float', '', 2, self.op_bl, 5]],
            '5': [['', '', '', 'exit']],
            '6': [['{', '', 7, 'error']],
            '7': [['\\n', 8, 11, 'error']],
            '8': [['\\n', '', 9, 'error']],
            '9': [['}', '', 10, self.op, 8]],
            '10': [['', '', '', 'exit']],
            '11': [['if', 12, 28, 'error'],
                   ['while', 15, 28, 'error'],
                   ['id', '', 17, 'error'],
                   ['cin', '', 19, 'error'],
                   ['cout', '', 22, 'error']],
            '12': [['?', 13, 6, 'error']],
            '13': [[':', 14, 6, 'error']],
            '14': [['', '', '', 'exit']],
            '15': [['do', 16, 6, 'error']],
            '16': [['', '', '', 'exit']],
            '17': [['=', 18, 25, 'error']],
            '18': [['', '', '', 'exit']],
            '19': [['>>', '', 20, 'error']],
            '20': [['id', '', 21, 'error']],
            '21': [['>>', '', 20, 'exit']],
            '22': [['<<', '', 23, 'error']],
            '23': [['id', '', 24, 'error']],
            '24': [['<<', '', 23, 'exit']],
            '25': [['+', '', 26, 'error', ''],
                   ['-', '', 26, 'error', ''],
                   ['(', 27, 25, 'error', ''],
                   ['id', '', 271, 'error', ''],
                   ['con', '', 271, 'error', '']],
            '26': [['id', '', 271, 'error'],
                   ['con', '', 271, 'error'],
                   ['(', 27, 25, 'error']],
            '27': [[')', '', 271, 'error']],
            '271': [['+', '', 25, 'exit'],
                    ['-', '', 25, 'exit'],
                    ['*', '', 26, 'exit'],
                    ['/', '', 26, 'exit']],
            '28': [['!', '', 28, self.exp, 29],
                   ['(', 30, 28, self.exp, 29]],
            # '281': [['', '', '', '28', '']],
            '29': [['<', 31, 25, 'error'],
                   ['>', 31, 25, 'error'],
                   ['<=', 31, 25, 'error'],
                   ['>=', 31, 25, 'error'],
                   ['==', 31, 25, 'error'],
                   ['!=', 31, 25, 'error']],
            '30': [[')', '', 31, 'error']],
            '31': [['or', '', 28, 'exit'],
                   ['and', '', 28, 'exit']]
        }

    def error(self, message = ''):
        if len(self.lexemes) <= self.i:
            lexan.error_text.append('Syntax error in line {}'.format(self.lexemes[self.i - 1]['line']))
        else:
            lexan.error_text.append('Syntax error in line {}'.format(self.lexemes[self.i]['line']))
        # synan.SyntaxAnalyser.syntax_error(message)

    def automat(self):
        #for lex_row in self.lexemes:
        while not self.is_end:
            lex_row = self.lexemes[self.i]
            self.i += 1
            lex = lex_row['lex']
            # if lex == '{':
            #     print('kek')
            non_equal = ''
            self.analys_table.append([lex, [*self.stack], self.state])
            for row in self.avtomat_stanes[str(self.state)]:
                # print(row)
                non_equal = row[3]
                if (row[0] == lex) or (row[0] == 'id' and lex_row['code'] == 100) or (row[0] == 'con' and lex_row['code'] == 101):
                    # print(self.stack)
                    # self.analys_table.append([lex, [*self.stack], self.state])
                    if row[1] != '':
                        self.stack.append(row[1])
                    self.state = row[2]
                    break

            else:
                if non_equal == 'error':
                    self.error()
                    self.is_end = True
                    break
                elif non_equal == 'exit':
                    if len(self.stack) > 0:
                        self.state = self.stack.pop()
                        self.i -= 1
                    else:
                        self.is_end = True
                        break
                else:
                    # print(row)
                    if row[4] != '':
                        self.stack.append(row[4])

                    if non_equal == self.op_bl:
                        self.state = 6
                        self.i -= 1
                    elif non_equal == self.op:
                        self.state = 11
                        self.i -= 1
                    elif non_equal == self.exp:
                        self.state = 25
                        self.i -= 1
                    elif non_equal == self.log_e:
                        self.state = 28
                        self.i -= 1
                    elif non_equal == '28':
                        self.state = 28
                        self.i -= 1


    def make_table(self):
        str_to = '{:30s}|{:30s}|{:30s}|\n'.format('lexem', 'stack', 'state')
        str_to += '-' * (3 * 31) + '\n'
        for line in self.analys_table:
            # str_to += '\n' + '-' * (len(line) * 31) + '\n'
            for v in line:
                str_to += '{:30s}|'.format(str(v))
            str_to += '\n' + '-' * (len(line) * 31) + '\n'
        return str_to

