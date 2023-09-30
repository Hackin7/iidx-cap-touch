'''
# SPDX-FileCopyrightText: 2017 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()

import time
import busio
import board
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)

while not i2c.try_lock():
    pass

try:
    while True:
        print(
            "I2C addresses found:",
            [hex(device_address) for device_address in i2c.scan()],
        )
        time.sleep(2)

finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()

'''
print("Hello World!")
import time
import board
import busio

import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.mouse import Mouse
import adafruit_mpr121


keycodes = ([Keycode.Z, Keycode.X] + [Keycode.A]*(7+3))# + [Keycode.F,Keycode.T,Keycode.G,Keycode.Y,Keycode.H,Keycode.U,Keycode.J][::-1])
key_prev_value = [False for i in range(len(keycodes))]

turntable_pins = [2, 3, 4]

i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
#i2c = busio.I2C(board.SCL1, board.SDA1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
mouse = Mouse(usb_hid.devices)


mpr121 = adafruit_mpr121.MPR121(i2c)
def run():
    prev_key = None
    prev_turntable = 0
    while True:
        for i in range(len(keycodes)):
            if mpr121[i].value == key_prev_value[i]:
                continue
            key_prev_value[i] = mpr121[i].value
            if mpr121[i].value:
                print(f"Pin {i} touched!")
                ### Turntable Code #####################################
                if prev_turntable != i:
                    print(f"prev {prev_turntable} touched!")
                    keyboard.press(Keycode.Z)
                    mouse.move(y=100)

                ########################################################
                keyboard.press(keycodes[i])
                prev_key = keycodes[i]
                prev_turntable = i
            else:
                keyboard.release(keycodes[i])
                prev_key = None
        #time.sleep(0.01)
while True:
    try:
        run()
    except Exception as e:
        print(e)
#'''
