import sys
import requests
import json
import time
from threading import Thread
from datetime import datetime, timezone
from termcolor import colored
import calendar

availability = "http://api.coolkidmacho.com/droptime/"
redeem = "https://api.minecraftservices.com/productvoucher/"
create = "https://api.minecraftservices.com/minecraft/profile"
urls = [redeem] * 100
claimSuccess = False
snipeSuccess = False
delay = 0

def repeat(times, function, *args):
    for i in range(times): function(*args)

def isDropping(username):
	r = requests.get(availability + username)
	if ("list index out of range" in r.text):
		return False
	else:
		return True

def getAvailableTime(username):
	now = datetime.now()
	r = requests.get(availability + username)
	jsonText = json.loads(r.text)
	snipe_time = jsonText["UNIX"]
	snipe_time = datetime.fromtimestamp(int(snipe_time))
	wait_time = snipe_time - now
	return wait_time

def bearerIsValid(token):
	headers = {
		"Accept": "application/json",
		"Authorization": "Bearer " + token
	}
	try:
		r = requests.post(create, headers=headers)
		if (r.status_code == 401 or r.status_code == 500):
			return False
		else:
			return True
	except ConnectionError:
		sys.exit("Connection error.")

def createAccount(username, token, dropTime):
	headers = {
		"Accept": "application/json",
		"Authorization": "Bearer " + token
	}

	body = {
		"profileName": username
	}
	
	try:
		r = requests.post(create, data=json.dumps(body), headers=headers)
		time = r.elapsed.total_seconds()
		print(colored("RECV @ ", 'magenta') + str(datetime.utcnow()) + " [+" + str(time) + "]")
		if (r.status_code == 200):
			print(colored("[200]", 'green') + " Profile has been created.")
			snipeSuccess = True
		elif (r.status_code == 400):
			if ("ALREADY_REGISTERED" in r.text):
				print(colored("[400]", 'red') + " Microsoft account already has a Minecraft profile.")
			elif ("DUPLICATE" in r.text):
				print(colored("[400]", 'red') + " Name taken.")
			elif ("NOT_ALLOWED" in r.text):
				print(colored("[400]", 'red') + " Name blocked.")
			elif ("CONSTRAINT_VIOLATION" in r.text):
				print(colored("[400]", 'red') + " Name invalid.")
			elif ("NOT_ENTITLED" in r.text):
				print(colored("[400]", 'red') + " Giftcard failed.")
			else:
				print("[400] ???")
		elif (r.status_code == 401):
			print(colored("[401]", 'red') + " Your bearer token expired.")
		elif (r.status_code == 429):
			print(colored("[429]", 'red') + " Rate limited.")
		elif (r.status_code == 500):
			print(colored("[500]", 'red') + " API Overloaded.")
		else:
			print(colored("[???]", 'red') + " idk what happened tbh")
	except requests.exceptions.ConnectionError:
		print(colored("[500]", 'red') + " Connection error.")

if __name__ == '__main__':
	thread_list = []
	username = input(colored("What name do you want to snipe?: ", 'green'))
	
	if (isDropping(username)):
		token = input(colored("What is the Microsoft Bearer Token?: ", 'green'))
		
		if (bearerIsValid(token)):
			
			userDelay = input(colored("What is your delay? (in ms): ", 'green'))
			delay = int(userDelay)
			gc =input(colored("What is the giftcard code?: ", 'green'))
			
			wait = getAvailableTime(username)
			days = wait.days
			hours = wait.seconds//3600
			minutes = (wait.seconds//60)%60
			seconds = wait.seconds - hours*3600 - minutes*60
			microseconds = wait.microseconds
			ms = microseconds * 1000
			wait_string = f"{days} day(s), {hours} hour(s), {minutes} minute(s), {seconds} second(s)"
			
			ttl = float(str(wait.seconds + (86400 * wait.days)))
			delay = delay / 1000.0
			
			print("Sniping " + colored(username, 'blue') + " on giftcard " + colored(gc, 'blue') + " in " + colored(str(wait_string), 'blue') + ".")
			print("Using a delay of " + colored(str(delay), 'blue') + " second(s).")
			
			time.sleep(ttl - delay)
			
			claimSuccess = True
			if (claimSuccess == True):
				for i in range(6):
					print(colored("SENT @ ", 'green') + str(datetime.utcnow()))
					createAccount(username, token, wait)
					time.sleep(0.01)
				if (snipeSuccess == True):
					print("Snipe was successful.")
				else:
					print("Snipe failed.")
			else:
				sys.exit("An error occured. Snipe canceled.")
		else:
			sys.exit("Invalid bearer token.")
	else:
		sys.exit("That name is not dropping.")
