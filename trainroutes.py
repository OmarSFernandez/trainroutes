import requests     # Module for accessing website data
import json         # Module for parsing JSON resulting from request for data
import re           # Module for regular expressions 
from collections import Counter     #Used to count number of stops in a route
from pprint import pprint

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

#In order to create a add dictionary keys to a data dictionary while parsing data.
#I'm using this to have each line be a key. Their values being a list of strings containing there respective stops.
class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
    # Function to add key:value pair
    def add(self, key, value): 
        self[key] = value 

route_dict = my_dictionary() 

#Answering part 1
data_value_1 = data_extract(api_url_1)
print('1. Long names for all Light Rail and Heavy Rail subway lines:')
for listed_attr in data_value_1:                # Iterating through each dictionary in the data list
    current_attr = listed_attr['attributes']   # Extracting value for 'attribute' key
    long_name = current_attr['long_name']         # Extracting value of 'long_name' key
    print(long_name)

#Answering part 2 a and b
data_value_2 = data_extract(api_url_2)
sorted_data_list = []
route_list = []
print('2. Most and least stops')
for listed_attr in data_value_2:                     # Iterating through each dictionary in the data list
    current_attr = listed_attr['attributes']         # Extracting value for 'attribute' key
    stop_route = current_attr['description']         # Extracting string containing stop and route name
    route = re.findall("(?<=- ).* \([A-Z]\)", stop_route)  
    if route == []:
        route = re.findall("(?<=- ).*(?= -)", stop_route)
        if route == []: 
            route = re.findall("(?<=- ).*", stop_route)
            if route == []:
                route = ["No Match"]        # Extracting route from stop descriptions with regular expression
    route_list += route                              # Adding each route to list of route to traverse through
    #Creating list of dictionaries containing 'description', 'stop' and 'line' to sort through later
    #Previous json data did not have distinct 'line' denotation
    sorted_data_list += [{'description' : current_attr['description'], 'stop' : current_attr['name'], 'line' : route[0]}]

two_dict = Counter(route_list)                       # Importing list of routes titles derived from json response into counter object



print('Here is the counter dictionary representing each route and the number of stops they represent')
print(two_dict)

#Extracting the routes with the least and most stops from the counter dictionary
minimum = min(two_dict, key=two_dict.get)           
maximum = max(two_dict, key=two_dict.get)

print('Route with the least stops: ' + str(minimum) + ' with ' + str(two_dict[minimum]) + ' stops')
print('Route with the most stops: ' + str(maximum) + ' with ' + str(two_dict[maximum]) + ' stops')

#Answering 2c

#Creating dictionary that will hold 'lines' as keys and 'stops' for each line as a list value.
for line in two_dict.keys():
    route_dict.add(line, [])

print(sorted_data_list)
print(route_dict)

for entry in sorted_data_list:
    if any(entry['stop'] in s for s in route_dict[entry['line']]):
        continue
    else:
        route_dict[entry['line']] += [entry['stop']]

pprint(route_dict)