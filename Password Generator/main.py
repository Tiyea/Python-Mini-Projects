from tkinter import messagebox, simpledialog
import tkinter as tk
import webbrowser
import string
import random
import os


class AboutDialog(simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, 'About us')

    def body(self, frame):
        padding = {'padx': 15, 'pady': 5}

        tk.Label(frame, text='This program made by Sina.f').grid(row=1, column=1, columnspan=2, **padding)
        tk.Button(frame, text='GitHub', width=8, command=lambda: webbrowser.open('https://github.com/sina-programer')).grid(row=2, column=1, **padding)
        tk.Button(frame, text='Telegram', width=8, command=lambda: webbrowser.open('https://t.me/sina_programer')).grid( row=2, column=2, **padding)

        self.geometry('240x90')
        self.resizable(False, False)

        return frame

    def buttonbox(self):
        pass


class App:
    characters = {
        'low': string.ascii_letters,
        'medium': string.ascii_letters + string.digits,
        'high': string.ascii_letters + string.digits + string.punctuation + string.ascii_uppercase
    }

    def __init__(self, master):
        self.master = master
        self.master.config(menu=App.init_menu(self.master))


        top_frame = tk.Frame(self.master)
        top_frame.pack(side=tk.TOP, pady=10)

        self.levelVar = tk.StringVar()
        self.levelVar.set('Select a level')
        level_frame = tk.Frame(top_frame)
        level_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(level_frame, text='Level: ').pack(side=tk.LEFT)
        tk.OptionMenu(level_frame, self.levelVar, *App.characters.keys()).pack(side=tk.RIGHT)

        self.lengthVar = tk.IntVar()
        self.lengthVar.set(8)
        length_frame = tk.Frame(top_frame)
        length_frame.pack(side=tk.RIGHT, padx=20)
        tk.Label(length_frame, text='Length: ').pack(side=tk.LEFT)
        tk.Spinbox(length_frame, from_=4, to=20, width=10, textvariable=self.lengthVar).pack(side=tk.RIGHT)


        bottom_frame = tk.Frame(self.master)
        bottom_frame.pack(pady=5)

        self.passwordVar = tk.StringVar()
        pass_frame = tk.Frame(bottom_frame)
        pass_frame.grid(row=2, column=1, padx=20, rowspan=2)
        tk.Label(pass_frame, text='Password: ').pack(side=tk.LEFT)
        tk.Entry(pass_frame, width=20, bd=2, textvariable=self.passwordVar, state='readonly').pack(side=tk.RIGHT)

        tk.Button(bottom_frame, text='Copy', width=10, command=self.copy_password).grid(row=1, column=2, padx=20, pady=3, rowspan=2)
        tk.Button(bottom_frame, text='Generate', width=10, command=self.generate).grid(row=3, column=2, padx=20, rowspan=2)

    def generate(self):
        length = self.lengthVar.get()
        characters = self.characters.get(self.levelVar.get().lower(), None)

        if characters:
            password = ''.join(random.sample(characters, length))
            self.passwordVar.set(password)

        else:
            messagebox.showwarning('ERROR', 'Please select a level')

    def copy_password(self):
        password = self.passwordVar.get()

        if password:
            self.master.clipboard_clear()
            self.master.clipboard_append(password)

        else:
            messagebox.showwarning('ERROR', 'Please first generate a password')

    @staticmethod
    def init_menu(master):
        menu = tk.Menu(master)
        menu.add_command(label='About us', command=lambda: AboutDialog(master))
        return menu



ICON_PATH = 'icon.ico'


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Password Generator')
    root.geometry('350x130+500+300')
    root.resizable(False, False)

    if os.path.exists(ICON_PATH):
        root.iconbitmap(default=ICON_PATH)

    app = App(root)
    root.mainloop()
