from termcolor import cprint
from itertools import cycle

import subprocess
import time
import os


colors = iter(cycle(['blue', 'red']))
os.system('cls')

print('\n Welcome to WiFi Password Extractor (written by Sina.F)\n')
time.sleep(.7)

for _ in range(12):
    for char in '/-\|':
        print(f'\r Extracting WiFi Passwords...  {char}', end='')
        time.sleep(.15)

time.sleep(1)
print('\n\n\n {:<30}|  Password\n'.format('Host Name'))
output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode().splitlines()
profiles = [line.split(':', 1)[-1].lstrip() for line in output if 'All User Profile' in line]

for profile in profiles:
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', profile, 'key=clear']).decode('ISO-8859-1').splitlines()
    color = next(colors)

    try:
        password = [line.split(':', 1)[1].lstrip() for line in result if 'Key Content' in line][0]
        cprint(f' {profile:<30}|  {password}', color=color)

    except Exception:
        cprint(f' {profile:<30}|  <No Password>', color=color)

    finally:
        time.sleep(.7)


figlet = '''\n
   _____ _                __ 
  / ____(_)              / _|
 | (___  _ _ __   __ _  | |_ 
  \___ \| | '_ \ / _` | |  _|
  ____) | | | | | (_| |_| |  
 |_____/|_|_| |_|\__,_(_)_| 
'''

for line in figlet.splitlines():
    print(line)
    time.sleep(.2)

time.sleep(1)
input('\n\n Press <enter> to exit...')
