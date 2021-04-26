"""
Class For Handling Dection and Processing of Captured Plates 
"""
import cv2

class PlateDection():

    '''
    Bulk Plate Prosessing Code
    '''
    def processPlate(self,videoCapture):
        frame = videoCapture.read()
        img = cv2.resize(frame,(620,480))
        