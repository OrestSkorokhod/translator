import lexan

from lexem import Lexem

from tkinter import *
from tkinter import messagebox as mb
import time

# s=0
# def check():
#     global s
#     # answer = mb.askyesno(title="Вопрос", message="Перенести данные?")
#     # if answer == True:
#     s = entry.get()
#     entry.delete(0, END)
#     label['text'] = s
# root = Tk()
# entry = Entry()
# entry.pack(pady=10)
# Button(text='Передать', command=check).pack()
# label = Label(height=3)
# label.pack()
#
# root.mainloop()
# print('MY TEXT::', s)
class MyDialog:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.myLabel = tk.Label(top, text='Enter your username below')
        self.myLabel.pack()

        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()

        self.mySubmitButton = tk.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        global username
        username = self.myEntryBox.get()
        self.top.destroy()

def onClick():
    inputDialog = MyDialog(root)
    root.wait_window(inputDialog.top)
    print('Username: ', username)

class Lab7:


    def __init__(self, lexemes):
        self.lexemes = lexemes
        self.stack = []
        self.poliz = []
        self.mi = []
        self.m = {}
        self.rozbir_poliz_table = ''
        self.execute_poliz_table = ''
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

        prev = ''
        for lexem in self.lexemes:
            # if lexem.idn_code or lexem.con_code or lexem.lexem in ('('):
            #     if prev.lexem == '-':
            #         prev.lexem = '@'
            if lexem.lexem == '-':
                if prev.idn_code or prev.con_code or lexem.lexem in (')'):
                    pass
                else:
                    lexem.lexem = '@'




            prev = lexem

        print('LEXEMES:', self.lexemes)

        self.make_poliz()

        # for lexem in self.poliz:
        #     if lexem.lexem in ('(', ')'):
        #         del lexem

        print(self.poliz)
        self.execute_poliz()


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
                # self.debug()

                lexem = self.lexemes.pop(0)


                self.rozbir_poliz_table += '{}'.format(lexem).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.stack + stack).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.poliz).ljust(60) + '\n'





                # if lexem.lexem in ('(', ')', '[', ']'):
                #     pass
                print('lexem in expression:', lexem)
                # print('stack', stack)
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
                            if lexem.lexem == '(':
                                stack.append(lexem)

                            elif lexem.lexem == ')':

                                while stack[-1].lexem != '(':
                                    print(stack)
                                    self.poliz.append(stack.pop())
                                stack.pop()

                            elif self.priority[stack[-1].lexem] >= self.priority[lexem.lexem]:
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


                self.rozbir_poliz_table += '{}'.format(lexem).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.stack).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.poliz).ljust(60) + '\n'







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
                            if lexem.lexem in  ('(', '['):
                                stack.append(lexem)

                            elif lexem.lexem in (')', ']'):
                                if lexem.lexem == ')':
                                    check = '('
                                else:
                                    check = '['

                                while stack[-1].lexem != check:
                                    # print(stack)
                                    self.poliz.append(stack.pop())
                                stack.pop()

                            elif self.priority[stack[-1].lexem] >= self.priority[lexem.lexem]:
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

            mitka = 'm{}'.format(len(self.m) + 1)
            lex = Lexem(lexem='{}'.format(mitka))
            self.m[mitka] = 0


            # self.poliz.append(lex)
            self.poliz.append(Lexem(lexem='{}УПХ'.format(mitka)))

            # self.stack[-1] = 'if{}'.format(lex)
            self.stack[-1] = Lexem(lexem='if{}'.format(mitka))

            lexem = self.lexemes.pop(0)
            print(lexem)

            print('Poliz:', self.poliz)

            # lexem = self.lexemes.pop(0) # { from input
            # print('before block', lexem)
            op_block()
            # print('plz')
            lexem = self.lexemes.pop(0)
            print('after if block', lexem)
            print(self.lexemes)
            lexem = self.lexemes.pop(0)
            # lexem = self.lexemes.pop(0)
            # lexem = self.lexemes.pop(0)
            lexem = self.lexemes.pop(0)
            while 'if' not in  self.stack[-1].lexem:
                lex = self.stack.pop()
                self.poliz.append(lex)

            # lex = 'm{}БПm{}'.format(len(self.mi) + 1, len(self.mi))
            mitka_num = len(self.m)
            mitka = 'm{}'.format(mitka_num)
            lex = 'm{}БП'.format(mitka_num + 1)
            self.poliz.append(Lexem(lexem=lex))
            # print('mi', self.mi)
            self.m[mitka] = len(self.poliz)
            # lex = 'БП'
            # self.poliz.append(Lexem(lexem=lex))
            lex = '{}:'.format(mitka)
            self.poliz.append(Lexem(lexem=lex))

            # print('stack: ', self.stack)

            self.stack[-1].lexem += 'm{}'.format(mitka_num + 1)

            print('stack: ', self.stack)
            print(self.lexemes)
            op_block()

            # self.debug()

            self.lexemes.pop(0)

            while 'if' not in  self.stack[-1].lexem:
                lex = self.stack.pop()
                self.poliz.append(lex)

            mitka = self.stack.pop()
            print('mitka: ',mitka)
            mitka = int(mitka.lexem[5:])
            print("elelelfgdfgfd")
            print('mitka: ',mitka)
            self.poliz.append(Lexem(lexem='m{}:'.format(mitka)))
            # mitka = 'm{}'.format(mitka)
            # print('mitka: ',mitka)
            print('MITKI:', self.m)


            self.m['m{}'.format(mitka)] = len(self.poliz) - 1

            # self.debug()
            if self.lexemes[0].lexem == '\\n':
                self.lexemes.pop(0)

            print('MITKI:', self.m)
            # self.debug()
            # print(self.lexemes)
            # self.poliz.append(lexem)

        def loop():

            lexem = self.lexemes.pop(0)
            mitka = 'm{}'.format(len(self.m) + 1)
            mitka_num = len(self.m) + 1
            self.poliz.append(Lexem(lexem='{}:'.format(mitka)))
            self.m[mitka] = len(self.poliz)
            lexem = Lexem(lexem='while{}'.format(mitka))
            self.stack.append(lexem)
            self.m['m{}'.format(len(self.m) + 1)] = 0
            while_m = (mitka_num, mitka_num + 1)
            stack = []

            # print('first lexem after if:' , lexem)
            while lexem.lexem != 'do':
                # print('stack', stack)
                lexem = self.lexemes.pop(0)


                self.rozbir_poliz_table += '{}'.format(lexem).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.stack).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.poliz).ljust(60) + '\n'




                print('Lexem in while condition:', lexem)
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

                            print('stack: ', stack)
                            if lexem.lexem in  ('(', '['):
                                stack.append(lexem)

                            elif lexem.lexem in (')', ']'):
                                if lexem.lexem == ')':
                                    check = '('
                                else:
                                    check = '['

                                while stack[-1].lexem != check:
                                    # print(stack)
                                    self.poliz.append(stack.pop())
                                stack.pop()
                            # print('stack: ', stack)
                            elif self.priority[stack[-1].lexem] >= self.priority[lexem.lexem]:
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

            mitka = 'm{}'.format(len(self.m) + 1)

            # self.poliz.append(lex)
            self.poliz.append(Lexem(lexem='m{}УПХ'.format(while_m[1])))
            self.lexemes.pop(0)
            op_block()

            while 'while' not in  self.stack[-1].lexem:
                lex = self.stack.pop()
                self.poliz.append(lex)

            mitka = self.stack.pop()
            # print(mitka)

            mitka = int(mitka.lexem[6:])
            print(mitka)
            self.m['m{}'.format(mitka + 1)] = 0
            # self.poliz.append(Lexem(lexem=self.mi[metka - 1]))
            self.poliz.append(Lexem(lexem='m{}БП'.format(mitka)))
            self.poliz.append(Lexem(lexem='m{}:'.format(mitka + 1)))
            self.m['m{}'.format(mitka + 1)] = len(self.poliz) - 1

            # self.debug()
            if self.lexemes[0].lexem == '\\n':
                self.lexemes.pop(0)


            # self.debug()


        def output():
            lexem = self.lexemes.pop(0)
            self.stack.append(lexem)

            while lexem.lexem != '\\n':

                self.rozbir_poliz_table += '{}'.format(lexem).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.stack).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.poliz).ljust(60) + '\n'



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

                self.rozbir_poliz_table += '{}'.format(lexem).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.stack).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.poliz).ljust(60) + '\n'


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

                self.rozbir_poliz_table += '{}'.format(lexem).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.stack).ljust(60)
                self.rozbir_poliz_table += '|{}'.format(self.poliz).ljust(60) + '\n'

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






    def execute_poliz(self):

        self.variables = {}
        operands = ('+', '-', '/', '*', 'not', 'and', '!', '@', '<', '>', '==', '<=', '>=')
        i = 0
        spisok = []
        m = {}
        to_do = 0
        first_element = 0
        second_element = 0
        j = 0
        lenght = len(self.poliz) - 1
        self.to_print = ''

        print('MITKI::', self.m)
        print('lenght:', lenght)
        while j < lenght +150:
            j += 1
            # print('element:', i)

            spisok = []
            to_do = 0
            first_element = 0
            second_element = 0
            # print(j)
            first_element = self.poliz[i]
            print('element:', first_element, i)

            if i >= lenght:
                print('STOPPED')
                break

            if first_element.idn_code:
                i += 1
                # print('spisok:', spisok)
                # print('element:', first_element, i)
                print('el:', self.poliz[i])
                while self.poliz[i].idn_code or self.poliz[i].con_code or self.poliz[i].lexem in operands:
                    # print('element:', first_element, i)
                    spisok.append(self.poliz[i])

                    # print('spisok w:', spisok)
                    i += 1
                to_exe = [first_element,] + spisok
                if self.poliz[i].lexem == '=':
                    self.variables[first_element.lexem] = self.count_poliz(spisok)
                    i += 1
                elif self.poliz[i].lexem == 'cout':
                    # print('spisok:', spisok)
                    # add_print = ''
                    self.to_print += '{} {}\n'.format( self.variables[first_element.lexem], ' '.join([self.variables[k.lexem].lexem for k in spisok]))
                    #
                    # self.to_print += '{} '.format(self.variables[first_element.lexem])
                    # for k in spisok:
                    #     self.to_print += self.variables[k.lexem].lexem + ' '
                    # self.to_print += '\n'

                    # print('print:', self.to_print)
                    i += 1
                elif self.poliz[i].lexem == 'cin':
                    print('in cin')
                    self.s = 'lol'
                    def cin():
                        def cin_s():
                            print('kekekekekkekekekekekekekek')

                            def check():
                                print('kek6')
                                # answer = mb.askyesno(title="Вопрос", message="Перенести данные?")
                                # if answer == True:
                                self.s = entry.get()
                                print('MY TEXT in check', self.s)
                                entry.delete(0, END)
                                label['text'] = self.s
                                dia.destroy()
                                dia.quit()


                            print('kek7')
                            s = self.s
                            print('MY TEXT', s)
                            dia = Tk()
                            entry = Entry(dia)
                            entry.pack( pady=5)
                            Button(dia, text='Передать', command=check).pack()
                            label = Label(dia, height=3)
                            label.pack()
                            print('MY TEXT, lol', s)
                            print('kek1')
                            dia.mainloop()
                            print('kek2')
                            print('kek3')
                            # time.sleep(5)
                            while self.s == 'lol':
                                print('SSSS', self.s)
                                time.sleep(1)
                            else:
                                print('MY TEXT, rly', self.s)
                            print('iiiiii', i)
                        cin_s()
                    print('kek5')
                    cin()
                    print('kek4')
                    self.variables[self.poliz[i-1].lexem] = int(self.s)
                    i += 1
                elif self.poliz[i].lexem in ('<', '>', '==', '<=', '>='):
                    # print('kekek:', first_element, spisok, self.poliz[i])

                    # print(first_element, spisok)
                    pass
            elif ':' in first_element.lexem and 'm' in first_element.lexem:
                # m[first_element.lexem[-2]] = i
                # print(i)
                # if i >= lenght:
                #     print('STOPPED')
                #     break
                i += 1

                # if 'БП' not in self.poliz[i - 1].lexem:
                #     print(self.poliz[i-1])
                #     while 'УПХ' not in self.poliz[i].lexem:
                #         spisok.append(self.poliz[i])
                #         i += 1
                #     print('kekek:', first_element, spisok, self.poliz[i])
                #     is_true = False
                #     is_true = self.count_poliz(spisok)
                #     if is_true.lexem == 'True':
                #         is_true = True
                #     else:
                #         is_true = False
                #
                #     print('is true?: ',is_true)
                #     if is_true:
                #         # print('TRUE'*5)
                #         # i += 1
                #         pass
                #     else:
                #         # print('FALSE'*5)
                #         # print(first_element.lexem)
                #         i = m[self.poliz[i].lexem[1:-3]]
                #         print('False, go to ', self.poliz[i].lexem, i)



                # print(l)

                # i += 1
            elif 'УПХ' in self.poliz[i].lexem:
                print('TO DO', to_exe)
                is_true = False

                is_true = self.count_poliz(to_exe)
                if is_true.lexem == 'True':
                    is_true = True
                else:
                    is_true = False

                print('is true?: ',is_true)
                if is_true:
                    # print('TRUE'*5)
                    i += 1
                    pass
                else:
                    # print('FALSE'*5)
                    # print(first_element.lexem)
                    i = self.m[self.poliz[i].lexem[0:-3]]
                    print('False, go to ', self.poliz[i].lexem, i)

            elif 'БП' in self.poliz[i].lexem:
                # print('mitka', self.poliz[i].lexem[1:-2])
                m[str(int(self.poliz[i].lexem[1:-2]) + 1)] = i + 1
                print(self.m)
                # for k in self.m.keys():
                #     print(type(k))
                # print(self.m[Lexem(lexem='m1')])
                i = self.m[self.poliz[i].lexem[0:-2]]
                print('Go to for БП: ', i)
                print(self.variables)

            elif 'УПХ' in self.poliz[i].lexem:
                print('Exe:', to_exe)
                is_true = False
                is_true = self.count_poliz(to_exe)
                if is_true.lexem == 'True':
                    is_true = True
                else:
                    is_true = False

                print('is true?: ',is_true)
                if is_true:
                    print('TRUE'*5)
                    i += 1
                    pass
                else:
                    print('FALSE'*5)
                    # print(first_element.lexem)
                    i = self.m[self.poliz[i].lexem[0:2]]
                    print('False, go to ', self.poliz[i].lexem, i)
                pass
            # print('new ell:', self.poliz[i])
            # i += 1
            if i >= lenght:
                print('STOPPED')
                break

        # print(i)
        print(self.variables)



    def count_logic(self, spisok):
        # print('spisok to count: ', spisok)
        pass



    def count_poliz(self, spisok):
        print('spisok to count: ', spisok)

        def summa(a, b):


            return float(a) + float(b)
        def vidnim(a, b):


            return float(a) - float(b)
        def mnoj(a, b):
            return float(a) * float(b)

        def dil(a, b):


            return float(a) / float(b)
        def un_min(a):

            return - float(a)

        def less(a, b):
            # print('CHECK', a, b)
            return float(a) < float(b)

        def more(a, b):
            # print('CHECK', a, b)
            return float(a) > float(b)

        def less_eq(a, b):
            # print('CHECK', a, b)
            return float(a) <= float(b)

        def more_eq(a, b):
            # print('CHECK', a, b)
            return float(a) >= float(b)

        def equal(a, b):
            # print('CHECK', a, b)
            return float(a) == float(b)

        def not_equal(a, b):
            # print('CHECK', a, b)
            return float(a) != float(b)

        def and_op(a, b):
            # print('CHECK', a, b)
            # return float(a) and float(b)
            if a == 'True' and b == 'True':
                return True
            else:
                return False

        def or_op(a, b):
            if a == 'True' or b == 'True':
                return True
            else:
                return False

        def not_op(a):
            if a == 'True':
                return False
            else:
                return True

        opers = {'+': summa,
                 '-': vidnim,
                 '*': mnoj,
                 '/': dil,
                 '@': un_min,
                 '<': less,
                 '>': more,
                 '<=': less_eq,
                 '>=': more_eq,
                 '==': equal,
                 '!=': not_equal,
                 'and': and_op,
                 'or': or_op,
                 '!': not_op,

                 }

        # self.rozbir_poliz_table = ''

        self.poliz_stack = []
        number = 0
        # print('keke', dil(225, 25))
        for j in spisok:
            # print(j)
            number += 1
            # print(number)
            # self.rozbir_poliz_table += '{}'.format(','.join([str(i) for i in self.poliz_stack])).ljust(70)
            # self.rozbir_poliz_table += '| {}'.format(','.join([str(spisok[i-1]) for i in range(number, len(spisok)+1)])).ljust(70) + '\n'
            if j.lexem.isdigit():


                self.poliz_stack.append(j)

            elif j.lexem in ('+', '-', '*', '/', '<', '>', '!=', '==', '<=', '>=', 'and', 'or'):
                r2 = self.poliz_stack.pop()
                r1 = self.poliz_stack.pop()
                # print(r1, r2)
                self.poliz_stack.append(Lexem(lexem='{}'.format(opers.get(j.lexem)(r1.lexem, r2.lexem))))
            elif j.lexem in ('@', '!'):
                r1 = self.poliz_stack.pop()
                self.poliz_stack.append(Lexem(lexem='{}'.format(opers.get(j.lexem)(r1.lexem))))
            else:
                self.poliz_stack.append(Lexem(lexem='{}'.format(self.variables[j.lexem])))
        # self.rozbir_poliz_table += '{}'.format(','.join([str(i) for i in self.poliz_stack])).ljust(70)
        return self.poliz_stack[0]
