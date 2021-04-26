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

        # Resizes Images and coverts it to grzay
        img = cv2.resize(frame,(620,480))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # bluring iamge for easy Proessign 
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)

        # cannys Edges 
        edged = cv2.Canny(filtered, 30, 200)

        # Finds COntors
        nts = cv2.findContours(edged.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        