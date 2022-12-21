import re
from bs4 import BeautifulSoup
import requests
import TextToSpeech as ts
import time


def logHistory(term, type):
    historytxt = open("History.txt", "a")
    historytxt.write(term + " ")
    historytxt.write(type + " ")
    startTime = time.localtime()
    historytxt.write(time.strftime("%d/%m/%y %H:%M", startTime))
    historytxt.write("\n")
    historytxt.close()


def read(para, startIndex):  # Takes an array of paragraphs and reads it, asking the user if they want to read more
    if '\n' in para:
        para.remove('\n') # Removes blank new lines from paragraph array
    for i in range(startIndex, len(para)):
        if len(para[i]) > 2:
            displayP(para[i])
            print("")
            if i == len(para) - 1:
                break
            if not findOutMore():
                break

def findOutMore():  # Asks the user if they want to find out more, returns boolean
    choice = "h"
    while choice != "y" and choice != "n":
        choice = input("Find out more? y/n ").lower()
    if choice == "y":
        return True
    return False


def ContentSelection(contentNames):  # Lets you select a content and returns the content chosen
    # Display Contents
    print("What would you like to find out more about? ")
    for x in range(0, len(contentNames)):
        print(str(x + 1) + ") " + contentNames[x])
    print("\n")
    choice = ""
    while (not choice.isnumeric()) or int(choice) > len(contentNames) or int(choice) == 0:
        choice = input("Enter Number of choice: ")
    return contentNames[int(choice) - 1]


# Displays the text of the paragraph, takes the p text and splits it into an array of its words. Prints out the array of words with a space.
def displayP(p):
    charArray = p.split()
    i = 0  # Counter keeps track of index of char array
    while i < len(charArray):
        line = ""  # Holds the temp string
        for x in range(20):  # Prints the words 10 at a time
            if i >= len(charArray):
                break
            line = line + charArray[i] + " "
            i += 1
        print(line)  # Prints the current line




# - Wiki Scrape Section - #


def noContents(short_desc, info):
    if short_desc is not None:
        print(short_desc.text)
    p = info.find_all("p")
    for i in range(len(p)):
        p[i] = p[i].text
    read(p, 0)


def multiple(info, soup):  # For terms that have multiple definitions in different contexts
    p = info.find_all("p")
    if len(p) > 1:  # Displays the first paragraph
        print(p[0].text)

    contents = info.find_all("h2")  # Find all terms that are related to this

    li = info.find_all("li")
    contentByTopic = str(info).split("<h2")  # Seperates content into a list.
    if info.find(id="mw-toc-heading") is not None:
        contentByTopic.pop(0)
        contents.pop(0)

    for i in range(0, len(contents)):  # Turn the html of each content name into a text content name
        contents[i] = contents[i].find(class_="mw-headline").text

    counter = len(contentByTopic[0].split("<li")) - 1  # Shows how many of the list items belong to the contents tab
    nameToLink = {}  # Name of the content maps to a list of link name
    for i in range(1, len(contentByTopic)):
        temp = []
        for j in range(
                len(contentByTopic[i].split("<li")) - 1):  # Adds the list items to the temp array from this section
            if li[counter].a is not None:
                temp.append(li[counter].a.attrs["title"])
            counter += 1
        nameToLink[contents[i - 1]] = temp  # Maps section name to relevant array of link names.

    print("This term has multiple meanings in different areas: ")
    choice = ContentSelection(contents)
    newSearchTerm = ContentSelection(nameToLink[choice])
    print("Searching for " + newSearchTerm + "...\n")
    wikiSearch(newSearchTerm)


def contentToSubMapping(contentToSub, content, level):  # Maps the content to the sub contents under it.
    tempList = []  # Temp list of the subheadings that belong to this
    contentName = content.find(class_="toctext").text  # Finds first toctext and turns the name into a string.
    subContents = content.find_all(
        class_=re.compile("toclevel-" + str(level + 1)))  # Gets the html for each big heading.
    for subContent in subContents:
        tempList.append(subContent.find(class_="toctext").text)
        contentToSubMapping(contentToSub, subContent, level + 1)
    contentToSub[contentName] = tempList


'''def nameToContentMapping(info):
    # Maps the topic name to the paragraphs under the topic.
    nameToContent = {}  # Creates dictionary that maps the content title to the actual content that belongs to it
    info = info.find_all("p")
    contentByTopic = str(info).split("mw-headline")  # Seperates content into a list.
    tempArray = []  # Temp array to hold the paragraphs belonging to the main summary content.
    summaryLen = len(contentByTopic[0].split("<p>"))
    for x in range(0, summaryLen):  # Puts first few paragraphs into an array and maps it to MAIN
        tempArray.append(info_p[x].text)
    nameToContent["MAIN"] = tempArray '''


