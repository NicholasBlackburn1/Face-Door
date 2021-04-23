"""
this class is for handling full Messaging capabilitys for Notifing the user during import situations in program
TODO: Finish Image Sending Function from mms gateway hehe
"""

from email.header import Header
from email.mime.text import MIMEText
import smtplib
import logging
import pathlib
import imghdr





# Sends Email to sms Gateway
def sendMessageToClient(logging,usrnumber,message,smsconfig):
    
    try:
        logging.info("starting to connect to server network")

        #Connects to gmail and sends hello ping
        server = smtplib.SMTP('smtp.gmail.com', 587)
        logging.info(server.ehlo())

        if(server.ehlo() is not None):
            server.starttls()
            server.login(smsconfig['gatwayemail'], smsconfig['gatewaypass'])
            server.sendmail(smsconfig['sendername'], str(usrnumber)+smsconfig['gatewayOutEmail'], str(message)+smsconfig['endingmessage'])
            logging.warn("Sent Email to"+usrnumber)
            server.close()
            logging.info("Closed connection to email server email sent UWU")
            return
    except:
        logging.warning("Could not send email!!!!! maby check address?")
        return


