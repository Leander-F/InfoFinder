import re
from bs4 import BeautifulSoup
import requests
import Wiki
import TextToSpeech as ts


# - Dictionary Meaning Search - #

def dictionarySearch(search):
    url = "https://www.dictionary.com/browse/" + search
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "lxml")
    if soup.find(class_ = "no-results-title css-1cywoo2 e6aw9qa1") is not None:
        print(search + " couldn't be found on the dictionary web scraper.")
        return False
    definitions = soup.find(class_ = "css-1avshm7 e16867sm0").find_all(class_ = "css-109x55k e1hk9ate4")  # Gets the main definitions for this word.
    defTypes = [] # Puts the def types into an array, e.g verb,adverb
    defMap = {} # Maps the def type to the meaning of the word based on that def type
    for d in definitions:
        defType = d.find(class_ = "luna-pos")  # Finds and stores the def type of this definition of the word.
        if defType is None: # Checks incase there is an exception
            defType = d.find(class_ = "pos")
        if defType is None:
            print(search + " couldn't be found on the dictionary web scraper.")
            return False
        defType = defType.text
        defTypes.append(defType)
        defMap[defType] = d.find("div", attrs={"value" : True}).text  # Maps the def type to the first definition of that type by finding the first div with a value.

    if len(defTypes) == 1:
        print(search + " is a " + defTypes[0] + ", ")
        Wiki.displayP(defMap[defTypes[0]])
    else:
        while True:
            print("")
            defType = Wiki.ContentSelection(defTypes)
            print("\n" + search + " is a " + defType + ", ")
            Wiki.displayP(defMap[defType])
            if not Wiki.findOutMore():
                break
    Wiki.logHistory(search, "Dictionary")
    return True
