import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import socket
import threading
from time import sleep

HOST = '192.168.0.23'  # Standard loopback interface address (localhost)
PORT = 65432           # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# GPIO.setup("P9_27", GPIO.IN)
ADC.setup()
PHOTO_RESISTOR_INSTRUCTION = "DOWN"
POTENTIOMETER_BELOW_CENTER_INSTRUCTION = "RIGHT"
POTENTIOMETER_ABOVE_CENTER_INSTRUCTION = "LEFT"
BUTTON_INSTRUCTION = "UP"
POTENTIOMETER_CHANGE = ADC.read("P9_38")
PHOTO_RESISTOR_CHANGE = ADC.read("P9_33")


def send_instruction(instruction):
    s.sendall(instruction)


def check_photo_resistor():
    global PHOTO_RESISTOR_CHANGE
    photo_resistor = ADC.read("P9_33")
    diff = abs(photo_resistor - PHOTO_RESISTOR_CHANGE)
    print("Photoresistor: {}".format(photo_resistor))
    if diff > 0.02:
        if photo_resistor < 0.05:
            print(PHOTO_RESISTOR_INSTRUCTION)
            send_instruction(PHOTO_RESISTOR_INSTRUCTION)
        PHOTO_RESISTOR_CHANGE = photo_resistor
    else:
        pass


def check_potentiometer():
    global POTENTIOMETER_CHANGE
    potentiometer = ADC.read("P9_38")
    diff = abs(potentiometer - POTENTIOMETER_CHANGE)
    print("Potentiometer: {}".format(potentiometer))
    if diff > 0.3:
        if potentiometer < 0.5:
            print(POTENTIOMETER_BELOW_CENTER_INSTRUCTION)
            send_instruction(POTENTIOMETER_BELOW_CENTER_INSTRUCTION)
        else:
            print(POTENTIOMETER_ABOVE_CENTER_INSTRUCTION)
            send_instruction(POTENTIOMETER_ABOVE_CENTER_INSTRUCTION)
        POTENTIOMETER_CHANGE = potentiometer
    else:
        pass


while True:
    photo_thread = threading.Thread(target=check_photo_resistor)
    potentiometer_thread = threading.Thread(target=check_potentiometer)
    photo_thread.start()
    potentiometer_thread.start()
    sleep(0.5)
