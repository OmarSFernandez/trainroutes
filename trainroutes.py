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
for listed_attr in data_value_1:                # Iterating through each dictionary in the data list
    current_attr = listed_attr['attributes']   # Extracting value for 'attribute' key
    long_name = current_attr['long_name']         # Extracting value of 'long_name' key
    print(long_name)

#Answering part 2 a and b
data_value_2 = data_extract(api_url_2)
route_list = []
print('2. Most and least stops')
for listed_attr in data_value_2:                     # Iterating through each dictionary in the data list
    current_attr = listed_attr['attributes']         # Extracting value for 'attribute' key
    stop_route = current_attr['description']         # Extracting string containing stop and route name
    route = re.findall("(?<=- ).*(?= -) | (?<=- ).* \([A-Z]\)?", stop_route)        # Extracting route from stop descriptions with regular expression
    route_list += route                              # Adding each route to list of route to traverse through

two_dict = Counter(route_list)                       # Importing list of routes titles derived from json response into counter object

# Regex is not handling every case. This for loop eliminates two 
for entry in list(two_dict):                        
    if two_dict[entry] < 2:                         #  Eliminating two route names that show up once. 
        del two_dict[entry]

print('Here is the counter dictionary representing each route and the number of stops they represent')
print(two_dict)

#Extracting the routes with the least and most stops from the counter dictionary
minimum = min(two_dict, key=two_dict.get)           
maximum = max(two_dict, key=two_dict.get)

print('Route with the least stops: ' + str(minimum) + ' with ' + str(two_dict[minimum]) + ' stops')
print('Route with the most stops: ' + str(maximum) + ' with ' + str(two_dict[maximum]) + ' stops')

