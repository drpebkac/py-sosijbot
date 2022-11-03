import requests
import json
import sys
import time
import re



class Post:
  def create_Body_Departures():
    print('placeholder')

  def create_Body_Arrivals():
    print('placeholder')

class Get:
  def getPilotData(pilot_data):
    pilot_data = pilot_data['pilots']
    return pilot_data

  def getControllerData(controller_data):
    controller_data = controller_data['controllers']
    return controller_data

class StartWorkFlow:
  def countDeps(pilot_data):
    print("")
  def countArrs(pilot_data):
    print("")


#Global variables
scopedairports = ["YSSY", "YBBN"]
exemptlist = ["SY_TWR", "SY_GND", "BN_TWR", "BN_GND"]
function_lock = 0

try:
  exempt_sid = str(sys.argv[1])
except:
  print("No exception defined for controller_cid. Assigning except_controller_cid id to default")
  exempt_sid = '0000000'

#Add pilot/controller CID to exemptlist for later use
exemptlist.append(exempt_sid)

#Entry point
while True:
  #If vatsim api temporary goes offline, the program breaks, include exception handling to avoid the bot from crashing
  while True:
    try:
      raw_vatdata = requests.get("https://data.vatsim.net/v3/vatsim-data.json")
      rawjson = json.loads(raw_vatdata.content)
      #This will only break out this loop, not the outter one
      break
    except:
      print("Vatsim API is temporary offline, retrying in 15 seconds")
      time.sleep(15.0)
  
  #Narrow down vatsim data and divide it between pilots and controllers alerts. Used for alerts
  pilot_data = Get.getPilotData(rawjson)
  controller_data = Get.getControllerData(rawjson)

  #Conditions to run alerts
  #If exempt CID is connected as pilot
  #Note this has nothing to do with the function mechanism for stopping the bot from spamming
  #This is only to stop notifying if the exempt CID is connected to VATSIM, or if one of the scopedairports are online
  for i in pilot_data:
    if str(i['cid']) == exemptlist:
      exempt_pilot_status = "online"
      break
    else:
      exempt_pilot_status = "offline"

  #If any of the scoped stations are online
  for a in controller_data :
    if a['callsign'] in exemptlist:
      exempt_station_status = "online"
      break
    else:
      exempt_station_status = "offline"

  # Begin composing notification when either scoped controllers and pilot CID is offline 
  # If both exempt status and function lock is 0, run if block and send notification
  # function_lock stops the bot from spamming every 15 seconds
  if exempt_station_status == "offline" and exempt_pilot_status == "offline":
    print("Calling notification mechanism")
    print(exempt_pilot_status)
    print(exempt_station_status)
  # If both exempt status is offline and function lock is 1, run if block and send notification
  elif exempt_station_status == "online" or exempt_pilot_status == "online":
    print("Hold off calling the notification classes")
    
  time.sleep(15.0)





