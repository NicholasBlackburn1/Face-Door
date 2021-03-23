

"""
Hanles the User Messaging and Notification System for the Backend of the SecuServe Program
"""

class MessageHandler(object):
    # Sends a sms message with a Message to the user 
    def sendSms(server,message,logger,name,user,):
        logger.warn(message)
        server.sendmail(name, user , Config.NAME + " " +
                        message + "  " + Config.ENDINGMESSAGE)
        
    # Sends Image with a Sms Message 
    def sendSmsWithImage(server,message,logger,name,user,imageURL):
        logger.warn(message)
        server.sendmail(name, user , Config.NAME + " " +
                        message + "  " +imageURL+"  "+ Config.ENDINGMESSAGE)
        