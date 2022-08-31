import json
import requests
import time
import re

rawvatdata = requests.get("https://data.vatsim.net/v3/vatsim-data.json")

outputtojson = json.loads(rawvatdata.content)

results = outputtojson['pilots']

#airport departures arrays
yssydep = []
ybbndep = []

#airport departures arrays
yssyarr = []
ybbnarr = []

#Gather departures and arrivals
for i in results:
  if i['flight_plan'] is not None:
    flightplan = i['flight_plan']
    dep = flightplan['departure']
    arr = flightplan['arrival']

    #Would be nice if you can use +=
    if re.search('YBBN', dep):
      ybbndep.append(dep)
    
    if re.search('YBBN', arr):
      ybbnarr.append(arr)

    if re.search('YSSY', dep):
      yssydep.append(dep)
    
    if re.search('YSSY', arr):
      yssyarr.append(arr)
      






print(ybbndep)
print(ybbnarr)
print(yssydep)
print(yssyarr)

      
    


      

    

  


#with open('data.json', 'w') as file:
#  json.dump(outputtojson, file)


