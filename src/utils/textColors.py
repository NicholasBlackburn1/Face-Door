"""
Simple Debuging Colorizer for the console uwu
"""

from colorama import init, Fore, Back, Style



def Debug(text):
    print(Fore.LIGHTWHITE_EX+str(text))
    print(Style.RESET_ALL)
    return



def Warning(text):
    print(Fore.YELLOW+str(text))
    print(Style.RESET_ALL)
    return


def Error(text):
    print(Fore.RED+str(text))
    print(Style.RESET_ALL)
    return

def PipeLine_Ok(text):
    print(Fore.GREEN+str(text))
    print(Style.RESET_ALL)
    return

def PipeLine_init(text):
    print(Fore.LIGHTBLUE_EX + str(text))
    print(Style.RESET_ALL)
    return

def PipeLine_Data(text):
    print(Fore.LIGHTMAGENTA_EX + str(text))
    print(Style.RESET_ALL)
    return