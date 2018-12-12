import lexan

# def s_error(error_message, ):
#     lexan.error_text = "Error: {} in line {}, lex: {}".format(error_message, line_of_file, error_lex)
# i = 0
#
# def prog(i):
#     if sp_og(i):
#         if lexan.lexems_out[i]['lex'] == '{':
#             i += 1
#             if sp_og(i):
#                 if lexan.lexems_out[i]['lex'] == '}':
#                     i += 1
#                     return True
#                 else:
#                     lexan.error('incorrect list of declaration')
#                 return False
#             else:
#                 lexan.error('{ is missing')
#                 return False
#         else:
#             lexan.error('1')
#
#
# def type_(i):
#     if lexan.lexems_out[i]['lex'] == 'int':
#         i += 1
#         return True
#     else:
#         if lexan.lexems_out[i]['lex'] == 'float':
#             i += 1
#             return True
#         else:
#             lexan.error('incorrect type', lexan.lexems_out[i]['lex'])
#
#
# def sp_og(i):
#     if og(i):
#         while lexan.lexems_out[i]['lex'] == '\n':
#             i += 1
#             if og(i):
#                 pass
#             else:
#                 lexan.error('missing declaration')
#                 return False
#             return True
#     else:
#         lexan.error('missing first declaration')
#         return False
#
#
# def sp_op(i):
#     if op(i):
#         if lexan.lexems_out[i]['lex'] == '\n':
#             i += 1
#         while lexan.lexems_out[i]:
#             if op(i):
#                 if lexan.lexems_out[i]['lex'] == '\n':
#                     i += 1
#                 else:
#                     lexan.error('missing end of line', lexan.lexems_out[i]['lex'])
#                     return False
#             else:
#                 lexan.error('missing operator or end of program')
#                 return False
#         return True
#
#
# def og(i):
#     pass
#
#
# def op(i):
#     if is_assignant():
#         return True
#
#
#
# def is_assignant(i):
#     if lexan.lexems_out[i]['code'] != 100:
#         return False
#     # global i
#     if lexan.lexems_out[i]['lex'] == '=':
#         pass


class SyntaxAnalyser:
    def __init__(self):
        self.i = 0



    def is_expresssion(self):
        pass

    def is_assigning(self):
        if lexan.lexems_out[self.i]['code'] != 100:
            return False
        self.i += 1
        if lexan.lexems_out[self.i]['lex'] != '=':
            lexan.error('Syntax error, expected "="', lexan.lexems_out[self.i]['lex'])
        self.i += 1
        if self.is_expression():
            return True

        lexan.error('Syntax error: expected expression', lexan.lexems_out[self.i]['lex'])


    def og(self):
        pass

    def op(self):
        if self.is_assigning():
            return True


    def prog(self, i):
        if sp_og(i):
            if lexan.lexems_out[i]['lex'] == '{':
                i += 1
                if sp_og(i):
                    if lexan.lexems_out[i]['lex'] == '}':
                        i += 1
                        return True
                    else:
                        lexan.error('incorrect list of declaration')
                    return False
                else:
                    lexan.error('{ is missing')
                    return False
            else:
                lexan.error('1')

    def type_(i):
        if lexan.lexems_out[i]['lex'] == 'int':
            i += 1
            return True
        else:
            if lexan.lexems_out[i]['lex'] == 'float':
                i += 1
                return True
            else:
                lexan.error('incorrect type', lexan.lexems_out[i]['lex'])

    def sp_og(i):
        if og(i):
            while lexan.lexems_out[i]['lex'] == '\n':
                i += 1
                if og(i):
                    pass
                else:
                    lexan.error('missing declaration')
                    return False
                return True
        else:
            lexan.error('missing first declaration')
            return False

    def sp_op(i):
        if op(i):
            if lexan.lexems_out[i]['lex'] == '\n':
                i += 1
            while lexan.lexems_out[i]:
                if op(i):
                    if lexan.lexems_out[i]['lex'] == '\n':
                        i += 1
                    else:
                        lexan.error('missing end of line', lexan.lexems_out[i]['lex'])
                        return False
                else:
                    lexan.error('missing operator or end of program')
                    return False
            return True



