import urllib.request #to fetch logs
import json

'''
Function to parse loaded data to db
Takes raw JSON data loaded from warcraftlogs.com API
parses the JSON and pushes relevant data to database.
Input: data from loadlog(), database connection
'''
def parsetodb(data, conn):

    playerdata = {} #"nick": bosspulls
    totalpulls = 0 #amount of boss pulls in log
    bossfights = [] #list of id's of encounters that are bossfights

    pdata = json.loads(data)

    #get boss pulls and their id's
    for i in range(len(pdata["fights"])):
        if pdata["fights"][i]["boss"] > 0:
            totalpulls += 1
            bossfights.append(pdata["fights"][i]["id"])

    #get amount of bosspulls for every character
    for i in range(len(pdata["friendlies"])):
        pulls = 0

        #skip NPCs and pets
        if (pdata["friendlies"][i]["type"] == "Pet") or (pdata["friendlies"][i]["type"] == "NPC"):
            continue

        for j in range(len(pdata["friendlies"][i]["fights"])):
            if pdata["friendlies"][i]["fights"][j]["id"] in bossfights:
                pulls += 1
        playerdata[pdata["friendlies"][i]["name"]] = pulls

    #push all the character pulls and total data to db
    for i in range(len(playerdata.keys())):
        pushed = False
        for j in range(len(conn["players"])): #do we know this player?
            try:
                if sorted(playerdata.keys())[i] in conn["players"][j]["characters"]:
                    conn["players"][j]["pulls"] += playerdata[sorted(playerdata.keys())[i]]
                    pushed = True
            except KeyError:
                pass
        if pushed == False:
            conn["players"].append({ "characters": [sorted(playerdata.keys())[i]],"pulls": playerdata[sorted(playerdata.keys())[i]], "benched": 0 })

    # add totals
    conn["totals"]["reports"] =+ 1
    conn["totals"]["pulls"] += totalpulls

    #some cleaning
    if len(conn["players"][0]["characters"]) == 0:
        del conn["players"][0]


    return conn




'''
Loads report data from warcraftlogs.com API and returns
unmodified JSON response.
Input: log id, API key
Output: JSON as got from API
'''
def loadlog(logid, key):
    urlbase = "https://www.warcraftlogs.com:443/v1/report/fights/"
    urlmid = logid + "?translate=false&api_key="
    urlend = key
    url = urlbase+urlmid+urlend
    jdata = urllib.request.urlopen(url).read()
    return jdata


'''
Check if the log already has been added.
Input: logid, database connection
Output: Boolean
'''
def isAdded(logid, conn):
    if logid in conn["logs"]:
        print("Log already in database!")
        return True
    return False


'''
Main function to use the module. This should be run from
code using this module.
Input: log id, API key, database connection
'''
def run(logid, key, conn):
    if not isAdded(logid, conn):
        conn["logs"].append(logid)
        conn = parsetodb(loadlog(logid,key),conn)
        print("Log added!")

    return conn



if __name__ == "__main__":
    print("Please run raid.py. Press ENTER to close the program")
    input(" ")
    raise SystemExit
