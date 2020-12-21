# SecuServe Security System

**An Auto Unlocking Door written in python and opencv on an Pi**

![example](https://cdn.discordapp.com/attachments/671837506651815956/778615885605765160/SecuServe_Logo_Design_1.png)

## What was my Inspiration for this project

This Project is for Ethan and I's Studio because we needed an security system and we really did not want to pay for one, So we decided to create one with Wireless cameras, Raspi, siren, two 600 pound electric magnetic lock and a 8 port relay board.

## What does this project accomplish

This Project uses Computer Vision to Recognize authorized individuals and allow them to enter our Studio. This Raspi powered Security System comes complete with push notifications to alert you that here is some one at the door, A Read Only File System to protect the py in case of a power outage, video capture of unauthorized individuals and Images taken of the authorized and non authorized individuals for safety sake.

## Features

<li> Sends Sms ethan and sends us messages based on the person who is recognized</li>
<li> able to be easily Started and Stopped on a Read Only os</li>
<li> Uses realtime Facial recognition to Recognize Authorized users and the non authorized Users</li>
<li> Uses GPIO control to control 2 big Electromagnet </li>
<li> Added Philips Hue Support for Visually Displaying if a Known person is here or not </li>
<li> added an flask onepager for displaying system data to user easly and securily </li>
<li> secure login for data security and privacy </li>
<li> Easy Web enterface to see data and to add more users  to the facial reconitions </li>

## Todo's
<li> get the opencv to respond to groups of recognized people with one unrecognized person so we don't have False alarms </li>
<li> get data to dynamically populate the webpage without the user refreshing the page</li>
<li> watchdog for handleing door control for raspi </li>
<li> Writing config data from webpage and saving it & displaying it on webpage </li>


## IMPORTANT INFO ABOUT FACES
<li> please use a non skin color background for the face image that your going to train</li>

## P.S 
### Please fork me
