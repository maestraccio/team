#!/usr/bin/python3
versie = 0.6
datum = 20230726
print("Team %s: %s" % (versie,datum))
import datetime, calendar, locale, os, ast, pathlib, sqlite3, subprocess, operator, random
from collections import Counter, OrderedDict
from datetime import *
from dateutil.relativedelta import *
from decimal import *
from os.path import expanduser
from prettytable import PrettyTable, from_db_cursor, from_csv
from time import sleep

basismap = os.path.dirname(os.path.realpath(__file__))
os.chdir(basismap)
locale.setlocale(locale.LC_ALL, "")
nu = str(date.today())

ResetAll                = "\033[0m"
Vet                     = "\033[1m"
Vaag                    = "\033[2m"
Onderstrepen            = "\033[4m"
Knipperen               = "\033[5m"
Omkeren                 = "\033[7m"
Verborgen               = "\033[8m"
ResetVet                = "\033[21m"
ResetVaag               = "\033[22m"
ResetOnderstrepen       = "\033[24m"
ResetKnipperen          = "\033[25m"
ResetOmkeren            = "\033[27m"
ResetVerborgen          = "\033[28m"
Default                 = "\033[39m"
Zwart                   = "\033[30m"
Rood                    = "\033[31m"
Groen                   = "\033[32m"
Geel                    = "\033[33m"
Blauw                   = "\033[34m"
Magenta                 = "\033[35m"
Cyaan                   = "\033[36m"
LichtGrijs              = "\033[37m"
DonkerGrijs             = "\033[90m"
LichtRood               = "\033[91m"
LichtGroen              = "\033[92m"
LichtGeel               = "\033[93m"
LichtBlauw              = "\033[94m"
LichtMagenta            = "\033[95m"
LichtCyaan              = "\033[96m"
Wit                     = "\033[97m"
AchtergrondDefault      = "\033[49m"
AchtergrondZwart        = "\033[40m"
AchtergrondRood         = "\033[41m"
AchtergrondGroen        = "\033[42m"
AchtergrondGeel         = "\033[43m"
AchtergrondBlauw        = "\033[44m"
AchtergrondMagenta      = "\033[45m"
AchtergrondCyaan        = "\033[46m"
AchtergrondLichtGrijs   = "\033[47m"
AchtergrondDonkerGrijs  = "\033[100m"
AchtergrondLichtRood    = "\033[101m"
AchtergrondLichtGroen   = "\033[102m"
AchtergrondLichtGeel    = "\033[103m"
AchtergrondLichtBlauw   = "\033[104m"
AchtergrondLichtMagenta = "\033[105m"
AchtergrondLichtCyaan   = "\033[106m"
AchtergrondWit          = "\033[107m"
coltoevoegen = LichtGroen
colbekijken = LichtGeel
colwijzigen = LichtCyaan
colverwijderen = LichtRood
colinformatie = Wit
colmeeting = LichtMagenta
colterug = DonkerGrijs
colgoed = Groen
colslecht = Rood
statcol = [Geel,LichtGeel,Magenta,Rood,Groen,LichtRood]
iocol = [Rood,Groen]

TeamLogo = """%s
    .______. 
    |/ \\/ \|___   __ ____ __
       ||  //_\\\\ 6_\\\\|| \V \\\\
       || ||'   // |||| || ||
      _/\_ \\\\_/|\\\\/|\/\ || /\\%s
""" % (Magenta,ResetAll)
for i in TeamLogo:
    print(i, end = "", flush=True)
    sleep(0.005)
print()
lang = False
while lang == False:
    qlang = input("Kies je taal | Choose your language:\n  > 1: NL\n    2: EN\n  : ")
    if qlang == "2":
        lang = "EN"
    else:
        lang = "NL"

nu = datetime.strftime(datetime.today(),"%Y%m%d")
afsluitlijst = ["X","Q"]
jalijst = ["J","Y"]
neelijst = ["N"]
skiplijst = ["!",">","S","D"] # Skip, Standaard, Default
inputindent = "  : "
if lang == "EN":
    checklijst = ["OUT","IN"]
    weg = "%s  Q!: Exit%s" % (ResetAll+colterug,ResetAll)
    terug = "%s  Q : Back%s" % (ResetAll+colterug,ResetAll)
    statuslijst = ["Planned","Started","Paused","Aborted","Completed","Overdue"]
    taakverdeling = ["Start","Due","TaskDescription","Name","Note","Status"]
    print("Today is %s." % (LichtBlauw+str(date.today().strftime("%A %Y%m%d"))+ResetAll)) 
else:
    checklijst = ["UIT","IN"]
    weg = "%s  Q!: Afsluiten%s" % (ResetAll+colterug,ResetAll)
    terug = "%s  Q : Terug%s" % (ResetAll+colterug,ResetAll)
    statuslijst = ["Gepland","Gestart","Gepauzeerd","Afgebroken","Afgerond","Verlopen"]
    taakverdeling = ["Start","Eind","Taakomschrijving","Naam","Aantekening","Status"]
    print("Het is vandaag %s." % (LichtBlauw+str(date.today().strftime("%A %Y%m%d"))+ResetAll))

# Veel formaten niet in gebruik, maar handig om mee te testen
forc2 = "{:^2}".format
forl2 = "{:<2}".format
forr2 = "{:>2}".format
forc3 = "{:^3}".format
forl3 = "{:<3}".format
forr3 = "{:>3}".format
forc4 = "{:^4}".format
forl4 = "{:<4}".format
forr4 = "{:>4}".format
forc5 = "{:^5}".format
forl5 = "{:<5}".format
forr5 = "{:>5}".format
forc8 = "{:^8}".format
forl8 = "{:<8}".format
forr8 = "{:>8}".format
forc10 = "{:^10}".format
forl10 = "{:<10}".format
forr10 = "{:>10}".format
forc11 = "{:^11}".format
forl11 = "{:<11}".format
forr11 = "{:>11}".format
forc12 = "{:^12}".format
forl12 = "{:<12}".format
forr12 = "{:>12}".format
forc15 = "{:^15}".format
forl15 = "{:<15}".format
forr15 = "{:>15}".format
forc20 = "{:^20}".format
forl20 = "{:<20}".format
forr20 = "{:>20}".format
forc25 = "{:^25}".format
forl25 = "{:<25}".format
forr25 = "{:>25}".format

def eindroutine():
    if lang == "EN":
        zeker = "Are you %ssure%s?\n%s" % (colslecht,ResetAll,inputindent)
        bedankt = "\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll)
    else:
        zeker = "Weet je het %szeker%s?\n%s" % (colslecht,ResetAll,inputindent)
        bedankt = "\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll)
    toch = input(zeker)
    if toch.upper() in jalijst:
        print(bedankt)
        exit()

def statusshow():
    for i in statuslijst:
        ID = statuslijst.index(i)+1
        print(forr3(ID),forc15(i))

