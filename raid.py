import logtodb as ltdb
import htmlgen as html
import dbman as db
from config import *
import sys
from pathlib import Path
import json


'''
MAIN of raid.py
This script uses warcraftlogs and internal database to
generate HTML page that contains attendance data straight from given reports
and some ranking data as a bonus.

Some bonus data from wowprogress may be included at some point.

For simplicity and portability data is saved in a JSON file,
instead of an actual database.

Usage: check --help or readme.txt

TODO:
-check using multiple args
-check behavior for missing params to -aa -al -b
-handle 404 errors

'''
def main():
    #check if database exists. If not, create it
    dbfile = Path(dbname)
    if (not dbfile.is_file()):
        print("File not found or corrupted, creating database..")
        dataform = { "logs": [], "players": [ {"characters": [], "pulls":0,"benched":0}], "totals": { "pulls":0, "reports":0 } }
        '''
        Data is contained in a datastructure described here
        {
            "logs": [ string1, string2, ...],
            "players": [
                    {
                    "characters":[nick1, nick2],
                    "pulls":0,
                    "benched":0
                    },
                    ...
            ],
            "totals": {
                    "pulls":0,
                    "reports":0
            }

        }
        '''
        if debug:
            print(dbname)
        with open(dbname, 'w+') as f:
            f.write(json.dumps(dataform))

        if debug:
            print("DB created:")
            print(json.dumps(dataform, sort_keys=True, indent=4, separators=(',', ': ')))


    #create db connection
    with open(dbname, 'r') as df:
        ds = json.loads(str(df.read()))
        conn = ds

        if debug:
            print("DEBUG: initial datastructure")
            print(ds)


    #handle argv and continue to execution
    argv = sys.argv
    modified = False
    iarg = 1 #start from 1, 0 is "raid.py"
    for iarg in range(len(argv)):
        if argv[iarg] == "-h" or argv[iarg] == "--help":
            print('''If raid.py is run without any arguments, it runs generation script that builds
            raid.html to working directory. Additional ways to run this are described below.

            There is a file named config, you should put your own API key there.

            Additional commandline arguments:
            -al (--addlog) id: add a new log to database. Example: raid.py -al 1234Aasjsbvaj

            -aa (--addalt) main alt: add an alt to player. Example: raid.py -aa Supsu Zupps
                Please note main has to exist in database prior to adding an alt. It doesn't matter
                if alt already exists from parsing reports.

            -p (--purge) all / reports: purges the database.
                You can remove either everything in the database, or just reports. Please note,
                purging reports clears the attendance data also. Before purging, you can generate
                a new HTML to have an "endpoint" report for your raiders before a new tier or such.
            -b (--benched) nick pulls: Adds benched pulls to player. Example: raid.py -b RaidHealzor 15
                adds 15 pulls on bench to player with said character name. You can also specify any of
                that players known alts (if you have one you can actually write. We all have our guildmate
                Lêgóläs -kind of guy.). All known alts are listed in HTML output.

                ''')
            break

        #--addlog
        elif argv[iarg] == "-al" or argv[iarg] == "--addlog":
            if debug:
                print("inside addlog handler")
            logid = argv[iarg+1]
            ltdb.run(logid, wclog, conn)
            if debug:
                print("After addlog")
                print(conn)

            inp = input("Do you want to build new html? (Y/N)")
            if inp=="Y":
                src = html.buildHTML(conn, wclog)
                with open(outputname, 'w+') as of:
                    of.write(src)
                    #write conn to file
                print("HTML file generated!")
            else:
                break


        elif argv[iarg] == "-b" or argv[iarg] == "--benched":
            try:
                char = argv[iarg+1]
                amount = argv[iarg+2]
            except:
                print("Invalid arguments")
                return 1
            db.addbenched(char, amount, conn)


        elif argv[iarg] == "-aa" or argv[iarg] == "--addalt":
            if debug:
                print("inside addalt handler")
            #add alt character
            mainc = argv[iarg+1]
            altc = argv[iarg+2]
            if debug:
                print(mainc)
                print(altc)
            db.addalt(mainc, altc, conn)
            if debug:
                print("After addalt")
                print(conn)
            inp = input("Do you want to build new html? (Y/N)")
            if inp=="Y":
                src = html.buildHTML(conn, wclog)
                with open(outputname, 'w+') as of:
                    of.write(src)
                    #write conn to file
                print("HTML file generated!")
            else:
                break

        elif argv[iarg] == "-p" or argv[iarg] == "--purge":
            if debug:
                print("inside purge handler")
            #purge database
            ptype = argv[iarg+1]
            ifall = False
            if ptype == "all":
                ifall = True
            else:
                ifall = False
            db.purge(ifall, conn)



        elif len(argv)==1 or argv[iarg] == "--build":
            if debug:
                print("got over arglist, inside build handler")

            #run generation
            src = html.buildHTML(conn, wclog)
            if debug:
                print("Source returned from htmlgen:")
                print(src)
            with open(outputname, 'w+') as of:
                of.write(src)
                #write conn to file
            print("HTML file generated!")
            break


    #update file
    with open(dbname, "w+") as of:
        if debug:
            print("End writer")
            print(conn)
        of.write(json.dumps(conn))

    return 0


main()
