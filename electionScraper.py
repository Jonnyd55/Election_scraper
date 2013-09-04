import urllib.request
from bs4 import BeautifulSoup
import re

#Read from  live url
def getTables(dataType):
    #This is teh URL you are scraping. 
    URL = "http://electionresults.virginia.gov/resultsPREC.aspx?eid=5&type=SWR&rid=2&cty=003&pty=DEM&osn=1"
    
    cnx = urllib.request.urlopen(URL)
    html = cnx.read()
    
    #Put the html file into a soup variable
    soup = BeautifulSoup(html)
    
	#Find the table for the Total Race results
    race = soup.find('tr', attrs={'id':'ContentPlaceHolder1xuwgResults_rh_0'})
    raceRows = race.findAll('tr')
    
	#Find the table with the id for the city-wide results
    city = soup.find('table', attrs={'id': "ContentPlaceHolder1xuwgCounty_t_0"})
    cityRows = city.findAll('tr')
    
    #find teh precincts reporting data
    reporting = soup.find('tr', attrs={'id': 'ContentPlaceHolder1xuwgCounty_r_0'})
    reportingRows = reporting.find('b')
        
    #Find the table with the id for the precincts data
    precinct = soup.find('table', attrs={'id': "G_ContentPlaceHolder1xuwgPrecinct"})    
    precinctRows = precinct.findAll('tr')
	  
    #Decide which data type you want, 1 for the precint tables, 0 for the city-wide results
    if dataType == 1:
        return precinctRows
    elif dataType == 0:
        return cityRows
    elif dataType == 2:
        return raceRows
    else:
        return reportingRows
        
def getPrecinctResults():
    
    data = getTables(1)
    
    messyPrecincts = []
    #this takes all the trs and feeds the messyPrecincts list
    for place in data[1:]:
        placeName = place.find('tbody', attrs={'class':'ig_82354991_r1'})    
        messyPrecincts.append(placeName)
    
    #Clean out the empty lists from messyPrecincts
    cleanTable = [x for x in messyPrecincts if x != None]
    results=[]
    #Get the data we need, print it out
    for numbers in cleanTable:    
        candidates = numbers.findAll('tr', attrs={'id': re.compile('ContentPlaceHolder1xuwgPrecinct')})
        firstCandData = candidates[0].findAll('td')
        secondCandData = candidates[1].findAll('td')
        
        firstName = firstCandData[2].text
        firstRaw = firstCandData[3].text
        firstPct = firstCandData[4].text
        
        secondName = secondCandData[1].text
        secondRaw = secondCandData[2].text
        secondPct = secondCandData[3].text
        
        precinctBuilder = []
        
        precinctBuilder.append(firstName)
        precinctBuilder.append(firstRaw)
        precinctBuilder.append(firstPct)
        precinctBuilder.append(secondName)
        precinctBuilder.append(secondRaw)
        precinctBuilder.append(secondPct)
        
        
        results.append(precinctBuilder)

    return results

def getPrecinctNames():
    data = getTables(1)
    messyPrecincts = []
    #this take all the trs, but returns empty lists when no 'b' is found
    for place in data[1:]:
        placeName = place.findAll('b')
        messyPrecincts.append(placeName)
    
    #I have a list, but it also includes every blank list item, so I remove all the blank lists
    precinctsUnlisted = [x for x in messyPrecincts if x != []]
    
    #Declare new list
    list = []    
    
    #Turn list of lists into list of strings
    for spots in precinctsUnlisted[:len(list)-2]:
        chopped = spots[0].text
        splitter = chopped.split("- ")
        list.append(splitter[1])
    
    return list
    
def getCityResults():
    
    #get data for precinct results
    precinctsReporting = getTables(3)
    reportingLive = precinctsReporting.text.split(": ")
    
    #get data for city results
    data = getTables(0)
    results=[]
    #Get the data we need, print it out
    for numbers in data[1:3]:    
        candidates = numbers.findAll('td')
        results.append(candidates)
    
    #Grab list of first candidate tds
    firstCand = results[0]
    #Grab list of second candidate tds
    secondCand = results[1]
    #final list will hold the different values for each candidate.
    cityBuild = []
    cityBuild.append(firstCand[2].text)
    cityBuild.append(firstCand[3].text)
    cityBuild.append(firstCand[4].text)
    cityBuild.append(secondCand[1].text)
    cityBuild.append(secondCand[2].text)
    cityBuild.append(secondCand[3].text)
    cityBuild.append(reportingLive[1])
    
    return cityBuild
      
def getRaceResults():
    data = getTables(2)
	
    results = []
    for numbers in data[1:3]:
        candidates = numbers.findAll('td')
        results.append(candidates)
	
    firstCand = results[0]
    secondCand = results[1]
    
    raceBuild = []
    raceBuild.append(firstCand[2].text)
    raceBuild.append(firstCand[3].text)
    raceBuild.append(firstCand[4].text)
    raceBuild.append(secondCand[1].text)
    raceBuild.append(secondCand[2].text)
    raceBuild.append(secondCand[3].text)
	
    return raceBuild

def joinData():
    #call the functions to return the two lists, which will be used to build the dictionary
    places = getPrecinctNames()
    votes = getPrecinctResults()
    cityVotes = getCityResults()
    raceVotes = getRaceResults()
    
    #Creates a new dictionary that uses places list as the key and the votes list and the Value
    dictionary = dict(zip(places, votes))
    
    precinctStarter = "var precinctResults =["
    cityStarter = "var cityResults ="
    raceStarter = "var raceResults ="
	
    closer = "]"
    #Get the resulting file by typing python filename.py > results.js
    print(raceStarter)
    print(raceVotes)
    print(" ")
    print(cityStarter)
    print(cityVotes)
    print(" ")
    print(precinctStarter)
    print(dictionary)
    print(closer)
    
joinData()