def team():
    try:
        with open("teamlijst","r") as t:
            teamlijst = ast.literal_eval(t.read())
    except:
        teamlijst = []
        with open("teamlijst","w") as t:
            print(teamlijst, end = "", file = t)
    return teamlijst

def taak():
    try:
        with open("takenlijst","r") as t:
            takenlijst = ast.literal_eval(t.read())
    except:
        takenlijst = []
        with open("takenlijst","w") as t:
            print(takenlijst, end = "", file = t)
    return takenlijst

def checkstatusdatum():
    if lang == "EN":
        verlopentaak = "There is a Task Overdue."
    else:
        verlopentaak = "Er is een Verlopen Taak."
    oei = False
    takenlijst = taak()
    for i in takenlijst:
        if datetime.strptime(str(i[0]),"%Y%m%d") > datetime.strptime(nu,"%Y%m%d"):
            i[5] = 1
        if datetime.strptime(str(i[0]),"%Y%m%d") <= datetime.strptime(nu,"%Y%m%d") and i[5] == 1:
            i[5] = 2
        if datetime.strptime(str(i[1]),"%Y%m%d") < datetime.strptime(nu,"%Y%m%d") and i[5] == 2:
            i[5] = 6
        if i[5] == 6:
            oei = True
    if oei == True:
        print(colslecht+verlopentaak+ResetAll)
    takenlijst = sorted(takenlijst)
    with open("takenlijst","w") as t:
        print(takenlijst, end = "", file = t)
    print()

def teamnieuw():
    if lang == "EN":
        nieuwevoornaam = "Type the GivenName:\n%s" % inputindent
        nieuweachternaam = "Type the LastName:\n%s" % inputindent
        nieuwpersoneelsnummer = "Type the AgentNumber:\n%s" % inputindent
        nieuweaantekening = "Type a Note (opt):\n%s" % inputindent
    else:
        nieuwevoornaam = "Typ de VoorNaam:\n%s" % inputindent
        nieuweachternaam = "Typ de AchterNaam:\n%s" % inputindent
        nieuwpersoneelsnummer = "Typ het PersoneelsNummer:\n%s" % inputindent
        nieuweaantekening = "Typ een Aantekening (opt):\n%s" % inputindent
    teamlijst = team()
    voornaam = False
    while voornaam == False:
        VN = input(nieuwevoornaam)
        if VN.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(VN) == 2 and VN[0].upper() in afsluitlijst and VN[1].upper() in skiplijst:
            eindroutine()
        elif len(VN) < 1:
            pass
        else:
            voornaam = True
    achternaam = False
    while achternaam == False:
        AN = input(nieuweachternaam)
        if AN.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(AN) == 2 and AN[0].upper() in afsluitlijst and AN[1].upper() in skiplijst:
            eindroutine()
        elif len(AN) < 1:
            pass
        else:
            achternaam = True
    personeelsnummer = False
    while personeelsnummer == False:
        PN = input(nieuwpersoneelsnummer)
        if PN.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(PN) == 2 and PN[0].upper() in afsluitlijst and PN[1].upper() in skiplijst:
            eindroutine()
        elif len(PN) < 1:
            pass
        else:
            personeelsnummer = True
    AT = input(nieuweaantekening)
    if AT.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(AT) == 2 and AT[0].upper() in afsluitlijst and AT[1].upper() in skiplijst:
        eindroutine()
    nieuwteam = [PN,VN,AN,0,AT]
    teamlijst.append(nieuwteam)
    teamlijst = sorted(teamlijst)
    with open("teamlijst","w") as t:
        print(teamlijst, end = "", file = t)
    print()

def teamshow():
    teamlijst = team()
    lijn = "+--+----------+----------+-------------------------+-----+------------+"
    if lang == "EN":
        kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("AN")[:10],forc10("GivenName")[:10],forc25("LastName")[:25],forc5("Chk")[:5],forc12("Note")[:12])
    else:
        kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("PN")[:10],forc10("VoorNaam")[:10],forc25("AchterNaam")[:25],forc5("Chk")[:5],forc12("Aantekening")[:12])
    print(colbekijken+lijn+ResetAll)
    print(kop)
    print(lijn)
    for i in teamlijst:
        ID = teamlijst.index(i)+1
        print(forr3(ID),forc10(i[0])[:10],forr10(i[1])[:10],forl25(i[2])[:25],iocol[int(forc5(i[3]))]+forc5(checklijst[int(forc5(i[3]))])[:5]+ResetAll,forl12(i[4])[:12])
    print(colbekijken+lijn+ResetAll)
    print()
 
