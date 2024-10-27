import network
import socket
import time
from machine import Pin
#from mysecrets import *

SSID = 'Suntrap'
PASSWORD="Finn&Freya1720"

# Replace with your Wi-Fi credentials and PC server IP
SERVER_IP = "192.168.1.19"  # Replace with your PC's IP address
SERVER_PORT = 12345
# 192.168.1.19
# 192.168.27.84

print("Starting Wi-Fi Connection...")

# Button pins
RIGHT_BUTTON_PIN = 19
RANDOM_BUTTON_PIN = 7
LEFT_BUTTON_PIN = 0
MUSIC_BUTTON_PIN = 2
CLAP_BUTTON_PIN = 16
WRONG_BUTTON_PIN = 17
#sensor_pin = machine.Pin(16, machine.Pin.IN)

# LED pins
LED1_PIN = 17
LED2_PIN = 14

# Initialize LEDs
led1 = Pin(LED1_PIN, Pin.OUT)
led2 = Pin(LED2_PIN, Pin.OUT)

def scan_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()  # Scans for available Wi-Fi networks

    print("\nAvailable Wi-Fi Networks:")
    for net in networks:
        ssid = net[0].decode()  # SSID is a byte object, decode to string
        rssi = net[3]  # Signal strength
        print(f"SSID: {ssid}, Signal Strength: {rssi} dBm")

    print()  # Blank line for readability

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)

    # Activate the WLAN interface if not already active
    if not wlan.active():
        print("Activating Wi-Fi interface...")
        wlan.active(True)
    else:
        print("Wi-Fi interface already active.")

    # Turn LED1 on to indicate Wi-Fi connection attempt
    led1.on()
    for color in COLORS:       
        color_chase(color, 0.04)

    # Scan and print available Wi-Fi networks
    scan_wifi()

    # If not connected, attempt connection
    if not wlan.isconnected():
        print(f'Attempting to connect to network: {SSID}')

        # Try connecting with the provided SSID and PASSWORD
        wlan.connect(SSID, PASSWORD)

        # Wait for connection with a timeout and print status
        timeout = 10  # seconds
        start_time = time.time()
        while not wlan.isconnected():
            elapsed_time = time.time() - start_time
            print(f'Connecting... {elapsed_time:.1f}s elapsed')

            # Check if timeout has been exceeded
            if elapsed_time > timeout:
                print(f'Failed to connect to Wi-Fi after {timeout} seconds. Check SSID/PASSWORD.')
                print('Current WLAN status:', wlan.status())  # Print status code
                rainbow_cycle(0)
                return False

            # Sleep for a second before checking again
            time.sleep(1)

    # Wi-Fi connected, print configuration
    print('Connected to Wi-Fi')
    print('Network configuration:', wlan.ifconfig())

    # Turn LED RING Orange to show almost successful connection
    pixels_fill(ORANGE)
    pixels_show()

    return True

def connect_server():
    addr = socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]
    s = socket.socket()

    try:
        s.connect(addr)
        print('Connected to server:', addr)
        pixels_fill(GREEN)
        pixels_show()

        # Flash LED2 to indicate server connection success
        led1.off()
        led2.off()
        for x in range(5):
            led2.on()
            time.sleep(0.2)
            led2.off()
            time.sleep(0.2)

        led2.on()
        return s

    except Exception as e:
        print(f'Failed to connect to server: {e}')

        # Flash LED1 to indicate failure to connect to the server
        led1.off()
        led2.off()
        for x in range(10):
            led1.on()
            time.sleep(1)
            led1.off()
            time.sleep(1)

        return None





# -------Lights-----------



# Example using PIO to drive a set of WS2812 LEDs.
 
import array, time
from machine import Pin
import rp2
 
# Configure the number of WS2812 LEDs.
NUM_LEDS = 16
PIN_NUM = 1
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

#------------------main

#--------------------------MAIN


def main():
    led1.off()
    led2.off()

    # LED1 on at start
    led1.on()
    time.sleep(2)

    # Attempt to connect to Wi-Fi
    if not connect_wifi():
        print("Wi-Fi connection failed. Exiting.")
        brightness = 0.9
        rainbow_cycle(0)
        return

    # Attempt to connect to the server
    s = connect_server()
    if not s:
        print("Server connection failed. Exiting.")
        rainbow_cycle(0)
        return

    # Initialize buttons
    right_button = Pin(RIGHT_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    random_button = Pin(RANDOM_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    left_button = Pin(LEFT_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    music_button = Pin(MUSIC_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    clap_button = Pin(CLAP_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    wrong_button = Pin(WRONG_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    
    

    try:
        while True:
            if right_button.value():
                print('Right button pressed')
                s.send(b'RIGHT\n')
                time.sleep(0.2)  # Debounce delay
                
                #color_chase(RED, 0.05)
                #pixels_fill(BLACK)
                #time.sleep(0.2)
            
                
            if random_button.value():
                print('Random button pressed')
                s.send(b'RANDOM\n')
                time.sleep(0.2)
                
                for x in range(3):
                    pixels_fill(RED)
                    pixels_show()
                    time.sleep(0.1)
                    
                    pixels_fill(WHITE)
                    pixels_show()
                    time.sleep(0.1)
                    
                pixels_fill(RED)
                pixels_show()
                                
                
            if left_button.value():
                print('Left button pressed')
                s.send(b'LEFT\n')
                time.sleep(0.2)
                
                pixels_fill(BLUE)
                pixels_show()
                time.sleep(0.2)
                
            if music_button.value():
                print('Music button pressed')
                s.send(b'MUSIC\n')
                time.sleep(0.2)
                
                pixels_fill(DARKRED)
                pixels_show()
                
            if clap_button.value():
                print('Clap button pressed')
                s.send(b'CLAP\n')
                
                pixels_fill(GREEN)
                pixels_show()
                time.sleep(0.5)
                color_chase(WHITE, 0.01)
                color_chase(CYAN, 0.01)
                color_chase(GREEN, 0.01)
                time.sleep(1)
                color_chase(BLACK, 0.01)
                
            if wrong_button.value():
                print('Wrong button pressed')
                s.send(b'WRONG\n')
                
                pixels_fill(RED)
                pixels_show()
                time.sleep(0.5)
                color_chase(WHITE, 0.01)
                color_chase(RED, 0.01)
                time.sleep(1)
                color_chase(BLACK, 0.01)
                
            time.sleep(0.1)
    except Exception as e:
        print(f'An error occurred during communication: {e}')
        rainbow_cycle(0)
    finally:
        s.close()
        print("Socket closed.")






main()
