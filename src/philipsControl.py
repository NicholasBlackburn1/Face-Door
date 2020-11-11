"""
This python class controls philips hue Led 
for visual of Security system
"""
from logging import log
import Config
import logging

logging.basicConfig(filename="/mnt/user/hue.log", level=logging.DEBUG)

def setup(brige):
    logging.warn("Setting up Hue")
    
   

    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    brige.connect()

    # Get the bridge state (This returns the full dictionary that you can explore)
    brige.get_api()
    
    
def breakin(bridge):
    logging.warn("Warning Evil Light on.. Someone is Breaking in!")

    # sets color of Lights 
    lights = bridge.get_light_objects()
    lights.xy = Config.HUE_ALARM
    
    logging.info("Checking to see if light is on")
    if(bridge.get_light(1, 'on')):
         logging.info("Light is on!!!! I Work yess")
    else:
        logging.critical("Light is not on trueining it on")
        # Set brightness of lamp 1 to max
        bridge.set_light(1, 'bri', 254)

def allgood(bridge):
    logging.warning("all good bros no one here to kill u\n")
    lights = bridge.get_light_objects()
    lights.xy = Config.HUE_AllGOOD
    
    logging.info("Checking to see if light is on")
    if(bridge.get_light(1, 'on')):
         logging.info("Light is on!!!! I Work yess")
    else:
        logging.critical("Light is not on trueining it on")
        # Set brightness of lamp 1 to max
        bridge.set_light(1, 'bri', 254)
        
def lightsoff(bridge):

    logging.warning("lights are on turning off\n")
    
    logging.info("Checking to see if light is on")
    if(bridge.get_light(1, 'on')):
         logging.info("Light is on!!!! Shutting off")
         bridge.set_light(1, 'bri', 0)
    else: 
        logging.warning("lights are off keeping them off")
    
    
    