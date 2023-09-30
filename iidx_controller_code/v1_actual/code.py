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
import time


keycodes = ([Keycode.Z, Keycode.X] + [Keycode.A, Keycode.F, Keycode.F] +
[Keycode.F,Keycode.T,Keycode.G,Keycode.Y,Keycode.H,Keycode.U,Keycode.J][::1])
key_prev_value = [False for i in range(len(keycodes))]


i2c = busio.I2C(scl=board.GP3, sda=board.GP2)
#i2c = busio.I2C(board.SCL1, board.SDA1)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)  # We're in the US :)
mpr121 = adafruit_mpr121.MPR121(i2c)#, address=0x5c)

mouse = Mouse(usb_hid.devices)
i2c1 = busio.I2C(scl=board.GP1, sda=board.GP0)
mpr121_turntable = adafruit_mpr121.MPR121(i2c1)#, address=0x5c)
turntable_count = 0
turntable_last_pressed = time.monotonic()

turntable_prev_value = [False for i in range(len(keycodes))]
turntable_pins = [2, 3, 4]
def run():
    prev_key = None
    prev_turntable = 0
    turntable_last_pressed = time.monotonic()
    while True:
        for i in range(len(keycodes)):
            if mpr121[i].value == key_prev_value[i]:
                continue
            key_prev_value[i] = mpr121[i].value
            if mpr121[i].value:
                print(f"Pin {i} touched!")
                ### Turntable Code #####################################
                '''
                if keycodes[i] == Keycode.A and prev_turntable != i:
                    ### is sliding across
                    if -1 <= prev_turntable - i < 0: # Going Up
                        for i in range(12):
                            keyboard.press(Keycode.UP_ARROW)
                            time.sleep(0.001)
                            keyboard.release(Keycode.UP_ARROW)
                        print("Up")
                    elif 0 < prev_turntable - i <= 1: # Going Down
                        for i in range(12):
                            keyboard.press(Keycode.DOWN_ARROW)
                            time.sleep(0.001)
                            keyboard.release(Keycode.DOWN_ARROW)
                        print("Down")
                    else: # Reset Position
                        pass
                    #keyboard.press(keycodes[i])
                    print(prev_turntable, i, prev_turntable - i)
                    prev_turntable = i
                    continue
                elif keycodes[i] == Keycode.A:
                    prev_turntable = i
                    continue
                '''
                ########################################################
                keyboard.press(keycodes[i])
                prev_key = keycodes[i]
            else:
                keyboard.release(keycodes[i])
                prev_key = keycodes[i]
        #time.sleep(0.01)
        for i in range(len(keycodes)):
            if mpr121_turntable[i].value == turntable_prev_value[i]:
                continue
            turntable_prev_value[i] = mpr121_turntable[i].value
            if mpr121_turntable[i].value:
                print(f"Turntable Pin {i} touched!")
                ### Turntable Code #####################################
                if time.monotonic() - turntable_last_pressed > 2:
                    #print("trigger reset")
                    #turntable_last_pressed = time.monotonic()
                    #prev_turntable = i
                    #continue
                    pass
                turntable_last_pressed = time.monotonic()
                if prev_turntable != -1 and prev_turntable != i:
                    mouse.move(y=50)
                    '''
                    if 1 <= prev_turntable - i <= 2:
                        print("mouse down")
                        mouse.move(y=50)
                        #keyboard.press(Keycode.DOWN_ARROW)
                    elif -2 <= prev_turntable - i <= -1:
                        print("mouse up")
                        mouse.move(y=-50)
                        #keyboard.press(Keycode.UP_ARROW)
                    #print(f"prev {prev_turntable} touched!")
                    '''

                ########################################################
                prev_turntable = i
            else:
                pass
                #keyboard.release(keycodes[i])
                #prev_turntable = -1
while True:
    try:
        run()
    except Exception as e:
        print(e)
#'''