def taaknieuw():
    if lang == "EN":
        startdatum = "Give the Start date (YYYYMMDD):\n%s" % inputindent
        einddatum = "Give the Due date (YYYYMMDD, or \"+N\" adds days to the Start date):\n%s" % inputindent
        omschrijving = "Give the TaskDescription:\n%s" % inputindent
        moetlanger = "Give at least 4 characters."
        wie = "Give the ID of the Agent:\n%s" % inputindent
        aantekening = "Give extra Info (opt):\n%s" % inputindent
        staten = "Give the ID of one of these Statuses:"
    else:
        startdatum = "Geef de Startdatum op (YYYYMMDD):\n%s" % inputindent
        einddatum = "Geef de Einddatum op (YYYYMMDD, of \"+N\" voegt dagen toe aan Startdatum):\n%s" % inputindent
        omschrijving = "Geef de Taakbeschrijving op:\n%s" % inputindent
        moetlanger = "Geef tenminste 4 karakters op."
        wie = "Geef de ID van de Medewerker:\n%s" % inputindent
        aantekening = "Geef extra Informatie (opt):\n%s" % inputindent
        staten = "Geef de ID van één van deze Statusen:"
    takenlijst = taak()
    StartDatum = False
    while StartDatum == False:
        SD = input(startdatum)
        if SD.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(SD) == 2 and SD[0].upper() in afsluitlijst and SD[1].upper() in skiplijst:
            eindroutine()
        try:
            if SD[0] == "+":
                delta = int(SD[1:])
                origstart = datetime.today()
                startdat = origstart + timedelta(days = delta)
            elif SD[0] == "-":
                delta = int(SD[1:])
                origstart = datetime.today()
                startdat = origstart - timedelta(days = delta)
            else:
                startdat = datetime.strptime(SD,"%Y%m%d")
            start = int(datetime.strftime(startdat,"%Y%m%d"))
            if lang == "EN":
                print("The Start date is %s." % start)
            else:
                print("De Startdatum is %s." % start)
            StartDatum = True
        except:
            startdat = datetime.today()
            start = int(datetime.strftime(startdat,"%Y%m%d"))
            if lang == "EN":
                print("The default Start date (today: %s) is selected." % start)
            else:
                print("De standaardStartdatum (vandaag: %s) is geselecteerd." % start)
            StartDatum = True
    EindDatum = False
    while EindDatum == False:
        ED = input(einddatum).replace(" ","").replace("-","").replace("/","").replace(":","").replace("\\","")
        if ED.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(ED) == 2 and ED[0].upper() in afsluitlijst and ED[1].upper() in skiplijst:
            eindroutine()
        try:
            if ED[0] == "+":
                delta = int(ED[1:])
                origstart = datetime.strptime(str(start),"%Y%m%d")
                einddat = origstart + timedelta(days = delta)
            else:
                einddat = datetime.strptime(ED,"%Y%m%d")
            eind = int(datetime.strftime(einddat,"%Y%m%d"))
            if eind >= start:
                if lang == "EN":
                    print("The Due date is %s." % start)
                else:
                    print("De Einddatum is %s." % start)
                EindDatum = True
        except:
            einddat = startdat+timedelta(days = 7)
            eind = int(datetime.strftime(einddat,"%Y%m%d"))
            if lang == "EN":
                print("The default Due date (Start date + 7 days: %s) is selected." % eind)
            else:
                print("De standaardEinddatum (Startdatum + 7 dagen: %s) is geselecteerd." % eind)
            EindDatum = True
    koe = False
    while koe == False:
        OS = input(omschrijving)
        if OS.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(OS) == 2 and OS[0].upper() in afsluitlijst and OS[1].upper() in skiplijst:
            eindroutine()
        if len(OS) < 4:
            print(moetlanger)
        else:
            koe = True
    teamlijst = team()
    teamshow()
    pisang = False
    while pisang == False:
        LL = input(wie)
        if LL.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(LL) == 2 and LL[0].upper() in afsluitlijst and LL[1].upper() in skiplijst:
            eindroutine()
        try:
            LL = int(LL)
            if 0 <= LL-1 <= len(teamlijst):
                die = teamlijst[LL-1]
                if lang == "EN":
                    print("%s %s is the chosen one." % (die[1],die[2]))
                else:
                    print("%s %s is gekozen." % (die[1],die[2]))
                pisang = True
        except:
            pass
    AT = input(aantekening)
    if AT.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(AT) == 2 and AT[0].upper() in afsluitlijst and AT[1].upper() in skiplijst:
        eindroutine()
    staat = False
    while staat == False:
        print(staten)
        statusshow()
        ST = input(inputindent)
        if ST.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(ST) == 2 and ST[0].upper() in afsluitlijst and ST[1].upper() in skiplijst:
            eindroutine()
        if ST == "":
            if datetime.strptime(str(start),"%Y%m%d") > datetime.strptime(str(nu),"%Y%m%d"):
                ST = "1"
            elif datetime.strptime(str(start),"%Y%m%d") <= datetime.strptime(str(nu),"%Y%m%d") <= datetime.strptime(str(eind),"%Y%m%d"):
                ST = "2"
            elif datetime.strptime(str(eind),"%Y%m%d") <= datetime.strptime(str(nu),"%Y%m%d"):
                ST = "6"
        try:
            ST = int(ST)
            if 0 <= ST-1 <= len(statuslijst):
                stus = statuslijst[ST-1]
                if lang == "EN":
                    print("%s is the chosen status." % stus)
                else:
                    print("%s is de gekozen status." % stus)
                staat = True
        except:
            pass
    nieuwtaak = [start,eind,OS,die[1]+" "+die[2],AT,ST]
    takenlijst.append(nieuwtaak)
    takenlijst = sorted(takenlijst)
    checkstatusdatum()
    with open("takenlijst","w") as t:
        print(takenlijst, end = "", file = t)

def takensmal():
    lijn = "+--+----+----+-----------+-----------+-----------+---------+"
    if lang == "EN":
        kop = "%s %s %s %s %s %s %s" % (forr3("ID"),forc4("Strt")[:4],forc4("Due")[:4],forc11("TaskDescr.")[:11],forc11("Name")[:11],forc11("Note")[:11],forc10("Status")[:10])
    else:
        kop = "%s %s %s %s %s %s %s" % (forr3("ID"),forc4("Strt")[:4],forc4("Eind")[:4],forc11("Taakomschr.")[:11],forc11("Name")[:11],forc11("Aantekening")[:11],forc10("Status")[:10])
    print(colbekijken+lijn+ResetAll)
    print(kop)
    print(lijn)
    takenlijst = taak()
    for i in takenlijst:
        ID = takenlijst.index(i)+1
        print(forr3(ID),forc4(str(i[0]))[4:],forc4(str(i[1]))[4:],statcol[int(i[5])-1]+forl11(i[2])[:11]+ResetAll,forl11(i[3])[:11],forl11(i[4])[:11],statcol[int(i[5])-1]+forl10(statuslijst[int(i[5])-1])[:10]+ResetAll)
    print(colbekijken+lijn+ResetAll)
    print()

def takenbreed():
    lijn = "+--+--------+--------+--------------------+--------------------+--------------------+--------------+"
    if lang == "EN":
        kop = "%s %s %s %s %s %s %s" % (forr3("ID"),forc8("Start")[:8],forc8("Due")[:8],forc20("TaskDescription")[:20],forc20("Name")[:20],forc20("Note")[:20],forc15("Status")[:15])
    else:
        kop = "%s %s %s %s %s %s %s" % (forr3("ID"),forc8("Start")[:8],forc8("Eind")[:8],forc20("Taakomschrijving")[:20],forc20("Name")[:20],forc20("Aantekening")[:20],forc15("Status")[:15])
    print(colbekijken+lijn+ResetAll)
    print(kop)
    print(lijn)
    takenlijst = taak()
    for i in takenlijst:
        ID = takenlijst.index(i)+1
        print(forr3(ID),forc8(str(i[0]))[:8],forc8(str(i[1]))[:8],statcol[int(i[5])-1]+forl20(i[2])[:20]+ResetAll,forl20(i[3])[:20],forl20(i[4])[:20],statcol[int(i[5])-1]+forl15(statuslijst[int(i[5])-1])[:15]+ResetAll)
    print(colbekijken+lijn+ResetAll)
    print()

