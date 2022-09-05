from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def getChampUrl(userInput):
    if len(userInput.split(",")) == 1:
        print("Please use format:")
        print("Champion Name, Champion Role")
        print("ex: Master Yi, Jungle")
        exit()

    userChampionName = userInput.split(",")[0]
    userRole = userInput.split(",")[1]
    
    userChampionName = userChampionName.lower()
    userChampionName = userChampionName.replace(" ", "")
    userChampionName = userChampionName.replace("'", "")
    
    userRole = userRole.replace(" ", "")
    userRole = userRole.lower()

    if userRole == "bot":
        userRole = "adc"
    elif userRole == "sup":
        userRole = "support"
    elif userRole == "jg" or userRole == "jgl" or userRole == "jng":
        userRole = "jungle"
    elif userRole == "middle":
        userRole = "mid"
    
    roles = {'top', 'jungle', 'mid', 'adc', 'support'}

    if userRole not in roles:
        print('Inputted role does not exist')
        exit()
    my_url = 'https://na.op.gg/champions'

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    championNames = page_soup.findAll("img", {"class": "bg-image"})

    listOfChampions = []
    for champion in championNames:
        listOfChampions.append(champion["alt"])

    isNotChampion = True
    for champion in listOfChampions:
        if userChampionName == champion:
            isNotChampion = False
            break

    if isNotChampion:
        print("Inputted champion does not exist, double check spelling, capitalization, and punctuation!")
        exit()

    championUrl = 'https://na.op.gg/champions/' + userChampionName + '/' + userRole + '/build'
    return championUrl

def getChampPage(championUrl):
    uClient = uReq(championUrl)
    page_html = uClient.read()
    uClient.close()

    championPage_soup = soup(page_html, "html.parser")
    return championPage_soup

def getChampItems(championPage_soup):
    championItemBody = championPage_soup.findAll("div", {"class": "css-jhxxsn e1dnizum0"})[2]
    
    startingItemBody = championItemBody.findAll("img")
    startingItem1 = startingItemBody[0]["alt"]
    startingItem2 = startingItemBody[1]["alt"]
    
    try:
        secondStartingItem = championItemBody.findAll("div", {"class": "item_icon css-13iw28v etbnemc0"})[1]
        secondItemQuantityBody = secondStartingItem.findAll("span", {"class": "css-12wt4yp e11yrp6z1"})[0]
        secondItemQuantity = "(" + secondItemQuantityBody.string + ")"
    except:
        secondItemQuantity = ""
    
    coreItems = championItemBody.findAll("td", {"class": "css-1srg9dv epbr24v1"})[0].findAll("img")
    
    boots = championItemBody.findAll("td", {"class": "css-g795n0 epbr24v1"})[2].findAll("img")[0]["alt"]

    output = "\nStarting Items:\n    " + startingItem1 + "\n    " + startingItem2 + " " + secondItemQuantity + "\n\nBoots:\n    " + boots + "\n\nCore Items:\n"

    for item in coreItems:
        output = output + "    " + item["alt"] + "\n"

    return output

def getChampRunes(championPage_soup):
    
    keystone = championPage_soup.findAll("div", {"class": "css-1soapw6 e12igh9s4"})[0].findAll("img")[1]["alt"]
    output = "Runes:\n    " + keystone + "\n"
    runes = championPage_soup.findAll("div", {"class": "css-1x2xypo e1o8f101"})
    
    counter = 0
    for rune in runes:
        if counter == 3:
            output += "\n"
        output = output + "    " + rune.findAll("img")[0]["alt"] + '\n'
        counter += 1
        
    littleRunes = championPage_soup.findAll("img", {"class": "css-1tnxdkh e1gtrici1"})
    for runes in littleRunes:
        if runes["src"] == "https://opgg-static.akamaized.net/images/lol/perkShard/5005.png?image=q_auto,f_png,w_48&v=1662111457525":
            output = output + "\n    Attack Speed"
        elif runes["src"] == "https://opgg-static.akamaized.net/images/lol/perkShard/5008.png?image=q_auto,f_png,w_48&v=1662111457525":
            output = output + "\n    Adaptive Force"
        elif runes["src"] == "https://opgg-static.akamaized.net/images/lol/perkShard/5002.png?image=q_auto,f_png,w_48&v=1662111457525":
            output = output + "\n    Armor"
        elif runes["src"] == "https://opgg-static.akamaized.net/images/lol/perkShard/5003.png?image=q_auto,f_png,w_48&v=1662111457525":
            output = output + "\n    Magic Resist"
        elif runes["src"] == "https://opgg-static.akamaized.net/images/lol/perkShard/5007.png?image=q_auto,f_png,w_48&v=1662111457525":
            output = output + "\n    Cooldown Reduction"
        elif runes["src"] == "https://opgg-static.akamaized.net/images/lol/perkShard/5001.png?image=q_auto,f_png,w_48&v=1662111457525":
            output = output + "\n    Health"

    return output

if __name__ == "__main__":
    userChampionName = str(input("Type the name of your champion here: "))
    championUrl = getChampUrl(userChampionName)
    championPage_soup = getChampPage(championUrl)
    try:
        itemOutput = getChampItems(championPage_soup)
        runeOutput = getChampRunes(championPage_soup)
        output = itemOutput + '\n' + runeOutput
        print(output)
    except:
        print("Inputted champion has insufficient data in this role")
