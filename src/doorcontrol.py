"""
Controls the Door Using GPIO pins on the pi 
"""
import RPI.GPIO as gpio

gpio.setmode(gpio.RPI)

door_pin =  4
alarm_pin = 13

# maps the state of pins to output 
gpio.setup(door_pin,gpio.OUT)
gpio.setup(alarm_pin,gpio.OUT)

def setup():
    #sets up pins 
    gpio.output(door_pin, gpio.HIGH)
    gpio.output(alarm_pin, gpio.HIGH)
        
        
def doorClose(): 
    gpio.output(door_pin, gpio.HIGH)
    
def doorOpen(): 
    gpio.output(door_pin, gpio.LOW)


def alarmOn():
    gpio.output(alarm_pin, gpio.LOW)
    
def alarmOff():
    gpio.output(alarm_pin, gpio.HIGH)
    
    