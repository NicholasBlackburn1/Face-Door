"""
Class For Handling Dection and Processing of Captured Plates 
"""

import cv2
import numpy
import pytesseract
import imutils
class PlateDection():

    '''
    Bulk Plate Prosessing Code
    '''
    def processPlate(self,videoCapture):
    img = cv2.imread('text.jpg',cv2.IMREAD_COLOR)
    img = imutils.resize(img, width=500 )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
        # find contours from the edged image and keep only the largest
    # ones, and initialize our screen contour
    cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1=img.copy()
    cv2.drawContours(img1,cnts,-1,(0,255,0),3)
    #sorts contours based on minimum area 30 and ignores the ones below that
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
    screenCnt = None #will store the number plate contour
    img2 = img.copy()
    cv2.drawContours(img2,cnts,-1,(0,255,0),3) 
    count=0
        
    idx=7
    # loop over contours
    for c in cnts:
    # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if len(approx) == 4: #chooses contours with 4 corners
                    screenCnt = approx
                    x,y,w,h = cv2.boundingRect(c) #finds co-ordinates of the plate
                    new_img=img[y:y+h,x:x+w]
                    cv2.imwrite('./'+str(idx)+'.png',new_img) #stores the new image
                    idx+=1
                    break
                
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)
    text=pytesseract.image_to_string(Cropped_loc,lang='eng') #converts image characters to string
    cv2.imwrite('./'+str(idx)+'.png',img) #stores the new image
    print("Number is:" ,text)
    cv2.imshow("img1",img1)
    cv2.imshow("img2",img2) #top 30 contours
    cv2.imshow("cropped",cv2.imread(Cropped_loc)) 
    cv2.imshow("Final image with plate detected",img)
    cv2.waitKey(0)