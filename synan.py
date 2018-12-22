import lexan


class SyntaxAnalyser:
    def __init__(self):
        self.i = 0

    def syntax_error(self, message):
        lexan.error_text.append("Syntax error: {} in line {} : {}\n".format(message, lexan.lexems_out[self.i]['line'],
                                                                            lexan.lexems_out[self.i]['lex']))

    def log_sign(self):
        if lexan.lexems_out[self.i]['lex'] == '<':
            self.i += 1
            return True
        if lexan.lexems_out[self.i]['lex'] == '>':
            self.i += 1
            return True
        if lexan.lexems_out[self.i]['lex'] == '<=':
            self.i += 1
            return True
        if lexan.lexems_out[self.i]['lex'] == '>=':
            self.i += 1
            return True
        if lexan.lexems_out[self.i]['lex'] == '!=':
            self.i += 1
            return True
        if lexan.lexems_out[self.i]['lex'] == '==':
            self.i += 1
            return True
        return False

    def relation(self):
        if self.expression():
            if self.log_sign():
                if self.expression():
                    return True
                else:
                    self.syntax_error('missing expression for compare')
                    return False
            else:
                self.syntax_error("missing logical sign")
                return False
        else:
            return False

    def log_f(self):
        print(lexan.lexems_out[self.i]['lex'])
        if lexan.lexems_out[self.i]['lex'] == '(':
            self.i += 1
            if self.log_e():
                if lexan.lexems_out[self.i]['lex'] == ')':
                    self.i += 1
                    return True
                else:
                    self.syntax_error('missing ")"')
                    return False
            else:
                self.syntax_error('missing logical expression')
                return False
        if lexan.lexems_out[self.i]['lex'] == '!':
            self.i += 1
            if self.log_f():
                return True
            else:
                self.syntax_error('missing logical expression after "!"')
                return False
        if self.relation():
            return True
        return False

    def log_t(self):
        while self.log_f():
            if lexan.lexems_out[self.i]['lex'] == 'and':
                self.i += 1
            else:
                return True
        else:
            self.syntax_error('missing log_f')
            return False

    def log_e(self):
        while self.log_t():
            if lexan.lexems_out[self.i]['lex'] == 'or':
                self.i += 1
            else:
                return True
        else:
            self.syntax_error('missing log_t')
            return False

    def kft(self):
        for lex in lexan.con_out:
            if lexan.lexems_out[self.i]['lex'] == lex['name']:
                self.i += 1
                return True
        else:
            return False

    def kpt(self):
        if self.kft():
            return True
        # if self.kft():
        #     if lexan.lexems_out[self.i]['lex'] == 'e' or lexan.lexems_out[self.i]['lex'] == 'E':
        #         self.i += 1
        #         self.sign()
        #         if self.cbz():
        #             return True

    def f_exp(self):
        if lexan.lexems_out[self.i]['lex'] == '}':
            self.i += 1
            return True
        if self.kpt():
            return True
        if self.id_():
            return True
        if lexan.lexems_out[self.i]['lex'] == '(':
            self.i += 1
            if self.expression():
                if lexan.lexems_out[self.i]['lex'] == ')':
                    self.i += 1
                    return True
                else:
                    self.syntax_error('missing ")"')
                    return False
            else:
                self.syntax_error('missing expression')
                return False
        else:
            return False

    def sign(self):
        if lexan.lexems_out[self.i]['lex'] == '+' or lexan.lexems_out[self.i]['lex'] == '-':
            self.i += 1

    def t_exp(self):
        self.sign()

        while self.f_exp():
            if lexan.lexems_out[self.i]['lex'] == '/' or lexan.lexems_out[self.i]['lex'] == '*':
                self.i += 1
                self.sign()
            elif lexan.lexems_out[self.i]['lex'] == '\\n':
                return True
            else:
                return True
        self.syntax_error('missing expression(F)')
        return False

    def expression(self):
        while self.t_exp():
            if lexan.lexems_out[self.i]['lex'] == '+' or lexan.lexems_out[self.i]['lex'] == '-':
                self.i += 1
            elif lexan.lexems_out[self.i]['lex'] == '\\n':
                return True
            else:
                return True
        return False

    def loop(self):

        if lexan.lexems_out[self.i]['lex'] == 'while':
            self.i += 1
            if self.log_e():
                if lexan.lexems_out[self.i]['lex'] == 'do':
                    self.i += 1
                    if self.op_block():
                        return True
                    else:
                        self.syntax_error('missing block of operators')
                        return False
                else:
                    self.syntax_error('missing "do"')
                    return False
            else:
                self.syntax_error('missing logical expression')
                return False
        else:
            return False

    def condition(self):
        if lexan.lexems_out[self.i]['lex'] == 'if':
            self.i += 1
            if self.log_e():
                if lexan.lexems_out[self.i]['lex'] == '?':
                    self.i += 1
                    if self.op_block():
                        if lexan.lexems_out[self.i]['lex'] == ':':
                            self.i += 1
                            if self.op_block():
                                return True
                            else:
                                self.syntax_error('missing second block of operators in loop')
                                return False
                        else:
                            self.syntax_error('missing ":" in condition')
                            return False
                    else:
                        self.syntax_error('missing first block of operators in loop')
                        return False
                else:
                    self.syntax_error('missing "?"')
                    return False
            else:
                self.syntax_error('missing logical expression')
                return False
        else:
            return False

    def assigning(self):
        if self.id_():
            if lexan.lexems_out[self.i]['lex'] == '=':
                self.i += 1
                if self.expression():
                    return True
                else:
                    self.syntax_error('missing expression')
                    return False
            else:
                self.syntax_error('missing "="')
                return False
        else:
            return False

    def input(self):
        if lexan.lexems_out[self.i]['lex'] == 'cin':
            self.i += 1
            while lexan.lexems_out[self.i]['lex'] == '>>':
                self.i += 1
                if self.id_():
                    pass
                else:
                    return False
            return True

    def output(self):
        if lexan.lexems_out[self.i]['lex'] == 'cout':
            self.i += 1
            while lexan.lexems_out[self.i]['lex'] == '<<':
                self.i += 1
                if self.id_():
                    pass
                else:
                    self.syntax_error('missing identifier to output')
                    return False
            return True

    def op(self):
        if self.loop():
            return True
        if self.condition():
            return True
        if self.input():
            return True
        if self.output():
            return True
        if self.assigning():
            return True
        # if lexan.lexems_out[self.i]['lex'] == '}':
        #     return True
        return False

    def sp_op(self):
        if self.op():
            # print(self.i, len(lexan.lexems_out))
            if self.i + 1 >= len(lexan.lexems_out):
                self.syntax_error('missing end of line')
                return False
            if lexan.lexems_out[self.i]['lex'] == '\\n':
                # print(lexan.lexems_out[self.i]['lex'])
                self.i += 1
                while lexan.lexems_out[self.i]:
                    if self.op():
                        if self.i + 1 >= len(lexan.lexems_out):
                            self.syntax_error('missing end of line')
                            return False
                        if lexan.lexems_out[self.i]['lex'] == '\\n':
                            self.i += 1
                        # elif lexan.lexems_out[self.i]['lex'] == '}':
                        #     return True
                        else:
                            self.syntax_error('missing end of line')
                            return False
                    else:
                        if lexan.lexems_out[self.i]['lex'] == '}':
                            return True
                        else:
                            self.syntax_error('missing operator or end of program')
                            return False
                return True
            else:
                self.syntax_error('missing end of line')
                return False
        else:
            self.syntax_error('incorrect operator')
            return False

    def op_block(self):
        if lexan.lexems_out[self.i]['lex'] == '{':
            self.i += 1
            if lexan.lexems_out[self.i]['lex'] == '\\n':
                self.i += 1
                if self.sp_op():
                    if lexan.lexems_out[self.i]['lex'] == '}':
                        self.i += 1
                        return True
                    else:
                        self.syntax_error('missing }')
                        return False
                else:
                    self.syntax_error('incorrect sp_op')
                    return False
            else:
                self.syntax_error('missing "\\n"')
                return False
        else:
            self.syntax_error('missing {')
            return False

    def id_(self):
        for idn in lexan.idn_out:
            if lexan.lexems_out[self.i]['lex'] == idn['lex']:
                self.i += 1
                return True
        else:
            # self.syntax_error('incorrect identifier')
            return False

    def sp_zm(self):
        if self.id_():
            while lexan.lexems_out[self.i]['lex'] == ',':
                self.i += 1
                if self.id_():
                    pass
                else:
                    return False
            if lexan.lexems_out[self.i]['lex'] == '\\n':
                # self.i += 1
                return True
            return False
        else:
            self.syntax_error('missing identifier')
            return False

    def type_(self):
        if lexan.lexems_out[self.i]['lex'] == 'int':
            self.i += 1
            return True
        elif lexan.lexems_out[self.i]['lex'] == 'float':
            self.i += 1
            return True
        else:
            self.syntax_error('incorrect type')

    def og(self):
        if self.type_():
            if self.sp_zm():
                return True
            else:
                self.syntax_error('incorrect list of variables')
                return False
        else:
            self.syntax_error('incorrect type of variable')
            return False

    def sp_og(self):
        if self.og():
            while lexan.lexems_out[self.i]['lex'] == '\\n':
                self.i += 1
                if lexan.lexems_out[self.i]['lex'] == '{':
                    return True
                if self.og():
                    pass
                else:
                    return False

        else:
            self.syntax_error('missing first declaration')
            return False

    def prog(self):
        self.i = 0
        if self.sp_og():
            if self.op_block():
                if lexan.lexems_out[self.i]['lex'] == '\\n':
                    self.i += 1
                if self.i == len(lexan.lexems_out):
                    return True
                else:
                    self.syntax_error('lexemes after end of program')
            else:
                self.syntax_error('incorrect block of operators')
                return False
        else:
            self.syntax_error('incorrect list of declaration')
            return False