def takenzeven():
    lijn = "+"+"----+"*7
    eerstedatum = datetime.strptime(nu,"%Y%m%d")-timedelta(days = 1)
    print(colbekijken+lijn+ResetAll)
    datumbereik = []
    for i in range(7):
        ij = eerstedatum + timedelta(days = i)
        j = datetime.strftime(ij,"%m%d")
        datumbereik.append(j)
        if i == 1:
            if lang == "EN":
                j = LichtBlauw+forc4("NOW")+ResetAll
            else:
                j = LichtBlauw+forc4("NU")+ResetAll
        print(" "+j, end = "")
    print()
    print(lijn)
    takenlijst = taak()
    for i in takenlijst:
        if i[0] < int(datetime.strftime(eerstedatum,"%Y%m%d")) and i[1] >= int(datetime.strftime(eerstedatum,"%Y%m%d")):
            indexstartdatum = 0
            print("",statcol[int(i[5])-1]+str(takenlijst.index(i)+1)+i[2][:4]+ResetAll, end = "")
        if str(i[0])[4:] in datumbereik:
            indexstartdatum = datumbereik.index(str(i[0])[4:])
            print("     "*indexstartdatum,statcol[int(i[5])-1]+str(takenlijst.index(i)+1)+forl4(i[2][:4])+ResetAll, end = "")
        if str(i[1])[4:] == str(i[0])[4:]:
            print()
        elif str(i[1])[4:] in datumbereik:
            indexeinddatum = datumbereik.index(str(i[1])[4:])
            print(statcol[int(i[5])-1]+"....."*(indexeinddatum-indexstartdatum-1)+ResetAll+forl4(i[3][:4]))
        elif i[1] < int(datetime.strftime(eerstedatum,"%Y%m%d")) or i[0] > int(datetime.strftime(eerstedatum,"%Y%m%d")):
            pass
        else:
            print(statcol[int(i[5])-1]+"....."*(7-1-1-indexstartdatum)+ResetAll+forl4(i[3][:4]))
    print(colbekijken+lijn+ResetAll)
    print()

def takenveertien():
    lijn = "+"+"----+"*14
    eerstedatum = datetime.strptime(nu,"%Y%m%d")-timedelta(days = 3)
    print(colbekijken+lijn+ResetAll)
    datumbereik = []
    for i in range(14):
        ij = eerstedatum + timedelta(days = i)
        j = datetime.strftime(ij,"%m%d")
        datumbereik.append(j)
        if i == 3:
            if lang == "EN":
                j = LichtBlauw+forc4("NOW")+ResetAll
            else:
                j = LichtBlauw+forc4("NU")+ResetAll
        print(" "+j, end = "")
    print()
    print(lijn)
    takenlijst = taak()
    for i in takenlijst:
        if i[0] < int(datetime.strftime(eerstedatum,"%Y%m%d")) and i[1] >= int(datetime.strftime(eerstedatum,"%Y%m%d")):
            indexstartdatum = 0
            print("",statcol[int(i[5])-1]+str(takenlijst.index(i)+1)+i[2][:4]+ResetAll, end = "")
        if str(i[0])[4:] in datumbereik:
            indexstartdatum = datumbereik.index(str(i[0])[4:])
            print("     "*indexstartdatum,statcol[int(i[5])-1]+str(takenlijst.index(i)+1)+forl4(i[2][:4])+ResetAll, end = "")
        if str(i[1])[4:] == str(i[0])[4:]:
            print()
        elif str(i[1])[4:] in datumbereik:
            indexeinddatum = datumbereik.index(str(i[1])[4:])
            print(statcol[int(i[5])-1]+"....."*(indexeinddatum-indexstartdatum-1)+ResetAll+forl4(i[3][:4]))
        elif i[1] < int(datetime.strftime(eerstedatum,"%Y%m%d")) or i[0] > int(datetime.strftime(eerstedatum,"%Y%m%d")):
            pass
        else:
            print(statcol[int(i[5])-1]+"....."*(14-1-1-indexstartdatum)+ResetAll+forl4(i[3][:4]))
    print(colbekijken+lijn+ResetAll)
    print()

def takendertig():
    lijn = "+"+"----+"*30
    eerstedatum = datetime.strptime(nu,"%Y%m%d")-timedelta(days = 7)
    print(colbekijken+lijn+ResetAll)
    datumbereik = []
    for i in range(30):
        ij = eerstedatum + timedelta(days = i)
        j = datetime.strftime(ij,"%m%d")
        datumbereik.append(j)
        if i == 7:
            if lang == "EN":
                j = LichtBlauw+forc4("NOW")+ResetAll
            else:
                j = LichtBlauw+forc4("NU")+ResetAll
        print(" "+j, end = "")
    print()
    print(lijn)
    takenlijst = taak()
    for i in takenlijst:
        if i[0] < int(datetime.strftime(eerstedatum,"%Y%m%d")) and i[1] >= int(datetime.strftime(eerstedatum,"%Y%m%d")):
            indexstartdatum = 0
            print("",statcol[int(i[5])-1]+str(takenlijst.index(i)+1)+i[2][:4]+ResetAll, end = "")
        if str(i[0])[4:] in datumbereik:
            indexstartdatum = datumbereik.index(str(i[0])[4:])
            print("     "*indexstartdatum,statcol[int(i[5])-1]+str(takenlijst.index(i)+1)+forl4(i[2][:4])+ResetAll, end = "")
        if str(i[1])[4:] == str(i[0])[4:]:
            print()
        elif str(i[1])[4:] in datumbereik:
            indexeinddatum = datumbereik.index(str(i[1])[4:])
            print(statcol[int(i[5])-1]+"....."*(indexeinddatum-indexstartdatum-1)+ResetAll+forl4(i[3][:4]))
        elif i[1] < int(datetime.strftime(eerstedatum,"%Y%m%d")) or i[0] > int(datetime.strftime(eerstedatum,"%Y%m%d")):
            pass
        else:
            print(statcol[int(i[5])-1]+"....."*(30-1-1-indexstartdatum)+ResetAll+forl4(i[3][:4]))
    print(colbekijken+lijn+ResetAll)
    print()

def takenblok():
    takenlijst = taak()
    collijst = []
    for i in takenlijst:
        collijst.append(i[5]-1)
    takendict = {}
    taakindex = 1
    for i in takenlijst:
        takendict[taakindex] = i[2]
        taakindex += 1
    breedte = 3
    breed = 0
    tel = 0
    for i,j in takendict.items():
        breed += 1
        tel += 1
        print(forr3(i)+" : "+statcol[collijst[tel-1]]+forl20(j[:15])+ResetAll,end = "")
        if breed == breedte or tel == len(takendict):
            print()
            breed = 0

def takenshow():
    if lang == "EN":
        sob = "View:\n  1 : Narrow (60 chars)\n  2 : Wide (100 chars)\n  3 : Timeline (7 days)\n  4 : Timeline (14 days)\n  5 : Timeline (30 days)\n >6 : Compact block\n%s" % inputindent
        geentaken = "There are no tasks."
    else:
        sob = "Toon:\n  1 : Smal (60 tekens)\n  2 : Breed (100 tekens)\n  3 : Tijdlijn (7 dagen)\n  4 : Tijdlijn (14 dagen)\n  5 : Tijdlijn (30 dagen)\n >6 : Compact blok\n%s" % inputindent
        geentaken = "Er zijn geen taken."
    takenlijst = taak()
    if len(takenlijst) == 0:
        print(geentaken)
        return
    now = input(sob)
    if now.upper() in afsluitlijst:
        return
    elif len(now) == 2 and now[0].upper() in afsluitlijst and now[1].upper() in skiplijst:
        eindroutine()
    if now == "1":
        takensmal()
    elif now == 2:
        takenbreed()
    elif now == "3":
        takenzeven()
    elif now == "4":
        takenveertien()
    elif now == "5":
        takendertig()
    else: # now == "6":
        takenblok()

