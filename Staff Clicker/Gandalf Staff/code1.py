import board
import digitalio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


keyboard = Keyboard(usb_hid.devices)


rightArrow_pin = board.GP19       # pin to connect button to
randomSelect_pin = board.GP7
leftArrow_pin = board.GP0

led1 = digitalio.DigitalInOut(board.GP15)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.GP16)
led2.direction = digitalio.Direction.OUTPUT

led1.value = True
print("Let's")
time.sleep(1)
led1.value = False
print("Go")

time.sleep(1)

led2.value = True
print("Let's")
time.sleep(1)
led2.value = False
print("Go")


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

ledRedFlash(2)
ledYellowFlash(2)

# Initializing Button
right = digitalio.DigitalInOut(rightArrow_pin)
right.direction = digitalio.Direction.INPUT
right.pull = digitalio.Pull.DOWN


randomSelect = digitalio.DigitalInOut(randomSelect_pin)
randomSelect.direction = digitalio.Direction.INPUT
randomSelect.pull = digitalio.Pull.DOWN


leftArrow = digitalio.DigitalInOut(leftArrow_pin)
leftArrow.direction = digitalio.Direction.INPUT
leftArrow.pull = digitalio.Pull.DOWN







while True:
	# Check if button is pressed and if it is, to press the Macros and toggle LED
    if right.value:  
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