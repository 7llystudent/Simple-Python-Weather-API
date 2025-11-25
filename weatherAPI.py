#This is a simple weather API that can return weather information

#Imports
import requests
import redis
import json

#Base API url
API_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

#My personal API key
API_KEY = "3XJC86V7NTMCM2S6G9HUKCY8L"

#Introduce the API
print("Hello! Welcome to the JJJ weather service!")
print()

#Prompt user to enter a location they want a weather report for
location_key = input("Please enter a location you would like for a weather report: ")

#The parameters for the api requests
params = {
    "location": location_key,
    "date1": "2025-11-27",
    "date2": "2025-11-28",
    "key": API_KEY,
    "unitGroup": "us",
    "include": "days",
    "elements": "temp,tempmin,tempmax"
}

#Connect to redis on local host
r = redis.Redis(host = 'localhost', port = 6379, decode_responses = True)

#Check the cache
if r.exists(location_key):
    
    #If the location exists as a key in the cache, print it from the cache
    print(f"Key '{location_key}' exists in cache.")
    print(r.get(location_key))
else:

    #If the location doesn't exist as a key in the cache, we need to make an API request to get it from the API and set it in the
    #cache
    print(f"Key '{location_key}' does not exist in cache.")
    print()

    #Hold the response from the API for the set params
    response = requests.get(API_URL, params=params)

    #Convert json into dictionary
    response_dict = response.json()

    #Check for error chode and print error if one is caught
    if(response.status_code == 200):

        #Print out the API response of the weather info
        print(json.dumps(response_dict, indent = 4, sort_keys = True))

        #Set the new location in the cache
        r.set(location_key, json.dumps(response_dict, indent=4, sort_keys = True), ex = 60)
    else:

        #Print out the error code if one is sent
        print(f"Error: {response.status_code}")

    