def wijzigtaak():
    if lang == "EN":
        startdatum = "Give the Start date (YYYYMMDD), or \"+N\" to start N days later:\n%s" % inputindent
        einddatum = "Give the Due date (YYYYMMDD), or \"+N\" for N days more:\n%s" % inputindent
        omschrijving = "Give the TaskDescription:\n%s" % inputindent
        moetlanger = "Give at least 4 characters."
        wie = "Give the ID of the Agent:\n%s" % inputindent
        aantekening = "Give extra Info (opt):\n%s" % inputindent
        staten = "Give the ID of one of these Statuses:"
        welk = "Give the ID of the Task you want to change:\n%s" % inputindent
        wat = "Give the ID of what you want to change:"
    else:
        startdatum = "Geef de Startdatum op (YYYYMMDD), of \"+N\" om N dagen later te starten:\n%s" % inputindent
        einddatum = "Geef de Einddatum op (YYYYMMDD), of \"+N\" voor N dagen méér:\n%s" % inputindent
        omschrijving = "Geef de Taakbeschrijving op:\n%s" % inputindent
        moetlanger = "Geef tenminste 4 karakters op."
        wie = "Geef de ID van de Medewerker:\n%s" % inputindent
        aantekening = "Geef extra Informatie (opt):\n%s" % inputindent
        staten = "Geef de ID van één van deze Statusen:"
        welk = "Geef de ID op van de Taak die je wilt wijzigen:\n%s" % inputindent
        wat = "Geef de ID op van wat je wilt wijzigen:"
    takenlijst = taak()
    takenblok()
    kelapa = False
    while kelapa == False:
        welke = input(welk)
        if welke.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(welke) == 2 and welke[0].upper() in afsluitlijst and welke[1].upper() in skiplijst:
            eindroutine()
        try:
            welke = int(welke)
            if 0 <= welke-1 <= len(takenlijst):
                die = takenlijst[welke-1]
                start = die[0]
                eind = die[1]
                if lang == "EN":
                    print("%s %s is selected." % (statcol[die[5]-1]+statuslijst[die[5]-1]+ResetAll,statcol[die[5]-1]+die[2]+ResetAll))
                else:
                    print("%s %s is geselecteerd." % (statcol[die[5]-1]+statuslijst[die[5]-1]+ResetAll,statcol[die[5]-1]+die[2]+ResetAll))
                print(wat)
                for i in range(len(die)):
                    j = die[i]
                    if i == 5:
                        j = statcol[die[5]-1]+statuslijst[die[5]-1]+ResetAll
                    print(" "+forc3(i+1)+":",forl20(taakverdeling[i]),j)
                watte = input(inputindent)
                if watte.upper() in afsluitlijst:
                    uit = True
                    return uit
                elif len(watte) == 2 and watte[0].upper() in afsluitlijst and watte[1].upper() in skiplijst:
                    eindroutine()
                if watte == "1":
                    StartDatum = False
                    while StartDatum == False:
                        SD = input(startdatum)
                        if SD.upper() in afsluitlijst:
                            uit = True
                            return uit
                        elif len(SD) == 2 and SD[0].upper() in afsluitlijst and SD[1].upper() in skiplijst:
                            eindroutine()
                        try:
                            if SD[0] == "+":
                                delta = int(SD[1:])
                                origstart = datetime.strptime(str(takenlijst[welke-1][1-1]),"%Y%m%d")
                                startdat = origstart + timedelta(days = delta)
                            elif SD[0] == "-":
                                delta = int(SD[1:])
                                origstart = datetime.strptime(str(takenlijst[welke-1][1-1]),"%Y%m%d")
                                startdat = origstart - timedelta(days = delta)
                            else:
                                startdat = datetime.strptime(SD,"%Y%m%d")
                            start = int(datetime.strftime(startdat,"%Y%m%d"))
                            if lang == "EN":
                                print("The Start date is %s." % start)
                            else:
                                print("De Startdatum is %s." % start)
                            takenlijst[welke-1][1-1] = start
                            StartDatum = True
                        except:
                            startdat = datetime.today()
                            start = int(datetime.strftime(startdat,"%Y%m%d"))
                            if lang == "EN":
                                print("The default Start date (today: %s) is selected." % start)
                            else:
                                print("De standaardStartdatum (vandaag: %s) is geselecteerd." % start)
                            takenlijst[welke-1][1-1] = start
                            StartDatum = True
                elif watte == "2":
                    EindDatum = False
                    while EindDatum == False:
                        ED = input(einddatum)
                        if ED.upper() in afsluitlijst:
                            uit = True
                            return uit
                        elif len(ED) == 2 and ED[0].upper() in afsluitlijst and ED[1].upper() in skiplijst:
                            eindroutine()
                        try:
                            if ED[0] == "+":
                                delta = int(ED[1:])
                                origeind = datetime.strptime(str(takenlijst[welke-1][2-1]),"%Y%m%d")
                                einddat = origeind + timedelta(days = delta)
                            elif ED[0] == "-":
                                delta = int(ED[1:])
                                origeind = datetime.strptime(str(takenlijst[welke-1][2-1]),"%Y%m%d")
                                einddat = origeind - timedelta(days = delta)
                            else:
                                einddat = datetime.strptime(ED,"%Y%m%d")
                            eind = int(datetime.strftime(einddat,"%Y%m%d"))
                            if eind > start:
                                if lang == "EN":
                                    print("The Due date is %s." % start)
                                else:
                                    print("De Einddatum is %s." % start)
                                takenlijst[welke-1][2-1] = eind
                                EindDatum = True
                        except:
                            einddat = datetime.today()
                            eind = int(datetime.strftime(einddat,"%Y%m%d"))
                            if lang == "EN":
                                print("The default Due date (today: %s) is selected." % eind)
                            else:
                                print("De standaardEinddatum (vandaag: %s) is geselecteerd." % eind)
                            takenlijst[welke-1][2-1] = eind
                            EindDatum = True
                elif watte == "3":
                    koe = False
                    while koe == False:
                        OS = input(omschrijving)
                        if OS.upper() in afsluitlijst:
                            uit = True
                            return uit
                        elif len(OS) == 2 and OS[0].upper() in afsluitlijst and OS[1].upper() in skiplijst:
                            eindroutine()
                        if len(OS) < 4:
                            print(moetlanger)
                        else:
                            takenlijst[welke-1][3-1] = OS
                            koe = True
                elif watte == "4":
                    teamlijst = team()
                    teamshow()
                    pisang = False
                    while pisang == False:
                        LL = input(wie)
                        if LL.upper() in afsluitlijst:
                            return
                        elif len(LL) == 2 and LL[0].upper() in afsluitlijst and LL[1].upper() in skiplijst:
                            eindroutine()
                        try:
                            LL = int(LL)
                            if 0 <= LL-1 <= len(teamlijst):
                                die = teamlijst[LL-1]
                                if lang == "EN":
                                    diedus = "%s %s is the chosen one." % (die[1],die[2])
                                else:
                                    diedus = "%s %s is gekozen." % (die[1],die[2])
                                print(diedus)
                                takenlijst[welke-1][4-1] = die[1]+" "+die[2]
                                pisang = True
                        except:
                            pass
                elif watte == "5":
                    AT = input(aantekening)
                    if AT.upper() in afsluitlijst:
                        uit = True
                        return uit
                    elif len(AT) == 2 and AT[0].upper() in afsluitlijst and AT[1].upper() in skiplijst:
                        eindroutine()
                    takenlijst[welke-1][5-1] = AT
                elif watte == "6":
                    staat = False
                    while staat == False:
                        print(staten)
                        statusshow()
                        ST = input(inputindent)
                        if ST.upper() in afsluitlijst:
                            uit = True
                            return uit
                        elif len(ST) == 2 and ST[0].upper() in afsluitlijst and ST[1].upper() in skiplijst:
                            eindroutine()
                        if ST == "":
                            if datetime.strptime(str(start),"%Y%m%d") > datetime.strptime(str(nu),"%Y%m%d"):
                                ST = "1"
                            elif datetime.strptime(str(start),"%Y%m%d") <= datetime.strptime(str(nu),"%Y%m%d") <= datetime.strptime(str(eind),"%Y%m%d"):
                                ST = "2"
                            elif datetime.strptime(str(eind),"%Y%m%d") <= datetime.strptime(str(nu),"%Y%m%d"):
                                ST = "6"
                        try:
                            ST = int(ST)
                            if 0 <= ST-1 <= len(statuslijst):
                                stus = statuslijst[ST-1]
                                if lang == "EN":
                                    stiedus = "%s is the chosen status." % stus
                                else:
                                    stiedus = "%s is de gekozen status." % stus
                                print(stiedus)
                                takenlijst[welke-1][6-1] = ST
                                staat = True
                        except:
                            pass
                takenlijst = sorted(takenlijst)
                with open("takenlijst","w") as t:
                    print(takenlijst, end = "", file = t)
                kelapa = True
        except:
            pass
    checkstatusdatum()
    print()

