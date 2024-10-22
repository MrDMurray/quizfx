import time
import machine
import bluetooth
from micropython import const
from machine import Pin

# Constants for GATT
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)

# UUIDs for our custom service and characteristic
_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

# Create a BLE object
ble = bluetooth.BLE()
ble.active(True)

# Callback for BLE events
def ble_irq(event, data):
    if event == _IRQ_CENTRAL_CONNECT:
        conn_handle, _, _ = data
        print("Connected")
    elif event == _IRQ_CENTRAL_DISCONNECT:
        conn_handle, _, _ = data
        print("Disconnected")
        advertise()

# Function to build advertising payload manually
def encode_name(name):
    return bytes((len(name) + 1, 0x09)) + bytes(name, 'utf-8')

def advertise():
    name = 'PicoW_Clicker'
    adv_data = b"\x02\x01\x06" + encode_name(name)  # Flags and device name
    ble.gap_advertise(100, adv_data)

# Register GATT services manually
def setup_ble():
    ble.irq(ble_irq)
    
    # Register the service and characteristic
    service = (_SERVICE_UUID, ((_CHAR_UUID, bluetooth.FLAG_NOTIFY),))
    
    # Register the service and return the service handle (ignoring returned characteristic handle structure)
    handles = ble.gatts_register_services([service])
    
    # Debugging output to inspect the structure of handles
    print("Handles structure:", handles)
    
    # In this case, we'll assume characteristic handle is manually managed
    characteristic_handle = 1  # Assuming first characteristic is handle 1 (you may need to adjust)
    print("Manually assigned characteristic handle:", characteristic_handle)

    return characteristic_handle

# Setup Bluetooth and get characteristic handle
char_handle = setup_ble()

if char_handle is not None:
    advertise()

# Initialize buttons
right_button = Pin(19, Pin.IN, Pin.PULL_DOWN)
random_button = Pin(7, Pin.IN, Pin.PULL_DOWN)
left_button = Pin(0, Pin.IN, Pin.PULL_DOWN)

# Main loop
while char_handle:
    if right_button.value():
        print("Right button pressed")
        ble.gatts_notify(0, char_handle, b'RIGHT')  # Manually use handle 1
        time.sleep(0.2)
    if random_button.value():
        print("Random button pressed")
        ble.gatts_notify(0, char_handle, b'RANDOM')  # Manually use handle 1
        time.sleep(0.2)
    if left_button.value():
        print("Left button pressed")
        ble.gatts_notify(0, char_handle, b'LEFT')  # Manually use handle 1
        time.sleep(0.2)
    time.sleep(0.1)
