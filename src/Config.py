
"""
This file is custom vars for the Program you can add Names vars to the name sectiom
"""
# sms sending info
SMSGATWAYEMAIL = str('hackercraftstudio@gmail.com')
SMSGATEWAYPASSWORD = str('CatFish123@')

NAME = str("[SecuServe Security System]")
ENDINGMESSAGE=str("By nicholas Blackburn")

NICKSPHONE=str('4123891615@vtext.com')
ETHANSPHONE=str('7249390029@messaging.sprintpcs.com')

# ADD Image Names and path vars
FILE_LOC = "/mnt/user/people/"
ETHAN_IMAGE =FILE_LOC+"ethan.jpg"
NICK_IMAGE = FILE_LOC+"nick.jpg"
ETHANS_MOM_IMAGE = FILE_LOC+"ethansMom.jpg"  
DR_DAN_IMAGE = FILE_LOC+"drDan.jpg"


'''
THis section is for adding new names to the system
to define names 
NAME_VAR = str("Persons Name")
'''
#uknown person 

UNRECONIZED= str("Unknown")
#Owners
ETHAN_WAGNER = str("Ethan Wagner")
NICHOLAS_BLACKBURN = str("Nicholas Blackburn")
# adults 
LAURA_WAGNER = str("Laura Wagner")
DR_DAN = str("Danial Wagner")

# Dont touch this is the rgb color Conversion for the Philips hue light
def rgb_to_xy(red, green, blue):
    """ conversion of RGB colors to CIE1931 XY colors
    Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
    Args: 
        red (float): a number between 0.0 and 1.0 representing red in the RGB space
        green (float): a number between 0.0 and 1.0 representing green in the RGB space
        blue (float): a number between 0.0 and 1.0 representing blue in the RGB space
    Returns:
        xy (list): x and y
    """

    # gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
    blue =  pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)

    # convert rgb to xyz
    x = red * 0.649926 + green * 0.103455 + blue * 0.197109
    y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    z = green * 0.053077 + blue * 1.035763

    # convert xyz to xy
    x = x / (x + y + z)
    y = y / (x + y + z)

    # TODO check color gamut if known
     
    return [x, y]

#Phillips Hue Lights Ip addr
HUE_IP = str('10.0.0.230')

#hue Color Pref
HUE_ALARM = rgb_to_xy(255,0,0)
HUE_AllGOOD= rgb_to_xy(0,255,0)
HUE_STARTUP = rgb_to_xy(0,0,255)


#ecrytion for privacey DO NOT CHANGE ANYTHING OR UR SCREWED
BLOCK_SIZE = 2556
PAD = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]
SALT  = b"this is a salt SUPER MUCH SALT times one billion"
ENCRYPITON_PASSWORD = 'L4xVTDwcEGWkAng7X9mKqdBP8hrfZtYvuzS2jyQUe6ps5FNb3C'




## Tokenifyer
IMAGE = 'image'
GROUP = 'group'
TIME = 'time'
NAME_TOKEN = 'name'
FACE = 'face'
OWNER_FACE = 'ownerface'
PARENT_FACE = 'parentface'
UNKNOWN_FACE = 'unknownface'
