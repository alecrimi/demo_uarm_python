"""
Author: Isaac Alonso  alonso.isaac@gmail.com 
Made during BrainHackZurich
"""


import serial
from time import sleep
import Tkinter as tk

clamp_status = False
height_mode = True
x, y, z = 0, 0, 0

# right click switches between controlling the y or z axis
def rightclick(event):
    global height_mode
    if height_mode:
        height_mode = False
        print('height mode on')
    else:
        height_mode = True
        print('height mode off')

# left click opens/closes the clamp
def leftclick(event):
    global clamp_status
    if clamp_status:
        print('opening clamp')
        command = "#25 M2232 V0\n"
        clamp_status = False
    else:
        print('closing clamp')
        command = "#25 M2232 V1\n"
        clamp_status = True

    ser.write(command.encode())
    # wait for confirmation
    ser.readline()
    # ideally here we should check that confirmation is correct

# when switching between height/reach mode the clamp will make position jumps
# due to the last position of the mouse
# we could try to use the mouse wheel for height or reach, so we don't have to
# switch modes
def motion(event):
    global x,y,z
    # in height mode we control x and z
    if height_mode:
        x, z = event.x, event.y
    # otherwise we control x and y
    else:
        x, y = event.x, event.y

    # polar coordinates command
    command = "#25 G2201 X" + str(300-y) + \
                       " Y" + str(180-x/2) + \
                       " Z" + str(z) + \
                       " F5000\n"

    print(180-x/2, 300-y, z)
    ser.write(command.encode())
    ser.readline()


root = tk.Tk()
back = tk.Frame(master=root, width=360, height=300)
back.pack()

with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:

    back.bind('<Motion>', motion)
    back.bind('<Button-1>', leftclick)
    back.bind('<Button-3>', rightclick)

    root.mainloop()
