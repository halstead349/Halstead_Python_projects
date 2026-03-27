# 
import requests

Parameters = {
    "amount" : 10,
    "type" : "boolean",
}

response = requests.get(url="https://opentdb.com/api.php", params=Parameters)
response.raise_for_status()
#print(response)
question_data = response.json()["results"]
