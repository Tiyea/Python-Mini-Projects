from tkinter import messagebox, simpledialog
import tkinter as tk
import webbrowser
import winsound
import csv
import os


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


class App:
    def __init__(self, master):
        self.master = master
        self.master.config(menu=self.init_menu(master))

        self.content = load_csv(DATA_PATH)
        self.male_content = list(filter(lambda row: row[1], self.content))
        self.female_content = list(filter(lambda row: row[2], self.content))

        self.gender = tk.IntVar()
        self.length = tk.IntVar()
        self.letter = tk.StringVar()
        self.index = tk.IntVar()

        self.create_UI()

    def create_UI(self):
        tk.Radiobutton(self.master, text='Total', value=0, variable=self.gender).grid(row=0, column=0)
        tk.Radiobutton(self.master, text='Male', value=1, variable=self.gender).grid(row=1, column=0, padx=15)
        tk.Radiobutton(self.master, text='Female', value=2, variable=self.gender).grid(row=2, column=0)


        input_frame = tk.Frame(self.master)
        input_frame.grid(row=0, column=1, rowspan=3, padx=20)

        tk.Label(input_frame, text='Length: ').grid(row=0, column=0)
        tk.Spinbox(input_frame, from_=2, to=20, width=3, textvariable=self.length).grid(row=0, column=1, pady=5)

        tk.Label(input_frame, text='Letter: ').grid(row=1, column=0)
        tk.Entry(input_frame, width=5, textvariable=self.letter).grid(row=1, column=1, pady=5)

        tk.Label(input_frame, text='Index: ').grid(row=2, column=0)
        tk.Spinbox(input_frame, from_=1, to=20, width=3, textvariable=self.index).grid(row=2, column=1, pady=5)


        tk.Button(self.master, text='Export', width=22, command=self.export).grid(row=3, column=0, columnspan=2, pady=15)

    def export(self):
        gender = self.gender.get()
        if gender == 0:
            content = self.content.copy()
        elif gender == 1:
            content = self.male_content.copy()
        elif gender == 2:
            content = self.female_content.copy()

        length = self.length.get()
        letter = self.letter.get()
        index = self.index.get()
        idx = index - 1

        if letter.strip():
            content = list(filter(lambda row: len(row[0]) == length, content))  # filter by length
            content = list(filter(lambda row: row[0][idx] == letter, content))  # filter by character
            names = list(map(lambda row: row[0], content))

            code = f'{gender}{length}{index}_{ord(letter)}'
            with open(f"names_{code}.txt", 'w', encoding='utf-8') as handler:
                handler.write('\n'.join(names))

            messagebox.showinfo('Complete', f'Your request saved with code: {code}')

        else:
            messagebox.showwarning('ERROR', 'Please enter a valid letter for search')

    def init_menu(self, master):
        menu = tk.Menu(master)
        menu.add_command(label='About us', command=lambda: AboutDialog(self.master))

        return menu  


def load_csv(filepath) -> list[list]:
    with open(filepath, encoding='utf-8') as file:
        return list(csv.reader(file))



ICON_PATH = 'icon.ico'
DATA_PATH = 'data.csv'


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Name Finder')
    root.geometry(f'200x140+550+250')
    root.resizable(False, False)

    if os.path.exists(DATA_PATH):
        if os.path.exists(ICON_PATH):
            root.iconbitmap(default=ICON_PATH)

        app = App(root)

    else:
        winsound.MessageBeep()
        tk.Label(root, text=f'Please run the app next to the <{DATA_PATH}>', fg='red').pack()


    root.mainloop()
