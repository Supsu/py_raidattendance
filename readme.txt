Raid attendance parser by Supsu
Written using Python 3.6.1

This little software uses www.warcraftlogs.com API v1 and
www.wowprogress.com data exports to generate a simple
html webpage to track raid attendance. It also shows guild's
current world and realm ranking.

Some things to consider:
-run raid.py in a folder that you can write files in, or specify
such folders and filename as absolute path in config.py

-first command should be adding a single log with
        python raid.py -al logidhere
    or else you risk corrupting the datafile.

-software is primarily intended for personal and intra-guild use,
    therefore it has pretty much no error handling. It should be ironed out
    enough that datafile should stay somewhat intact, but most error situations
    are not handled in code, and return Python interpreter's traces and errors.

-You have to have a key to warcraftlogs api and put it into config.py.

config.py:
    config.py is loaded every time the software starts. It contains some vital
    configurations for it to work:

    wclog = "APIKEYHERE"
            You must insert your warcraftlogs.com API key here. Enclosed with ""

    dbname = "path/to/file.json"
            Data(base)file's path and name. If just filename specified, uses the
            folder where you run the software. Name your files with .json extension,
            just to be safe :)

    debug = False
            Controls debug options. Probably never turn this on.

    outputname = "path/to/file.html"
            Path and filename to .html that is the report.

    attbp1-3
            Specify percentage breakpoints for coloring in report. Values at or over
            attbp1 are green, yellow for 2, red for 3, grey under attbp3.

    wp_ values:
            guild takes your guild's name, enclosed in "", whitespace replaced with +
            realm takes realm name as wowprogress.com understands it. Like tarren-mill or
            lightning-s-blade.
            region takes eu/us/cn/whateverthereisidontknow

    showloglist
            Either True or False (capitalization required). If True, report contains
            a list of warcraftlogs reports used to calculate attendance.

Usage:
    raid.py is run with command line arguments.

    --addlog or -al
        Add a log to datafile.
        Example: --addlog asbhdgahsgfd

    --addalt or -aa
        Add alt character to player. If both characters already exist in datafile,
        merge them. Otherwise just add the character to player's character listing.
        Example: --addalt RaidHealorz RestoMage

    --purge or -p
        Purge the database. Ment to be used between tiers.
        Requires you to specify another argument. To be honest, it doesn't matter what
        it is, if it's not all.
        Example(s): --purge all             #this removes ALL data from datafile
                    --purge reports         #this removes logs and attendances, but keeps characters with their alts.

    --benched or -b
        Add pulls to someone who has been benched. Can be used to manipulate
        attendance% for other reasons too. Attendance is calculated (pulls+benched)/totalpulls
        Takes players nick (or one known alt's nick) and amount of benched pulls.
        Example: --benched RaidHealzor 15


    Running raid.py without any arguments will build the .html file.
    Most operations also ask if you want to build the report.
