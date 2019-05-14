import lexan

from lexem import Lexem



class Lab7:


    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.stack = []
        self.poliz = []
        self.mi = []
        self.is_code = False
        self.to_print = ''
        self.priority = {
        # '(': 1,
        # '=':2,
        # '+':7,
        # '-': 7,
        # '*': 8,
        # '/': 8,
        # '@': 8,
        '\\n': -2,
        '=': -1,
        '(': 0,
        '[': 0,
        ')': 1,
        ']': 1,
        'or': 3,
        'and': 4,
        '!': 5,
        '<': 6,
        '>': 6,
        '<=': 6,
        '>=': 6,
        '==': 6,
        '+':7,
        '-': 7,
        '*': 8,
        '/': 8,
        '@': 8,
        # '=': 10,
         }
        # print(self.lexemes)
        print('-' * 70)
        self.make_poliz()

        print(self.poliz)

    def debug(self):
        print('-'*50)
        print(self.lexemes)
        print(self.stack)
        print(self.poliz)


    def make_poliz(self):

        def assigning():
            # print('assigning')
            # print('p1:', lexem)
            # print(self.stack)
            # self.poliz.append(lexem)


            stack = []

            lexem = self.lexemes.pop(0)
            print('assigning first lexem:', lexem)
            self.poliz.append(lexem)
            # print('kek')
            while lexem.lexem != '\\n':
                # print('kek')
                lexem = self.lexemes.pop(0)
                print('lexem in expression:', lexem)
                # print('stack', self.stack)
                if lexem.idn_code or lexem.con_code:
                # print('p1:', lexem)
                # print('kek')
                    self.poliz.append(lexem)
                elif lexem.lexem not in self.priority:
                    pass
                elif stack:
                # print('kek')
                    def p2():
                        if stack:

                            if self.priority[stack[-1].lexem] >= self.priority[lexem.lexem]:
                                self.poliz.append(stack.pop())
                                p2()
                            else:
                                stack.append(lexem)

                    p2()
                elif not stack:
                    # print('kek')
                    stack.append(lexem)

                # lexem = self.lexemes.pop(0)

            self.stack.extend(list(stack))

            del stack
            print('end of assigning:', lexem)


        def condition():
            priority = {
            'if': 0,
            '?': 1,
            'else': 1,

            }

            lexem = self.lexemes.pop(0)
            self.stack.append(lexem)

            stack = []

            # print('first lexem after if:' , lexem)
            while lexem.lexem != '?':
                # print('stack', stack)
                lexem = self.lexemes.pop(0)
                print('Lexem in if condition:', lexem)
                if lexem.idn_code or lexem.con_code:
                # print('p1:', lexem)
                # print('kek')
                    self.poliz.append(lexem)
                elif lexem.lexem not in self.priority:
                    pass
                elif stack:
                # print('kek')
                    def p2():
                        if stack:

                            if self.priority[stack[-1].lexem] >= self.priority[lexem.lexem]:
                                self.poliz.append(stack.pop())
                                p2()
                            else:
                                stack.append(lexem)

                    p2()
                elif not stack:
                    # print('kek')
                    stack.append(lexem)

                # lexem = self.lexemes.pop(0)

            self.stack.extend(list(stack))

            del stack

            while self.stack[-1].lexem != 'if':
                print('stack:', (self.stack))
                if self.stack[-1].lexem in ('[', ']', '(', ')'):
                    self.stack.pop()
                # print('stack:', (self.stack))
                # print(type(self.stack[-1]))
                else:
                    self.poliz.append(self.stack.pop())
                # print('kek')

            lex = Lexem(lexem='m{}'.format(len(self.mi) + 1))

            self.mi.append(lex)

            self.poliz.append(lex)
            self.poliz.append(Lexem(lexem='УПХ'))

            # self.stack[-1] = 'if{}'.format(lex)
            self.stack[-1] = Lexem(lexem='if{}'.format(lex))

            lexem = self.lexemes.pop(0)
            print(lexem)

            print('Poliz:', self.poliz)

            # lexem = self.lexemes.pop(0) # { from input
            # print('before block', lexem)
            op_block()
            # print('plz')
            lexem = self.lexemes.pop(0)
            print('after if block', lexem)
            lexem = self.lexemes.pop(0)
            lexem = self.lexemes.pop(0)
            while 'if' not in  self.stack[-1].lexem:
                lex = self.stack.pop()
                self.poliz.append(lex)

            # lex = 'm{}БПm{}'.format(len(self.mi) + 1, len(self.mi))
            lex = 'm{}'.format(len(self.mi) + 1)
            self.poliz.append(Lexem(lexem=lex))
            lex = 'БП'
            self.poliz.append(Lexem(lexem=lex))
            lex = 'm{}'.format(len(self.mi))
            self.poliz.append(Lexem(lexem=lex))
            self.mi.append(Lexem(lexem='m{}'.format(len(self.mi) + 1)))

            # print('stack: ', self.stack)

            self.stack[-1].lexem += '{}'.format(self.mi[-1])

            print('stack: ', self.stack)
            print(self.lexemes)
            op_block()

            # self.debug()

            self.lexemes.pop(0)

            while 'if' not in  self.stack[-1].lexem:
                lex = self.stack.pop()
                self.poliz.append(lex)

            metka = self.stack.pop()
            metka = int(metka.lexem[-1])
            self.poliz.append(Lexem(lexem=self.mi[metka - 1]))

            # self.debug()
            if self.lexemes[0].lexem == '\\n':
                self.lexemes.pop(0)

            # self.debug()
            # print(self.lexemes)
            # self.poliz.append(lexem)

        def loop():

            lexem = self.lexemes.pop(0)
            mitka = Lexem(lexem='m{}'.format(len(self.mi) + 1))
            self.mi.append(mitka)
            lexem = Lexem(lexem='while{}'.format(mitka.lexem))
            self.stack.append(lexem)
            self.poliz.append(mitka)

            stack = []

            # print('first lexem after if:' , lexem)
            while lexem.lexem != 'do':
                # print('stack', stack)
                lexem = self.lexemes.pop(0)
                print('Lexem in if condition:', lexem)
                if lexem.idn_code or lexem.con_code:
                # print('p1:', lexem)
                # print('kek')
                    self.poliz.append(lexem)
                elif lexem.lexem not in self.priority:
                    pass
                elif stack:
                # print('kek')
                    def p2():
                        if stack:

                            if self.priority[stack[-1].lexem] >= self.priority[lexem.lexem]:
                                self.poliz.append(stack.pop())
                                p2()
                            else:
                                stack.append(lexem)

                    p2()
                elif not stack:
                    # print('kek')
                    stack.append(lexem)

                # lexem = self.lexemes.pop(0)

            self.stack.extend(list(stack))

            del stack

            while 'while' not in self.stack[-1].lexem:
                print('stack for clear:', (self.stack))
                if self.stack[-1].lexem in ('[', ']', '(', ')'):
                    self.stack.pop()
                # print('stack:', (self.stack))
                # print(type(self.stack[-1]))
                else:
                    self.poliz.append(self.stack.pop())
                # print('kek')

            lex = Lexem(lexem='m{}'.format(len(self.mi) + 1))

            self.mi.append(lex)

            self.poliz.append(lex)
            self.poliz.append(Lexem(lexem='УПХ'))
            self.lexemes.pop(0)
            op_block()

            while 'while' not in  self.stack[-1].lexem:
                lex = self.stack.pop()
                self.poliz.append(lex)

            metka = self.stack.pop()
            metka = int(metka.lexem[-1])
            self.poliz.append(Lexem(lexem=self.mi[metka - 1]))
            self.poliz.append(Lexem(lexem='БП'))
            self.poliz.append(Lexem(lexem=self.mi[metka]))

            # self.debug()
            if self.lexemes[0].lexem == '\\n':
                self.lexemes.pop(0)


            # self.debug()


        def output():
            lexem = self.lexemes.pop(0)
            self.stack.append(lexem)

            while lexem.lexem != '\\n':
                lexem = self.lexemes.pop(0)
                if lexem.lexem == '>>':
                    continue
                elif lexem.idn_code or lexem.con_code:
                    self.poliz.append(lexem)

            self.poliz.append(self.stack.pop())

        def input():
            lexem = self.lexemes.pop(0)
            self.stack.append(lexem)

            while lexem.lexem != '\\n':
                lexem = self.lexemes.pop(0)
                if lexem.lexem == '>>':
                    continue
                elif lexem.idn_code or lexem.con_code:
                    self.poliz.append(lexem)

            self.poliz.append(self.stack.pop())
            # self.debug()


        ########################
        #### ALL START HERE ####
        ########################

        # skip init of vars

        while True:
            lexem = self.lexemes[0]
            if lexem.lexem == '{':
                self.lexemes.pop(0)
                break
            else:
                self.lexemes.pop(0)

        #   MAIN LOOP

        def op_block():

            # lexem = self.lexemes.pop(0)
            lexem = self.lexemes[0]
            print('first lexem of block:', lexem)
            i = 50
            while self.lexemes and i > 0:
                lexem = self.lexemes[0]
                print(lexem)
                i -= 1

                if lexem.lexem == '}':
                    break
                # lexem = self.lexemes[0]
                # print(lexem)

                # if self.is_code:
                if lexem.idn_code:
                    assigning()
                elif lexem.lexem == 'if':
                    condition()
                elif lexem.lexem == 'while':
                    loop()
                elif lexem.lexem == 'cout':
                    output()
                elif lexem.lexem == 'cin':
                    input()


                #
                # if lexem.lexem == '{':
                #     self.is_code = True

            else:
                while self.stack:
                    self.poliz.append(self.stack.pop())

        op_block()






    def assigning_poliz(self):
        pass
