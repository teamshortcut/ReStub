#import libraries
import requests
import time

#declare variables
LOCALE = 'en-US' #locale for use with API
LANGUAGE = 'en-US' #language for use with API
URL = 'http://api.cloudsightapi.com/image_responses/' #url for use with the GET request to the API

name = "" #empty variables that will later be used to store the name and categories of the API's response
categories = ""

header = {
		'Authorization' : [key] #authorization header for use with the API
	}

#declare functions	
def postRequest(): #sends the post request to the API, sending the image. Will return a token.
	global URL #lets the variable URL be used outside of this function.
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
		time.sleep(5)

postRequest()
