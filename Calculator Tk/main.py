from math import sqrt
from functools import wraps
from tkinter import simpledialog
import tkinter as tk
import webbrowser
import os


def clause_handler(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        self = args[0]
        clause = self.clause.get()
        if clause:
            return func(*args, clause, **kwargs)

    return wrapper



class AboutDialog(simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, 'About us')

    def body(self, frame):
        padding = {'padx': 15, 'pady': 5}

        tk.Label(frame, text='This program made by Sina.F').grid(row=1, column=1, columnspan=2, **padding)
        tk.Button(frame, text='GitHub', width=8, command=lambda: webbrowser.open('https://github.com/sina-programer')).grid(row=2, column=1, **padding)
        tk.Button(frame, text='Telegram', width=8, command=lambda: webbrowser.open('https://t.me/sina_programer')).grid(row=2, column=2, **padding)

        self.geometry('240x90')
        self.resizable(False, False)

        return frame

    def buttonbox(self):
        pass


class Calculator:
    characters = {
        '×': '*',
        '÷': '/',
        '^': '**',
        '√': 'sqrt',
    }
    translator = str.maketrans(characters)

    def __init__(self, master):
        self.clause = tk.StringVar()
        self.clause.trace('w', lambda *args: self.validate())

        master.config(menu=self.init_menu(master))

        # set shortcuts -----------------------------------------
        master.bind('0', lambda _: self.update('0'))
        master.bind('1', lambda _: self.update('1'))
        master.bind('2', lambda _: self.update('2'))
        master.bind('3', lambda _: self.update('3'))
        master.bind('4', lambda _: self.update('4'))
        master.bind('5', lambda _: self.update('5'))
        master.bind('6', lambda _: self.update('6'))
        master.bind('7', lambda _: self.update('7'))
        master.bind('8', lambda _: self.update('8'))
        master.bind('9', lambda _: self.update('9'))
        master.bind('+', lambda _: self.update('+'))
        master.bind('-', lambda _: self.update('-'))
        master.bind('*', lambda _: self.update('×'))
        master.bind('/', lambda _: self.update('÷'))
        master.bind('^', lambda _: self.update('^('))
        master.bind('.', lambda _: self.update('.'))
        master.bind('(', lambda _: self.update('('))
        master.bind(')', lambda _: self.update(')'))
        master.bind('r', lambda _: self.round_number())
        master.bind('c', lambda _: self.clear())
        master.bind('<Delete>', lambda _: self.backspace())
        master.bind('<BackSpace>', lambda _: self.backspace())
        master.bind('<Return>', lambda _: self.calculate())
        # -------------------------------------------------------

        # create elements ---------------------------------------
        self.entry = tk.Entry(master, width=25, textvariable=self.clause, justify=tk.RIGHT, state='readonly', font=('consolas', 13, 'bold'))
        self.entry.pack(pady=15)

        buttons_frame = tk.Frame(master)
        buttons_frame.pack(pady=5)
        padding = {'pady': 5, 'padx': 5}

        row = 1
        tk.Button(buttons_frame, text='(', width=6, command=lambda: self.update('(')).grid(row=row, column=1, **padding)
        tk.Button(buttons_frame, text=')', width=6, command=lambda: self.update(')')).grid(row=row, column=2, **padding)
        tk.Button(buttons_frame, text='C', width=6, command=self.clear).grid(row=row, column=3, **padding)
        tk.Button(buttons_frame, text='←', width=6, command=self.backspace).grid(row=row, column=4, **padding)

        row = 2
        tk.Button(buttons_frame, text='R', width=6, command=self.round_number).grid(row=row, column=1, **padding)
        tk.Button(buttons_frame, text='xʸ', width=6, command=lambda: self.update('^(')).grid(row=row, column=2, **padding)
        tk.Button(buttons_frame, text='x²', width=6, command=lambda: self.update('^(2)')).grid(row=row, column=3, **padding)
        tk.Button(buttons_frame, text='²√', width=6, command=lambda: self.update('√(')).grid(row=row, column=4, **padding)

        row = 3
        tk.Button(buttons_frame, text='7', width=6, command=lambda: self.update('7')).grid(row=row, column=1, **padding)
        tk.Button(buttons_frame, text='8', width=6, command=lambda: self.update('8')).grid(row=row, column=2, **padding)
        tk.Button(buttons_frame, text='9', width=6, command=lambda: self.update('9')).grid(row=row, column=3, **padding)
        tk.Button(buttons_frame, text='×', width=6, command=lambda: self.update('×')).grid(row=row, column=4, **padding)

        row = 4
        tk.Button(buttons_frame, text='4', width=6, command=lambda: self.update('4')).grid(row=row, column=1, **padding)
        tk.Button(buttons_frame, text='5', width=6, command=lambda: self.update('5')).grid(row=row, column=2, **padding)
        tk.Button(buttons_frame, text='6', width=6, command=lambda: self.update('6')).grid(row=row, column=3, **padding)
        tk.Button(buttons_frame, text='÷', width=6, command=lambda: self.update('÷')).grid(row=row, column=4, **padding)

        row = 5
        tk.Button(buttons_frame, text='1', width=6, command=lambda: self.update('1')).grid(row=row, column=1, **padding)
        tk.Button(buttons_frame, text='2', width=6, command=lambda: self.update('2')).grid(row=row, column=2, **padding)
        tk.Button(buttons_frame, text='3', width=6, command=lambda: self.update('3')).grid(row=row, column=3, **padding)
        tk.Button(buttons_frame, text='+', width=6, command=lambda: self.update('+')).grid(row=row, column=4, **padding)

        row = 6
        tk.Button(buttons_frame, text='=', width=6, command=self.calculate).grid(row=row, column=1, **padding)
        tk.Button(buttons_frame, text='0', width=6, command=lambda: self.update('0')).grid(row=row, column=2, **padding)
        tk.Button(buttons_frame, text='.', width=6, command=lambda: self.update('.')).grid(row=row, column=3, **padding)
        tk.Button(buttons_frame, text='-', width=6, command=lambda: self.update('-')).grid(row=row, column=4, **padding)
        # -------------------------------------------------------

    @clause_handler
    def calculate(self, clause):
        if result := Calculator.evaluate(clause):
            self.clause.set(result)

    @clause_handler
    def round_number(self, clause):
        if result := Calculator.evaluate(clause):
            self.clause.set(str(round(eval(result))))

    @clause_handler
    def backspace(self, clause):
        self.clause.set(clause[:-1])

    def update(self, text):
        self.clause.set(self.clause.get() + text)

    def clear(self):
        self.clause.set('')

    def validate(self):
        result = Calculator.evaluate(self.clause.get())

        if result:
            self.entry.config(fg='black')
        else:
            self.entry.config(fg='red')

    @staticmethod
    def evaluate(clause):
        clause = Calculator.translate(clause)
        try:
            return str(eval(clause))

        except Exception:
            return None

    @staticmethod
    def translate(clause: str):
        return clause.translate(Calculator.translator)

    @staticmethod
    def init_menu(master):
        menu = tk.Menu(master)
        menu.add_command(label='About us', command=lambda: AboutDialog(master))

        return menu



ICON_PATH = 'icon.png'


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Calculator')
    root.geometry('280x290+570+250')
    root.resizable(False, False)
    root.focus_force()

    if os.path.exists(ICON_PATH):
        root.iconphoto(True, tk.PhotoImage(file=ICON_PATH))

    app = Calculator(root)
    root.mainloop()
