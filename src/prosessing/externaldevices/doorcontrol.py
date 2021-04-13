
"""
Relay control
Relays need to be tide to ground to enable and 5v to disengage relays
"""
import RPI.GPIO as gpio

gpio.setmode(gpio.RPI)

door_pin =  4
alarm_pin = 13
def setup():
      #sets up pins mode 
    gpio.setup(door_pin,gpio.OUT)
    gpio.setup(alarm_pin,gpio.OUT)
    
    # Sets all  pins High to not accentally enable door locks or alarm 
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
    
    
