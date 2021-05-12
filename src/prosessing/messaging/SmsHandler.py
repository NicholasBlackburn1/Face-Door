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

    phone = str(phoneNum)
    msg = str(message)
    apikey = str(apikey)
    print("textbelt request:"+"   "+ phone+ "   "+ msg+ "  "+ apikey)

    resp = requests.post(endpoint, {
    'phone': phone,
    'message': msg,
    'key': apikey,
    })
    logging.warn("Responce from Textbelt"+ "  "+ str(message)+" "+"Was Sent"+"  "+ str(resp.json()['success']))
    print("Responce from Textbelt"+ "  "+ str(message)+" "+"Was Sent"+"  "+ str(resp.json()['success'])+ "   "+"textid:"+str(resp.json()['textId']+"\n"))
  
    # if the custom endpoint fails, Use Default one
    if(resp.json()['success'] == False):
        logging.warn("Faild to send message via the first endpoint now sending it with the Default one")
        print("textbelt request:"+"   "+ phone+ "   "+ msg+ "  "+ apikey)

        phone = str(phoneNum)
        msg = str(message)
        apikey =str(apikey)
        resp = requests.post('https://textbelt.com/text', {
        'phone': phone,
        'message': msg,
        'key': apikey,
        })
        print("Responce from Textbelt"+ "  "+ str(message)+" "+"Was Sent"+"  "+ str(resp.json()['success'])+ "   "+ "error:"+"  "+str(resp.json()['error']))
        logging.info("Responce from Textbelt"+ "  "+ str(message)+" "+"Was Sent"+"  "+ str(resp.json()['success'])+ "   "+ "error:"+"  "+str(resp.json()['error']))
   

    


# Sends life threating Info
def sendWarnMessage(message,phoneNum):
    _message(default_endpoint,'apikey',phoneNum,"[SECU-SERVE]"+ str(" ")+"WARNING! WARNING! WARNING!"+str("  ")+str(message))



# Sends Warning threating Info
def sendMessage(message,phoneNum):
    _message(default_endpoint,'apikey',phoneNum,"[SECU-SERVE]"+str("  ")+str(message))


def sendCapturedImageMessage(message,phoneNum,url,api):
    _message(default_endpoint,apikey=api,phoneNum=phoneNum,message="[SECU-SERVE-CAPUTURED]"+str("  ")+str(message)+" "+str(url))