def normal(short_desc, info, soup):  # For normal definitions that don't have mutltiple meanings
    contents = soup.find("div", class_="toc").find("ul")

    contentNames = contents.find_all("span", class_="toctext")  # Gets a list of the content names.
    for i in range(0, len(contentNames)):
        contentNames[i] = contentNames[i].text  # Replaces the html with the name of the content in the list.

    contentToSub = {}  # Dictionary that maps headings to their subheadings as a list.
    mainContents = contents.find_all(class_=re.compile("toclevel-1"))  # Gets the html for each big heading.
    mainContentNames = []
    unwantedContent = ["See also", "Notes", "References", "Bibliography", "External links"]
    for content in mainContents:  # Loops through the main contents and puts the subheadings under them
        contentToSubMapping(contentToSub, content, 1)
        name = content.find("span", class_="toctext").text
        if name not in unwantedContent:
            mainContentNames.append(name)  # Puts the names of the main content names into an array
        else:  # Break when first unwanted name found as all names after will be unwanted
            break

    # Maps the topic name to the paragraphs under the topic.
    nameToContent = {}  # Creates dictionary that maps the content title to the actual content that belongs to it
    info_p = info.find_all("p")
    contentByTopic = str(info).split("mw-headline")  # Seperates content into a list.
    tempArray = []  # Temp array to hold the paragraphs belonging to the main summary content.
    summaryLen = len(contentByTopic[0].split("<p")) - 1
    for x in range(0, summaryLen):  # Puts first few paragraphs into an array and maps it to MAIN
        tempArray.append(info_p[x].text)
    nameToContent["MAIN"] = tempArray
    pCounter = summaryLen  # Counts what index the p info should be at when copying the para to the array.
    for y in range(1, len(contentByTopic)):  # For each topic
        pAmount = len(re.split("<p>| <p ", contentByTopic[y])) - 1  # Stores the amount of paragraphs this topic has
        temp = []
        for i in range(
                pAmount):  # Keeps adding the paragraphs to the temp array so that the array can be mapped to the topic name.
            # if pCounter < len(info_p):
            temp.append(info_p[pCounter].text)
            pCounter += 1
        nameToContent[contentNames[y - 1]] = temp

    nameToContent["Contents"] = []
    contentToSub["MAIN"] = mainContentNames
    contentToSub["Contents"] = mainContentNames

    # Displays the short description and summary information
    if short_desc is not None:
        print(short_desc.text)
        print("")
    displayP(info_p[0].text)
    if (len(info_p) > 1):
        displayP(info_p[1].text)
        print("")
    print("")

    if findOutMore():
        chosenContent = ContentSelection(["MAIN", "Contents"])  # Displays sub topic selection and lets user pick one.
        if len(nameToContent[chosenContent]) != 0:
            read(nameToContent[chosenContent], 0)  # Reads the content to the user.
        while len(contentToSub[chosenContent]) != 0:  # Checks if topic has subtopics user can chose from and repeats until no more subtopics
            subs = [] # Stores the sub content of the chosen content that aren't empty.
            for sub in contentToSub[chosenContent]: # Loops through sub content array of the chosen content to remove empty headings.
                if (len(contentToSub[sub]) == 0 and len(nameToContent[sub]) == 0) is False:
                    subs.append(sub)
            if len(subs) == 0:
                break
            chosenContent = ContentSelection(subs)
            if len(nameToContent[chosenContent]) != 0:
                read(nameToContent[chosenContent], 0)
            else:
                print("No information on this topic")


def wikiSearch(search):
    url = "https://en.wikipedia.org/wiki/" + search
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    info = soup.find("div", class_="mw-body-content mw-content-ltr")
    if info is not None:
        info = info.find("div", class_="mw-parser-output")
        if "is a stub. You can help Wikipedia by expanding it." in info.text:
            print("WARNING: The information provided may not be accurate or up to date. \n")
    short_desc = soup.find("div", class_="shortdescription nomobile noexcerpt noprint searchaux")
    if soup.find(class_="no-article-text-sister-projects") is not None or info is None:  # if the wiki article doesn't exist
        print("No information on this, check if there's a spelling error")
        return False
    else:
        logHistory(search, "Wiki")
        if short_desc is not None and "Topics referred to by the same term" in short_desc:
            multiple(info, soup)
        elif info.find(class_="toctitle") is None:
            noContents(short_desc, info)
        else:
            normal(short_desc, info, soup)

    return True
