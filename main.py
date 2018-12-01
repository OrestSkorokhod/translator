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


def prepare_to_write(array_from, table_to):
    for line in array_from:
        row = []
        for k, v in line.items():
            row.append(v)
        table_to.append_row(row)


def write_in_file():
    prepare_to_write(lexems_out, table)
    lex_table = open('lex.txt', 'w')
    lex_table.write(str(table))
    lex_table.close()

    prepare_to_write(idn_out, idn_table)
    idn_t = open('idn.txt', 'w')
    idn_t.write(str(idn_table))
    idn_t.close()

    prepare_to_write(con_out,con_table)
    con_t = open('const.txt', 'w+')
    con_t.write(str(con_table))
    con_t.close()


def add_lex(lex):
    global last_type
    global line_of_file
    global is_spog
    global lexems_out
    global idn_out

    if lex in lexems_in:
        code = lexems_in.index(lex) + 1
        idn_code = ''
        con_code = ''

        if lex == 'int' or lex == 'float':
            if not is_spog:
                error('unallowed declaration', lex)
            last_type = lex
        elif lex == '\n':
            lex = '\\n'
        elif lex == '{':
            is_spog = False
    elif lex[0].isalpha():
        value = 0
        code = 100
        idn_code = len(idn_out) + 1
        con_code = ''

        for idn in idn_out:
            if lex == idn['lex']:
                idn_code = idn['idn_code']
                if is_spog:
                    error('re-declaration variable', lex)
                break
        else:
            if is_spog:
                idn_out.append({'idn_code': idn_code, 'lex': lex, 'type': last_type, 'value': value})
            else:
                error('undeclarated variable', lex)
    else:
        code = 101
        con_code = len(con_out) + 1
        con_out.append({'code': con_code, 'name': lex, 'type': type_of_const(float(lex))})
        idn_code = ''


    lexems_out.append({'number': len(lexems_out) + 1, 'line': line_of_file, 'lex': lex, 'code': code, 'idn_code': idn_code,
                       'con_code': con_code})


state = 1
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
                write_in_file()
                sys.exit()
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
        lex += ch
        ch = next_char()
        if ch.isdigit():
            state = 5

        elif ch == 'e' or ch == 'E':
            state = 6

        elif ch in rozdilniki:
            add_lex(lex)
            state = 1
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
