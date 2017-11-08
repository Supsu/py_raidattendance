from config import *
import json
import urllib.request
'''
Function to build HTML table for attendance numbers from database.
Input: source object, database connection
'''
def _buildAttendance(source, conn):
    totalpulls = conn["totals"]["pulls"]

    source += "<table id=\"att_table\"><th>Nick(s)</th><th>Pulls</th><th>Benched</th><th>Attendance%</th>\n"
    for i in range(len(conn["players"])):
        source += "<tr><td class=\"nicks\">"
        for j in range(len(conn["players"][i]["characters"])):
            source += conn["players"][i]["characters"][j] + "  "

        source += "      </td>\n<td class=\"pulls\">"
        source += str( conn["players"][i]["pulls"] )

        source += "</td>\n<td class=\"benched\">"
        source += str( conn["players"][i]["benched"] )

        source += "</td>\n<td class=\"attperc"
        if totalpulls == 0:
            source += "\">inf"

        else:
            amount = round( ((conn["players"][i]["pulls"]+conn["players"][i]["benched"])/totalpulls)*100, 3)
            #check for colourclasses
            if amount >= attbp1:
                source += " att_good\">"
            elif amount >= attbp2:
                source += " att_mid\">"
            elif amount >= attbp3:
                source += " att_low\">"
            else:
                source += "\">"

            source += str(amount)
        source += "</td>\n</tr>\n"
    source += "</table>\n"
    source += "<span id=\"totalpulls\">Total pulls: " + str(totalpulls) + "</span>\n"
    if debug:
        print("Source from buildattendance:")
        print(source)
    return source

'''
Function to get rankings from warcraftlogs and to list them in the HTML.
Rankings are not stored in software database, they are always loaded from API
Input: html source, API key
'''
def _buildRankings(source, key):
    wpurl = "https://www.wowprogress.com/guild/" + wp_region + "/" + wp_realm + "/" + wp_guild + "/json_rank"
    if debug:
        print("wpurl: " + wpurl)
    rankdata = json.loads(urllib.request.urlopen(wpurl).read())

    source += "<br><br><br>"
    source += "<div id=\"wp_ranks\">"
    source += "<span>Following data provided by <a href=\"https://www.wowprogress.com\">WoWProgress.com</a></span><br>"
    source += "<span id=\"worldrank\">World rank: " + str(rankdata["world_rank"]) + "</span><br>"
    source += "<span id=\"realmrank\">Realm rank: " + str(rankdata["realm_rank"]) + "</span><br></div>"


    return source

'''
Function to build surrounding parts of HTML like body and head tags, styling,
scripts and such.
Input: html source
'''
def _buildFinal(source, conn):
    #build head piece
    if debug:
        print("Source that was passed to buildfinal:")
        print(source)

    start = "<html>\n<body onload=\"build()\">\n<head>\n<title>Raid Attendance</title>"
    start += ('''
    <style>
    .attperc {background-color: #b6b6b6;}
    .nicks {text-align: left;width: 50%;}
    th {text-align: left;}
    td {border: 1px dotted;}
    table {width: 50%;border: 2px solid;}
    .att_good {background-color: #168c26;}
    .att_mid {background-color: #868e0f;}
    .att_low {background-color: #c1481d;}
    </style>
    ''')

    source = start + "</head>\n<body>" + source


    #list known log id's
    if showloglist:
        source += "<br><br><br><div id=\"logdiv\">Known logs, first added on top:<br>\n<ul id\"=loglist\">"
        for i in range(len(conn["logs"])):
            source += "<li><a href=\"https://www.warcraftlogs.com/reports/" + str(conn["logs"][i])+"\" target=\"_blank\">"+str(conn["logs"][i]) + "</a></li>\n"
        source += "</ul></div>"




    #place for scripts
    source +='''<script></script>\n'''

    #end the file
    source += "</body>\n</html>\n"

    print("HTML code generated...")
    return source



'''
The main function of the module.
Uses other functions to build HTLM source code and returns it.
Input: database connection, api key
Output: HTML source
'''
def buildHTML(conn, key):
    source = ""
    source = _buildAttendance(source,conn)
    source = _buildRankings(source,key)
    source = _buildFinal(source, conn)

    return source





if __name__ == "__main__":
    print("Please run raid.py. Press ENTER to close the program")
    input(" ")
    raise SystemExit
