"""
this class is for handling full Messaging capabilitys for Notifing the user during import situations in program
TODO: Get Custom Textbelt Gateway to work so i dont have to charge users to use this program
"""
import requests
import logging



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

    


