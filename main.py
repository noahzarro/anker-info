import requests
from bs4 import BeautifulSoup


vgm_url = 'https://www.coop.ch/de/lebensmittel/getraenke/bier/multipacks-ab-12x50cl/anker-lager-bier-24x50cl/p/3458809'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')


promotion = soup.find(attrs={"data-testauto": "productlistpromotion3458809"})

# exit if promotion field does not exist
if promotion == None:
    print("no promotion")
    exit()

if "50%" in promotion.get_text():
    print("Anker halbe Priis")
else:
    print("Anker Aktion, aber nöd halbe Priis")