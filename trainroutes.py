import requests

#Setting variables for authentication
mbtaSite = 'https://mbta.com/'
userName = 'omar.str@gmail.com'
key = '2fbf2f24d7af4315a1e999a89c54811c'

print('Here are the long names for all Light Rail and Heavy Rail subway lines:')
# Using requests module to access the MBTA website.
# Using API key to prevent getting rate-limited.
r = requests.get(mbtaSite, auth=(userName, key))

#Letting the user know that accessing the website was successful (2xx = success)
print('The status code is: ' + str(r.status_code))

