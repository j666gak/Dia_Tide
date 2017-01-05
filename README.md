# Dia_Tide
A Python script to convert Diasend export and upload in to Tidepool.org
 <p>
## Full Description
Over the past number of years I have accumalated a number of different blood testing meters, and each one requires it own software to download results. Then Diasend.com (used by various hospitals) have a portal that includes and Uploader including driver for most Blood Glucose Meters, which makes it extremely useful however the graphs and analysis tools (in my personal opinion) could use some improvement. At this point I came across an Opensource project Tidepool.org which among other things have good analytic and graph capabilities, but currently limited to only two specific BGM's. Therefore this script is to bridge the gap between the number of devices that Diasend can communicate with, and the analytical capabilities of Tidepool.
 <p>
 I hope you find this as useful as I have.
 <p>
 Special thanks to tk2 from Freelancer.com who worked on this project (code) with me.

## Configuration
* Your export from Diasend.com must be named diasend.xls and stored in the same folder as as tide_0_2.py
* On line 169 of tide_0_2.py you need to replace text with the email address and password you have created for Tidepool
* Optional - Line 172 / 173 text can be edited before uploading to add a device name for either your BGM or CGM
<p>
- Static Configuration
Timezone = Europe/London
Units = mmol/L

## Sucessfuly Tested On
O/S = Windows 8 <p>
Python = 2.7 <p>
Diasend format = 5th Jan 2017 <p>

## Terms & Conditions
Script is used at own risk, including but no limited to data and computer system. No support/updates/communication are implied or intended. The script MUST not be used in any commercial or business capacity.
