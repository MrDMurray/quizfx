import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard = Keyboard(usb_hid.devices)


# Setup Button Pins 0,7,19

rightArrow_pin = board.GP19       
randomSelect_pin = board.GP7
leftArrow_pin = board.GP0


# Setup LED out pins 15 and 16

led1 = digitalio.DigitalInOut(board.GP15)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP16)
led2.direction = digitalio.Direction.OUTPUT


# LED Flash Functions

def ledRedFlash(n):
    for x in range(n):
        led1.value = True
        time.sleep(0.2)
        led1.value = False
        time.sleep(0.2)
        
def ledYellowFlash(n):
    for x in range(n):
        led2.value = True
        time.sleep(0.2)
        led2.value = False
        time.sleep(0.2)

# Startup Sequence:
ledRedFlash(2)
ledYellowFlash(2)
print("Ready to go")

# Initializing right arrow next slide button
rightArrow = digitalio.DigitalInOut(rightArrow_pin)
rightArrow.direction = digitalio.Direction.INPUT
rightArrow.pull = digitalio.Pull.DOWN

# Initializing pick random student
randomSelect = digitalio.DigitalInOut(randomSelect_pin)
randomSelect.direction = digitalio.Direction.INPUT
randomSelect.pull = digitalio.Pull.DOWN

# Initializing right arrow next slide button
leftArrow = digitalio.DigitalInOut(leftArrow_pin)
leftArrow.direction = digitalio.Direction.INPUT
leftArrow.pull = digitalio.Pull.DOWN



# main loop

while True:
    if rightArrow.value:  
        print(" right button Pressed")
        keyboard.press(Keycode.RIGHT_ARROW)
        time.sleep(0.15)
        keyboard.release(Keycode.RIGHT_ARROW)
        
        ledRedFlash(1)

        
    if randomSelect.value:
        print(" randomSelect button Pressed")
        keyboard.press(Keycode.F10)
        time.sleep(0.15)
        keyboard.release(Keycode.F10)
        
        ledRedFlash(2)
        
        
    if leftArrow.value:
        print("leftArrow button Pressed")
        keyboard.press(Keycode.LEFT_ARROW)
        time.sleep(0.15)
        keyboard.release(Keycode.LEFT_ARROW)
        
        ledRedFlash(3)
        
    time.sleep(0.1)