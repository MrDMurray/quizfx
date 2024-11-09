import network
import socket
import time
import random
from machine import Pin
#from mysecrets import *


# Button pins
WHITE_BUTTON_PIN = 19
BRIGHTER_BUTTON_PIN = 0
DARKER_BUTTON_PIN = 7
RANDO_BUTTON_PIN = 2
CLAP_BUTTON_PIN = 16
OFF_BUTTON_PIN = 17
#sensor_pin = machine.Pin(16, machine.Pin.IN)

# LED pins
LED1_PIN = 17
LED2_PIN = 14

# Initialize LEDs
led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)

# -------Lights-----------



# Example using PIO to drive a set of WS2812 LEDs.
 
import array, time
from machine import Pin
import rp2
 
# Configure the number of WS2812 LEDs.
NUM_LEDS = 18
PIN_NUM = 1
global brightness
brightness = 0.2 #0.2
 
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()
 
 
# Create the StateMachine with the ws2812 program, outputting on pin
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(PIN_NUM))
 
# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)
 
# Display a pattern on the LEDs via an array of LED RGB values.
ar = array.array("I", [0 for _ in range(NUM_LEDS)])
 
##########################################################################
def pixels_show():
    dimmer_ar = array.array("I", [0 for _ in range(NUM_LEDS)])
    for i,c in enumerate(ar):
        r = int(((c >> 8) & 0xFF) * brightness)
        g = int(((c >> 16) & 0xFF) * brightness)
        b = int((c & 0xFF) * brightness)
        dimmer_ar[i] = (g<<16) + (r<<8) + b
    sm.put(dimmer_ar, 8)
    time.sleep_ms(10)
 
def pixels_set(i, color):
    ar[i] = (color[1]<<16) + (color[0]<<8) + color[2]
 
def pixels_fill(color):
    for i in range(len(ar)):
        pixels_set(i, color)
 
def color_chase(color, wait):
    for i in range(NUM_LEDS):
        pixels_set(i, color)
        time.sleep(wait)
        pixels_show()
    time.sleep(0.2)
 
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)
 
 
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            pixels_set(i, wheel(rc_index & 255))
        pixels_show()
        time.sleep(wait)
 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (150, 30, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
ORANGE = (255, 68, 51)
COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)

"""
print("fills")
for color in COLORS:       
    pixels_fill(color)
    pixels_show()
    time.sleep(0.2)
 
print("chases")
for color in COLORS:       
    color_chase(color, 0.01)
 
print("rainbow")
rainbow_cycle(0)
"""


#--------------------------MAIN


def main():
    
    global brightness


    # Initialize buttons
    white_button = Pin(WHITE_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    brighter_button = Pin(BRIGHTER_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    darker_button = Pin(DARKER_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    rando_button = Pin(RANDO_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    disco_button = Pin(CLAP_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    off_button = Pin(OFF_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    
    pixels_fill(BLACK)
    pixels_show()
    brightness = 0
    for lums in range(100):
        brightness = brightness + 0.002
        print(brightness)
        pixels_fill(WHITE)
        pixels_show()
        time.sleep(0.01)

    try:
        while True:
            
            
            
            if white_button.value():
                print('White button pressed')
                pixels_fill(WHITE)
                pixels_show()
            
                
            if brighter_button.value():
                print('Brighter button pressed')

                if brightness <=1 and brightness >0.05:
                    brightness = brightness + 0.05
                    print(brightness)
                    pixels_show()
                    time.sleep(0.3)
                else:
                    print("Brtightness Maxed out!")
                    pixels_fill(WHITE)
                    pixels_show()
                    time.sleep(.3)
                    pixels_fill(BLACK)
                    pixels_show()
                    time.sleep(.3)
                    pixels_fill(WHITE)
                    pixels_show()
                                
                
            if darker_button.value():
                print('Darker button pressed')

                brightness = brightness - 0.05
                print(brightness)
                pixels_show()
                time.sleep(0.3)
                

                
            if rando_button.value():
                print('Rando button pressed')
                
                # show a random colour
                randomIndex = random.randint(0, len(COLORS)-1)
                # Getting the element present at the above index from the tuple
                randomItem = COLORS[randomIndex]
                pixels_fill(randomItem)
                pixels_show()
                time.sleep(0.2)
                
            if disco_button.value():
                print('Disco button pressed')
                
                pixels_fill(GREEN)
                pixels_show()
                time.sleep(0.5)
                color_chase(WHITE, 0.01)
                color_chase(CYAN, 0.01)
                color_chase(GREEN, 0.01)
                color_chase(RED, 0.01)
                color_chase(YELLOW, 0.01)
                color_chase(PURPLE, 0.01)
                time.sleep(1)
                color_chase(BLACK, 0.01)
                color_chase(YELLOW, 0.01)
                color_chase(RED, 0.01)
                color_chase(YELLOW, 0.01)
                color_chase(RED, 0.01)
                color_chase(BLACK, 0.01)
                
                print("rainbow")
                rainbow_cycle(0)
                color_chase(BLACK, 0.01)
                
                # COLORS = (BLACK, RED, YELLOW, GREEN, CYAN, BLUE, PURPLE, WHITE)
                
            if off_button.value():
                print('Off button pressed')
                brightness = 0.2
                
                color_chase(BLACK, 0.01)
                pixels_fill(BLACK)
                pixels_show()
                
            time.sleep(0.1)
            
    except Exception as e:
        print(f'An error occurred during communication: {e}')
        rainbow_cycle(0)
    finally:
        s.close()
        print("Socket closed.")






main()
