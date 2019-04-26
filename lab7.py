import lexan





class Lab7():


    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.stack = []
        self.poliz = []
        self.is_code = False
        self.priority = {
        '(': 1,
        '=':2,
        '+':7,
        '-': 7,
        '*': 8,
        '/': 8,
        '@': 8,
         }
        # print(self.lexemes)
        print('-' * 70)
        self.make_poliz()

        print(self.poliz)


    def make_poliz(self):
        for lexem in self.lexemes:

            if self.is_code:
                # print(lexem, lexem.idn_code, lexem.con_code)
                print(lexem)

                if lexem.idn_code or lexem.con_code:
                    # print('p1:', lexem)
                    self.poliz.append(lexem)
                elif lexem.lexem not in self.priority:
                    continue
                elif self.stack:
                    def p2():
                        if self.priority[self.stack[-1].lexem] >= self.priority[lexem.lexem]:
                            self.poliz.append(lexem)
                            p2()
                        else:
                            self.stack.append(lexem)
                    p2()
                elif not self.stack:
                    self.stack.append(lexem)

            if lexem.lexem == '{':
                self.is_code = True
        else:
            while self.stack:
                self.poliz.append(self.stack.pop())








    def assigning_poliz(self):
        pass
