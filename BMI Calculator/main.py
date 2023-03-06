from itertools import pairwise
from tkinter import simpledialog
import tkinter as tk
import webbrowser
import winsound
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
    bins = [0, 9, 18.5, 24.9, 1000]  # (start, stop]
    labels = ['Underweight', 'Normal', 'Overweight', 'Obesity']
    colors = ['#BEA600', '#00AA00', '#FF6400', '#EE0000']

    def __init__(self, master):
        master.config(menu=self.init_menu(master))
        master.bind('<Return>', lambda _: self.calculate())


        self.height = tk.IntVar()
        self.height.set(170)
        self.weight = tk.IntVar()
        self.weight.set(75)

        tk.Label(master, text='Height (cm): ').grid(row=1, column=1, padx=10)
        weight_scaler = tk.Scale(master, from_=120, to=210, variable=self.height, orient=tk.HORIZONTAL)
        weight_scaler.bind('<MouseWheel>', lambda event: rolling(event, self.height))
        weight_scaler.grid(row=1, column=2)

        tk.Label(master, text='Weight (kg): ').grid(row=2, column=1, padx=10)
        height_scaler = tk.Scale(master, from_=30, to=150, variable=self.weight, orient=tk.HORIZONTAL)
        height_scaler.bind('<MouseWheel>', lambda event: rolling(event, self.weight))
        height_scaler.grid(row=2, column=2, pady=5)

        tk.Button(master, text='Calculate', width=24, command=self.calculate).grid(row=3, column=1, columnspan=2, padx=15, pady=10)

        bmi_frame = tk.Frame(master)
        bmi_frame.grid(row=4, column=1, columnspan=2)
        tk.Label(bmi_frame, text='Your BMI: ').pack(side=tk.LEFT)
        self.bmi_lbl = tk.Label(bmi_frame)
        self.bmi_lbl.pack(side=tk.RIGHT)

    def calculate(self):
        height = self.height.get()
        weight = self.weight.get()
        bmi_score = weight / ((height / 100) ** 2)
        idx = cut(bmi_score, App.bins)

        self.bmi_lbl.config(text=f'{bmi_score:.3f}  {App.labels[idx]}', fg=App.colors[idx])

    @staticmethod
    def init_menu(master):
        menu = tk.Menu(master)
        menu.add_command(label='About us', command=lambda: AboutDialog(master))
        return menu



def rolling(event, variable: tk.Variable):
    value = variable.get()
    delta = event.delta
    if delta > 0:
        value += 1
    else:
        value -= 1

    variable.set(value)


def cut(n, bins):  # pd.cut
    for idx, (start, stop) in enumerate(pairwise(bins)):
        if start < n <= stop:
            return idx



ICON_PATH = 'icon.ico'


if __name__ == "__main__":
    root = tk.Tk()
    root.title('BMI Calculator')
    root.geometry('210x180+550+250')
    root.resizable(False, False)

    if os.path.exists(ICON_PATH):
        root.iconbitmap(default=ICON_PATH)

    app = App(root)
    root.mainloop()