def wijzigmedewerker():
    if lang == "EN":
        kies = "Choose an Agent to %sCHANGE%s:" % (colwijzigen, ResetAll)
        wie = "Give the ID of the Agent:\n%s" % inputindent
        wat = "What do you want to change?:\n  1 : Agent Number\n  2 : Given Name\n  3 : Last Name\n  4 : Check\n  5 : Note\n%s" % inputindent
        hoechk = "  0 : OUT\n  1 : IN\n%s" % inputindent
    else:
        kies = "Kies een Medewerker om te %sWIJZIGEN%s:" % (colwijzigen, ResetAll)
        wie = "Geef de ID van de Medewerker:\n%s" % inputindent
        wat = "Wat wil je Wijzigen?:\n  1 : Personeelsnummer\n  2 : VoorNaam\n  3 : AchterNaam\n  4 : Check\n  5 : Aantekening\n%s" % inputindent
        hoechk = "  0 : UIT\n  1 : IN\n%s" % inputindent
    teamlijst = team()
    print(kies)
    teamshow()
    pisang = False
    while pisang == False:
        LL = input(wie)
        if LL.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(LL) == 2 and LL[0].upper() in afsluitlijst and LL[1].upper() in skiplijst:
            eindroutine()
        try:
            LL = int(LL)
            if 0 <= LL-1 <= len(teamlijst):
                die = teamlijst[LL-1]
                welk = input(wat)
                if welk.upper() in afsluitlijst:
                    return
                elif len(welk) == 2 and welk[0].upper() in afsluitlijst and welk[1].upper() in skiplijst:
                    eindroutine()
                if welk == "1":
                    personeelsnummer = False
                    while personeelsnummer == False:
                        PN = input()
                        if PN.upper() in afsluitlijst:
                            return
                        elif len(PN) == 2 and PN[0].upper() in afsluitlijst and PN[1].upper() in skiplijst:
                            eindroutine()
                        elif len(PN) < 1:
                            pass
                        else:
                            teamlijst[LL-1][0] = PN
                            personeelsnummer = True
                elif welk == "2":
                    voornaam = False
                    while voornaam == False:
                        VN = input()
                        if VN.upper() in afsluitlijst:
                            return
                        elif len(VN) == 2 and VN[0].upper() in afsluitlijst and VN[1].upper() in skiplijst:
                            eindroutine()
                        elif len(VN) < 1:
                            pass
                        else:
                            teamlijst[LL-1][1] = VN
                            voornaam = True
                elif welk == "3":
                    achternaam = False
                    while achternaam == False:
                        AN = input()
                        if AN.upper() in afsluitlijst:
                            return
                        elif len(AN) == 2 and AN[0].upper() in afsluitlijst and AN[1].upper() in skiplijst:
                            eindroutine()
                        elif len(AN) < 1:
                            pass
                        else:
                            teamlijst[LL-1][2] = AN
                            achternaam = True
                    teamlijst[LL-1][2] = AN
                elif welk == "4":
                    inofuit = False
                    while inofuit == False:
                        Chk = input(hoechk)
                        try:
                            Chk = int(Chk)
                            if 0 <= Chk < len(checklijst):
                                teamlijst[LL-1][3] = Chk
                                inofuit = True
                        except:
                            pass
                elif welk == "5":
                    AT = input()
                    teamlijst[LL-1][4] = AT
                with open("teamlijst","w") as t:
                    print(teamlijst, end = "", file = t)
                teamlijst = team()
        except:
            pass
        pisang = True
    print()

