from bs4 import BeautifulSoup
from collections import Counter
import requests
import time
import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

discordHeaders = {"User-Agent": "myBotThing (http://www.google.com/, v0.1)", "Content-Type": "application/json", }

sitemap = "https://shop.exclucitylife.com/sitemap_products_1.xml"


def monitor(sitemap):
    oglist = []
    alertflag = 1
    response = requests.get(sitemap, headers=headers)
    productLocs = 0
    soup = BeautifulSoup(response.text, "html.parser")
    currentlocs = soup.findAll("loc")
    loclen = len(currentlocs)
    print(loclen)
    for loc in soup.find_all("loc"):
        link = loc.text
        oglist.append(link)
    while True:
        newlist = []
        print("Sleeping...")
        time.sleep(2)

        for loc in soup.find_all("loc"):
            link = loc.text
            newlist.append(link)

        for link in newlist:
            if not link in oglist:
                oglist.append(link)
                print("New Product added!        " + oglist[-1])
                alertflag = 0
                products = open('funkolist.txt', 'w')
                body = {
                    "content": "",
                    "embeds": [
                        {
                            "title": "link",
                            "description": oglist[-1],
                        }
                    ]
                }
                r = requests.post(
                    'https://discordapp.com/api/webhooks/394374752975978496/SG6WZHXlHcTLJd8er0vlrzr5dNGvNVHCXdZeumQozItpIi821Dls3A2i9iOL-p0Pg8-I',
                    headers=discordHeaders, json=body)
        if alertflag == 1:
            print("No new products added...")


def startup():
    body = {
        "content": "",
        "embeds": [
            {
                "title": "Starting...",
                "description": "Monitor has been enabled"
            }
        ]
    }
    r = requests.post(
        'https://discordapp.com/api/webhooks/394374752975978496/SG6WZHXlHcTLJd8er0vlrzr5dNGvNVHCXdZeumQozItpIi821Dls3A2i9iOL-p0Pg8-I',
        headers=discordHeaders, json=body)


startup()
monitor(sitemap)
