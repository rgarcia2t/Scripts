# default arguments values
# error cases (a missing argument, a wrong type, a file not found...)
# document all arguments and options
# progress bar for waiting time
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import sys
import webbrowser
from terminaltables import AsciiTable
import logging
import time
import pytz
from pytz import timezone
import datetime
from datetime import datetime


print ('Number of arguments: ', len(sys.argv), ' arguments.')
print ('Argument List: ', str(sys.argv))
args = str(sys.argv).replace("[","").replace("]","")

evname=""
minmag=""
maxmag=""
faulttype=""
startdate=""
enddate=""
orderby=""
format=""
minlat=""
maxlat=""
minlon=""
maxlon=""
lat=""
lon=""
rad=""
country=""
state=""
check = "no"
help = ""

for word in args[12:].split():	  # 12 can change, depend on the name of the file
	# print(word)

	# ev:PineHills
	if "ev" in word:
		# print("Found Earthquake Name")
		evname = word.split(":")[1].replace("'","").replace(",","")
		# print(evname)
	
	# mag1:0-10000000000
	if "mag1" in word:
		# print("Found Magnitude")
		mag = word.split(":")[1].replace("'","").replace(",","")
		minmag = mag.split("-")[0]
		maxmag = mag.split("-")[1]
		# print(mag)
		# print(minmag)
		# print(maxmag)
	
	# type:normal
	if "type" in word:
		# print("Found Fault Type")
		ftype = word.split(":")[1].replace("'","").replace(",","")
		faulttype = ""
		if(ftype.find("normal") != -1):
			faulttype += ",NM"
		if(ftype.find("reverse") != -1):
			faulttype += ",RS"
		if(ftype.find("strike") != -1):
			faulttype += ",SS"
		faulttype = faulttype[1:]
		# print(faulttype)
	
	# date:1995-09-12,2000-08-01
	if "date" in word:
		# print("Found time")
		date = word.split(":")[1].replace("'","")
		startdate = date.split(",")[0]
		enddate = date.split(",")[1]
		# print(startdate)
		# print(enddate)

	# order:time-asc
	if "order" in word:
		# print("Found Order By")
		orderby = word.split(":")[1].replace("'","").replace(",","")
		# print(orderby)
	
	# format:json
	if "format" in word:
		# print("Found Format")
		format = word.split(":")[1].replace("'","").replace(",","")	 
		# print(format)
	
	# coordinates:lat:1-10,lon:1-11
	if "coordinates" in word:
		lat1 = word.split(":")[2].split(",")[0]
		minlat = lat1.split("-")[0]
		maxlat = lat1.split("-")[1]
		lon1 = word.split(":")[3].replace("'","")
		minlon = lon1.split("-")[0]
		maxlon = lon1.split("-")[1]
		# print(minlat)
		# print(maxlat)
		# print(minlon)
		# print(maxlon)
	
	# circle:lat:1,lon:2,rad:3
	if "circle" in word:
		lat = word.split(":")[2].split(",")[0]
		lon = word.split(":")[3].split(",")[0]
		rad = word.split(":")[4].replace("'","")
		# print(lat)
		# print(lon)
		# print(rad)

	# country:British-Vrigin-Island,state:CA
	if "country" in word:
		country = word.split(":")[1].split(",")[0].replace("'","").replace("-"," ")
		print(country)
		if "state" in word: 
			state = word.split(",")[1].split(":")[1].replace("'","")
			# print(state)

	# eventid:nc73184841
	if "eventid" in word:
		eventid = word.split(":")[1].replace("'","").replace(",","")
		# print(eventid)
	
	# help
	if "help" in word:
		help = "yes"

URL = "https://strongmotioncenter.org/testuser/wserv2/events/query"

if(args.find("eventid") != -1):
	# use eventid to generate data
	PARMS = {'eventid':eventid, 'format':format, 'orderby':orderby}
	r=requests.get(url = URL, params = PARMS)
	if format == "json":
		with open('tests.json', 'w') as f1:
			f1.write(str(r.text))
		print("Generated data and saved it as local file (tests.json)")
		with open('tests.json') as f2:
			for line in f2:
				if line.find("count") != -1:
					check = "yes"
					break  
	else:
		with open('tests.xml', 'w') as f1:
			f1.write(str(r.text))
		print("Generated data and saved it as local file (tests.xml)")
		with open('tests.xml') as f2:
			for line in f2:
				if line.find("count") != -1:
					check = "yes"
					break 
