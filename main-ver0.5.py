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
  def gatherDeps(pilot_data):
    print(pilot_data)
  def gatherArrs(pilot_data):
    print(pilot_data)




#Global variables
scopedairports = ["YSSY", "YBBN"]
exemptstations = ["SY_TWR", "SY_GND", "BN_TWR", "BN_GND"]

#Entry point
while True:
  try:
    exempt_sid = sys.argv[1]
  except:
    print("No exception defined for controller_cid. Assigning except_controller_cid id to default")
    exempt_sid = 000000

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
  pilot_data = Get.getControllerData(rawjson)
  controller_data = Get.getPilotData(rawjson)

  #Conditions to run alerts
  #If exempt CID is connected as pilot
  for i in pilot_data:
    if str(i['cid']) == exempt_sid:
      exempt_pilot_status = "online"
      break
    else:
      exempt_pilot_status = "offline"

  #If any of the scoped stations are online
  for a in controller_data :
    if a['callsign'] in exemptstations:
      exempt_station_status = "online"
      break
    else:
      exempt_station_status = "offline"

  # Begin composing notification when either scoped controllers and pilot CID is offline 
  if exempt_station_status == "offline" and exempt_pilot_status == "offline":
    # Get count of departures and arrival per airport
    ybbn_deps = StartWorkFlow.gatherDeps(pilot_data)
    yssy_deps = StartWorkFlow.gatherDeps(pilot_data)
    ybbn_arr = StartWorkFlow.gatherArrs(pilot_data)
    yssy_arr = StartWorkFlow.gatherArrs(pilot_data)
  else: 
    print("Scoped CIDs and stations are online, no notifications will be sent")

    
  time.sleep(15.0)





