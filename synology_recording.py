#!/usr/bin/python3
import sys
import requests
import json

#SYNOLOGY_CAM_ID 2 == frond door.
#SYNOLOGY_CAM_ID 1 == garden.

#example execution to start recording for camId nr 2. 
#	"python synology_recording.py record_start 2"
# or to stop the same camera id
# 	"python3 synology_recording.py record_stop 2"

SYNOLOGY_USER_NAME = "cameraGast"				      # your login code to access surveilance station
SYNOLOGY_PASSWORD = "your_secret_password"		# and here the password. 
SYNOLOGY_CAM_ID = "2"							            # the camera ID that you want to control
IP_ADDRESS = "192.168.178.222"    				    # your Synology NAS ip address
PORT = "5000"                     				    # the port used by Synology DiskStation Manager

#below there is nothing you need / change
PROTOCOL = "http"
API_PATH = "/webapi/"
BASE_URL = PROTOCOL + "://" + IP_ADDRESS + ":" + PORT + API_PATH
API_AUTH_FILE = "auth.cgi"
API_CAMERA_FILE = "entry.cgi"

CAM_MODE = sys.argv[1]
SYNOLOGY_CAM_ID = sys.argv[2]

AUTH_PAYLOAD = {'api': 'SYNO.API.Auth', 'version': '2', 'session': 'SurveillanceStation'}
LOGIN_PAYLOAD = {'method': 'Login', 'account': SYNOLOGY_USER_NAME, 'passwd': SYNOLOGY_PASSWORD, 'format': 'cookie'}
LOGIN_PAYLOAD.update(AUTH_PAYLOAD)
LOGOUT_PAYLOAD = {'method': 'Logout'}
LOGOUT_PAYLOAD.update(AUTH_PAYLOAD)
	
if CAM_MODE == "record_start":
    ACTION_PAYLOAD = {'api': 'SYNO.SurveillanceStation.ExternalRecording', 'method': 'Record', 'version': '1', 'cameraId': SYNOLOGY_CAM_ID, 'action': 'start','on': 'true'}	
if CAM_MODE == "record_stop":
    ACTION_PAYLOAD = {'api': 'SYNO.SurveillanceStation.ExternalRecording', 'method': 'Record', 'version': '1', 'cameraId': SYNOLOGY_CAM_ID, 'action': 'stop','on': 'true'}	
	
session = requests.session()

login = session.get(BASE_URL + API_AUTH_FILE, params=LOGIN_PAYLOAD, timeout=5)
action = session.get(BASE_URL + API_CAMERA_FILE, params=ACTION_PAYLOAD, timeout=5)
logout = session.get(BASE_URL + API_AUTH_FILE, params=LOGOUT_PAYLOAD, timeout=5)

session.close()
print(action.text)    