else:
	# use parameters to generate data
	# PARMS = {'evname': evname, 'minmag': minmag, 'maxmag': maxmag, 'faulttype': faulttype, 'startdate':startdate, 'enddate': enddate, 'orderby':orderby, 'format':format, 'minlat':minlat, 'maxlat':maxlat, 'minlon': minlon, 'maxlon':maxlon, 'lat':lat, 'lon': lon, 'rad': rad, 'country':country, 'state':state}
	PARMS = {'orderby': orderby, 'format': format}
	if evname != "":
		PARMS['evname']=evname
	# else:
	# 	print("Please enter evname")
	if minmag != "":
		PARMS['minmag']=minmag
	# else:
	# 	print("Please enter minmag")
	if maxmag != "":
		PARMS['maxmag']=maxmag
	# else:
	# 	print("Please enter maxmag")
	if faulttype != "":
		PARMS['faulttype']=faulttype
	# else:
	# 	print("Please enter faulttype")
	if startdate != "":
		PARMS['startdate']=startdate
	# else:
	# 	print("Please enter startdate")
	if enddate != "":
		PARMS['enddate']=enddate
	# else:
	# 	print("Please enter enddate")
	if minlat != "":
		PARMS['minlat']=minlat
	# else:
	# 	print("Please enter minlat")
	if maxlat != "":
		PARMS['maxlat']=maxlat
	# else:
	# 	print("Please enter maxlat")
	if minlon != "":
		PARMS['minlon']=minlon
	# else:
	# 	print("Please enter minlon")
	if maxlon !="":
		PARMS['maxlon']=maxlon
	# else:
	# 	print("Please enter maxlon")
	if lat !="":
		PARMS['lat']=lat
	# else:	
	# 	print("Please enter lat")
	if lon !="":
		PARMS['lon']=lon
	if rad != "":
		PARMS['rad']=rad
	# else:
	# 	print("Please enter rad")
	if country != "":
		PARMS['country']=country
	# else:
	# 	print("Please enter country")
	if state != "":
		PARMS['state']=state
	# else:
	# 	print("Please enter state")
	r=requests.get(url = URL, params = PARMS)
	print(PARMS)
	if format == "json":
		with open('tests.json', 'w') as f1:
			f1.write(str(r.text))
		print("Generated data and saved it as local file (tests.json)")
		with open('tests.json') as f2:
			for line in f2:
				if line.find("count") != -1:
					check = "yes"
					break 
		with open('tests.json') as f3:
			for line in f3:
				if line.find("url") != -1:
					print(line.replace(" ","").replace(",",""))
					break
	elif format == "xml":
		with open('tests.xml', 'w') as f1:
			f1.write(str(r.text))
		print("Generated data and saved it as local file (tests.xml)")
		with open('tests.xml') as f2:
			for line in f2:
				if line.find("description") != -1:
					check = "yes"
					break  
		with open('tests.xml') as f3:
			for line in f3:
				if line.find("url") != -1:
					print(line.replace(" ","").replace(",",""))
					break
	elif format =="csv":
		# csv
		URL = 'https://strongmotioncenter.org/testuser/wserv2/events/query?'
		count = 0
		print(PARMS)
		for i in str(PARMS):
			if i == ':':
				count += 1
		for j in range(count):
			dic = PARMS.popitem()
			key = str(dic).split("'")[1].replace("'","").replace(" ","").replace("(","").replace(")","")
			value = str(dic).split("'")[3].replace("'","").replace(" ","").replace("(","").replace(")","")
			if(j!=0):
				URL += '&'
			URL = URL + key + '=' + value
		URL += "&nodata=404"
		print(URL)
		webbrowser.open(url=URL)

if((format == "" or orderby == "") or (evname=="" and minmag=="" and maxmag=="" and faulttype=="" and startdate=="" and enddate=="" and minlat=="" and maxlat=="" and minlon=="" and maxlon=="" and lat=="" and lon=="" and rad=="" and country=="" and state=="")):
  print("\n")
  print("Error: Should contain format and orderby and atleast one of the following parameters: \n")
  print("evname | minmag | maxmag | faulttype | startdate | enddate | minlat | maxlat | minlon | maxlon | lat | lon | rad | country | state | ")
  #sys.exit()

		