def wijzigteam():
    if lang == "EN":
        sel = "Select the IDs of the Agents you want to %sCHANGE%s,\nseparated by commas, or * for all:\n%s" % (colwijzigen,ResetAll,inputindent)
        tog = "Check these Agents OUT or IN:\n  0 : OUT\n  1 : IN\n%s" % inputindent
        wat = "What do you want to change?\n >1 : Check this group OUT or IN\n  2 : Change Note for everyone in this group\n%s" % inputindent
        nieuweaantekening = "Type or clear the Note:\n%s" % inputindent
    else:
        sel = "Selecteer ID's van de Medewerkers die je wilt %sWIJZIGEN%s,\ngescheiden door een komma, of * voor alle:\n%s" % (colwijzigen,ResetAll,inputindent)
        tog = "Check deze Medewerkers UIT of IN:\n  0 : UIT\n  1 : IN\n%s" % inputindent
        wat = "Wat wil je wijzigen?\n >1 : Check deze groep UIT of IN\n  2 : Wijzig Aantekening voor iedereen in deze groep\n%s" % inputindent
        nieuweaantekening = "Typ of wis de Aantekening:\n%s" % inputindent
    teamlijst = team()
    teamshow()
    select = input(sel).replace(" ","")
    if select.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(select) == 2 and select[0].upper() in afsluitlijst and select[1].upper() in skiplijst:
        eindroutine()
    if select == "*":
        medewerkerlijst = teamlijst
    else:
        medewerkerlijst = []
        try:
            selectlijst = select.split(",")
            for i in selectlijst:
                i = int(i)
                medewerkerlijst.append(teamlijst[i-1])
        except:
            pass
    wijzig = input(wat)
    if wijzig.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(wijzig) == 2 and wijzig[0].upper() in afsluitlijst and wijzig[1].upper() in skiplijst:
        eindroutine()
    if wijzig == "2":
        AT = input(nieuweaantekening)
        if AT.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(AT) == 2 and AT[0].upper() in afsluitlijst and AT[1].upper() in skiplijst:
            eindroutine()
        for i in medewerkerlijst:
            i[4] = AT
    else:
        toggleall = input(tog)
        if toggleall == "0":
            for i in medewerkerlijst:
                i[3] = 0
        elif toggleall == "1":
            for i in medewerkerlijst:
                i[3] = 1
    with open("teamlijst","w") as t:
        print(teamlijst, end = "", file = t)
    teamlijst = team()
    print()

def vergadering():
    if lang == "EN":
        naamkop = colmeeting+forc10("Name:")+ResetAll
        meetingstart = "Comments are collected and shown but not stored.\nThe meeting has started. End with \"Q\"."
        extradeelnemer = "Add extra participants, FirstNames, divided by a comma:\n%s" % inputindent
    else:
        naamkop = colmeeting+forc10("Naam:")+ResetAll
        meetingstart = "Opmerkingen worden verzameld en getoond maar niet opgeslagen.\nDe vergadering is gestart. Beëindig met \"Q\"."
        extradeelnemer = "Voeg extra deelnemers toe, VoorNamen, gescheiden door komma's:\n%s" % inputindent
    teamlijst = team()
    teamshow()
    meetinglijstsorted = []
    meetinglijstrandom = {}
    gast = False
    while gast == False:
        extra = input(extradeelnemer).replace(" ","")
        if extra.upper() in afsluitlijst:
            gezellig = False
            break
        elif len(extra) == 2 and extra[0].upper() in afsluitlijst and extra[1].upper() in skiplijst:
            eindroutine()
        elif extra == "":
            gast = True
        else:
            extralijst = extra.split(",")
            for i in extralijst:
                meetinglijstsorted.append(i)
                gast = True
    for i in teamlijst:
        if i[3] == 1:
            meetinglijstsorted.append(i[1])
    while len(meetinglijstsorted) > 0:
        r = random.choice(meetinglijstsorted)
        meetinglijstrandom[r]= ""
        meetinglijstsorted.remove(r)
    lijn = "   +"+"----------+"*(len(meetinglijstrandom)+1)
    print(lijn)
    print("    %s " % naamkop, end = "")
    for i in meetinglijstrandom:
        if len(i) <= 10:
            j = forl10(i)
        else:
            j = i[:10]
        print(j, end = " ")
    print()
    print(lijn)
    print(meetingstart)
    puttel = 0
    gezellig = True
    while gezellig == True:
        puttel += 1
        for i,j in meetinglijstrandom.items():
            print(forr2(puttel),forr10(i[:10]),": ", end = "")
            put = input()
            putty = meetinglijstrandom[i]+" %d: " % puttel+put
            if put.upper() in afsluitlijst:
                gezellig = False
                break
            elif len(put) == 2 and put[0].upper() in afsluitlijst and put[1].upper() in skiplijst:
                eindroutine()
            meetinglijstrandom[i] = putty
        print(lijn)
    for i,j in meetinglijstrandom.items():
        print(colmeeting+forr10(i[:10]),":",j+ResetAll)
    print(colmeeting+lijn+ResetAll)
    print()

def verwijdertaak():
    if lang == "EN":
        sel = "Select the IDs of the Tasks that you want to %sDELETE%s,\nseparated by commas, or * for all:\n%s" % (colslecht, ResetAll, inputindent)
    else:
        sel = "Selecteer ID's van de Taken die je wilt %sVERWIJDEREN%s,\ngescheiden door een komma, of * voor alle:\n%s" % (colslecht, ResetAll, inputindent)
    takenlijst = taak()
    takenshow()
    select = input(sel).replace(" ","")
    if select.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(select) == 2 and select[0].upper() in afsluitlijst and select[1].upper() in skiplijst:
        eindroutine()
    if select == "*":
        taaklijst = takenlijst
    else:
        taaklijst = []
        try:
            selectlijst = select.split(",")
            for i in selectlijst:
                i = int(i)
                taaklijst.append(takenlijst[i-1])
        except:
            pass
    for i in taaklijst:
        takenlijst.remove(i)
    with open("takenlijst","w") as t:
        print(takenlijst, end = "", file = t)
    takenlijst = taak()
    uit = True
    return uit

def verwijdermedewerker():
    if lang == "EN":
        sel = "Select the IDs of the Agents that you want to %sDELETE%s,\nseparated by commas, or * for all:\n%s" % (colslecht, ResetAll, inputindent)
    else:
        sel = "Selecteer ID's van de Medewerkers die je wilt %sVERWIJDEREN%s,\ngescheiden door een komma, of * voor alle:\n%s" % (colslecht, ResetAll, inputindent)
    teamlijst = team()
    teamshow()
    select = input(sel).replace(" ","")
    if select.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(select) == 2 and select[0].upper() in afsluitlijst and select[1].upper() in skiplijst:
        eindroutine()
    if select == "*":
        medewerkerlijst = teamlijst
    else:
        medewerkerlijst = []
        try:
            selectlijst = select.split(",")
            for i in selectlijst:
                i = int(i)
                medewerkerlijst.append(teamlijst[i-1])
        except:
            pass
    for i in medewerkerlijst:
        teamlijst.remove(i)
    with open("teamlijst","w") as t:
        print(teamlijst, end = "", file = t)
    teamlijst = team()
    uit = True
    return uit

def uitklapteam():
    if lang == "EN":
        teamverdeling = ["Agent Number","Given Name","Last Name","Check","Note"]
        welk = "Give the ID of the Agent you want to expand:\n%s" % inputindent
    else:
        teamverdeling = ["Personeelsnummer","VoorNaam","AchterNaam","Check","Aantekening"]
        welk = "Geef de ID op van de Medewerker die je wilt uitklappen:\n%s" % inputindent
    teamlijst = team()
    kelapa = False
    while kelapa == False:
        welke = input(welk)
        if welke.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(welke) == 2 and welke[0].upper() in afsluitlijst and welke[1].upper() in skiplijst:
            eindroutine()
        try:
            welke = int(welke)
            if 0 <= welke-1 <= len(teamlijst):
                die = teamlijst[welke-1]
                for i in range(len(die)):
                    j = die[i]
                    if i == 3:
                        j = iocol[die[3]]+checklijst[die[3]]+ResetAll
                    print(forl20(teamverdeling[i]),j)
        except:
            pass
    print()

