import requests     # Module for accessing website data
import json         # Module for parsing JSON resulting from request for data

#Setting variables for authentication
mbtaSite = 'https://api-v3.mbta.com/routes?filter[type]=0,1'    #accessing only the light (type:0) and heavy (type:1) rail types
userName = 'omar.str@gmail.com'
key = '2fbf2f24d7af4315a1e999a89c54811c'

# Using requests module to access the MBTA website.
# Using API key to prevent getting rate-limited.
reqResults = requests.get(mbtaSite, auth=(userName, key))

#Letting the user know that accessing the website was successful (2xx = success)
print('The status code is: ' + str(reqResults.status_code))
resDict = json.loads(reqResults.text)

#Accessing the value of the main key 'data'
data_value = resDict['data']

print('Here are the long names for all Light Rail and Heavy Rail subway lines:')
for attributeData in data_value:
    myAttribute = attributeData['attributes']
    longName = myAttribute['long_name']
    print(longName)