if check == "no" and (format == "xml" or format == "json") and help == "":
	print("usage: python teste.py [options]")
	print("\n*********** Recommended Parameters [options] Below **********")
	print("[arg_name] for an optional value")
	print("ev ------ Earthquake Name\t\t[earthquakeName]")
	print("mag1 ------ Magnitude\t\t[min-max]")
	print("type ------ Fault Type\t\t[normal/reverse/strike/normal,reverse/normal,strike/normal,reverse,strike]")
	print("date ------ Date/Time\t\t[yyyy-mm-dd,yyyy-mm-dd]")
	print("order ------ Order By\t\t[time/time-asc/magnitude/magnitude-asc]")
	print("format ------ Format\t\t[json/xml/csv]")
	print("coordinates ------ Coordinates\t\tcoordinates:lat:1-10,lon1-11")
	print("\tlat ------ Latitude\t\t[min-max]")
	print("\tlon ------ Longitude\t\t[min-max]")
	print("circle ------ Circle\t\tcircle:lat:1,lon:2,rad:3")
	print("\tlat ------ Latitude\t\t[num]")
	print("\tlon ------ Longitude\t\t[num]")
	print("\trad ------ Radius\t\t[num]")
	print("country ------ Country\t\t[countryName]")
	print("\tstate ------ State\t\t[stateName]")
	print("eventid ------ EventID\t\t[eventid]")
	print("\n************* Examples Below ***************")
	print("python tests.py mag:0-1000 orderby:time format:json date:2019-05-29,2019-05-31")


if(help != ""):
	print("helping instruction")
	data = [['parameter','description'],["country","Country of event epicenter."],["enddate","Latest origin time (in UTC) to include in search. Format: yyyy-mm-dd hh:mm:ss"],["eventid","Preferred USGS event ID of earthquake (including network code). For example, an event ID of 37904927 and a network code of CI would be appended as CI37904927. Multiple event IDs can be listed as CI37904927,CI38043999."],["evname","Name of event. Names typically contain a city or vicinity to the epicenter. Accepts wildcards."],["faulttype","Faulting type. Options are NM(normal), RS(reverse), SS(strike-slip)."],["format","Format of output. Options are xml, json, or csv."],["lat","For radius searches, latitude in degrees of the center."],["lon","For radius searches, longitude in degrees of the center."],["maxlat","Maximum latitude, inclusive upper bound of search range for latitude."],["maxlon","Maximum longitude, inclusive upper bound of search range for longitude."],["minlat", "Minimum latitude, inclusive lower bound of search range for latitude."],["minlon","Minimum longitude, inclusive lower bound of search range for longitude."],["maxmag","Maximum magnitude, inclusive upper bound of search range for magnitude (Mw, Ml, Md, Mb, or Ms)."],["minmag","Minimum magnitude, inclusive lower bound of search range for magnitude (Mw, Ml, Md, Mb, or Ms)."],["nodata","If no data is returned by the service, return a 404 response rather than the default 204."],["orderby","Order of data output. Options are time(time descending), time-asc(time ascending), magnitude(magnitude descending), or magnitude-asc(magnitude ascending)."], ["rad","For radius searches, distance in kilometers from the center."], ["startdate","Earliest origin time (in UTC) to include in search. Format: yyyy-mm-dd hh:mm:ss"], ["state","State, province, territory, or prefecture of epicenter (when available)."]]

	table = AsciiTable(data)
	print(table.table)

tme = time.localtime()
timeString = time.strftime("%m/%d/%Y %I:%M:%S", tme)

date_format='%m/%d/%Y %H:%M:%S %Z'
date = datetime.now(tz=pytz.utc)
date = date.astimezone(timezone('US/Pacific'))


f = open("timestamp.txt", 'w')
#f.write("PARAMETERS ENTERED \nevname: " + evname + '\nminmag: ' + minmag + '\nmaxmag: ' + maxmag + '\nfaulttype: ' + faulttype + '\nstartdate: ' + startdate + '\nenddate: ' + enddate + '\nminlat: ' + minlat + '\nmaxlat: ' + maxlat +  '\nminlon: ' + minlon + '\nmaxlon: ' + maxlon + '\nlat: ' + lat + '\nlon: ' + lon + '\nrad: ' + rad + '\ncountry: ' + country + '\nstate: ' + state +  '\nformat: ' + format + '\n' + "This is event was logged on " + date.strftime(date_format))
f.write("Parameters entered: \n" + str(PARMS) + "\n" + date.strftime(date_format))

f.close()

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.warning('is when this event was logged.')
input("Press Enter to continue...")
