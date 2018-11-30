from beautifultable import BeautifulTable
import sys

i = -1
with open('test.txt') as file:
    file_text = file.read()

line_of_file = 1
HAS_TO_READ = True
last_type = 0
is_spog = True

lexems_out = []
idn_out = []
con_out = []

rozdilniki = [' ', '(', ')', '\n', '\t', '+', '=', '*', '/', '?', '-', ',', '{', '}', '']
lexems_in = ['int', 'float', 'while', 'do', 'if', 'cin',
             'cout', '{', '}', ',', '.', ':', '=', '<<',
             '>>', '<', '>', '<=', '>=', '==', '!=', '+', '-', '*',
             '(', ')', '/', '?', '\n']
errors = ['unknown idn', 'unknown symbol', 'unallowed declaration', 'undeclarated variable', 're-declaration variable']

table = BeautifulTable()
table.column_headers = ['№', 'Row', 'Lex', 'Lex code', 'Code of IDN', 'Code of CONST']

idn_table = BeautifulTable()
idn_table.column_headers = ['Code', 'Name', 'Type', 'Value']

con_table = BeautifulTable()
con_table.column_headers = ['Code', 'Name', 'Type']


def type_of_const(const):
    if const % 1 == 0:
        return 'int'
    else:
        return 'float'


def error(type_of_error, error_lex):
    global line_of_file
    if type_of_error in errors:
        print("Error: {} in line {}, lex: {}".format(type_of_error, line_of_file, error_lex))
        sys.exit()
    else:
        print('unknown error')


def next_char():
    global i
    i += 1
    if i > len(file_text) - 1:
        return ''
    else:
        return file_text[i]


state = 1


def save_inf():
    lex_table = open('lex.txt', 'w')
    lex_table.write(str(table))
    lex_table.close()

    # print(str(idn_table))
    idn_t = open('idn.txt', 'w')
    idn_t.write(str(idn_table))
    idn_t.close()

    # print(str(con_table))
    con_t = open('const.txt', 'w+')
    con_t.write(str(con_table))
    con_t.close()
    sys.exit()


def add_lex(lex):
    global last_type
    global line_of_file
    global is_spog
    global lexems_out
    global idn_out

    if not is_spog:
        if lex == 'int' or lex == 'float':
            error('unallowed declaration', lex)
        elif lex not in lexems_in:
            if not (lex == '' or lex[0].isdigit() or lex[0] == '.'):
                for one_lex in idn_out:
                    if lex == one_lex['lex']:
                        break
                else:
                    error('undeclarated variable', lex)

    if lex == '{':
        is_spog = False

    if lex in lexems_in:
        code = lexems_in.index(lex) + 1
        if lex == 'int' or lex == 'float':
            last_type = lex
        idn_code = ''
        con_code = ''
    elif lex[0].isdigit() or (lex[0] == '.' and lex[1].isdigit()):
        code = 101
        con_code = len(con_table) + 1
        con_table.append_row([con_code, lex, type_of_const(float(lex))])
        con_out.append({'code': con_code, 'name': lex, 'type': type_of_const(float(lex))})
        idn_code = ''
    else:
        value = 0
        code = 100
        idn_code = len(idn_table) + 1
        con_code = ''


        if not idn_out:
            idn_table.append_row([idn_code, lex, last_type, value])
            idn_out.append({'idn_code': idn_code, 'lex': lex, 'type': last_type, 'value': value})
        else:
            for lex_line in idn_out:
                if lex == lex_line['lex']:
                    idn_code = lex_line['idn_code']
                    if is_spog:
                        error('re-declaration variable', lex)
                    break
            else:
                    idn_table.append_row([idn_code, lex, last_type, value])
                    idn_out.append({'idn_code': idn_code, 'lex': lex, 'type': last_type, 'value': value})

    if lex == '\n':
        lex = '\\n'
    table.append_row([len(table) + 1, line_of_file, lex, code, idn_code, con_code])
    lexems_out.append({'number': len(table) + 1, 'line': line_of_file, 'lex': lex, 'code': code, 'idn_code': idn_code,
                       'con_code': con_code})


j = 0

while j <= (len(file_text) + 3):
    j += 1

    if state == 1:
        if HAS_TO_READ:
            ch = next_char()
        while ch == ' ' or ch == '\n' or ch == '\t':
            if ch == '\n':
                add_lex('\n')
                line_of_file += + 1
            ch = next_char()
        lex = ''
        if ch.isalpha():
            lex += ch
            ch = next_char()
            state = 2
        elif ch.isdigit():
            lex += ch
            ch = next_char()
            state = 3
        elif ch == '.':
            lex += ch
            ch = next_char()
            state = 4
        elif ch == '>':
            lex += ch
            state = 9
        elif ch == '<':
            lex += ch
            state = 10
        elif ch == '=':
            lex += ch
            state = 11
        elif ch == '!':
            lex += ch
            state = 12
        elif ch in rozdilniki:
            lex += ch
            if ch == '':
                save_inf()
                #sys.exit()
            HAS_TO_READ = True
            add_lex(lex)
            state = 1
        else:
            if ch == '':
                pass
            else:
                error('unknown symbol', ch)
    elif state == 2:
        if ch.isdigit() or ch.isalpha():
            state = 2
            lex += ch
            ch = next_char()
        else:
            add_lex(lex)
            HAS_TO_READ = False
            state = 1
    elif state == 3:
        if ch.isdigit():
            state = 3
            lex += ch
            ch = next_char()
        elif ch == '.':
            state = 5
        elif ch == 'e' or ch == 'E':
            state = 6
            lex += ch
            ch = next_char()
        elif ch in rozdilniki:
            add_lex(lex)
            HAS_TO_READ = False
            state = 1
        else:
            error('unknown symbol', ch)
    elif state == 4:
        lex += ch
        #ch = next_char()
        if ch.isdigit():
            state = 5
        else:
            error('unknown idn', lex)
            state = 1
    elif state == 5:

        ch = next_char()
        if ch.isdigit():
            state = 5
            lex += ch
        elif ch == 'e' or ch == 'E':
            state = 6
            lex += ch
        #elif ch in rozdilniki:
         #   add_lex(lex)
          #  state = 1
        else:
            add_lex(lex)
            state = 1
            #lex += ch
            #error('unknown idn', lex)
    elif state == 6:
        lex += ch
        ch = next_char()
        if ch.isdigit():
            state = 8
        elif ch == '+' or ch == '-':
            lex += ch
            ch = next_char()
            state = 7
        else:
            error('unknown idn', lex)
    elif state == 7:
        if ch.isdigit():
            state = 8
        else:
            lex += ch
            error('unknown idn', lex)

    elif state == 8:
        lex += ch
        ch = next_char()
        if ch.isdigit():
            state = 8
        elif ch in rozdilniki:
            add_lex(lex)
            HAS_TO_READ = False
            state = 1
        else:
            lex += ch
            error('unknown idn', lex)
    elif state == 9:
        ch = next_char()
        if ch == '>':
            lex += ch
        elif ch == '=':
            lex += ch
        HAS_TO_READ = True
        add_lex(lex)
        state = 1
    elif state == 10:
        ch = next_char()
        if ch == '<':
            lex += ch
        elif ch == '=':
            lex += ch
        HAS_TO_READ = True
        add_lex(lex)
        state = 1
    elif state == 11:
        ch = next_char()
        if ch == '=':
            lex += ch
        #HAS_TO_READ = True
        add_lex(lex)
        state = 1
    elif state == 12:
        ch = next_char()
        if ch == '=':
            lex += ch
        #HAS_TO_READ = True
        add_lex(lex)
        state = 1

save_inf()