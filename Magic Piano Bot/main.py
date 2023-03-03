import webbrowser
import pyautogui
import win32api
import win32con
import keyboard
import random
import time


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(random.randint(10, 30) / 1000)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


quit_key = 'q'  # interrupt the process by pressing this key
link = 'https://gameforge.com/en-US/littlegames/magic-piano-tiles/#'
positions = [(430, 500), (490, 500), (560, 500), (650, 500)]  # positions of lines to check

webbrowser.open(link)
input('When the page was loaded, press enter...')
time.sleep(2)


while not keyboard.is_pressed(quit_key):
    for x, y in positions:
        if not pyautogui.pixel(x, y)[2]:  # if the pixel was black
            click(x, y)
