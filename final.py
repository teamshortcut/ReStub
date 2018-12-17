#import libraries
import time
import picamera
import RPi.GPIO as GPIO
import requests

#declare variables
LOCALE = 'en-US' #locale for use with API
LANGUAGE = 'en-US' #language for use with API
URL = 'http://api.cloudsightapi.com/image_responses/' #url for use with the GET request to the API

name = "" #empty variables that will later be used to store the name and categories of the API's response
categories = ""

header = {
		'Authorization' : 'CloudSight meSNWQPE7LZ_ybXLMlDflA' #authorization header for use with the API
	}

#declare functions
def flashOn(num): #flashes the LED on, with paramater for which GPIO port it uses
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(num, GPIO.OUT)
    GPIO.output(num, True)

def flashOff(num): #flashes the LED off, with paramater for which GPIO port it uses
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(num, GPIO.OUT)
    GPIO.output(num, False)

def end(success):
	if success == True:
		flashOn(6) #whatever green LED number is
        	time.sleep(5)
        	flashOff(6)
	else:
		flashOn(7) #whatever red LED number is
        	time.sleep(5)
        	flashOff(7)

def postRequest(): #sends the post request to the API, sending the image. Will return a token.
	global URL #lets the variable URL be used outside of this function.
	URL = 'http://api.cloudsightapi.com/image_responses/' #makes sure URL is reset
	print("Here we go again...")
	imageFile = {'image_request[image]': ('image.jpg', open('image.jpg', 'rb'), 'image/jpg')} #assigns the image to send to a variable
	print(imageFile)
	
	postData = { #the data to send to the API
		#'image_request[remote_image_url]': 'https://www.google.co.uk/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png',
		'image_request[locale]': LOCALE,
		'image_request[language]': LANGUAGE
	}
	
	rPost = requests.post("https://api.cloudsightapi.com/image_requests", headers=header, data=postData, files=imageFile) #the actual request, with authorization header, data and image file attached.
	print(rPost.status_code)
	print(rPost.text)
	print(rPost.json()['token'])
	token = rPost.json()['token'] #assigns the token that got returned to a variable
	URL = URL + token #then edits the URL to include the token
	print(URL)
	getRequest() #runs the function that will send the GET request

def getRequest(): #sends the GET request to the API. Will return result of image recognition in JSON
	global name #enables name and categories to be used outside of this function
	global categories
	rGet = requests.get(URL, headers=header) #sends the GET request to the URL (including the token) with the authorization header.
	print(rGet.status_code)
	print(rGet.text)
	
	if (rGet.json()['status'] == "not completed"): #if the API is still in the process or recognising the image, run the GET request again.
		getRequest();
		print("not completed")
	elif (rGet.json()['status'] == "completed"): #if it is completed, assign the result (the name) to the variable name.
		print("completed!")
		print(rGet.json()['name'])
		name = rGet.json()['name']
		
		if ('categories' in (rGet.json())): #if the API returned categories, assingn them to the variables categories
			print(rGet.json()['categories'])
			print("categories identified")
			categories = rGet.json()['categories'] 
		else: #if not, assign the value "none" to the variable
			print("no categories")
			categories = "none"
		
		if ("cigar" in name or "drugs" in categories or "adult" in categories or "brown" in name): #check to see if the result returned was a cigarette
			print("Yup, that's a cigarette.")
			time.sleep(2)
			#run final function successfully
			end(True)
		else:
			print("Nope, definitely not a cigarette.")
			time.sleep(2)
			#run final function unsuccessfully
			end(False)
	else:
		print ("Not sure what happened there...")
		print(rGet.status_code)
		print(rGet.text)
		time.sleep(2)
		end(false)

def start(): #function to run at start
	flashOff(5) #turn off LEDs
	flashOff(6)
	flashOff(7)
	
	#initialize variables
	LOCALE = 'en-US' #locale for use with API
	LANGUAGE = 'en-US' #language for use with API	
	URL = 'http://api.cloudsightapi.com/image_responses/' #url for use with the GET request to the API

	name = "" #empty variables that will later be used to store the name and categories of the API's response
	categories = ""

	header = {
		'Authorization' : 'CloudSight XXX' #authorization header for use with the API
	}

	while True:
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		input_state = GPIO.input(18)
		if input_state == False: #if button is pressed
			print('Button Pressed')
			with picamera.PiCamera() as camera: #take picture
				flashOn(5) #flash LED on
				camera.start_preview()
				time.sleep(5)
				camera.capture('/home/pi/Downloads/image.jpg')
				camera.stop_preview()
				flashOff(5) #flash LED off
			postRequest() #run the POST request, starting the API section of the code
		#else:
			#print("Loop again")
			
start() #starts the first function
