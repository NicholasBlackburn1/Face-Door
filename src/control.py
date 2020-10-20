import gpiozero as gpio
from gpiozero.pins.data import GPIO17, GPIO4

Door = gpio.OutputDevice(GPIO4)
Alarm = gpio.OutputDevice(GPIO17)

# Setups Pins
def setup():
    Alarm.on()
    Door.on()
    Door._write(1)
    Alarm._write(1)
    
def doorControl():
    if(Door.)
