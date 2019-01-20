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
        if lexan.lexems_out[self.i]['lex'] == '(':
            self.i += 1
            if self.log_e():
                if lexan.lexems_out[self.i]['lex'] == ')':
                    self.i += 1
                    return True
                self.syntax_error('missing ")" after logical expression')
                return False
            self.syntax_error('missing logical expression after "(" ')
            return False
        if lexan.lexems_out[self.i]['lex'] == '!':
            self.i += 1
            if self.log_f():
                return True
            else:
                self.syntax_error('missing logical expression after "!" ')
                return False
        if self.relation():
            return True
        return False

    def log_t(self):
        if self.log_f():
            while lexan.lexems_out[self.i]['lex'] == 'and':
                self.i += 1
                if self.log_f():
                    pass
                else:
                    self.syntax_error('missing logical expression after "and" ')
                    return False
            return True
        return False

    def log_e(self):
        if self.log_t():
            while lexan.lexems_out[self.i]['lex'] == 'or':
                self.i += 1
                if self.log_t():
                    pass
                else:
                    self.syntax_error('missing logical expression after "or" ')
                    return False
            return True
        return False

    def constant(self):
        for lex in lexan.con_out:
            if lexan.lexems_out[self.i]['lex'] == lex['name']:
                self.i += 1
                return True
        else:
            return False

    def f_exp(self):
        if self.id_():
            return True
        if self.constant():
            return True
        if lexan.lexems_out[self.i]['lex'] == '(':
            self.i += 1
            if self.expression():
                if lexan.lexems_out[self.i]['lex'] == ')':
                    self.i += 1
                    return True
                self.syntax_error('missing ")" after expression')
                return False
            self.syntax_error('missing expression after "(" ')
            return False
        return False

    def sign(self):
        if lexan.lexems_out[self.i]['lex'] in ['+', '-']:
            self.i += 1

    def t_exp(self):
        self.sign()
        if self.f_exp():
            while lexan.lexems_out[self.i]['lex'] in ['*', '/']:
                znak = lexan.lexems_out[self.i]['lex']
                self.i += 1
                if self.f_exp():
                    pass
                else:
                    self.syntax_error('missing expression(F) after {}'.format(znak))
                    return False
            return True
        return False

    def expression(self):
        if self.t_exp():
            while lexan.lexems_out[self.i]['lex'] in ['+', '-']:
                znak = lexan.lexems_out[self.i]['lex']
                self.i += 1
                if self.t_exp():
                    pass
                else:
                    self.syntax_error('missing expression(T) after {}'.format(znak))
                    return False
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
            if lexan.lexems_out[self.i]['lex'] == '>>':
                self.i += 1
                if self.id_():
                    while lexan.lexems_out[self.i]['lex'] == '>>':
                        self.i += 1
                        if self.id_():
                            pass
                        else:
                            self.syntax_error('missing identifier to input')
                            return False
                    return True
                self.syntax_error('missing identifier to input')
                return False
            self.syntax_error('missing >> after "cin"')
            return False
        return False

    def output(self):
        if lexan.lexems_out[self.i]['lex'] == 'cout':
            self.i += 1
            if lexan.lexems_out[self.i]['lex'] == '<<':
                self.i += 1
                if self.id_():
                    while lexan.lexems_out[self.i]['lex'] == '<<':
                        self.i += 1
                        if self.id_():
                            pass
                        else:
                            self.syntax_error('missing identifier to output')
                            return False
                    return True
                self.syntax_error('missing identifier to output')
                return False
            self.syntax_error('missing << after "cout"')
            return False
        return False

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
        return False

    def sp_op(self):
        if self.op():
            if lexan.lexems_out[self.i]['lex'] == '\\n':
                self.i += 1
                while self.op():
                    if lexan.lexems_out[self.i]['lex'] == '\\n':
                        self.i += 1
                    else:
                        self.syntax_error('missing end of line')
                        return False
                return True
            self.syntax_error('missing end of line')
            return False
        else:
            self.syntax_error('missing operator')

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
                # print(idn['lex'])
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
                    self.syntax_error('missing identifier')
                    return False
            else:
                return True
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
            return False
            # self.syntax_error('incorrect type')

    def og(self):
        if self.type_():
            if self.sp_zm():
                return True
            else:
                self.syntax_error('incorrect list of variables')
                return False
        else:
            # self.syntax_error('incorrect type of variable')
            return False

    def sp_og(self):
        if self.og():
            while lexan.lexems_out[self.i]['lex'] == '\\n':
                self.i += 1
                if self.og():
                    pass
                # elif lexan.lexems_out[self.i]['lex'] == '{':
                #     return True
                else:
                    # self.syntax_error('missing declaration or end of declaration list')
                    return True
            else:
                self.syntax_error('missing end of line')
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
