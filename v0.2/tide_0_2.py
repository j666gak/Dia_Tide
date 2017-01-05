# -*- coding: utf-8 -*-
import requests
import json
import sys
import hashlib
import datetime
import pytz
import xlrd

# Class for Tidepool API
class Tidepool():
    API_URL = "https://api.tidepool.org/"
    UPLOAD_URL = "https://uploads.tidepool.org/"
    
    CBGdeviceId = None
    SMBGdeviceId = None

    timezone = pytz.timezone('Europe/London') # timezone

    # Generate unique upload ID for each upload session
    def gen_uploadId(self,deviceId):
        m = hashlib.md5()
        meta = deviceId + "_" + str(datetime.datetime.now())
        m.update(meta)
        self.uploadId = "upid_" + m.hexdigest()[0:12]
        return

    # Login to tidepool account
    def login(self,email,passd):
        r = requests.post(self.API_URL+"auth/login", auth=(email, passd))
        token = r.headers['x-tidepool-session-token']
        response = json.loads(r.text)
        self.userid = response['userid']
        self.token = token
        return

    # Refresh token
    def refresh(self):
        headers = {'x-tidepool-session-token':self.token}
        r = requests.get(self.API_URL+"auth/login",headers=headers)
        return

    # Get the group which the current user is assigned to
    def get_groups(self):
        headers = {'x-tidepool-session-token':self.token}
        r = requests.get(self.API_URL+"access/groups/%s"%self.userid,headers=headers)
        groups = json.loads(r.text)
        self.groups = groups
        return groups

    # Logout
    def logout(self):
        headers = {'x-tidepool-session-token':self.token}
        r = requests.post(self.API_URL+"auth/logout",headers=headers)
        return

    # Upload cbg data to tidepool
    # cbg is a list of tuple (date,glucose)
    def upload_cbg(self,cbg,group):
        assert self.CBGdeviceId is not None
        assert group in self.groups

        self.gen_uploadId(self.CBGdeviceId) # Generate new uploadId

        headers = {'x-tidepool-session-token':self.token,'Content-Type':'application/json'}

        for timestamp,glucose in cbg:
            deviceTime = timestamp.isoformat()  # Format time
    
            # Add UTC offset
            UTCtimestamp = self.timezone.localize(timestamp)
            tzoffset = int(UTCtimestamp.utcoffset().total_seconds()/60)

            # Create the data payload
            uploaddata = {
                "type": "cbg",
                "units": "mmol/L",
                "value": glucose,
                "clockDriftOffset": 0,
                "conversionOffset": 0,
                "deviceId": self.CBGdeviceId,
                "deviceTime": deviceTime,
                "time": UTCtimestamp.isoformat(),
                "timezoneOffset": tzoffset,
                "uploadId": self.uploadId
            }

            # Upload data
            print "Uploading..",deviceTime,glucose
            r = requests.post(self.UPLOAD_URL+"data",headers=headers,json=uploaddata)
        return

    # Upload smbg data to tidepool
    # smbg is a list of tuple (date,glucose)
    def upload_smbg(self,smbg,group):
        assert self.SMBGdeviceId is not None
        assert group in self.groups

        self.gen_uploadId(self.SMBGdeviceId) # Generate new uploadId

        headers = {'x-tidepool-session-token':self.token,'Content-Type':'application/json'}

        for timestamp,glucose in smbg:
            deviceTime = timestamp.isoformat()  # Format time
    
            # Add UTC offset
            UTCtimestamp = self.timezone.localize(timestamp)
            tzoffset = int(UTCtimestamp.utcoffset().total_seconds()/60)

            # Create the data payload
            uploaddata = {
                "type": "smbg",
                "subType": "manual",
                "units": "mmol/L",
                "value": glucose,
                "clockDriftOffset": 0,
                "conversionOffset": 0,
                "deviceId": self.CBGdeviceId,
                "deviceTime": deviceTime,
                "time": UTCtimestamp.isoformat(),
                "timezoneOffset": tzoffset,
                "uploadId": self.uploadId
            }

            # Upload data
            print "Uploading..",deviceTime,glucose
            r = requests.post(self.UPLOAD_URL+"data",headers=headers,json=uploaddata)
        return

# Function to convert Diasend timestamp to ISO
def parse_timestamp(timestamp):
    timestamp = datetime.datetime.strptime(timestamp,'%d/%m/%Y %H:%M')
    return timestamp

# Function to read smbg and cbg data from Diasend xls file
def load_workbook(filename):
    workbook = xlrd.open_workbook(filename)
    
    # Get smbg data from first tab
    sheet_smbg = workbook.sheet_by_index(0)
    Ndata = sheet_smbg.nrows

    smbg,cbg = [],[]

    for row in range(5,Ndata):
        timestamp = sheet_smbg.cell(row,0).value
        isotime   = parse_timestamp(timestamp)
        glucose   = sheet_smbg.cell(row,1).value
        smbg.append((isotime,glucose))

    # Get cbg data from second tab
    sheet_cbg = workbook.sheet_by_index(1)
    Ndata = sheet_cbg.nrows

    for row in range(2,Ndata):
        timestamp = sheet_cbg.cell(row,0).value
        isotime   = parse_timestamp(timestamp)
        glucose   = sheet_cbg.cell(row,1).value
        cbg.append((isotime,glucose))

    return smbg,cbg

# Main function starts here
def main():
    smbg,cbg = load_workbook("diasend.xls") # Extract data from xls file

    # Create tidepool instance and login
    tp = Tidepool()
    tp.login('your email','your password')

    # Set device ID
    tp.CBGdeviceId  = "device1" # Set device name for continuous blood glucose
    tp.SMBGdeviceId = "device2" # Set device name for self-monitored blood glucose

    # Select group ID
    groups = tp.get_groups()    # Get groups which the user belongs to
    group  = groups.keys()[0]   # Select first one (usually with root privilege)

    # Upload data
    tp.upload_cbg(cbg,group)
    tp.upload_smbg(smbg,group)

    tp.logout()

if __name__ == "__main__":
    main()
