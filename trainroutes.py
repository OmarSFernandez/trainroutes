import requests     # Module for accessing website data
import json         # Module for parsing JSON resulting from request for data
import re           # Module for regular expressions 
from collections import Counter     #Used to count number of stops in a route
from collections import defaultdict
from pprint import pprint

#Setting variables for authentication
route_url = 'https://api-v3.mbta.com/routes?filter[type]=0,1'    #Accessing only the light (type:0) and heavy (type:1) rail types
#api_url_2 = 'https://api-v3.mbta.com/stops?filter[route_type]=0,1&include=route' #Accessing all of the stops and their route names
user_name = 'omar.str@gmail.com'
key = '2fbf2f24d7af4315a1e999a89c54811c'

#Function that returns list of dictionaries containing
def data_extract(api_url):
    # Using requests module to access the MBTA website.
    # Using API key to prevent getting rate-limited.
    req_response = requests.get(api_url, auth=(user_name, key))   #Returns a json string
    #Letting the user know that accessing the website was successful (2xx = success)
    #print('Data Extract URL Successful with code ' + str(req_response.status_code))
    #Converting json string to dictionary for data extraction
    req_dict = json.loads(req_response.text)          
    #Accessing the value of the main key 'data', which is a list of dictionaries
    data_value = req_dict['data']
    #Return the list of dictionaries containing the data
    return data_value

#Function for finding the shortest path between 'nodes' or stops in our case
#For more info visit: https://www.python.org/doc/essays/graphs/
def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start in graph == False:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

route_data = data_extract(route_url)            #Using function 
route_ids = []

# ***** PART 1 ANSWER *****
print('***** 1 ANSWER *****')
print('1. Long names for all Light Rail and Heavy Rail subway lines:')
for listed_attr in route_data:                                                              # Iterating through each dictionary in the data list
    route_ids += [listed_attr['id']]
    current_attr = listed_attr['attributes']                                                # Extracting value for 'attribute' key
    long_name = current_attr['long_name']                                                   # Extracting value of 'long_name' key
    print(long_name)

#print(route_ids)

# ***** PART 2 A & B ANSWER *****
print('***** 2 A & B ANSWER *****')
route_dict = defaultdict(list)
stop_dict = defaultdict(list)
route_conn_dict = defaultdict(list)
stop_name_dict = {}
stop_id_dict = {}
for route_id in route_ids:
    url = "https://api-v3.mbta.com/stops?filter[route]=" + route_id
    stop_data = data_extract(url)
    #route_dict.update({route_id : []})
    #route_dict.add(route_id, [])
    for listed_attr in stop_data:
        current_attr = listed_attr['attributes']
        stop_id = listed_attr['id']                     # Recording the stop id to fix St Paul use case
        stop_name = current_attr['name']
        route_dict[route_id] += [stop_id]             # Recording what stops belong to this route
        stop_dict[stop_id] += [route_id]          # Creating a dictionary of stop keys and list of routes values.
        stop_name_dict[stop_id] = stop_name
        stop_id_dict[stop_name] = stop_id
#pprint(stop_dict)
#pprint(stop_name_dict)
 #       if stop_name in stop_dict.keys():               # Conditional to ensure each stop is added to the dictionary only once
 #           stop_dict[stop_name] += [route_id]          # Creating a dictionary of stop keys and list of routes values.
 #       else:
 #           stop_dict.update({stop_name : []})
 #           stop_dict[stop_name] += [route_id]            # Recording what routes stop at this stop for question 2C'''

    
#pprint(route_dict)
#pprint(stop_dict)

count_dict = {}
for route in route_dict:
    stop_count = len(route_dict[route])
    count_dict[route] = stop_count
    print("The number of stops on " + route + " is " + str(stop_count))

#print(count_dict)  # Dictionary with values

min_stops = min(count_dict.values()) 
max_stops = max(count_dict.values()) 
min_key = [key for key in count_dict if count_dict[key] == min_stops] 
max_key = [key for key in count_dict if count_dict[key] == max_stops]

pprint("The route(s) with the least stops is(are): " +  str(min_key) + " with " + str(min_stops) + " stops")
pprint("The route(s) with the most stops is(are): " +  str(max_key) + " with " + str(max_stops) + " stops")

# ***** PART 2 C ANSWER *****      
print('***** PART 2 C ANSWER *****')
ntrsct_groups = []                # Establishing list containing lists of intersecting lines
route_conn_dict = defaultdict(list)     #Declaring dictionary with routes as keys and list of intersecting routes are values.

for key in stop_dict:
    if len(stop_dict[key]) > 1:
        print(str(stop_name_dict[key]) + " connects routes: " + str(stop_dict[key]))        # Printing out stops that are found in 2 or more routes. AKA "peer groups"
        ntrsct_groups += [stop_dict[key]]

for key in route_dict:  #For each route_id
    for ntrsct_group in ntrsct_groups:  #Check each peer group (list of lines that directly intersect)
        if key in ntrsct_group:       #If route_id is in current peer group list, iterate through list
            for item in ntrsct_group: 
                if key != item and any(item in s for s in route_conn_dict[key]) == False:   #Don't include route in list if its the same as the current key or it its already in the list.
                    route_conn_dict[key] += [item] 
        else:
            continue

#pprint(route_conn_dict)


# ***** PART 3 ANSWER ***** 
print('***** PART 3 ANSWER *****')
route_found = False
s1_routes = []
s2_routes = [] 
stop_1 = stop_id_dict[str(input("Enter your first stop: "))]      # The names of stop must be spelled exactly as they are in the /stops enpoint
stop_2 = stop_id_dict[str(input("Enter your second stop: "))]

for key in stop_dict:                               # Getting what routes stop at that stop
    if key == stop_1:
        s1_routes = stop_dict[key][0]
    if key == stop_2:
        s2_routes = stop_dict[key][0]

print(find_shortest_path(route_conn_dict, s1_routes, s2_routes))