def uitklaptaak():
    if lang == "EN":
        taakverdeling = ["Start","Due","TaskDescription","Name","Note","Status"]
        welk = "Give the ID of the Task you want to expand:\n%s" % inputindent
    else:
        taakverdeling = ["Start","Eind","Taakomschrijving","Naam","Aantekening","Status"]
        welk = "Geef de ID op van de Taak die je wilt uitklappen:\n%s" % inputindent
    takenlijst = taak()
    kelapa = False
    while kelapa == False:
        welke = input(welk)
        if welke.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(welke) == 2 and welke[0].upper() in afsluitlijst and welke[1].upper() in skiplijst:
            eindroutine()
        try:
            welke = int(welke)
            if 0 <= welke-1 <= len(takenlijst):
                die = takenlijst[welke-1]
                start = die[0]
                eind = die[1]
                for i in range(len(die)):
                    j = die[i]
                    if i == 5:
                        j = statcol[die[5]-1]+statuslijst[die[5]-1]+ResetAll
                    #print(" "+forc3(i+1)+":",forl20(taakverdeling[i]),j)
                    print(forl20(taakverdeling[i]),j)
        except:
            pass
    print()

baas = True
while baas == True:
    takenlijst = taak()
    if lang == "EN":
        print("There are %s tasks." % len(takenlijst))
    else:
        print("Er zijn %s taken." % len(takenlijst))
    checkstatusdatum()
    takenveertien()
    teamshow()
    if lang == "EN":
        keuzeopties = "Choose from the following options:\n  1 : %sAdd%s\n >2 : %sView%s\n  3 : %sChange%s\n  4 : %sDelete%s\n  5 : %sMeeting%s\n  6 : %sNotepad (Vim)%s\n%s\n%s" % (coltoevoegen,ResetAll,colbekijken,ResetAll,colwijzigen,ResetAll,colverwijderen,ResetAll,colmeeting,ResetAll,colinformatie,ResetAll,weg,inputindent)
        toetom = "%sADD%s a Task or an Agent:\n >1 : Task\n  2 : Agent\n%s\n%s" % (coltoevoegen,ResetAll,terug,inputindent)
        zietom = "%sVIEW%s Tasks or Agents:\n >1 : Tasks\n  2 : Agents\n%s\n%s" % (colbekijken,ResetAll,terug,inputindent)
        andiot = "%sCHANGE%s a Task or Team data:\n  1 : Task\n  2 : One Agent\n >3 : Group\n%s\n%s" % (colwijzigen,ResetAll,terug,inputindent)
        watweg = "%sDELETE%s a Task or an Agent:\n >1 : Task\n  2 : Agent\n%s\n%s" % (colverwijderen,ResetAll,terug,inputindent)
    else:
        keuzeopties = "Kies uit de volgende opties:\n  1 : %sToevoegen%s\n >2 : %sBekijken%s\n  3 : %sWijzigen%s\n  4 : %sVerwijderen%s\n  5 : %sVergadering%s\n  6 : %sKladblok (Vim)%s\n%s\n%s" % (coltoevoegen,ResetAll,colbekijken,ResetAll,colwijzigen,ResetAll,colverwijderen,ResetAll,colmeeting,ResetAll,colinformatie,ResetAll,weg,inputindent)
        toetom = "%sVOEG%s een Taak of een Medewerker %sTOE%s:\n >1 : Taak\n  2 : Medewerker\n%s\n%s" % (coltoevoegen,ResetAll,coltoevoegen,ResetAll,terug,inputindent)
        zietom = "%sBEKIJK%s Taken of Medewerkers:\n >1 : Taken\n  2 : Medewerkers\n%s\n%s" % (colbekijken,ResetAll,terug,inputindent)
        andiot = "%sWIJZIG%s een Taak of Team gegevens:\n  1 : Taak\n  2 : Één Medewerker\n >3 : Groep\n%s\n%s" % (colwijzigen,ResetAll,terug,inputindent)
        watweg = "%sVERWIJDER%s een Taak of een Medewerker:\n >1 : Taak\n  2 : Medewerker\n%s\n%s" % (colverwijderen,ResetAll,terug,inputindent)
    keuze = input(keuzeopties)
    if keuze.upper() in afsluitlijst:
        eindroutine()
    elif len(keuze) == 2 and keuze[0].upper() in afsluitlijst and keuze[1].upper() in skiplijst:
        eindroutine()
    if keuze == "1":
        toevoegen = input(toetom)
        if toevoegen.upper() in afsluitlijst:
            pass
        elif len(toevoegen) == 2 and toevoegen[0].upper() in afsluitlijst and toevoegen[1].upper() in skiplijst:
            eindroutine()
        elif toevoegen == "2":
            nite = True
            while nite == True:
                uit = teamnieuw()
                if uit == True:
                    nite = False
        else:
            nita = True
            while nita == True:
                uit = taaknieuw()
                if uit == True:
                    nita = False
    elif keuze == "3":
        veranderen = input(andiot)
        if veranderen.upper() in afsluitlijst:
            pass
        elif len(veranderen) == 2 and veranderen[0].upper() in afsluitlijst and veranderen[1].upper() in skiplijst:
            eindroutine()
        elif veranderen == "1":
            wita = True
            while wita == True:
                uit = wijzigtaak()
                if uit == True:
                    wita = False
        elif veranderen == "2":
            wime = True
            while wime == True:
                uit = wijzigmedewerker()
                if uit == True:
                    wime = False
        else:
            wite = True
            while wite == True:
                uit = wijzigteam()
                if uit == True:
                    wite = False
    elif keuze == "4":
        verwijderen = input(watweg)
        if verwijderen.upper() in afsluitlijst:
            pass
        elif len(verwijderen) == 2 and verwijderen[0].upper() in afsluitlijst and verwijderen[1].upper() in skiplijst:
            eindroutine()
        elif verwijderen == "2":
            veme = True
            while veme == True:
                uit = verwijdermedewerker()
                if uit == True:
                    veme = False
        else:
            veta = True
            while veta == True:
                uit = verwijdertaak()
                if uit == True:
                    veta = False
    elif keuze == "5":
        vergadering()
    elif keuze == "6":
        print(colinformatie, end = "")
        subprocess.run(["vim","team.txt"])
        print(ResetAll, end = "")
    else: # 2
        bekijken = input(zietom)
        if bekijken.upper() in afsluitlijst:
            pass
        elif len(bekijken) == 2 and bekijken[0].upper() in afsluitlijst and bekijken[1].upper() in skiplijst:
            eindroutine()
        elif bekijken == "2":
            teamshow()
            uitklapteam()
        else:
            takenshow()
            uitklaptaak()
