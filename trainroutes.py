import requests     # Module for accessing website data
import json         # Module for parsing JSON resulting from request for data
import re           # Module for regular expressions 
from collections import Counter     #Used to count number of stops in a route

#Setting variables for authentication
api_url_1 = 'https://api-v3.mbta.com/routes?filter[type]=0,1'    #Accessing only the light (type:0) and heavy (type:1) rail types
api_url_2 = 'https://api-v3.mbta.com/stops?filter[route_type]=0,1&include=route' #Accessing all of the stops and their route names
user_name = 'omar.str@gmail.com'
key = '2fbf2f24d7af4315a1e999a89c54811c'

#Function that returns
def data_extract(api_url):
    # Using requests module to access the MBTA website.
    # Using API key to prevent getting rate-limited.
    req_response = requests.get(api_url, auth=(user_name, key))   #Returns a json string
    #Letting the user know that accessing the website was successful (2xx = success)
    print('The status code is: ' + str(req_response.status_code))
    #Converting json string to dictionary for data extraction
    req_dict = json.loads(req_response.text)          
    #Accessing the value of the main key 'data', which is a list of dictionaries
    data_value = req_dict['data']
    #Return the list of dictionaries containing the data
    return data_value



#Answering part 1
data_value_1 = data_extract(api_url_1)
print('1. Long names for all Light Rail and Heavy Rail subway lines:')
for listed_attr in data_value_1:                #Iterating through each dictionary in the data list
    current_attr = listed_attr['attributes']   #Extracting value for 'attribute' key
    long_name = current_attr['long_name']         #Extracting value of 'long_name' key
    print(long_name)

#Answering part 2 a and b
data_value_2 = data_extract(api_url_2)
route_list = []
print('2. Most and least stops')
for listed_attr in data_value_2:                #Iterating through each dictionary in the data list
    current_attr = listed_attr['attributes']   #Extracting value for 'attribute' key
    stop_route = current_attr['description']         #Extracting string containing stop and route name
    route = re.findall("(?<=- ).*(?= -)", stop_route) 
    route_list += route

print(route_list)
print(Counter(route_list).keys())
print(Counter(route_list).values())

