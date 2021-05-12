"""
this class is for handling full Messaging capabilitys for Notifing the user during import situations in program
TODO: Get Custom Textbelt Gateway to work so i dont have to charge users to use this program
"""
import requests
import logging

default_endpoint ='https://textbelt.com/text'

# this Sends and checks to see if the endpoint works
def checkEndpoint(phoneNum,apikey):
    phone = str("'")+str(phoneNum)+str("'")
    key = str(apikey)
    resp = requests.post('https://textbelt.com/text', {
    'phone': phone,
    'message': 'Hello world This is A Test Message from SecuServe UwU',
    'key': key,
    })
    
    print(resp.json()['success'])
    logging.info("Responce from Textbelt"+ "  "+ "Enpoint Checking  "+" "+"Was Sent"+"  "+ str(resp.json()['success']))

# this is for handling sending all the messages UwU
def _message(endpoint,apikey,phoneNum,message):

    phone = str("'")+str(phoneNum)+str("'")
    key = apikey
    msg = str(message)
    resp = requests.post(endpoint, {
    'phone': phone,
    'message': msg,
    'key': key,
    })
    logging.warn("Responce from Textbelt"+ "  "+ str(message)+" "+"Was Sent"+"  "+ str(resp.json()['success']))
    print("Responce from Textbelt"+ "  "+ str(message)+" "+"Was Sent"+"  "+ str(resp.json()['success']))
  
    # if the custom endpoint fails, Use Default one
    if(resp.json()['success'] == False):
        logging.warn("Faild to send message via the first endpoint now sending it with the Default one")
        phone = str("'")+str(phoneNum)+str("'")
        key = str(apikey)
        msg = str(message)
        resp = requests.post(default_endpoint, {
        'phone': phone,
        'message': msg,
        'key': key,
        })
        logging.info("Responce from Textbelt"+ "  "+ str(message)+" "+"Was Sent"+"  "+ str(resp.json()['success']))
   

    


# Sends life threating Info
def sendWarnMessage(message,phoneNum):
    _message(default_endpoint,'apikey',phoneNum,"[SECU-SERVE]"+ str(" ")+"WARNING! WARNING! WARNING!"+str("  ")+str(message))



# Sends Warning threating Info
def sendMessage(message,phoneNum):
    _message(default_endpoint,'apikey',phoneNum,"[SECU-SERVE]"+str("  ")+str(message))


def sendCapturedImageMessage(message,phoneNum,url):
    _message(default_endpoint,'9922bca307918d04d792c1203234ee40a7bb393bfaGlsn8KKkjGL9Tp1b2zJZwJi',phoneNum,"[SECU-SERVE-CAPUTURED]"+str("  ")+str(message)+" "+str(url))
