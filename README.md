This script was built to pull data off the Virginia Board of Election results pages for use on election night. 
See June 2013 results pages here: http://electionresults.virginia.gov/default.aspx?eid=5

This script will only work on precinct-level pages, like this one (Attorney General primary results for Accomack County. This is the link that is currently in the script): http://electionresults.virginia.gov/resultsPREC.aspx?eid=5&type=SWR&rid=2&cty=003&pty=DEM&osn=1

The script will return three lists (javascript arrays)

Lists:
	1. raceResults = [candidate1 name, cand1 votes, cand1 vote%, cand2 name, cand2 votes, cand2 vote%]
	2. cityResults = [candidate1 name, cand1 votes, cand1 vote%, cand2 name, cand2 votes, cand2 vote%, PRECINCTS REPORTING]
	3. precinctResults = [{precinct1: [candidate1 name, cand1 votes, cand1 vote%, cand2 name, cand2 votes, cand2 vote%], precinct2 = [candidate1 name, cand1 votes, cand1 vote%, cand2 name, cand2 votes, cand2 vote%] ..etc.}]

This was built in Python 3.3 using beautiful soup 4.
	
Limitations: It does not return the total number of votes or the absentee ballots cast. Runtime has varied between 5 and 10 seconds, depending on the page. I extended this script to capture data for five cities and spit out 15 different variables and the run time was 30 seconds. The scraping seems to take up the bulk to the run time.

Why?: I wrote this both to learn some more python, but also as a way to **hopefully** pull live data off the site on election night to feed my election night apps. 

See a way to make it better? PLEASE let me know! jpdport@gmail.com or @JonDavenport1.






