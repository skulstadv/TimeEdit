#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import sys 
import time
import datetime
import requests
import random
from pyvirtualdisplay import Display 
from selenium import webdriver 

# Help function, called when there are invalid arguments

def help():
	print '\nUsage: python TimeEdit.py -u -p -r -s -e\nSends a curl request to using [-u] username, [-p] password, [-r] room, [-s] start-time, [-e] end-time\n\t-u\tYour feide username\n\t-p\tYour feide password\n\t-r\tRoom number [A266, A267, A268, A269, A270]\n\t-s\tStart-time\n\t-e\tEnd-time\n\tExample: python TimeEdit.py user password A266 08:00 18:00\n' 
	return

# Grab logincookie using selenium with chrome webdriver  (phantomjs does not work)
def create_cookie(username, password):
	display = Display(visible=0, size=(800,600)) 
	display.start() 
	driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver") 
	driver.get("https://no.timeedit.net/web/hig/db1/timeedit/sso/feide?back=https%3A%2F%2Fno.timeedit.net%2Fweb%2Fhig%2Fdb1%2Fstudent%2F") 
	search_box = driver.find_element_by_id('username') 
	search_box.send_keys(username) 
	search_box = driver.find_element_by_id('password') 
	search_box.send_keys(password) 
	search_box.submit() 
	all_cookies = driver.get_cookies() 
	all_cookies = str(all_cookies) 

	cookie = all_cookies[70:]	# The cookie we want is at pos 70 - first occurence of ' 
	cookie = cookie[0:cookie.find("'")] 
	driver.quit() 
	return cookie

# Get the right room ID from room number. 
def  get_room_ID(room):
	room_ID = [300]			# Array with ID's with ID of room Axxx at index xxx
	for i in range(0,300):
		room_ID.append(0)
	room_ID[266] = "162176"
	room_ID[267] = "162177"
	room_ID[268] = "162178"
	room_ID[269] = "162179"
	room_ID[270] = "162180"
	room_ID[300] = '161930'
	room = str(room_ID[int(room[1:4])]) + '.185'
	return room

# Create data dictionary to pass along with request. First arg is days ahead in time
# @start_time and @end_time is in format MMHH
def create_data_dict(name_reservation, days_ahead, room, start_time, end_time):
	date = datetime.date.today() + datetime.timedelta(days=days_ahead)
	date = '20' + str(date.strftime('%y%m%d'))
	data = {
	'fe49' : name_reservation,
	'fe50' : name_reservation + '@stud.ntnu.no',
	'id' : '-1',
	'dates' : date,
	'datesEnd' : date,
	'startTime' : start_time,
	'endTime' : end_time,
	'o' : room,
	'url' : 'https%3A%2F%2Fno.timeedit.net%2Fweb%2Fhig%2Fdb1%2Fstudent%2Fr.html%3Fh%3Dt%26sid%3D5%26id%3D-1%26step%3D2%26id%3D-'
	+ '1%26dates%3D' + date + '%26datesEnd%3D' + date + '%26startTime%3D8%253A00%26endTime%3D22%253A00%26o%3D' + 
	room + '%252C10%252C%2BA' + room + '%252C%2Bgrupperom',
	'kind' : 'reserve'}
	return data
	
help()
# Renaming som runtime arguments for readability
username = sys.argv[1]
password = sys.argv[2]
room = sys.argv[3]
start_time = sys.argv[4]
end_time = sys.argv[5]
# Create cookie from arg1 (username) and arg2 (password)
cookie = create_cookie(username, password)
# Get the room id from arg3
room = get_room_ID(room)
# Create the data field of the request
data = create_data_dict(username, 15, room, start_time, end_time)

# URL is static
url = 'https://no.timeedit.net/web/hig/db1/student/r.html?h=t&sid=5&id=-1&step=2&id=-1&dates=20170219&datesEnd=20170219&startTime=11%3A00&endTime=11%3A05&o=162177.185%2C8%2C+A267%2C+grupperom&nocache=3'

# Include cookie in headers along with user agent (dont want the website to think we are a bot)
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
, 'cookie':  'sso-parameters=back=https%3A%2F%2Fno.timeedit.net%2Fweb%2Fhig%2Fdb1%2Fstudent%2Fr.html%3Fh%3Dt%26sid%3D5%26id%3D-1&ssoserver=feide; TEwebhigdb1=' + cookie}

# Putting it all together in the request
r = requests.post(url = url, headers = headers, data = data)
answer = r.text.encode('UTF-8')
i = 0
while ("innenfor dato- og klokkeslettgrensene" in answer):
	r = requests.post(url = url, headers = headers, data = data)
	answer = r.text.encode('UTF-8')
	i += 1
	print 'It isnt past midnight yet, trying again...'
print answer
