"""
this class is for handling full Messaging capabilitys for Notifing the user during import situations in program
"""

from email.header import Header
from email.mime.text import MIMEText
import smtplib
import logging
import pathlib
import ConfigParser
import imghdr


PATH = str(pathlib.Path().absolute())+"/src/prosessing/"+"Config.ini"
config_object = ConfigParser()
config_object.read(PATH)

smsconfig = config_object["SMS"]


# CHecks to see of server responds
def checkEmailGatewayStatus(logging):
    try:
        # Sends An hello world message to email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        logging.info(server.ehlo())
        if(server.ehlo() is not None):
            server.close()
            return True
    except:
        logging.info('Something went wrong...')


# Sends mms message with images for user
def addImageToEmail(file,msg,usrnumber,messagefromprogram):
    # Header of email
    msg['From'] = smsconfig['sendername']
    msg['To'] = str(usrnumber)+smsconfig['gatewayOutEmail']
    msg['Subject'] = Header('Server Info' + smsconfig['sendername']).encode()

    # attache a MIMEText object to save email content
    msg_content = MIMEText(messagefromprogram, 'plain', 'utf-8')
    msg.attach(msg_content)
    # to add an attachment is just add a MIMEBase object to read a picture locally.
    
    with open(file, 'rb') as fp:
        img_data = fp.read()
        msg.add_attachment(img_data, maintype='image',subtype=imghdr.what(None, img_data))



# Sends Email to sms Gateway
def sendMessageToClient(logging,usrnumber,message):
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


