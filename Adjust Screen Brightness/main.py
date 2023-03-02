import screen_brightness_control as sbc
import tkinter as tk
import webbrowser
import os


class App:
    def __init__(self, master):
        self.window = master
        self.window.config(menu=self.init_menu())

        self.monitors = {
            monitor: tk.IntVar()
            for monitor in sbc.list_monitors()
        }

        for idx, (monitor, variable) in enumerate(self.monitors.items()):
            frame = tk.Frame()
            frame.pack(pady=6)

            tk.Label(frame, text=f'{monitor}: ').grid(column=0, row=0, padx=3)

            variable.set(sbc.get_brightness()[idx])
            scaler = tk.Scale(frame, from_=0, to=100, variable=variable, orient=tk.HORIZONTAL)
            scaler.grid(column=1, row=0, padx=10)
            scaler.bind('<MouseWheel>', lambda event: rolling(event, variable))

            tk.Button(frame, text='Adjust', width=8, command=lambda: sbc.set_brightness(variable.get(), display=idx)).grid(column=2, row=0, padx=3)
            tk.Button(frame, text='Reset', width=8, command=lambda: variable.set(sbc.get_brightness()[idx])).grid(column=3, row=0, padx=3)

    @staticmethod
    def about_dialog():
        dialog = tk.Tk()
        dialog.title('About us')
        dialog.geometry('220x90+550+350')
        set_icon(dialog)
        dialog.focus_force()

        print('\a')

        frame = tk.Frame(dialog)
        frame.pack(pady=10)
        tk.Label(frame, text='This program made by Sina.f').grid(column=0, row=0, columnspan=2, pady=5)
        tk.Button(frame, text='GitHub', width=8, command=lambda: webbrowser.open('https://github.com/sina-programer')).grid(column=0, row=2)
        tk.Button(frame, text='Telegram', width=8, command=lambda: webbrowser.open('https://t.me/sina_programer')).grid(column=1, row=2)

        dialog.mainloop()

    def init_menu(self):
        menu = tk.Menu(self.window)
        menu.add_command(label='About us', command=App.about_dialog)

        return menu


def rolling(event, variable: tk.Variable):
    value = variable.get()
    delta = event.delta
    if delta > 0:
        value += 1
    else:
        value -= 1

    variable.set(value)


def set_icon(master: tk.Tk):
    if os.path.exists(ICON_PATH):
        master.iconbitmap(ICON_PATH)



ICON_PATH = 'icon.ico'
WIDTH = 520
HEIGHT = 60 * len(sbc.list_monitors())  # 60 unit for each monitor
if os.path.exists(ICON_PATH):
    HEIGHT += 20


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    root.title('Adjust Screen Brightness')
    root.geometry(f'{WIDTH}x{HEIGHT}+550+300')
    set_icon(root)

    app = App(root)
    root.mainloop()
