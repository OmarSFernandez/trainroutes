import requests     # Module for accessing website data
import json         # Module for parsing JSON resulting from request for data
import re           # Module for regular expressions 
from collections import Counter     #Used to count number of stops in a route
from pprint import pprint

#Setting variables for authentication
route_url = 'https://api-v3.mbta.com/routes?filter[type]=0,1'    #Accessing only the light (type:0) and heavy (type:1) rail types
api_url_2 = 'https://api-v3.mbta.com/stops?filter[route_type]=0,1&include=route' #Accessing all of the stops and their route names
user_name = 'omar.str@gmail.com'
key = '2fbf2f24d7af4315a1e999a89c54811c'

#Function that returns list of dictionaries containing
def data_extract(api_url):
    # Using requests module to access the MBTA website.
    # Using API key to prevent getting rate-limited.
    req_response = requests.get(api_url, auth=(user_name, key))   #Returns a json string
    #Letting the user know that accessing the website was successful (2xx = success)
    print('Data Extract URL Successful with code ' + str(req_response.status_code))
    #Converting json string to dictionary for data extraction
    req_dict = json.loads(req_response.text)          
    #Accessing the value of the main key 'data', which is a list of dictionaries
    data_value = req_dict['data']
    #Return the list of dictionaries containing the data
    return data_value

route_data = data_extract(route_url)
route_ids = []

# ***** PART 1 ANSWER *****
print('1. Long names for all Light Rail and Heavy Rail subway lines:')
for listed_attr in route_data:                                                              # Iterating through each dictionary in the data list
    route_ids += [listed_attr['id']]
   # route_ids += ["https://api-v3.mbta.com/stops?filter[route]=" + listed_attr['id'], listed_attr['id']]       # Building a list of URLs to use for extracting stops data
    current_attr = listed_attr['attributes']                                                # Extracting value for 'attribute' key
    long_name = current_attr['long_name']                                                   # Extracting value of 'long_name' key
    print(long_name)

print(route_ids)

# ***** PART 2 A & B ANSWER *****
route_dict = {}
stop_dict = {}
for route_id in route_ids:
    url = "https://api-v3.mbta.com/stops?filter[route]=" + route_id
    stop_data = data_extract(url)
    route_dict.update({route_id : []})
    #route_dict.add(route_id, [])
    for listed_attr in stop_data:
        current_attr = listed_attr['attributes']
        stop_name = current_attr['name']
        route_dict[route_id] += [stop_name]             # Recording what stops belong to this route
        if stop_name in stop_dict.keys():               # Conditional to ensure each stop is added to the dictionary only once
            stop_dict[stop_name] += [route_id]          # Creating a dictionary of stop keys and list of routes values.
        else:
            stop_dict.update({stop_name : []})
            stop_dict[stop_name] += [route_id]            # Recording what routes stop at this stop for question 2C

    
pprint(route_dict)
pprint(stop_dict)

count_dict = {}
for route in route_dict:
    stop_count = len(route_dict[route])
    count_dict[route] = stop_count
    print("The number of stops on " + route + " is " + str(stop_count))

#print(count_dict)

min_stops = min(count_dict.values()) 
max_stops = max(count_dict.values()) 
min_key = [key for key in count_dict if count_dict[key] == min_stops] 
max_key = [key for key in count_dict if count_dict[key] == max_stops]

pprint("The route(s) with the least stops is(are): " +  str(min_key) + " with " + str(min_stops) + " stops")
pprint("The route(s) with the most stops is(are): " +  str(max_key) + " with " + str(max_stops) + " stops")

# ***** PART 2 C ANSWER *****      

for key in stop_dict:
    if len(stop_dict[key]) > 1:
        print(str(key) + " connects routes: " + str(stop_dict[key])) 

'''#Answering part 2 a and b
data_value_2 = data_extract(api_url_2)
sorted_data_list = []
route_list = []
#print('2. Most and least stops')
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

two_dict = Counter(route_list)                  '''     # Importing list of routes titles derived from json response into counter object

'''pprint(two_dict.keys())

print('Here is the counter dictionary representing each route and the number of stops they represent')
print(two_dict)'''

#Extracting the routes with the least and most stops from the counter dictionary
'''minimum = min(two_dict, key=two_dict.get)           
maximum = max(two_dict, key=two_dict.get)

print('Route with the least stops: ' + str(minimum) + ' with ' + str(two_dict[minimum]) + ' stops')
print('Route with the most stops: ' + str(maximum) + ' with ' + str(two_dict[maximum]) + ' stops')'''
'''
#Answering 2c

#Creating dictionary that will hold 'lines' as keys and 'stops' for each line as a list value.
for line in two_dict.keys():
    route_dict.add(line, [])

print(sorted_data_list)
print(route_dict)

#Eliminating repeated stop entries for alternate direction on each line.
for entry in sorted_data_list:
    if any(entry['stop'] in s for s in route_dict[entry['line']]):
        continue
    else:
        route_dict[entry['line']] += [entry['stop']]

#pprint(route_dict)


#Let's count the number of stops on each line!
count_dict = {}
for line in route_dict:
    stop_count = len(route_dict[line])
    count_dict[line] = stop_count
    print("The number of stops on " + line + " is " + str(stop_count))

#print(count_dict)

min_stops = min(count_dict.values()) 
max_stops = max(count_dict.values()) 
min_res = [key for key in count_dict if count_dict[key] == min_stops] 
max_res = [key for key in count_dict if count_dict[key] == max_stops]

pprint("The line(s) with the least stops is(are): " +  str(min_res) + " with " + str(min_stops) + " stops")
pprint("The line(s) with the most stops is(are): " +  str(max_res) + " with " + str(max_stops) + " stops")

connection_dict = my_dictionary() 
# Algirithm to compare every lines list of stops to determine if they have stops in common. 
# Creating dictionary with common stops as keys and lists of intersecting lines as values.
for prime_key in route_dict:                
    cur_list = route_dict[prime_key]
    for sec_key in route_dict:                                          # Compare every list of stops to every list of stops minus itself
        if prime_key == sec_key:
            break
        elif bool(set(cur_list) & set(route_dict[sec_key])) == False:   #
            continue
        else: 
            connections = str(set(cur_list) & set(route_dict[sec_key]))  # Returns set stops that appear in both lists
            for items in connections:                                    # Iterating through matching tops. Checking if common stops have keys in the connection dictionary
                if items in connection_dict.keys():
                    continue
                else:
                    connection_dict.add(items, [])
                    if any(prime_key in s for s in connection_dict[items]) == False:
                        connection_dict[items] += [prime_key]
                    if any(sec_key in s for s in connection_dict[items]) == False:
                        connection_dict[items] += [sec_key]
            
            print("Stop(s): " + connections + " connects: " + prime_key + " and " + sec_key)


pprint(connection_dict)

'''