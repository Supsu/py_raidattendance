from math import isnan
from config import *
import os

'''
Function to purge db, either all or only reports and attendance
Input: boolean True if purge all, db connection
'''
def purge(ifall, conn):
    #purge reports and attendance
    try:
        conn["logs"] = []
    except TypeError:
        os.remove(dbname)
        print("Database corrupted and deleted, please add log to start a new database.")
        raise SystemExit
    conn["totals"]["pulls"] = 0
    conn["totals"]["reports"] = 0
    for i in range(len(conn["players"])):
        conn["players"][i]["pulls"] = 0
        conn["players"][i]["benched"] = 0
    print("Reports and attendance purged!")

    if ifall: #purge characters too
        conn["players"] = [{"characters": [], "pulls":0, "benched":0}]
        print("Characters purged!")

    return conn

'''
Function to add alt character to a main
Input: main character, alt character, db connection
'''
def addalt(main, alt, conn):
    #check if main in db
    i_main = None
    i_alt = None

    for i in range(len(conn["players"])):
        if main in conn["players"][i]["characters"]:
            #main found
            i_main = i
            if debug:
                print("main found! i=" + str(i_main) )
            break

    #check if alt in db
    for i in range(len(conn["players"])):
        if alt in conn["players"][i]["characters"]:
            #alt already in db
            i_alt = i
            if debug:
                print("alt found! i=" + str(i_alt))
            break

    if i_main == i_alt:
        print("Alt already registered!")
        return


    elif not (isnan(i_main) and isnan(i_alt)):
        if debug:
            print("both indices found, merging..")
        #both chars already in db, merge to main
        conn["players"][i_main]["pulls"] += conn["players"][i_alt]["pulls"]
        conn["players"][i_main]["benched"] += conn["players"][i_alt]["benched"]
        for i in range(len(conn["players"][i_alt]["characters"])):
            conn["players"][i_main]["characters"].append(conn["players"][i_alt]["characters"][i])

        #delete old char
        if debug:
            print("Delete index: " + str(i_alt))
            print("Playerlist length: " + str(len(conn["players"])))
        del conn["players"][i_alt]

        print("Alt character merged to main!")

    elif i_main == None:
        print("Main not found!")
        return

    elif i_main != None and i_alt == None:
        conn["players"][i_main]["characters"].append(alt)
        print("Alt nick added to main!")

    return conn


'''
Function to add bench pulls to a player
Input: character, amount, db connection
'''
def addbenched(char, amount, conn):
    i_player = None

    for i in range(len(conn["players"])):
        if i_player != None:
            break
        for j in range(len(conn["players"][i]["characters"])):
            if conn["players"][i]["characters"][j] == char:
                i_player = i
                break


    conn["players"][i_player]["benched"] += int(amount)
    print("Benched pulls added!")
