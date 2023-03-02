from base64 import b64encode, b64decode
from tkinter import ttk, messagebox, simpledialog
from itertools import cycle
import tkinter as tk
import webbrowser
import winsound
import os


class Cryptographer:
    def encrypt(self, key, text):
        cryptograph = self.xor(key, text)
        return b64encode(cryptograph.encode()).decode()

    def decrypt(self, key, text):
        try:
            data = b64decode(text.encode()).decode()
            return self.xor(key, data)

        except:
            messagebox.showerror('ERROR', 'Please enter a valid encrypted text')

    @staticmethod
    def xor(key, text):
        result = ''
        for k, t in zip(cycle(key), text):
            result += ''.join(chr(ord(k) ^ ord(t)))
            
        return result


class AboutDialog(simpledialog.Dialog):
    def __init__(self, parent):
        winsound.MessageBeep()
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


class Tab:
    def __init__(self, notebook, title, function: 'Cryptographer.encrypt | Cryptographer.decrypt'):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=f"  {title}  ", padding=4)
        personalize = {
            'selectbackground': 'blue',
            'font': 'TkFixedFont',
            'width': 20
        }

        self.keyVar = tk.StringVar()
        tk.Label(frame, text='Key: ').grid(row=0, column=0, pady=15)
        tk.Entry(frame, textvariable=self.keyVar, **personalize).grid(row=0, column=1)

        tk.Label(frame, text='Text: ').grid(row=1, column=0, pady=15)
        self.text = tk.Text(frame, height=5, **personalize)
        self.text.grid(row=1, column=1)

        tk.Button(frame, text=title, width=22, command=lambda: self.insert_output(function(self.keyVar.get(), self.text.get('1.0', 'end')))).grid(row=2, column=1, pady=15)

        tk.Label(frame, text='Output: ').grid(row=3, column=0, pady=15)
        self.output = tk.Text(frame, height=5, **personalize)
        self.output.grid(row=3, column=1)

    def insert_output(self, text):
        if self.keyVar.get():

            if self.text.get('1.0', 'end').strip():
                self.output.delete('1.0', 'end')
                self.output.insert('1.0', text)

            else:
                messagebox.showwarning('ERROR', 'Please enter a text!')

        else:
            messagebox.showwarning('ERROR', 'Please enter a key!')

    def clear(self):
        self.keyVar.set('')
        self.text.delete('1.0', 'end')
        self.output.delete('1.0', 'end')


class App:
    def __init__(self, master):
        self.master = master
        self.master.config(menu=self.init_menu())
        self.master.bind('<Escape>', lambda _: self.clear())

        self.cryptographer = Cryptographer()

        notebook = ttk.Notebook(master)
        notebook.place(relx=0.02, rely=0.02, relheight=.97, relwidth=0.97)

        self.encryptTab = Tab(notebook, 'Encrypt', self.cryptographer.encrypt)
        self.decryptTab = Tab(notebook, 'Decrypt', self.cryptographer.decrypt)

    def clear(self):
        self.encryptTab.clear()
        self.decryptTab.clear()

    def init_menu(self):
        menu = tk.Menu(self.master)
        menu.add_command(label='Clear', command=self.clear)
        menu.add_command(label='About us', command=lambda: AboutDialog(self.master))

        return menu



ICON_PATH = 'icon.ico'


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Cryptographer')
    root.resizable(False, False)
    root.geometry('250x330+550+230')

    if os.path.exists(ICON_PATH):
        root.iconbitmap(default=ICON_PATH)

    app = App(root)
    root.mainloop()
