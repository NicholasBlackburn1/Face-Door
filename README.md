# SecuServe Security System

**An Facial Reconition Security System written in python and opencv on an Jetson Nano**

![example]()

## What was my Inspiration for this project

This Project is An competitor For the Ring Door bell System OwO. The ring Door Bell System costs 10$ a month so i Desided I could do a Better version

## What does this project accomplish

This Project uses Computer Vision to Recognize authorized individuals and allow them to enter our Studio. This Facial Reconition powered Security System comes complete with push notifications to alert you that here is some one at the door, A Read Only File System to protect the jetson nano in case of a power outage, video capture of unauthorized individuals and Images taken of the authorized and non authorized individuals for safety sake.

## Features

<li> Sends Sms messages based on the person who is recognized</li>
<li> able to be easily Started and Stopped on a Read Only os</li>
<li> Uses realtime Facial recognition to Recognize Authorized users and the non authorized Users</li>
<li> Unlocks/ Locks  Door and Sounds alarm </li>
<li> Added Philips Hue Support for Visually Displaying if a Known person is here or not </li>
<li> added an flask webPage for displaying system data to user easily and securily </li>
<li> secure login for data security and privacy </li>
<li> Easy Web enterface to see data and to add more users  to the facial reconitions </li>
<li> respond to groups of recognized people with one unrecognized person so we don't have False alarms </li>

## Todo's
<li> watchdog for handleing door control </li>
<li> Audio Greeting for a Single User. </li>
<li> Enable Landline Calling from security system </li>




## IMPORTANT INFO ABOUT FACE IMAGES
**please use a non skin color background for the face images  that your going to Upload**



## Opencv User Color Code  for Detected Faces

1. <span style="color:#00FF00">Admin Green</span> this color is only used for indicating Detected Admin Users.

2. <span style="color:#00FFFF">User Blue</span> this color is only used for indicating detected non Admin users

3. <span style="color:#FFB000">Unwated Orange</span> this color is only used for Displaying detected Banned Users.

4.  <span style="color:#FF00FF">Group Purple </span> this color is only used for Displaying a detected group of people. 


5.  <span style="color:#FF0000">Death Red </span> this color is only used for Displaying when a unreconized person shows up
## P.S 
### Please fork me and or help with development
