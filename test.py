import json
  
# Opening JSON file
f = open('settings.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)

print(data["Keywords"])
  
# Closing file
f.close()