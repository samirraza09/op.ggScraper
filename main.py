from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


def getChampUrl(userChampionName):
    my_url = 'https://na.op.gg/champion/statistics'

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()

    page_soup = soup(page_html, "html.parser")

    championNames = page_soup.findAll("div", {"class": "champion-index__champion-item__name"})

    listOfChampions = []

    for champion in championNames:
        listOfChampions.append(champion.string)
    isNotChampion = True
    championIndex = -1
    for champion in listOfChampions:

        championIndex += 1
        if userChampionName == champion:
            isNotChampion = False
            break

    userChampionName = userChampionName.lower()
    userChampionName = userChampionName.replace(" ", "")
    userChampionName = userChampionName.replace("'", "")

    if isNotChampion:
        print("Inputted champion does not exist, double check spelling, capitalization, and punctuation!")
        exit()

    championRoles = page_soup.findAll("div", {"class", "champion-index__champion-item__positions"})

    if len(championRoles[championIndex].text) >= 8:
        print("Which role are you playing?" + championRoles[championIndex].text)
        userRole = str(input())
        userRole = userRole.lower()
    else:
        userRole = ""

    championUrl = 'https://na.op.gg/champion/' + userChampionName + '/statistics/' + userRole
    return championUrl


def getChampPage(championUrl):
    championPage = uReq(championUrl).read()
    uReq(championUrl).close()

    championPage_soup = soup(championPage, "html.parser")
    return championPage_soup


def getChampItems(championPage_soup):
    championItemBody = championPage_soup.findAll("td", {
        "class": "champion-overview__data champion-overview__border champion-overview__border--first"})

    if len(championItemBody) < 10:
        print("Not enough people have played your champion so data cannot be retrieved")
        exit()

    # print(championItemBody[0].ul)
    startingItems = championItemBody[0].ul.findAll("li", {"class": "champion-stats__list__item tip"})

    index = 0
    print("")
    print("Starting Items: ")
    while index < len(startingItems):
        print("  " + str(index + 1) + ". " + startingItems[index]["title"].split("</b>")[0].split(">")[1])
        index += 1
    print("")

    coreItems = championItemBody[2].ul.findAll("li", {"class": "champion-stats__list__item tip"})

    print("Core Items: ")
    print("  1. " + coreItems[0]["title"].split("</b>")[0].split(">")[1])
    print("  2. " + coreItems[1]["title"].split("</b>")[0].split(">")[1])
    print("  3. " + coreItems[2]["title"].split("</b>")[0].split(">")[1])
    print("")

    print("Boots: ")
    boots = (championItemBody[7].li["title"].split("</b>")[0]).split(">")[1]
    print("   " + boots)


def getChampRunes(championPage_soup):
    championKeyStone = championPage_soup.findAll("tbody", {"class": "tabItem ChampionKeystoneRune-1"})
    championKeyStone = championKeyStone[0]
    championKeyStone = championKeyStone.findAll("div", {
        "class": "perk-page__item perk-page__item--keystone perk-page__item--active"})

    championKeyStone = championKeyStone[0].div.img["alt"]

    championRunes = championPage_soup.findAll("tbody", {"class": "tabItem ChampionKeystoneRune-1"})
    championRunes = championRunes[0]
    championRunes = championRunes.findAll("div", {"class": "perk-page__item perk-page__item--active"})
    # print(championRunes[0].div.img["alt"])

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

    userChampionName = str(input("Type the name of your champion here: "))
    championUrl = getChampUrl(userChampionName)
    championPage_soup = getChampPage(championUrl)
    getChampItems(championPage_soup)
    getChampRunes(championPage_soup)
