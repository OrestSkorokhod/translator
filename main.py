from tkinter import *
from tkinter.filedialog import askopenfilename,asksaveasfilename
#
# from tkintertable.Tables import TableCanvas
# from tkintertable.TableModels import TableModel
import lexan
import synan
import mpa
import relation

# from synan5 import SyntaxAnalyser5
import synan5



class Complier:
    def __init__(self, root, file_name):
        self.an_table = ''
        self.rel_table = ''
        self.rozbir_table = ''
        self.toolbar = Frame(root, bg="#AAAAAA")
        self.top_frame = Frame(root, bg="#AACAAA")
        self.bottom_frame = Frame(root, bg="#AADADA")
        self.toolbar.pack(side=TOP, fill=X)
        self.top_frame.pack(fill="both", expand=False, padx=30, pady=30)  # side =TOP)
        self.bottom_frame.pack(side=BOTTOM, fill="both", expand=True, padx=10, pady=10)
        # toolbar
        self.open_file_button = Button(self.toolbar, text="Open file")
        self.save_button = Button(self.toolbar, text="Save to file")
        self.compile_button = Button(self.toolbar, text="Analyse")

        self.lex_but = Button(self.toolbar, text="Lexemes table")
        self.idn_but = Button(self.toolbar, text="IDN table")
        self.con_but = Button(self.toolbar, text="CON table")

        self.rozbir_button = Button(self.toolbar, text="Analysis table")
        self.relation_button = Button(self.toolbar, text="Relation table")

        self.rozbit_table_button = Button(self.toolbar, text="Rozbir Table")

        self.open_file_button.grid(row=0, column=0, padx=5, pady=5, ipadx=5, ipady=5)
        self.save_button.grid(row=0, column=1, padx=5, pady=5, ipadx=5, ipady=5)
        self.compile_button.grid(row=0, column=2, padx=5, pady=5, ipadx=5, ipady=5)

        self.lex_but.grid(row=0, column=3, padx=5, pady=5, ipadx=5, ipady=5)
        self.idn_but.grid(row=0, column=4, padx=5, pady=5, ipadx=5, ipady=5)
        self.con_but.grid(row=0, column=5, padx=5, pady=5, ipadx=5, ipady=5)

        self.rozbir_button.grid(row=0, column=6, padx=5, pady=5, ipadx=5, ipady=5)
        self.relation_button.grid(row=0, column=7, padx=5, pady=5, ipadx=5, ipady=5)

        self.rozbit_table_button.grid(row=0, column=8, padx=5, pady=5, ipadx=5, ipady=5)


        self.text_area_top = Text(self.top_frame, font='Consolas 14', height=15, wrap=NONE)
        # self.text_area_line_numbers = Text(self.top_frame,font='Consolas 14',width=2,height=15,wrap=NONE)

        file = open(file_name, 'r')
        text = file.readlines()
        self.name_of_file = file_name
        # num_lines = sum(1 for line in text)
        # print(file.readlines())
        # num_lines = sum(1 for i in file.readlines())
        file.close()
        self.text_area_top.insert(1.0, "".join(text))
        # line_numbers = "\n".join(str(i) for i in range(1,num_lines+1))
        # print(line_numbers)
        # self.text_area_line_numbers.insert(1.0,line_numbers)

        self.scrollbar_y_text_area_top = Scrollbar(self.top_frame)
        self.scrollbar_y_text_area_top.pack(side='right', fill=Y)
        self.scrollbar_y_text_area_top['command'] = self.text_area_top.yview
        # self.scrollbar_y_text_area_top['command'] = self.on_top_scrollbar
        # self.text_area_top['yscrollcommand'] = self.on_textscroll
        self.text_area_top['yscrollcommand'] = self.scrollbar_y_text_area_top.set

        # self.scrollbar_y_text_area_top['command'] = self.text_area_line_numbers.yview
        # self.text_area_line_numbers['yscrollcommand'] = self.on_textscroll
        # self.text_area_line_numbers['yscrollcommand'] = self.scrollbar_y_text_area_top.set

        self.scrollbar_x_text_area_top = Scrollbar(self.top_frame, orient="horizontal")
        self.scrollbar_x_text_area_top.pack(side='bottom', fill=X)
        self.scrollbar_x_text_area_top['command'] = self.text_area_top.xview
        self.text_area_top['xscrollcommand'] = self.scrollbar_x_text_area_top.set
        # self.text_area_line_numbers.pack(side=LEFT,fill=BOTH)#fill=X,side=LEFT)
        # self.text_area_line_numbers.config(state=DISABLED)
        # text_area_bottom.config(state=DISABLED)
        self.text_area_top.pack(side=TOP, fill=BOTH)  # fill=X,side=LEFT)

        self.text_area_bottom = Text(self.bottom_frame, font='Consolas 14', height=15, wrap=CHAR)
        self.scrollbar_y_text_area_bottom = Scrollbar(self.bottom_frame)
        self.scrollbar_y_text_area_bottom.pack(side='right', fill=Y)
        self.scrollbar_y_text_area_bottom['command'] = self.text_area_bottom.yview
        self.text_area_bottom['yscrollcommand'] = self.scrollbar_y_text_area_bottom.set
        self.text_area_bottom.pack(side=TOP, fill=BOTH)  # fill=X,side=LEFT)

        # bind
        self.open_file_button.bind("<1>", self.open_file_handler)
        self.compile_button.bind("<1>", self.compile_handler)
        self.save_button.bind("<1>", self.save_handler)

        self.lex_but.bind("<1>", self.lex_table_handler)
        self.idn_but.bind("<1>", self.idn_table_handler)
        self.con_but.bind("<1>", self.con_table_handler)

        self.rozbir_button.bind("<1>", self.rozbir_table_handler)
        self.relation_button.bind("<1>", self.relation_table_handler)

        self.rozbit_table_button.bind("<1>", self.rozbir_handler)

        self.text_area_bottom.config(state=DISABLED)

    def edit_bottom_textarea(method_to_decorate):
        def wrapper(*args, **kwargs):
            args[0].text_area_bottom.config(state=NORMAL)
            # try:
            method_to_decorate(*args, **kwargs)
            # except Exception as ex:
            # print(ex)
            args[0].text_area_bottom.config(state=DISABLED)

        return wrapper


    @edit_bottom_textarea
    def rozbir_handler(self, event):

        # from tkinter.ttk import *
        new_window = Toplevel()
        new_window.title("Rozbir table")
        frame = Frame(new_window, height=50)
        frame.pack(fill=BOTH)

        text_area = Text(frame, font='Consolas 12', height=50, wrap=NONE)
        text_area.insert(1.0, self.rozbir_table)
        # np.savetxt(text_area,relationTable,fmt='%.d')
        text_area.pack(fill=BOTH)  # fill=X,side=LEFT)
        new_window.state('zoomed')

    @edit_bottom_textarea
    def relation_table_handler(self, event):

        # from tkinter.ttk import *
        new_window = Toplevel()
        new_window.title("Relation table")
        frame = Frame(new_window, height=50)
        frame.pack(fill=BOTH)

        text_area = Text(frame, font='Consolas 12', height=50, wrap=NONE)
        text_area.insert(1.0, self.rel_table)
        # np.savetxt(text_area,relationTable,fmt='%.d')
        text_area.pack(fill=BOTH)  # fill=X,side=LEFT)
        new_window.state('zoomed')

    @edit_bottom_textarea
    def rozbir_table_handler(self, event):

        # from tkinter.ttk import *
        new_window = Toplevel()
        new_window.title("Analysis table")
        frame = Frame(new_window, height=50)
        frame.pack(fill=BOTH)

        text_area = Text(frame, font='Consolas 12', height=50, wrap=NONE)
        text_area.insert(1.0, self.an_table)
        # np.savetxt(text_area,relationTable,fmt='%.d')
        text_area.pack(fill=BOTH)  # fill=X,side=LEFT)
        new_window.state('zoomed')

    @edit_bottom_textarea
    def lex_table_handler(self, event):
        # from tkinter.ttk import *
        new_window = Toplevel()
        new_window.title("Lexemes Table")
        frame = Frame(new_window, height=50)
        frame.pack(fill=BOTH)

        text_area = Text(frame, font='Consolas 12', height=50, wrap=NONE)
        text_area.insert(1.0, lexan.lex_str)
        # np.savetxt(text_area,relationTable,fmt='%.d')
        text_area.pack(fill=BOTH)  # fill=X,side=LEFT)
        new_window.state('zoomed')

    @edit_bottom_textarea
    def idn_table_handler(self, event):
        # from tkinter.ttk import *
        new_window = Toplevel()
        new_window.title("IDN table")
        frame = Frame(new_window, height=50)
        frame.pack(fill=BOTH)

        text_area = Text(frame, font='Consolas 12', height=50, wrap=NONE)
        text_area.insert(1.0, lexan.idn_str)
        # np.savetxt(text_area,relationTable,fmt='%.d')
        text_area.pack(fill=BOTH)  # fill=X,side=LEFT)
        new_window.state('zoomed')

    @edit_bottom_textarea
    def con_table_handler(self, event):
        # from tkinter.ttk import *
        new_window = Toplevel()
        new_window.title('CON table')
        frame = Frame(new_window, height=50)
        frame.pack(fill=BOTH)

        text_area = Text(frame, font='Consolas 12', height=50, wrap=NONE)
        text_area.insert(1.0, lexan.con_str)
        # np.savetxt(text_area,relationTable,fmt='%.d')
        text_area.pack(fill=BOTH)  # fill=X,side=LEFT)
        new_window.state('zoomed')


    @edit_bottom_textarea
    def open_file_handler(self, event):
        filename = askopenfilename(filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        try:
            file = open(filename, 'r')
            text = file.readlines()
            # num_lines = sum(1 for line in text)
            file.close()

            # line_numbers = "\n".join(str(i) for i in range(1,num_lines+1))

            # self.text_area_line_numbers.config(state=NORMAL)
            # self.text_area_line_numbers.delete('1.0', END)
            # self.text_area_line_numbers.insert(1.0,line_numbers)
            # self.text_area_line_numbers.config(state=DISABLED)

            self.text_area_top.delete('1.0', END)
            self.text_area_top.insert(1.0, "".join(text))
        except UnicodeDecodeError as ex:
            self.text_area_bottom.delete('1.0', END)
            self.text_area_bottom.insert(1.0, "Wrong file format!")

    @edit_bottom_textarea
    def compile_handler(self, event):
        self.text_area_bottom.delete('1.0', END)
        text = self.text_area_top.get('1.0', END)
        traceback = True
        text2 = ''

        file = open(self.name_of_file, 'w')
        file.write(self.text_area_top.get(1.0, END))
        file.close()

        lexan.lexical_analyzer(text)
        if lexan.error_text:
            if traceback:
                for error in lexan.error_text:
                    text2 += error
            else:
                text2 = lexan.error_text[0]
        else:

            rel = relation.Relation()
            self.rel_table = rel.make_table()

            #syntax analyser 2 lab
            # SynAn = synan.SyntaxAnalyser()
            # SynAn.prog()

            #syntax analyser 2 lab
            # SynAn = mpa.MPA()
            # SynAn.automat()
            # self.an_table = SynAn.make_table()

            if lexan.error_text:
                if traceback:
                    for error in lexan.error_text:
                        text2 += error + '\n'
                else:
                    text2 = lexan.error_text[0]
            else:
                text2 = 'Successfully\n'

            try:
                syn = synan5.SyntaxAnalyser5()
                syn.analyse()
            except Warning as e:
                text2 = str(e)
            finally:
                self.rozbir_table = syn.rozbir_table
                # text2 += self.rozbir_table
                # text2 += 'lexemes table\n' + lexan.lex_str + 'idn table\n' + lexan.idn_str + 'con table\n' + lexan.con_str

        # machine = mpa.MPA()
        # rel = relation.Relation()
        # self.rel_table = rel.make_table()
        # print(self.rel_table)
        self.text_area_bottom.insert(1.0, text2)



    @edit_bottom_textarea
    def save_handler(self, event):
        filename = asksaveasfilename(filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        file = open(filename, 'w')
        file.write(self.text_area_top.get(1.0, END))
        file.close()
        # self.text_area_top.delete('1.0', END)
        # self.text_area_top.insert(1.0,text)


if __name__ == "__main__":
    FILE_NAME = 'test.txt'
    root = Tk()
    gui = Complier(root, FILE_NAME)
    root.state('normal')
    root.mainloop()
