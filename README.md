# Face-Door
**An Auto Unlocking Door written in python and opencv on an Pi**


![example](https://github.com/NicholasBlackburn1/Face-Door/blob/main/example1.jpg)


## What was my Inspiration for this project 
This Project is for Ethan and I's Studio because we needed an security system and we really did not want to pay for one, So we decided to create one with Wireless cameras, Raspi, siren, two 600 pound electric magnetic  lock and a 8 port relay board. 


## What does this project accomplish
This Project uses Computer Vision to Recognize authorized individuals and allow them to enter our Studio. This Raspi powered Security System comes complete with push notifications to alert you that here is some one at the door, A Read Only File System to protect the py in case of a power outage, video capture of unauthorized individuals and Images taken of the authorized and non authorized individuals for safety sake. 

## Features 
<li> Sends Sms ethan and sends us messages based on the person who is recognized</li>
<li> able to be easily Started and Stopped on a Read Only os

## Todo's 

<li> get webserver to serve up the images taken by cv on a seperate thread </li>
<li> get the opencv to respond to groups of recognized people with one unrecognized person so we don't have False alarms </li>
