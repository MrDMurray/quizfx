import network
import socket
import time
from machine import Pin
from mysecrets import *

# Replace with your Wi-Fi credentials and PC server IP
#SSID = 'Your Network Name'   # in secrets py file
#PASSWORD = 'your_wifi_password' # in secrets py file
SERVER_IP = "192.168.1.19"  # Replace with your PC's IP address
SERVER_PORT = 12345

# Button pins
RIGHT_BUTTON_PIN = 19
RANDOM_BUTTON_PIN = 7
LEFT_BUTTON_PIN = 0

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(SSID, PASSWORD)
        # Wait for connection with a timeout
        timeout = 10  # seconds
        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                print('Failed to connect to Wi-Fi')
                return False
            time.sleep(1)
    print('Network configuration:', wlan.ifconfig())
    return True

def connect_server():
    addr = socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]
    s = socket.socket()
    try:
        s.connect(addr)
        print('Connected to server')
        return s
    except Exception as e:
        print('Failed to connect to server:', e)
        return None

def main():
    if not connect_wifi():
        return

    s = connect_server()
    if not s:
        return

    # Initialize buttons
    right_button = Pin(RIGHT_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    random_button = Pin(RANDOM_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
    left_button = Pin(LEFT_BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

    try:
        while True:
            if right_button.value():
                print('Right button pressed')
                s.send('RIGHT\n')
                time.sleep(0.2)  # Debounce delay
            if random_button.value():
                print('Random button pressed')
                s.send('RANDOM\n')
                time.sleep(0.2)
            if left_button.value():
                print('Left button pressed')
                s.send('LEFT\n')
                time.sleep(0.2)
            time.sleep(0.1)
    except Exception as e:
        print('An error occurred:', e)
    finally:
        s.close()

main()
