class Lexem:
    number = None
    line = None
    lexem = None
    code = None
    idn_code = None
    con_code = None

    def __init__(self, number=None, line=None, lexem=None,
    code=None, idn_code=None, con_code=None):
        self.number = number
        self.line = line
        self.lexem = lexem
        self.code = code
        self.idn_code = idn_code
        self.con_code = con_code

    def __repr__(self):
        return '{}'.format(self.lexem)

    def __str__(self):
        return '{}'.format(self.lexem)
