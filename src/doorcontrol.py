import gpiozero
from gpiozero.pins.data import GPIO11, GPIO4

door = gpiozero.LED(GPIO4)
alarm = gpiozero.LED(GPIO11)

def setup():
    #sets up pins 
    door.on()
    print("door state" + door.values())
    alarm.on()
    print("alarm state" + alarm.values())
        
        
def doorControl(): 
    door.toggle()
    print("doorState" + door.values())

def alarmControl():
    alarm.toggle()
    print("alarm State"+ alarm.values())