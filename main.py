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

    output = "\nStarting Items:\n\n    " + startingItem1 + "\n    " + startingItem2 + " " + secondItemQuantity + "\n\nBoots:\n\n    " + boots + "\n\nCore Items:\n\n"

    for item in coreItems:
        output = output + "    " + item["alt"] + "\n"
        
    print(output)

def getChampRunes(championPage_soup):
    championKeyStone = championPage_soup.findAll("tbody", {"class": "tabItem ChampionKeystoneRune-1"})
    championKeyStone = championKeyStone[0]
    championKeyStone = championKeyStone.findAll("div", {
        "class": "perk-page__item perk-page__item--keystone perk-page__item--active"})

    championKeyStone = championKeyStone[0].div.img["alt"]

    championRunes = championPage_soup.findAll("tbody", {"class": "tabItem ChampionKeystoneRune-1"})
    championRunes = championRunes[0]
    championRunes = championRunes.findAll("div", {"class": "perk-page__item perk-page__item--active"})

    runesIndex = 0
    runeList = [championKeyStone]
    while runesIndex < 5:
        runesIndex += 1
        runeList.append(championRunes[runesIndex].div.img["alt"])

    primaryRunes = [runeList[0], runeList[5], runeList[1], runeList[2]]
    secondaryRunes = [runeList[3], runeList[4]]

    primaryRunesString = ""
    for rune in primaryRunes:
        if rune == primaryRunes[3]:
            primaryRunesString = primaryRunesString + rune
        else:
            primaryRunesString = primaryRunesString + rune + " || "

    print("")
    print("Runes: ")
    print("   Primary: " + primaryRunesString)

    secondaryRunesString = ""
    for rune in secondaryRunes:
        if rune == secondaryRunes[1]:
            secondaryRunesString = secondaryRunesString + rune
        else:
            secondaryRunesString = secondaryRunesString + rune + " || "
    print("   Secondary: " + secondaryRunesString)

    miniRunes = championPage_soup.findAll("div", {"class": "fragment__detail"})
    miniRunes = miniRunes[0]
    miniRunes = miniRunes.findAll("img", {"class": "active tip"})
    # # print(miniRunes[0]["title"].split("<span>")[1].split("<")[0])

    miniRunesIndex = 0
    while miniRunesIndex < 3:
        print("   " + miniRunes[miniRunesIndex]["title"].split("<span>")[1].split("<")[0])
        miniRunesIndex = miniRunesIndex + 1

if __name__ == "__main__":

    output = ""
    userChampionName = str(input("Type the name of your champion here: "))
    championUrl = getChampUrl(userChampionName)
    championPage_soup = getChampPage(championUrl)
    getChampItems(championPage_soup)
    # getChampRunes(championPage_soup)
