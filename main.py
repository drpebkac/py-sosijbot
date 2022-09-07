import json
import requests
import sys
import time
import re

def create_Body_Departures():

  if lengthdepyssy >= 5 and functionstatus_1 != 1:
    jsoncontent = {
      "username": "SosijBot",
      "content": "<" + sys.argv[1] + ">  there are currently " + str(lengthdepyssy) + " departures at YSSY",
      "embeds": [
        {
          "fields": [
            {
              "name": "Flight detail summary",
              "value": str(webhookout_yssyfl)
            }
          ],
          "title": "First in line"
        }
      ]
    }

  if lengthdepybbn >= 5 and functionstatus_3 != 1:
    jsoncontent = {
      "username": "SosijBot",
      "content": "<" + sys.argv[1] + "> there are currently " + str(lengthdepybbn) + " departures at YBBN",
      "embeds": [
        {
          "fields": [
            {
              "name": "Flight detail summary",
              "value": str(webhookout_yssyfl)
            }
          ],
          "title": "First in line"
        }
      ]
    }

  requests.post(discord_weburi, json = jsoncontent)

def create_Body_Arrivals():

  if lengtharryssy >= 5 and functionstatus_2 != 1:
    jsoncontent = {
      "username": "SosijBot",
      "content": "<" + sys.argv[1] + "> there are currently " + str(lengtharryssy) + " arrivals at YSSY"
    }

  if lengtharrybbn >= 5 and functionstatus_4 != 1:
    jsoncontent = {
      "username": "SosijBot",
      "content": "<" + sys.argv[1] + "> there are currently " + str(lengtharrybbn) + " arrivals at YBBN"
    }
  
  requests.post(discord_weburi, json = jsoncontent)

#################################################################################

#Discord webhook
discord_weburi = sys.argv[1]

# Vatsim API
rawpilot_vatdata = requests.get("https://data.vatsim.net/v3/vatsim-data.json")
pilotresults = json.loads(rawpilot_vatdata.content)['pilots']
controllerresults = json.loads(rawpilot_vatdata.content)['controllers']

#Airport to scope
scopedairports = ["YSSY", "YBBN"]

# Used as variable declaration to trigger webhook function because Python is retarded
functionstatus_1 = None
functionstatus_2 = None
functionstatus_3 = None
functionstatus_4 = None

while True:

  #Declare airport departures for Sydney arrays. Use for count
  yssy_dep = []
  yssy_arr = []
  array_yssydeptimes = []
  array_yssydepcids = []

  #Declare airport departures for Brissy arrays. Use for count
  ybbn_dep = []
  ybbn_arr = []
  array_ybbndeptimes = []
  array_ybbndepcids = []

  firstinline_yssy_array = []
  firstinline_ybbn_array = []

  # EDDDYYYYYYY
  # Do not run webhook if Eddy is online
  exemptcid = sys.argv[2]
  exemptstations = ["SY_TWR", "SY_GND", "BN_TWR", "BN_GND"]

  for i in pilotresults:
    if exemptcid == str(i['cid']):
      eddy_pilot = "online"
      break
    else:
      eddy_pilot = "offline"

  # Rescoped for any controllers
  for i in controllerresults:
    if i['callsign'] in exemptstations or exemptcid == str(i['cid']):
      controller = "online"
      break
    else:
      controller = "offline"

  print(eddy_pilot)
  print(controller)

  #Gather departures and arrivals
  for i in pilotresults:
    if i['flight_plan'] is not None:
      flightplan = i['flight_plan']
      pilotcid = str(i['cid'])
      dep = flightplan['departure']
      arr = flightplan['arrival']

      #Would be nice if you can use +=
      #Iterate array for dep and arr for count 
      for airport in scopedairports:
        if re.search(airport, dep):
          if airport == "YSSY":
            yssy_dep.append(dep)
            array_yssydepcids.append(pilotcid)
          if airport == "YBBN":
            ybbn_dep.append(dep)
            array_ybbndepcids.append(pilotcid)

        if re.search(airport, arr):   
          if airport == "YSSY":
            yssy_arr.append(arr)
          if airport == "YBBN":
            ybbn_arr.append(arr)

  #Gather pilot first in line info for YSSY
  for i in pilotresults:
    if i['flight_plan'] is not None:
      pilotcid = str(i['cid'])
      flightplan = i['flight_plan']
      deptime = str(flightplan['deptime'])
      
      #Fetch and append dep and arr time
      for x in array_yssydepcids:
        if(re.search(pilotcid, x)):
          firstinline_yssy_array.append(deptime)
      for x in array_ybbndepcids:
        if(re.search(pilotcid, x)):
          firstinline_ybbn_array.append(deptime)

  #Sort departure time array by acssending
  firstinline_ybbn_array = sorted(firstinline_ybbn_array)
  firstinline_yssy_array = sorted(firstinline_yssy_array)

  try:
    firstinline_ybbn = str(firstinline_ybbn_array[0])
  except:
    firstinline_ybbn = False

  try:
    firstinline_yssy = str(firstinline_yssy_array[0])
  except:
    firstinline_yssy = False
  
  # Fetch flight data of first in line pilot CID
  for i in pilotresults:
    if i['flight_plan'] is not None:
      pilotcid = str(i['cid'])
      flightplan = i['flight_plan']
      deptime = str(flightplan['deptime'])
      callsign = i['callsign']
      dep = flightplan['departure']

      if pilotcid in array_yssydepcids:
        if(re.search(deptime, firstinline_yssy)):
          webhookout_yssycallsign = callsign
          webhookout_yssydeptime = deptime
          webhookout_yssyfl = flightplan
          webhookout_dep = dep
      if pilotcid in array_ybbndepcids:
        #for x in firstinline_ybbn:
        if(re.search(deptime, firstinline_ybbn)):
          webhookout_ybbncallsign = callsign
          webhookout_ybbndeptime = deptime
          webhookout_ybbnfl = flightplan
          webhookout_dep = dep

  # If Eddy is online, dont run function
  if eddy_pilot != "online" and controller != "online":
    lengthdepyssy = len(yssy_dep)
    lengtharryssy = len(yssy_arr)
    lengthdepybbn = len(ybbn_dep)
    lengtharrybbn = len(ybbn_arr)

    if lengthdepyssy >= 5 and functionstatus_1 != 1:
      print("There are " + str(lengthdepyssy) + " departures in YSSY")
      create_Body_Departures()
      #Reset variable so it doesnt parse in the next if block
      functionstatus_1 = 1
    elif lengthdepyssy < 5:
      functionstatus_1 = None
    
    if lengtharryssy >= 5 and functionstatus_2 != 1:
      print("There are " + str(lengtharryssy) + " arrivals in YSSY")
      create_Body_Arrivals()
      #Reset variable so it doesnt parse in the next if block
      functionstatus_2 = 1
    elif lengtharryssy < 5:
      functionstatus_2 = None

    if lengthdepybbn >= 5 and functionstatus_3 != 1:
      print("There are " + str(lengthdepybbn) + " departures in YBBN")
      create_Body_Departures()
      #Reset variable so it doesnt parse in the next if block
      functionstatus_3 = 1
    elif lengthdepybbn < 5:
      functionstatus_3 = None
    
    if lengtharrybbn >= 5 and functionstatus_4 != 1:
      print("There are " + str(lengtharrybbn) + " arrivals in YBBN")
      create_Body_Arrivals()
      #Reset variable so it doesnt parse in the next if block
      functionstatus_4 = 1
    elif lengtharrybbn < 5:
      functionstatus_4 = None
    
  time.sleep(15.0)
