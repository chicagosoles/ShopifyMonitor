from bs4 import BeautifulSoup
import requests
import time
import random
scrapeHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
discordHeaders = {"User-Agent": "myBotThing (http://www.google.com/, v0.1)", "Content-Type": "application/json", }
sitemap = "https://shop.exclucitylife.com/sitemap_products_1.xml"
oglist = []
newlist = []
response = requests.get(sitemap, headers=scrapeHeaders)
soup = BeautifulSoup(response.text, "html.parser")
initialcount = 0

#Sets the initial amount of product links and sends startup info to Discord 
def startup():
    global initialcount
    initialcount = getproducts()
    print ("Initial Number of Products: " + str(initialcount))
    body = {
        "content": "",
        "embeds": [
            {
                "title": "Starting...",
                "description": ("Monitor has been enabled\n" +
                                "Number of Products Loaded: " + str((getproducts())))
            }
        ]
    }
    r = requests.post('https://discordapp.com/api/webhooks/394374752975978496/SG6WZHXlHcTLJd8er0vlrzr5dNGvNVHCXdZeumQozItpIi821Dls3A2i9iOL-p0Pg8-I', headers=discordHeaders, json=body)


def reset():
    oglist = []
    newlist = []
    return oglist, newlist

#Returns the number of product links in the sitemap
def getproducts():
    counter = 0
    for loc in soup.find_all("loc"):
        counter += 1 
    return counter

def monitor():
    #Compiles a list of all product links in the sitemap
    for loc in soup.find_all("loc"):
        link = loc.text
        oglist.append(link)
        
    while True:
        #Waits for a random time
        waittime = random.randrange(5,10,1)
        print ("Sleeping for " + str(waittime) + " seconds...")
        time.sleep(waittime)
        
        #For the amount of times loc appears in the sitemap
        for loc in soup.find_all("loc"):
            comparelink = loc.text
            
            #If the link is not in the original list of links
            if not comparelink in oglist:
                print ("New product has been detected!")
                #Sends new link and the number of products loaded to the Discord webhook
                body = {
                    "content": "",
                    "embeds": [
                        {
                            "title": "New Product!",
                            "description":  ("Link: " + str(comparelink) + "\n" +
                                            "Number of Products Loaded: " + str((getproducts())))
                        }
                              ]
                        }
                r = requests.post('https://discordapp.com/api/webhooks/394374752975978496/SG6WZHXlHcTLJd8er0vlrzr5dNGvNVHCXdZeumQozItpIi821Dls3A2i9iOL-p0Pg8-I', headers=discordHeaders, json=body)

        #This is a test to see if the number of links increased but the comparelink method did not pick it up
        comparecount = getproducts()
        if comparecount > initialcount:
            body = {
                "content": "",
                "embeds": [
                    {
                        "title": "New Product But monitor didnt get the link",
                        "description":  ("Number of Products loaded now vs start :" + str(initialcount) + " vs " + str(comparecount))
                    }
                            ]
                    }
            r = requests.post('https://discordapp.com/api/webhooks/394374752975978496/SG6WZHXlHcTLJd8er0vlrzr5dNGvNVHCXdZeumQozItpIi821Dls3A2i9iOL-p0Pg8-I', headers=discordHeaders, json=body)
    return oglist
            
def getoglist():
    return oglist


startup()
monitor()
