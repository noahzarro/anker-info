import requests

response = requests.get("https://www.coop.ch/rest/v2/coopathome/products/3458809")

print(response.json())

promotion = response.json().get("selectedPromotion", None)

# exit if promotion field does not exist
if promotion == None:
    print("no promotion")
    exit()

if "50%" in promotion["text"]:
    print("Anker halbe Priis")
else:
    print("Anker Aktion, aber nöd halbe Priis")