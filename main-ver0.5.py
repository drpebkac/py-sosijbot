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

class WorkFlow:
  def checkExemptBeforeWorkFlow(pilot_data, controller_data):
    #Check conditions to run alerts
    #If exempt CID is connected as pilot
    #Note this has nothing to do with the function mechanism for stopping the bot from spamming
    #This is only to stop notifying if the exempt CID is connected to VATSIM, or if one of the scopedairports are online
    for i in pilot_data:
      if str(i['cid']) in exemptlist:
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

    if exempt_station_status == "offline" and exempt_pilot_status == "offline":
      WorkFlow.countDeops()

    elif exempt_station_status == "online" or exempt_pilot_status == "online":
      print("Hold off calling the notification classes")






  def countDeps(pilot_data):


      #I'd be damned if this actually works lol. Wrapping a class method in a fucking list array 
      #for airport in scopedairports:
        #if airport is 'YSSY':
          #yssy_dep = [WorkFlow.countDeps(pilot_data, airport)]
          #yssy_arr = [WorkFlow.countArrs(pilot_data, airport)]
    #elif airport is 'YBBN':
    #ybbn_dep = [WorkFlow.countDeps(pilot_data, airport)]
    #ybbn_arr = [WorkFlow.countArrs(pilot_data, airport)]
    for i in pilot_data:
      if i['flight_plan'] is not None:
        flightplan = i['flight_plan']
        cid = str(i['cid'])
        dep = flightplan['departure']








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

  WorkFlow.checkExemptBeforeWorkFlow(pilot_data, controller_data)

  time.sleep(15.0)





