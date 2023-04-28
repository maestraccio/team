#!/usr/bin/python3
versie = 0.2
datum = 20230428
print("Team %s: %s" % (versie,datum))
import datetime, calendar, locale, os, ast, pathlib, sqlite3, subprocess, operator, random
from collections import Counter, OrderedDict
from datetime import *
from dateutil.relativedelta import *
from decimal import *
from os.path import expanduser
from prettytable import PrettyTable, from_db_cursor, from_csv
from time import sleep

os.chdir("/var/www/.team")
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
colkalender = Geel
coldatabase = LichtMagenta
colinformatie = Wit
colmeeting = Groen
colcheck = LichtBlauw
colreset = Cyaan
colterug = DonkerGrijs
colstat0 = Geel
colstat1 = LichtGeel
colstat2 = Magenta
colstat3 = Rood
colstat4 = Groen
colstat5 = LichtRood
colgoed = Groen
colmatig = Geel
colslecht = Rood

print()
lang = False
while lang == False:
    qlang = input("Kies je taal | Choose your language:\n  > 1: NL\n    2: EN\n  : ")
    if qlang == "2":
        lang = "EN"
    else:
        lang = "NL"
if lang == "EN":
    terug = "%s    Q: Back%s\n" % (ResetAll+colterug,ResetAll)
else:
    terug = "%s    Q: Terug%s\n" % (ResetAll+colterug,ResetAll)

afsluitlijst = ["X","Q"]
jalijst = ["J","Y"]
neelijst = ["N"]
skiplijst = ["!",">","S","D"] # Skip, Standaard, Default
if lang == "EN":
    statuslijst = [colstat0+"0: planned"+ResetAll,colstat1+"1: started"+ResetAll,colstat2+"2: paused"+ResetAll,colstat3+"3: aborted"+ResetAll,colstat4+"4: done"+ResetAll,colstat5+"5: overdue"+ResetAll]
else:
    statuslijst = [colstat0+"0: gepland"+ResetAll,colstat1+"1: gestart"+ResetAll,colstat2+"2: gepauzeerd"+ResetAll,colstat3+"3: afgebroken"+ResetAll,colstat4+"4: afgerond"+ResetAll,colstat5+"5: verlopen"+ResetAll]

nu = str(date.today()).replace("-","")
nuy = nu[:4]
num = nu[4:6]
nud = nu[6:]
WW = date.today().strftime("%V")
DD = date.today().strftime("%d")
MM = date.today().strftime("%m")
YY = date.today().strftime("%y")
YYYY = date.today().strftime("%Y")

try:
#    home = str(os.path.expanduser("~")) # if the folder .team is in your home folder
    home = os.path.sep+"var"+os.path.sep+"www" # if the folder .team is in /var/www/
#    home = str(os.path.expanduser("~")+os.path.sep+"Documenten"+os.path.sep+"websites") # if the folder .team is in  $HOME/Documents/websites/
    os.mkdir(home+os.path.sep+".team")
    folder = home+os.path.sep+".team"
    print(folder)
except(Exception) as error:
    # print(error)
    pass
folder = home+os.path.sep+".team"
db = folder+os.path.sep+"team.db"
con = sqlite3.connect(db)
cur = con.cursor()

clteam = ["Voornaam","VN","Achternaam","AN","PN","Aantekening"]
cltakenlijst = ["Record","Begin","Eind","Taakomschrijving","Medewnummer","Status","Opmerking"]
pl = ["ID",clteam[0],clteam[2],"Chk",clteam[5]]
try:
    cur.execute("CREATE TABLE team (%s VARCHAR(25), %s VARCHAR(2), %s VARCHAR(25), %s VARCHAR(2), %s INTEGER, %s VARCHAR(25));" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
    con.commit()
except(Exception) as error:
    #print(error)
    pass
try:
    cur.execute("CREATE TABLE takenlijst (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
    con.commit()
except(Exception) as error:
    #print(error)
    pass
try:
    cur.execute("CREATE TABLE archief (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
    con.commit()
except(Exception) as error:
    #print(error)
    pass

def mkPresenteam():
    col = colcheck
    cursel = "SELECT %s FROM team WHERE NOT (%s = '%s' OR %s = '%s') ORDER BY %s" % (clteam[0],clteam[4],"0",clteam[4],"99999",clteam[0])
    cur.execute(cursel)
    Voornaamlijst = str(cur.fetchall()).replace("[","").replace("]","").replace("('","").replace("',)","").split(",")
    cursel = "SELECT %s FROM team WHERE NOT (%s = '%s' OR %s = '%s') ORDER BY %s" % (clteam[2],clteam[4],"0",clteam[4],"99999",clteam[0])
    cur.execute(cursel)
    Achternaamlijst = str(cur.fetchall()).replace("[","").replace("]","").replace("('","").replace("',)","").split(",") 
    cursel = "SELECT %s FROM team WHERE NOT (%s = '%s' OR %s = '%s') ORDER BY %s" % (clteam[5],clteam[4],"0",clteam[4],"99999",clteam[0])
    cur.execute(cursel)
    Aantekeninglijst = str(cur.fetchall()).replace("[","").replace("]","").replace("('","").replace("',)","").split(",") 
    try:
        cur.execute("CREATE TABLE presentie (%s INTEGER PRIMARY KEY, %s VARCHAR(25), %s VARCHAR(25), %s VARCHAR(3), %s VARCHAR(25));" % (pl[0],pl[1],pl[2],pl[3],pl[4]))
        con.commit()
        for i in range(len(Voornaamlijst)):
            cur.execute("INSERT INTO presentie(%s,%s,%s,%s) VALUES('%s','%s','%s','%s');" % (pl[1],pl[2],pl[3],pl[4],Voornaamlijst[i].strip(),Achternaamlijst[i].strip(),colslecht+"UIT"+ResetAll+col,Aantekeninglijst[i].strip()))
            con.commit()
        if lang == "EN":
            print("%s the %s was successful." % (col+"Resetting"+ResetAll,col+"Presence list"+ResetAll))
        else:
            print("Het %s van de %s was succesvol." % (col+"Resetten"+ResetAll,col+"Presentielijst"+ResetAll))
        presenteam()
        togglewie = "N"
    except(Exception) as error:
        pass
        #print(error)

def presenteam():
    col = colcheck
    cur.execute("SELECT %s,%s,%s,%s,%s FROM presentie;" % (pl[0],pl[1],pl[2],pl[3],pl[4]))
    Presentie = from_db_cursor(cur)
    Presentie.align = "l"
    print(col, end = "")
    print(Presentie)
    print(ResetAll, end = "")

mkPresenteam()

TeamLogo = """%s
.______.                   
|/ >< \| ___   __ ____ __ 
   ||   //_\\\\ 6_\\\\|| \V \\\\
   ||  ||'   // |||| || ||
  _/\_  \\\\_/|\\\\/|\/\ || /\\%s
""" % (Magenta,ResetAll)
for i in TeamLogo:
    print(i, end = "", flush=True)
    sleep(0.0025)

if lang == "EN":
    print("\nToday is "+LichtBlauw+str(date.today().strftime("%A"))+" "+nu+ResetAll+".\n")
else:
    print("\nHet is vandaag "+LichtBlauw+str(date.today().strftime("%A"))+" "+nu+ResetAll+".\n")

# Bij het opstarten willen we de data in de database vergelijken met de datum van vandaag, en eventueel een waarschuwing printen
curseloverStop = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s < %d AND (m.%s = '%s' OR m.%s = '%s' OR %s = '%s');" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[2],int(nu),cltakenlijst[5],statuslijst[0],cltakenlijst[5],statuslijst[1],cltakenlijst[5],statuslijst[5])
cur.execute(curseloverStop)
fetchalloverStop = str(cur.fetchall()).replace(" ","").replace("[","").replace("]","").replace("(","").replace(")","").split(",")
if fetchalloverStop[0] != "": 
    if lang == "EN":
        print("%sATTENTION: There are Tasks overdue or due today!%s" % (Rood,ResetAll))
    else:
        print("%sLET OP: Er zijn verlopen Taken of Taken die vandaag verlopen!%s" % (Rood,ResetAll))
curseloverStart = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE %s < %d AND %s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[1],int(nu),cltakenlijst[5],statuslijst[0])
cur.execute(curseloverStart)
fetchalloverStart = str(cur.fetchall()).replace(" ","").replace("[","").replace("]","").replace("(","").replace(")","").split(",")
if fetchalloverStart[0] != "": 
    if lang == "EN":
        print("%sATTENTION: There are unstarted Tasks!%s\n" % (Rood,ResetAll))
    else:
        print("%sLET OP: Er zijn Taken die nog moeten worden gestart!%s\n" % (Rood,ResetAll))
curselnuStart = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE %s = %d AND %s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[1],int(nu),cltakenlijst[5],statuslijst[0])
cur.execute(curselnuStart)
fetchallnuStart = str(cur.fetchall()).replace(" ","").replace("[","").replace("]","").replace("(","").replace(")","").split(",")
if fetchallnuStart[0] != "": 
    if lang == "EN":
        print("%sATTENTION: There are Tasks planned to start today!%s\n" % (Geel,ResetAll))
    else:
        print("%sLET OP: Er zijn Taken die vandaag nog moeten worden gestart!%s\n" % (Geel,ResetAll))
if fetchalloverStop[0] == "" and fetchallnuStart[0] == "" and fetchalloverStart[0] == "":
    if lang == "EN":
        print("All Tasks are on schedule. %sGood job.%s" % (colgoed,ResetAll))
    else:
        print("Alle Taken liggen op schema. %sGoed bezig.%s" % (colgoed,ResetAll))


# Hieronder begint het programma met interactieve input
Team = "Y"
while Team == "Y":
    toe = "N"       # 1
    comp = "N"      # 2
    mot = "N"       # 3
    Wat = "N"       # 4
    functie = "N"   # 5
    resetjn = "N"   # 6
    Extra = "Y"     # 9
    togglewie = "N" # 0

    try:
        presenteam()
    except(Exception) as error:
        if lang == "EN":
            print("%sCreate a presence list first with %s\"0\"%s" % (colslecht,ResetAll+colcheck,ResetAll))
        else:
            print("%sMaak eerst een presentielijst met %s\"0\"%s" % (colslecht,ResetAll+colcheck,ResetAll))
        #print(error)
    fl = "{:<30}".format
    fc = "{:^6}".format
    fr = "{:>24}".format
    if lang == "EN":
        functie = input("""Choose a job:
%s    %s
%s    %s
%s    %s
%s    %s
%s  > %s
%s    %s
%s    %s
%s    %s
%s    %s
%s    %s
%s    %s
%s    %s
  : """ % (coltoevoegen,fl("A dd")+fc("1 | 1!")+fr("A - T ask")+ResetAll,colbekijken,fl("V iew")+fc("2 | 2!")+fr("V - L ong")+ResetAll,colwijzigen,fl("M odify")+fc("3 | 3!")+fr("M - T ask")+ResetAll,colverwijderen,fl("D elete/archive")+fc("4 | 4!")+fr("D - A rchive")+ResetAll,colkalender,fl("C alendar and timeline")+fc("5 |   ")+fr("(ncal -3w)")+ResetAll,colreset,fl("R eset RecordID's and Backup")+fc("6 | 6!")+fr("R - B ackup All")+ResetAll,coldatabase,fl("S ql Database")+fc("7 |   ")+fr("(sqlite3 Team.db)")+ResetAll,colinformatie,fl("N otes")+fc("8 |   ")+fr("(vim Team.txt)")+ResetAll,colmeeting,fl("M eeting")+fc("9 | 9!")+fr("M - N o guests")+ResetAll,colcheck,fl("P resence list")+fc("0 | 0!")+fr("P - R eset")+ResetAll,LichtGrijs,fl("_S tandard job/Default")+fc("* !>SD")+fr("[*!, *>, *S, *D]")+ResetAll,colterug,fl("Q Back")+fc("q | %sq!" % (ResetAll+colslecht))+fr("Q - Q uit")+ResetAll)).replace(" ","").replace("-","")
    else:
        functie = input("""Kies een functie:
%s    %s
%s    %s
%s    %s
%s    %s
%s  > %s
%s    %s
%s    %s
%s    %s
%s    %s
%s    %s
%s    %s
%s    %s
  : """ % (coltoevoegen,fl("T oevoegen")+fc("1 | 1!")+fr("T - T aak")+ResetAll,colbekijken,fl("B ekijken")+fc("2 | 2!")+fr("B - U itgebreid")+ResetAll,colwijzigen,fl("W ijzigen")+fc("3 | 3!")+fr("W - T aak")+ResetAll,colverwijderen,fl("V erwijderen/archiveren")+fc("4 | 4!")+fr("V - A rchiveren")+ResetAll,colkalender,fl("K alender en tijdlijn")+fc("5 |   ")+fr("(ncal -3w)")+ResetAll,colreset,fl("R eset RecordID's en Backup")+fc("6 | 6!")+fr("R - B ackup Alles")+ResetAll,coldatabase,fl("D atabase")+fc("7 |   ")+fr("(sqlite3 Team.db)")+ResetAll,colinformatie,fl("A lgemene informatie")+fc("8 |   ")+fr("(vim Team.txt)")+ResetAll,colmeeting,fl("M eeting")+fc("9 | 9!")+fr("M - G een gasten")+ResetAll,colcheck,fl("P resentielijst")+fc("0 | 0!")+fr("P - R eset")+ResetAll,LichtGrijs,fl("_S tandaardopdracht/Default")+fc("* !>SD")+fr("[*!, *>, *S, *D]")+ResetAll,colterug,fl("Q Terug")+fc("q | %sq!" % (ResetAll+colslecht))+fr("Q - A fsluiten")+ResetAll)).replace(" ","").replace("-","")
    if functie.upper() in afsluitlijst or functie.upper() in neelijst:
        if lang == "EN":
            toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
        else:
            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
        if toch.upper() in jalijst:
            if lang == "EN":
                print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
            else:
                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
            exit()
    elif len(functie) >= 2 and (functie[0].upper() in afsluitlijst or functie[0].upper() in neelijst) and (functie[1].upper() in skiplijst or functie[1].upper() == "A"):
        if lang == "EN":
            toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
        else:
            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
        if toch.upper() in jalijst:
            if lang == "EN":
                print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
            else:
                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
            exit()
    if lang == "EN":
        if len(functie) >= 2 and (functie[0] == "1" or functie[0].upper() == "A") and (functie[1].upper() in skiplijst or functie[1] == "1" or functie[1].upper() == "T"):    # 1: Toevoegen
            functie = "1"
            toe = "1"
            print("Standard job \"%sAdd - Task%s\" chosen." % (coltoevoegen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "1" or functie[0].upper() == "A") and (functie[1] == "2" or functie[1].upper() == "M"):
            functie = "1"
            toe = "2"
            print("Standard job \"%sAdd - Member%s\" chosen." % (coltoevoegen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "2" or functie[0].upper() == "V") and (functie[1].upper() in skiplijst or functie[1].upper() == "L"):                         # 2: Bekijken
            functie = "2"
            comp = "1"
            print("Standard job \"%sView - Long%s\" chosen." % (colbekijken, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "3" or functie[0].upper() == "M") and (functie[1].upper() in skiplijst or functie[1] == "1" or functie[1].upper() == "T"):    # 3: Wijzigen
            functie = "3"
            mot = "1"
            print("Standard job \"%sModify - Task%s\" chosen." % (colwijzigen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "3" or functie[0].upper() == "M") and (functie[1] == "2" or functie[1].upper() == "M"):
            functie = "3"
            mot = "2"
            print("Standard job \"%sModify - Member%s\" chosen." % (colwijzigen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "4" or functie[0].upper() == "D") and (functie[1].upper() in skiplijst or functie[1] == "3" or functie[1].upper() == "A"):    # 4: Verwijderen/Archiveren
            functie = "4"
            Wat = "3"
            print("Standard job \"%sDelete/archive - Archive%s\" chosen." % (colverwijderen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "4" or functie[0].upper() == "D") and (functie[1] == "1" or functie[1].upper() == "T"):
            functie = "4"
            Wat = "1"
            print("Standard job \"%sDelete/archive - Delete Task%s\" chosen." % (colverwijderen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "4" or functie[0].upper() == "D") and (functie[1] == "2" or functie[1].upper() == "M"):
            functie = "4"
            Wat = "2"
            print("Standard job \"%sDelete/archive - Delete Member%s\" chosen." % (colverwijderen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1].upper() in skiplijst or functie[1] == "1" or functie[1].upper() == "B"):    # 6: Reset RecordID's en Backup
            functie = "6"
            resetjn = "1"
            print("Standard job \"%sReset RecordID's and Backup: Backup All and Reset RecordID's%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "2"):
            functie = "6"
            resetjn = "2"
            print("Standard job \"%sReset RecordID's and Backup: Backup only Tasks list and Reset RecordID's%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "3"):
            functie = "6"
            resetjn = "3"
            print("Standard job \"%sReset RecordID's and Backup: Backup only Team%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "4"):
            functie = "6"
            resetjn = "4"
            print("Standard job \"%sReset RecordID's and Backup: Backup only Archive%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "5"):
            functie = "6"
            resetjn = "5"
            print("Standard job \"%sReset RecordID's and Backup: Backup only Notes (Team.txt)%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "6"):
            functie = "6"
            resetjn = "6"
            print("Standard job \"%sReset RecordID's and Backup: Rollback Tasks list%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "7"):
            functie = "6"
            resetjn = "7"
            print("Standard job \"%sReset RecordID's and Backup: Rollback Team%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "8"):
            functie = "6"
            resetjn = "8"
            print("Standard job \"%sReset RecordID's and Backup: Rollback Archive%s\" chosen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "9"):
            functie = "6"
            resetjn = "9"
            print("Standard job \"%sReset RecordID's and Backup: Rollback Notes (Team.txt)%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "9" or functie[0].upper() == "M") and (functie[1].upper() in skiplijst or functie[1] == "0" or functie[1].upper() == "N"):    # 9: Meeting
            functie = "9"
            Extra = "N"
            print("Standard job \"%sMeeting - No guests%s\" chosen." % (colcheck, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "0" or functie[0].upper() == "P") and (functie[1].upper() in skiplijst or functie[1].upper() in ["R","O"]):                   # 0: Presentielijst
            functie = "0"
            togglewie = "R"
            print("Standard job \"%sPresence list - Reset%s\" chosen." % (colcheck, ResetAll))
        elif functie == "":
            functie = "5"
    else:
        if len(functie) >= 2 and (functie[0] == "1" or functie[0].upper() == "T") and (functie[1].upper() in skiplijst or functie[1] == "1" or functie[1].upper() == "T"):    # 1: Toevoegen
            functie = "1"
            toe = "1"
            print("Standaardfunctie \"%sToevoegen - Taak%s\" gekozen." % (coltoevoegen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "1" or functie[0].upper() == "T") and (functie[1] == "2" or functie[1].upper() == "M"):
            functie = "1"
            toe = "2"
            print("Standaardfunctie \"%sToevoegen - Medewerker%s\" gekozen." % (coltoevoegen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "2" or functie[0].upper() == "B") and (functie[1].upper() in skiplijst or functie[1].upper() == "U"):                         # 2: Bekijken
            functie = "2"
            comp = "1"
            print("Standaardfunctie \"%sBekijken - Uitgebreid%s\" gekozen." % (colbekijken, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "3" or functie[0].upper() == "W") and (functie[1].upper() in skiplijst or functie[1] == "1" or functie[1].upper() == "T"):    # 3: Wijzigen
            functie = "3"
            mot = "1"
            print("Standaardfunctie \"%sWijzigen - Taak%s\" gekozen." % (colwijzigen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "3" or functie[0].upper() == "W") and (functie[1] == "2" or functie[1].upper() == "M"):
            functie = "3"
            mot = "2"
            print("Standaardfunctie \"%sWijzigen - Medewerker%s\" gekozen." % (colwijzigen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "4" or functie[0].upper() == "V") and (functie[1].upper() in skiplijst or functie[1] == "3" or functie[1].upper() == "A"):    # 4: Verwijderen/Archiveren
            functie = "4"
            Wat = "3"
            print("Standaardfunctie \"%sVerwijderen/archiveren - Archiveren%s\" gekozen." % (colverwijderen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "4" or functie[0].upper() == "V") and (functie[1] == "1" or functie[1].upper() == "T"):
            functie = "4"
            Wat = "1"
            print("Standaardfunctie \"%sVerwijderen/archiveren - Taak verwijderen%s\" gekozen." % (colverwijderen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "4" or functie[0].upper() == "V") and (functie[1] == "2" or functie[1].upper() == "M"):
            functie = "4"
            Wat = "2"
            print("Standaardfunctie \"%sVerwijderen/archiveren - Medewerker verwijderen%s\" gekozen." % (colverwijderen, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1].upper() in skiplijst or functie[1] == "1" or functie[1].upper() == "B"):    # 6: Reset RecordID's en Backup
            functie = "6"
            resetjn = "1"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Backup van alles en reset RecordID's%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "2"):
            functie = "6"
            resetjn = "2"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Backup alleen Takenlijst en reset RecordID's%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "3"):
            functie = "6"
            resetjn = "3"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Backup alleen Team%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "4"):
            functie = "6"
            resetjn = "4"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Backup alleen Archief%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "5"):
            functie = "6"
            resetjn = "5"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Backup alleen Algemene informatie (Team.txt)%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "6"):
            functie = "6"
            resetjn = "6"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Terugzetten backup Takenlijst%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "7"):
            functie = "6"
            resetjn = "7"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Terugzetten backup Team%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "8"):
            functie = "6"
            resetjn = "8"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Terugzetten backup Archief%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "6" or functie[0].upper() == "R") and (functie[1] == "9"):
            functie = "6"
            resetjn = "9"
            print("Standaardfunctie \"%sReset RecordID's en Backup: Terugzetten backup Algemene informatie (Team.txt)%s\" gekozen." % (colreset, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "9" or functie[0].upper() == "M") and (functie[1].upper() in skiplijst or functie[1] == "0" or functie[1].upper() == "G"):    # 9: Meeting
            functie = "9"
            Extra = "N"
            print("Standaardfunctie \"%sMeeting - Geen gasten%s\" gekozen." % (colcheck, ResetAll))
        elif len(functie) >= 2 and (functie[0] == "0" or functie[0].upper() == "P") and (functie[1].upper() in skiplijst or functie[1].upper() in ["R","U"]):                   # 0: Presentielijst
            functie = "0"
            togglewie = "R"
            print("Standaardfunctie \"%sPresentielijst - Reset%s\" gekozen." % (colcheck, ResetAll))
        elif functie == "":
            functie = "5"

    # 1: TOEVOEGEN
    if functie == "1" or functie[0].upper() == "T":
        col = coltoevoegen
        insert = "Y"
        while insert == "Y":
            if toe not in ["1","2"]:
                if lang == "EN":
                    toe = input("%sDo you want to add a Task or a Member?%s\n%s  > 1: Task%s\n    2: Member\n%s  : " % (col,ResetAll,col,ResetAll,terug))
                else:
                    toe = input("%sWil je een Taak of een Medewerker toevoegen?%s\n%s  > 1: Taak%s\n    2: Medewerker\n%s  : " % (col,ResetAll,col,ResetAll,terug))
            if toe.upper() in afsluitlijst or toe.upper() in neelijst:
                break
            elif len(toe) == 2 and (toe[0].upper() in afsluitlijst or toe[0].upper() in neelijst) and toe[1].upper() in skiplijst:
                if lang == "EN":
                    toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                else:
                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                if toch.upper() in jalijst:
                    if lang == "EN":
                        print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                    else:
                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                    exit()
            # 1: TOEVOEGEN - 1: taak = default = else = "1!"
            # 1: TOEVOEGEN - 2: medewerker
            elif toe == "2" or toe.upper() == "M":
                medewerker = "Y"
                while medewerker == "Y":
                    voor = "Y"
                    while voor == "Y":
                        if lang == "EN":
                            voorNaam = input("Type the %sGiven name%s (max 25 characters):\n  : " % (col,ResetAll))
                        else:
                            voorNaam = input("Typ de %sVoornaam%s (max 25 karakters):\n  : " % (col,ResetAll))
                        if voorNaam.upper() in afsluitlijst or voorNaam.upper() in neelijst:
                            voor = "X"
                            break
                        elif len(voorNaam) == 2 and (voorNaam[0].upper() in afsluitlijst or voorNaam[0].upper() in neelijst) and voorNaam[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif len(voorNaam) > 25:
                            if lang == "EN":
                                print("This Given name is too long. Abbreviate it.")
                            else:
                                print("Deze Voornaam is te lang. Kort hem af.")
                        elif voorNaam == "?":
                            cur.execute("SELECT * FROM team")
                            Lijst = from_db_cursor(cur)
                            Lijst.align = "l"
                            Lijst.align[clteam[4]] = "r"
                            print(Lijst.get_string(sort_key=operator.itemgetter(1, 0), sortby=clteam[0]))
                        else:    
                            cur.execute("SELECT %s FROM team where %s='%s';" % (clteam[0], clteam[0], voorNaam))
                            vn = str(cur.fetchall()).replace("[","").replace("(","").replace(")","").replace("]","").replace("'","").replace(",","")
                            if voorNaam.rfind(" ") == -1 and voorNaam.rfind("-") == -1:
                                VN = voorNaam[0]+voorNaam[-1]
                                voor = "N"
                            elif voorNaam.rfind(" ") != -1:
                                VN = voorNaam[0]+voorNaam[voorNaam.rfind(" ")+1]
                                voor = "N"
                            elif voorNaam.rfind("-") != -1:
                                VN = voorNaam[0]+voorNaam[voorNaam.rfind("-")+1]
                                voor = "N"
                            else:
                                if lang == "EN":
                                    print("There is something odd with this given name, try again.")
                                else:
                                    print("Er is iets vreemds met deze voornaam, probeer het opnieuw.")
                            vnbestaatal = "N"
                            if voorNaam == vn:
                                vnbestaatal = "Y"
                                if lang == "EN":
                                    print("Attention: Given name \"%s\" already exists:" % voorNaam)
                                else:
                                    print("Let op: Voornaam \"%s\" bestaat al:" % voorNaam)
                                cur.execute("SELECT * FROM team where %s='%s';" % (clteam[0], voorNaam))
                                voornaammatch = from_db_cursor(cur)
                                voornaammatch.align = "l"
                                voornaammatch.align[clteam[4]] = "r"
                                print(voornaammatch)
                    if voor == "X":
                        medewerker = "X"
                        break
                    achter = "Y"
                    while achter == "Y":
                        if lang == "EN":
                            achterNaam = input("Type the %sFamily name%s (max 25 characters):\n  : " % (col,ResetAll))
                        else:
                            achterNaam = input("Typ de %sAchternaam%s (max 25 karakters):\n  : " % (col,ResetAll))
                        if achterNaam.upper() in afsluitlijst or achterNaam.upper() in neelijst:
                            achter = "X"
                            break
                        elif len(achterNaam) == 2 and (achterNaam[0].upper() in afsluitlijst or achterNaam[0].upper() in neelijst) and achterNaam[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif len(achterNaam) > 25:
                            if lang == "EN":
                                print("This Family name is too long. Abbreviate it.")
                            else:
                                print("Deze Achternaam is te lang. Kort hem af.")
                        cur.execute("SELECT %s FROM team where %s='%s';" % (clteam[2], clteam[2], achterNaam))
                        an = str(cur.fetchall()).replace("[","").replace("(","").replace(")","").replace("]","").replace("'","").replace(",","")
                        if achterNaam.rfind(" ") == -1 and achterNaam.rfind("-") == -1:
                            AN = achterNaam[:2]
                            achter = "N"
                        elif achterNaam.rfind(" ") != -1:
                            AN = achterNaam[0]+achterNaam[achterNaam.rfind(" ")+1]
                            achter = "N"
                        elif achterNaam.rfind("-") != -1:
                            AN = achterNaam[0]+achterNaam[achterNaam.rfind("-")+1]
                            achter = "N"
                        else:
                            if lang == "EN":
                                print("There is something odd with this family name, try again.")
                            else:
                                print("Er is iets vreemds met deze achternaam, probeer het opnieuw.")
                        anbestaatal = "N"
                        if achterNaam == an:
                            anbestaatal = "Y"
                            if lang == "EN":
                                print("Attention: Family name \"%s\" already exists:" % achterNaam)
                            else:
                                print("Let op: Achternaam \"%s\" bestaat al:" % achterNaam)
                            cur.execute("SELECT * FROM team where %s='%s';" % (clteam[2], achterNaam))
                            achternaammatch = from_db_cursor(cur)
                            achternaammatch.align = "l"
                            achternaammatch.align[clteam[4]] = "r"
                            print(achternaammatch)
                    if achter == "X":
                        medewerker = "X"
                        break
                    nummer = "Y"
                    while nummer == "Y":
                        if lang == "EN":
                            Nummer = input("Type the %sAgent Number%s (numerical):\n  : " % (col,ResetAll))
                        else:
                            Nummer = input("Typ het %sPersoneelsNummer%s (numeriek):\n  : " % (col,ResetAll))
                        if Nummer.upper() in afsluitlijst or Nummer.upper() in neelijst:
                            nummer = "X"
                        elif len(nummer) == 2 and (nummer[0].upper() in afsluitlijst or nummer[0].upper() in neelijst) and nummer[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            try:
                                Nummer = str(int(Nummer))
                                cur.execute("SELECT %s FROM team where %s='%s';" % (clteam[4], clteam[4], Nummer))
                                pn = str(cur.fetchall()).replace("[","").replace("(","").replace(")","").replace("]","").replace("'","").replace(",","")
                                pnbestaatal = "N"
                                if Nummer == pn:
                                    pnbestaatal = "Y"
                                    if lang == "EN":
                                        print("Attention: Agent Number \"%s\" already exists:" % Nummer)
                                    else:
                                        print("Let op: PersoneelsNummer \"%s\" bestaat al:" % Nummer)
                                    cur.execute("SELECT * FROM team where %s='%s';" % (clteam[4], Nummer))
                                    nummermatch = from_db_cursor(cur)
                                    nummermatch.align = "l"
                                    nummermatch.align[clteam[4]] = "r"
                                    print(nummermatch)
                                else:
                                    nummer = "N"
                            except:
                                if lang == "EN":
                                    print("An Agent Number can only contain digits.")
                                else:
                                    print("Een PersoneelsNummer mag alleen cijfers bevatten.")
                    if nummer == "X":
                        medewerker = "X"
                        break
                    aant = "Y"
                    while aant == "Y":
                        if lang == "EN":
                            Aantekening = input("Add a %sNote%s (optional, max. 25 characters):\n  : " % (col,ResetAll))
                        else:
                            Aantekening = input("Voeg een %sAantekening%s toe (optioneel, max. 25 karakters):\n  : " % (col,ResetAll))
                        if Aantekening.upper() in afsluitlijst or Aantekening.upper() in neelijst:
                            aant = "X"
                        elif len(Aantekening) == 2 and (Aantekening[0].upper() in afsluitlijst or Aantekening[0].upper() in neelijst) and Aantekening[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            aant = "OK"
                    if aant == "X":
                        break
                    print(voorNaam, VN, achterNaam, AN, Nummer,Aantekening)
                    if pnbestaatal == "Y":
                        if lang == "EN":
                            print("This Agent Number already exists and must be unique. Correct your entry.")
                        else:
                            print("Dit PersoneelsNummer bestaat al en moet uniek zijn. Pas de gegevens aan.")
                    elif vnbestaatal == "Y" and anbestaatal == "Y":
                        if lang == "EN":
                            print("This member already exists and will not be added.")
                        else:
                            print("Deze medewerker bestaat al en zal niet worden toegevoegd.")
                    else:
                        if lang == "EN":
                            ok = input("Is this right?\n%s  > 1: Yes, add to the list and abort%s\n%s    2: Yes, add and again%s\n    3: No, let me correct\n    4: No, never mind, abort\n  : " % (col,ResetAll,col,ResetAll))
                        else:
                            ok = input("Klopt dit?\n%s  > 1: Ja, toevoegen aan lijst en hier uit%s\n%s    2: Ja, toevoegen en nogmaals%s\n    3: Nee, corrigeren alstublieft\n    4: Nee, laat maar\n  : " % (col,ResetAll,col,ResetAll))
                        if ok.upper() in afsluitlijst or ok.upper() in neelijst:
                            medewerker = "N"
                            insert = "N"
                        elif len(ok) == 2 and (ok[0].upper() in afsluitlijst or ok[0].upper() in neelijst) and ok[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif ok == "1" or ok == "":
                            cur.execute("INSERT INTO team (%s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5],voorNaam,VN,achterNaam,AN,Nummer,Aantekening))
                            con.commit()
                            cur.execute("SELECT * FROM team where %s='%s';" % (clteam[4], Nummer))
                            nieuw = from_db_cursor(cur)
                            nieuw.align = "l"
                            nieuw.align[clteam[4]] = "r"
                            print(nieuw)
                            medewerker = "N"
                            insert = "N"
                        elif ok == "2":
                            cur.execute("INSERT INTO team (%s, %s, %s, %s, %s, %s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5],voorNaam,VN,achterNaam,AN,Nummer,Aantekening))
                            con.commit()
                            cur.execute("SELECT * FROM team where %s='%s';" % (clteam[4], Nummer))
                            nieuw = from_db_cursor(cur)
                            nieuw.align = "l"
                            nieuw.align[clteam[4]] = "r"
                            print(nieuw)
                        elif ok == "3":
                            pass
                        elif ok == "4":
                            medewerker = "N"
                            insert = "N"
                if medewerker == "X":
                    break
            # 1: TOEVOEGEN - 1: taak = default = else = "1>"
            else:
                if lang == "EN":
                    print("%sChoose \"x\" to \"Abort\".%s" % (colterug,ResetAll))
                    print("The default period for a new Task is (today + ) 7 days")
                else
                    print("%sKies \"x\" voor \"Afbreken\".%s" % (colterug,ResetAll))
                    print("De standaardperiode van een nieuwe Taak is (vandaag + ) 7 dagen")
                taak = "Y"
                while taak == "Y":
                    start = "Y"
                    while start == "Y":
                        if lang == "EN":
                            startDatum = input("Enter the %sStart date%s (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                        else:
                            startDatum = input("Voer de %sBegindatum%s in (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                        if startDatum.upper() in afsluitlijst or startDatum.upper() in neelijst:
                            start = "X"
                            taak = "X"
                        elif len(startDatum) == 2 and (startDatum[0].upper() in afsluitlijst or startDatum[0].upper() in neelijst) and startDatum[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif startDatum == "":
                            datumStart = nu
                            print(datumStart)
                            start = "N"
                        else:
                            try:
                                datumStart = int(startDatum[:4]+startDatum[4:6]+startDatum[6:])
                                datetime.strptime(str(datumStart),"%Y%m%d")
                                start = "N"
                            except:
                                if lang == "EN":
                                    print("That is not a valid date, try again.") # startDatum
                                else:
                                    print("Dat is geen geldige datum, probeer het opnieuw.") # startDatum
                    if start == "X":
                        taak = "X"
                        break
                    stop = "Y"
                    while stop == "Y":
                        if lang == "EN":
                            stopDatum = input("Enter the %sEnd date%s (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                        else:
                            stopDatum = input("Voer de %sEinddatum%s in (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                        if stopDatum.upper() in afsluitlijst or stopDatum.upper() in neelijst:
                            stop = "X"
                        elif len(stopDatum) == 2 and (stopDatum[0].upper() in afsluitlijst or stopDatum[0].upper() in neelijst) and stopDatum[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif stopDatum == "":
                            if lang == "EN":
                                print("The default period %s7 days%s is chosen." % (col,ResetAll))
                            else:
                                print("De standaardperiode %s7 dagen%s is gekozen." % (col,ResetAll))
                            datumStop = datetime.strftime(datetime.strptime(str(datumStart),"%Y%m%d")+timedelta(days=7),"%Y%m%d")
                            print(datumStop)
                            stop = "N"
                        else:
                            try:
                                datumStop = int(stopDatum[:4]+stopDatum[4:6]+stopDatum[6:])
                                if stopDatum >= startDatum:
                                    datetime.strptime(str(datumStop),"%Y%m%d")
                                    stop = "N"
                                else:
                                    if lang == "EN":
                                        print("The End date is before the Start date, that is wrong.")
                                    else:
                                        print("De Einddatum ligt vóór de Begindatum, dat kan niet.")
                            except:
                                if lang == "EN":
                                    print("That is not a valid date, try again.") # stopDatum
                                else:
                                    print("Dat is geen geldige datum, probeer het opnieuw.") # stopDatum
                    if stop == "X":
                        break
                    omschrijvingTaak = "Y"
                    while omschrijvingTaak == "Y":
                        if lang == "EN":
                            taakOmschrijving = input("Enter a %sTask description%s:\n  : " % (col,ResetAll))
                        else:
                            taakOmschrijving = input("Voer een %sTaakomschrijving%s in:\n  : " % (col,ResetAll))
                        if taakOmschrijving.upper() in afsluitlijst or taakOmschrijving.upper() in neelijst:
                            omschrijvingTaak = "X"
                        elif len(taakOmschrijving) == 2 and (taakOmschrijving[0].upper() in afsluitlijst or taakOmschrijving[0].upper() in neelijst) and taakOmschrijving[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif len(taakOmschrijving) < 5:
                            if lang == "EN":
                                print("Task description is mandatory. Enter at least 5 characters.")
                            else:
                                print("Taakomschrijving is verplicht. Geef tenminste 5 karakters op.")
                        else:
                            omschrijvingTaak = "N"
                    if omschrijvingTaak == "X":
                        break
                    werkerMede = "Y"
                    while werkerMede == "Y":
                        if lang == "EN":
                            voornaamPersoneels = input("Enter (a part of) the member's %sGiven name%s or \"?\" for a list:\n  : " % (col,ResetAll))
                        else:
                            voornaamPersoneels = input("Voer (een deel van) de %sVoornaam%s van de medewerker in of \"?\" voor een lijst:\n  : " % (col,ResetAll))
                        if voornaamPersoneels.upper() in afsluitlijst or voornaamPersoneels.upper() in neelijst:
                            werkerMede = "X"
                        elif len(voornaamPersoneels) == 2 and (voornaamPersoneels[0].upper() in afsluitlijst or voornaamPersoneels[0].upper() in neelijst) and voornaamPersoneels[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif voornaamPersoneels == "?":
                            cur.execute("SELECT * FROM team")
                            Lijst = from_db_cursor(cur)
                            Lijst.align = "l"
                            Lijst.align[clteam[4]] = "r"
                            print(Lijst.get_string(sort_key=operator.itemgetter(1, 0), sortby=clteam[0]))
                        else:
                            cur.execute("SELECT %s FROM team WHERE %s LIKE '%%%s%%';" % (clteam[0],clteam[0],voornaamPersoneels))
                            voorNamenLijst = cur.fetchall()
                            medewerkerNaam = str(voorNamenLijst).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
                            print(medewerkerNaam)
                            cur.execute("SELECT %s FROM team WHERE %s LIKE '%%%s%%';" % (clteam[4],clteam[0],voornaamPersoneels))
                            voorNummerLijst = cur.fetchall()
                            personeelsNummerLijst = str(voorNummerLijst).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").split(",")
                            personeelsNummer = str(voorNummerLijst).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","")
                            if len(voorNamenLijst) == 0:
                                if lang == "EN":
                                    print("I don't know that member.")
                                else:
                                    print("Die medewerker ken ik niet.")
                            elif len(voorNamenLijst) == 1:
                                werkerMede = "N"
                            else:
                                cur.execute("SELECT * FROM team WHERE %s LIKE '%%%s%%';" % (clteam[0],voornaamPersoneels))
                                medewNamenLijst = from_db_cursor(cur)
                                medewNamenLijst.align = "l"
                                medewNamenLijst.align[clteam[4]] = "r"
                                print(medewNamenLijst)
                                if lang == "EN":
                                    Nummert = input("Type the right member's Agent Number:\n  : ")
                                else:
                                    Nummert = input("Typ het PersoneelsNummer van de juiste medewerker:\n  : ")
                                if Nummert.upper() in afsluitlijst or Nummert.upper() in neelijst:
                                    werkerMede = "X"
                                elif len(Nummert) == 2 and (Nummert[0].upper() in afsluitlijst or Nummert[0].upper() in neelijst) and Nummert[1].upper() in skiplijst:
                                    if lang == "EN":
                                        toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                                    else:
                                        toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        if lang == "EN":
                                            print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                        else:
                                            print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                elif Nummert not in personeelsNummerLijst:
                                if lang == "EN":
                                    print("I don't know that member.")
                                else:
                                    print("Die medewerker ken ik niet.")
                                else:
                                    cur.execute("SELECT %s FROM team WHERE %s = '%s';" % (clteam[4],clteam[4],Nummert))
                                    NummertLijst = cur.fetchall()
                                    personeelsNummer = str(NummertLijst).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
                                    print(personeelsNummer)
                                    cur.execute("SELECT %s FROM team WHERE %s = '%s';" % (clteam[0],clteam[4],Nummert))
                                    NaamLijst = cur.fetchall()
                                    medewerkerNaam = str(NaamLijst).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
                                    cur.execute("SELECT * FROM team WHERE %s = '%s';" % (clteam[4],Nummert))
                                    NaampLijst = from_db_cursor(cur)
                                    medewerkerVANaam = str(NaampLijst).replace("[","").replace("]","").replace("(","").replace(")","").replace("'","").replace(",","")
                                    print(medewerkerVANaam)
                                    werkerMede = "N"
                    if werkerMede == "X":
                        break
                    voortgang = "Y"
                    while voortgang == "Y":
                        if lang == "EN":
                            preStatus = input("Choose one of the following %sStatuses%s:\n    %s\n    %s\n    %s\n    %s\n    %s\n    %s\n  : " % (col,ResetAll,statuslijst[0],statuslijst[1],statuslijst[2],statuslijst[3],statuslijst[4],statuslijst[5]))
                        else:
                            preStatus = input("Kies uit één van de volgende %sStatussen%s:\n    %s\n    %s\n    %s\n    %s\n    %s\n    %s\n  : " % (col,ResetAll,statuslijst[0],statuslijst[1],statuslijst[2],statuslijst[3],statuslijst[4],statuslijst[5]))
                        if preStatus.upper() in afsluitlijst or preStatus.upper() in neelijst:
                            voortgang = "X"
                        elif len(preStatus) == 2 and (preStatus[0].upper() in afsluitlijst or preStatus[0].upper() in neelijst) and preStatus[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif preStatus == "":
                            if int(datumStart) > int(nu):
                                Status = statuslijst[0]
                                print(Status)
                                voortgang = "N"
                            elif int(datumStart) <= int(nu) and int(datumStop) > int(nu):
                                Status = statuslijst[1]
                                print(Status)
                                voortgang = "N"
                            else:
                                if lang == "EN":
                                    print("A default Status could not be set.")
                                else:
                                    print("Er kon geen standaardStatus worden aangemaakt.")
                        elif preStatus == "0":
                            Status = statuslijst[0]
                            print(Status)
                            voortgang = "N"
                        elif preStatus == "1":
                            Status = statuslijst[1]
                            print(Status)
                            voortgang = "N"
                        elif preStatus == "2":
                            Status = statuslijst[2]
                            print(Status)
                            voortgang = "N"
                        elif preStatus == "3":
                            Status = statuslijst[3]
                            print(Status)
                            voortgang = "N"
                        elif preStatus == "4":
                            Status = statuslijst[4]
                            print(Status)
                            voortgang = "N"
                        elif preStatus == "5":
                            Status = statuslijst[5]
                            print(Status)
                            voortgang = "N"
                        else:
                            if lang == "EN":
                                print("I cannot make a Status out of that.")
                            else:
                                print("Daar kan ik geen Status van maken.")
                            Status = ""
                    if voortgang == "X":
                        break
                    aantekening = "Y"
                    while aantekening == "Y":
                        if lang == "EN":
                            Opmerking = input("Room for %sNotes%s:\n  : " % (col,ResetAll))
                        else:
                            Opmerking = input("Ruimte voor %sOpmerkingen%s:\n  : " % (col,ResetAll))
                        if Opmerking.upper() in afsluitlijst or Opmerking.upper() in neelijst:
                            aantekening = "X"
                        elif len(Opmerking) == 2 and (Opmerking[0].upper() in afsluitlijst or Opmerking[0].upper() in neelijst) and Opmerking[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            aantekening = "N"
                    if aantekening == "X":
                        break
                    toevoegen = "Y"
                    while toevoegen == "Y":
                        print(startDatum, stopDatum, taakOmschrijving, medewerkerNaam, personeelsNummer, Opmerking)
                        if lang == "EN":
                            goed = input("These data are valid, shall I register them?\n%s  > 1: Yes%s\n    2: No\n  : " % (col,ResetAll))
                        else:
                            goed = input("Deze gegevens zijn geldig, zal ik die registreren?\n%s  > 1: Ja%s\n    2: Nee\n  : " % (col,ResetAll))
                        if goed.upper() in afsluitlijst or goed.upper() in neelijst:
                            toevoegen = "X"
                        elif len(goed) == 2 and (goed[0].upper() in afsluitlijst or goed[0].upper() in neelijst) and goed[1].upper() in skiplijst:
                            if lang == "EN":
                                toch = input("Are you %s?\n  : " % (colslecht+"sure"+ResetAll))
                            else:
                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                if lang == "EN":
                                    print("\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll))
                                else:
                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif goed == "1" or goed.upper() in jalijst or goed == "":
                            try:
                                cur.execute("INSERT INTO takenlijst (%s, %s, %s, %s, %s, %s) VALUES ('%s','%s','%s','%s','%s','%s');" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],datumStart, datumStop, taakOmschrijving, personeelsNummer, Status, Opmerking))
                                con.commit()
                                cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[3],taakOmschrijving))
                                geinput = from_db_cursor(cur)
                                geinput.align = "l"
                                geinput.align[cltakenlijst[0]] = "m"
                                geinput.align[clteam[4]] = "r"
                                print(geinput)
                                toevoegen = "X"
                            except (Exception) as error:
                                print(error)
                        elif goed == "2" or goed.upper() in neelijst:
                            toevoegen = "X"
                        if toevoegen == "X":
                            break
                if taak == "X":
                    break
        if insert == "X":
            break

    # 2: BEKIJKEN
    elif functie == "2" or functie[0].upper() == "B":
        col = colbekijken
        kijk = "Y"
        while kijk == "Y":
            comp = "1"
            if comp.upper() in afsluitlijst or comp.upper() in neelijst:
                break
            elif len(comp) == 2 and (comp[0].upper() in afsluitlijst or comp[0].upper() in neelijst) and comp[1].upper() in skiplijst:
                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                if toch.upper() in jalijst:
                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                    exit()
            elif comp == "2" or comp.upper() == "C":
                comp = "2"
            # update alle Omschrijvingen naar Statuskleur
            cur.execute("SELECT COUNT(%s) FROM takenlijst;" % (cltakenlijst[0]))
            reccount = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","")
            print("\nEr staan %s%s records%s in de database." % (col,reccount,ResetAll))
            cur.execute("SELECT %s FROM takenlijst;" % (cltakenlijst[0]))
            reclist = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","").split(",")
            for i in reclist:
                cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[5],cltakenlijst[0],i))
                stcol = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","").replace(",","")
                if stcol[4:7] == colstat0[2:]:
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[3],cltakenlijst[0],i))
                    oms0all = str(cur.fetchall())
                    oms0kaal = oms0all.replace("[","").replace("]","").replace("(","").replace(",)","").replace("'","").replace("\\","").replace("","").replace("x1b"+colstat0[2:],"").replace("x1b"+colstat1[2:],"").replace("x1b"+colstat2[2:],"").replace("x1b"+colstat3[2:],"").replace("x1b"+colstat4[2:],"").replace("x1b"+colstat5[2:],"").replace("x1b"+ResetAll[2:],"")
                    coloms = colstat0+oms0kaal[:5]+ResetAll+oms0kaal[5:]
                elif stcol[4:7] == colstat1[2:]:
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[3],cltakenlijst[0],i))
                    oms1all = str(cur.fetchall())
                    oms1kaal = oms1all.replace("[","").replace("]","").replace("(","").replace(",)","").replace("'","").replace("\\","").replace("","").replace("x1b"+colstat0[2:],"").replace("x1b"+colstat1[2:],"").replace("x1b"+colstat2[2:],"").replace("x1b"+colstat3[2:],"").replace("x1b"+colstat4[2:],"").replace("x1b"+colstat5[2:],"").replace("x1b"+ResetAll[2:],"")
                    coloms = colstat1+oms1kaal[:5]+ResetAll+oms1kaal[5:]
                elif stcol[4:7] == colstat2[2:]:
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[3],cltakenlijst[0],i))
                    oms2all = str(cur.fetchall())
                    oms2kaal = oms2all.replace("[","").replace("]","").replace("(","").replace(",)","").replace("'","").replace("\\","").replace("","").replace("x1b"+colstat0[2:],"").replace("x1b"+colstat1[2:],"").replace("x1b"+colstat2[2:],"").replace("x1b"+colstat3[2:],"").replace("x1b"+colstat4[2:],"").replace("x1b"+colstat5[2:],"").replace("x1b"+ResetAll[2:],"")
                    coloms = colstat2+oms2kaal[:5]+ResetAll+oms2kaal[5:]
                elif stcol[4:7] == colstat3[2:]:
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[3],cltakenlijst[0],i))
                    oms3all = str(cur.fetchall())
                    oms3kaal = oms3all.replace("[","").replace("]","").replace("(","").replace(",)","").replace("'","").replace("\\","").replace("","").replace("x1b"+colstat0[2:],"").replace("x1b"+colstat1[2:],"").replace("x1b"+colstat2[2:],"").replace("x1b"+colstat3[2:],"").replace("x1b"+colstat4[2:],"").replace("x1b"+colstat5[2:],"").replace("x1b"+ResetAll[2:],"")
                    coloms = colstat3+oms3kaal[:5]+ResetAll+oms3kaal[5:]
                elif stcol[4:7] == colstat4[2:]:
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[3],cltakenlijst[0],i))
                    oms4all = str(cur.fetchall())
                    oms4kaal = oms4all.replace("[","").replace("]","").replace("(","").replace(",)","").replace("'","").replace("\\","").replace("","").replace("x1b"+colstat0[2:],"").replace("x1b"+colstat1[2:],"").replace("x1b"+colstat2[2:],"").replace("x1b"+colstat3[2:],"").replace("x1b"+colstat4[2:],"").replace("x1b"+colstat5[2:],"").replace("x1b"+ResetAll[2:],"")
                    coloms = colstat4+oms4kaal[:5]+ResetAll+oms4kaal[5:]
                elif stcol[4:7] == colstat5[2:]:
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[3],cltakenlijst[0],i))
                    oms5all = str(cur.fetchall())
                    oms5kaal = oms5all.replace("[","").replace("]","").replace("(","").replace(",)","").replace("'","").replace("\\","").replace("","").replace("x1b"+colstat0[2:],"").replace("x1b"+colstat1[2:],"").replace("x1b"+colstat2[2:],"").replace("x1b"+colstat3[2:],"").replace("x1b"+colstat4[2:],"").replace("x1b"+colstat5[2:],"").replace("x1b"+ResetAll[2:],"")
                    coloms = colstat5+oms5kaal[:5]+ResetAll+oms5kaal[5:]
                else:
                    "Er ging ies mis bij het bepalen van de Status."
                    break
                cur.execute("UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[3],coloms,cltakenlijst[0],i))
                con.commit()
            # Update alle taken met status "1: gestart" naar "5: verlopen" als de Eind < datum van vandaag -1
            cur.execute("SELECT %s FROM takenlijst WHERE %s < %d AND (%s = '%s' OR %s = '%s');" % (cltakenlijst[0],cltakenlijst[2],int(nu),cltakenlijst[5],statuslijst[0],cltakenlijst[5],statuslijst[1]))
            verlopen = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","").split(",")
            try:
                for i in verlopen:
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = %s;" % (cltakenlijst[6],cltakenlijst[0],i))
                    oudeAant = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace("","").replace("'","").replace("\\x1b33m",colstat0).replace("\\x1b93m",colstat1).replace("\\x1b35m",colstat2).replace("\\x1b31m",colstat3).replace("\\x1b32m",colstat4).replace("\\x1b91m",colstat5).replace("\\x1b96m",colwijzigen).replace("\\x1b0m",ResetAll)
                    cur.execute("SELECT %s FROM takenlijst WHERE %s = %s;" % (cltakenlijst[5],cltakenlijst[0],i))
                    oudeStatus = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace("","").replace("'","").replace("\\x1b33m",colstat0).replace("\\x1b93m",colstat1).replace("\\x1b35m",colstat2).replace("\\x1b31m",colstat3).replace("\\x1b32m",colstat4).replace("\\x1b91m",colstat5).replace("\\x1b0m",ResetAll)
                    #nieuweAant = "%s: " % (nu)+ "%s" % (oudeStatus)+ "%s -> %s" % (colwijzigen,ResetAll)+  "%s" % (statuslijst[5])+ " \"%s\"" % (oudeAant)
                    nieuweAant = "%s: %s%s -> %s%s \"%s\"" % (nu[4:],oudeStatus,colwijzigen,ResetAll,statuslijst[5],oudeAant)
                    cur.execute("UPDATE takenlijst SET %s = '%s', %s = '%s' WHERE %s = '%s'" % (cltakenlijst[5],statuslijst[5],cltakenlijst[6],nieuweAant,cltakenlijst[0],i))
                    con.commit()
            except:
                pass
            # Lijst alle verlopen en te laat gestarte taken
            if comp == "2":
                curseloverStart = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE %s = '%s';" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[5],statuslijst[5])
            else:
                curseloverStart = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE %s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[5],statuslijst[5])
            cur.execute(curseloverStart)
            fetchalloverStart = str(cur.fetchall()).replace(" ","").replace("[","").replace("]","").replace("(","").replace(")","").split(",")
            if len(fetchalloverStart) != 1: 
                print("%sTaken mat status \"%s%s%s\":%s" % (colslecht,ResetAll,statuslijst[5],colslecht,ResetAll))
                cur.execute(curseloverStart)
                aandachtoverStart = from_db_cursor(cur)
                aandachtoverStart.align = "l"
                aandachtoverStart.align[clteam[4]] = "r"
                aandachtoverStart.align[cltakenlijst[0]] = "m"
                aandachtoverStart.align[cltakenlijst[0][:3]] = "m"
                print(aandachtoverStart)
                print("Kies %sx: Afsluiten%s - %s3: Wijzigen%s om dit te corrigeren of %sx: Afsluiten%s - %s4: Verwijderen%s om deze te verwijderen." % (colterug,ResetAll,colwijzigen,ResetAll,colterug,ResetAll,colverwijderen,ResetAll))
            if comp == "2":
                curseloverStart = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE %s <= %d AND %s = '%s';" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[1],int(nu),cltakenlijst[5],statuslijst[0])
            else:
                curseloverStart = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE %s <= %d AND %s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[1],int(nu),cltakenlijst[5],statuslijst[0])
            cur.execute(curseloverStart)
            fetchalloverStart = str(cur.fetchall()).replace(" ","").replace("[","").replace("]","").replace("(","").replace(")","").split(",")
            if len(fetchalloverStart) != 1: 
                print("%sTaken die nog niet zijn \"%s%s%s\":%s" % (colslecht,ResetAll,statuslijst[1],colslecht,ResetAll))
                cur.execute(curseloverStart)
                aandachtoverStart = from_db_cursor(cur)
                aandachtoverStart.align = "l"
                aandachtoverStart.align[clteam[4]] = "r"
                aandachtoverStart.align[cltakenlijst[0]] = "m"
                aandachtoverStart.align[cltakenlijst[0][:3]] = "m"
                print(aandachtoverStart)
                print("Kies %sx: Afsluiten%s - %s3: Wijzigen%s om dit te corrigeren of %sx: Afsluiten%s - %s4: Verwijderen%s om deze te verwijderen." % (colterug,ResetAll,colwijzigen,ResetAll,colterug,ResetAll,colverwijderen,ResetAll))

            if comp != "2":
                print("Taken gesorteerd op %sStatus:%s" % (col,ResetAll))
                statlist = []
                Stat = PrettyTable([cltakenlijst[5],"#"])
                Stat.align[cltakenlijst[5]] = "l"
                Stat.align["#"] = "r"
                for i in statuslijst:
                    cur.execute("SELECT COUNT(%s) FROM takenlijst WHERE %s = '%s'" % (cltakenlijst[0],cltakenlijst[5],i))
                    j = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(")","").replace(" ","").replace("'","").replace(",","")
                    Stat.add_row([i,j])
                print(Stat)
                print("Taken gesorteerd op %sMedewerker%s:" % (col,ResetAll))
                Stat = PrettyTable([clteam[0],clteam[2],"#"])
                Stat.align[clteam[0]] = "l"
                Stat.align[clteam[2]] = "l"
                Stat.align["#"] = "r"
                cur.execute("SELECT %s FROM team;" % (clteam[4]))
                preteamlijst = cur.fetchall()
                teamlijst = str(preteamlijst).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","").split(",")
                for i in teamlijst:
                    cur.execute("SELECT COUNT(m.%s) FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s' ORDER BY %s ASC" % (cltakenlijst[0],cltakenlijst[4],clteam[4],cltakenlijst[4],i,clteam[0]))
                    j = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(")","").replace("","").replace("'","").replace(",","")
                    cur.execute("SELECT %s FROM team WHERE %s = '%s'" % (clteam[0],clteam[4],i))
                    k = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(")","").replace("","").replace("'","").replace(",","")
                    cur.execute("SELECT %s FROM team WHERE %s = '%s'" % (clteam[2],clteam[4],i))
                    l = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(")","").replace("","").replace("'","").replace(",","")
                    Stat.add_row([k,l,j])
                print(Stat)
            # SELECteam
            selectie = "Y"
            while selectie == "Y":
                keuze = input("\n%sOp welke criteria wil je verder selecteren?%s\n    0: %s\n    1: %s\n    2: %s\n    3*:%s\n    4*:%s\n    5*:%s\n    6: %s\n%s  > 7: %s%s\n    8*:%s\n    G: %s\n    C: %s\n%s    U: %s%s\n%s  : " % (col, ResetAll,cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],col,cltakenlijst[5],ResetAll,cltakenlijst[6],"Gearchiveerd","Compact",col,"Uitgebreid",ResetAll,terug))
                #print("Kies \"C\" of \"V\" om te schakelen tussen \"Compacte\" en \"Volledige\" modus.")
                if keuze.upper() in afsluitlijst or keuze.upper() in neelijst:
                    kijk = "X"
                    break
                elif len(keuze) == 2 and (keuze[0].upper() in afsluitlijst or keuze[0].upper() in neelijst) and keuze[1].upper() in skiplijst:
                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                    if toch.upper() in jalijst:
                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                        exit()
                elif keuze == "":
                    keuze = "7"
                if keuze.upper() == "U":
                    comp = "1"
                elif keuze.upper() == "C":
                    comp = "2"
                elif keuze == "0" or keuze[0].upper() == "R":
                    cur.execute("SELECT %s FROM takenlijst;" % cltakenlijst[0])
                    reclist = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").split(",")
                    record = "Y"
                    while record == "Y":
                        Record = input("Voer het %sRecordnummer%s in:\n  : " % (col,ResetAll))
                        if Record.upper() in afsluitlijst or Record.upper() in neelijst:
                            record = "X"
                        elif len(Record) == 2 and (Record[0].upper() in afsluitlijst or Record[0].upper() in neelijst) and Record[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif Record not in reclist:
                            print("Dat is geen geldig Recordnummer")
                        else:
                            try:
                                Record = int(Record)
                                if comp == "2":
                                    cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[0],Record,cltakenlijst[0])
                                else:
                                    cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],Record,cltakenlijst[0])
                                cur.execute(cursel)
                                selectieRec = from_db_cursor(cur)
                                selectieRec.align = "l"
                                selectieRec.align[clteam[4]] = "r"
                                selectieRec.align[cltakenlijst[0]] = "m"
                                selectieRec.align[cltakenlijst[0][:3]] = "m"
                                print(selectieRec)
                                record = "N"
                            except:
                                print("Dat is geen geldig Recordnummer")
                    if record == "X":
                        selectie = "N"
                elif keuze == "1" or keuze[0].upper() == "B":
                    startDatumA = ""
                    startA = "Y"
                    while startA == "Y":
                        if startDatumA == "":
                            startDatumA = input("Voer de %sVROEGSTE Begindatum%s van je bereik in (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                        if startDatumA.upper() in afsluitlijst or startDatumA.upper() in neelijst:
                            startA = "X"
                        elif len(startDatumA) == 2 and (startDatumA[0].upper() in afsluitlijst or startDatumA[0].upper() in neelijst) and startDatumA[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            datumStartA = startDatumA[:4]+startDatumA[4:6]+startDatumA[6:]
                            try:
                                datetime.strptime(datumStartA,"%Y%m%d")
                                print(datumStartA)
                                startA = "N"
                                startB = "Y"
                                while startB == "Y":
                                    startDatumB = input("Voer de %sLAATSTE Begindatum%s van je bereik in (YYYYMMDD of niets):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                                    if startDatumB.upper() in afsluitlijst or startDatumB.upper() in neelijst:
                                        startA = "X"
                                    elif len(startDatumB) == 2 and (startDatumB[0].upper() in afsluitlijst or startDatumB[0].upper() in neelijst) and startDatumB[1].upper() in skiplijst:
                                        toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                        if toch.upper() in jalijst:
                                            print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                            exit()
                                    else:
                                        if startDatumB == "":
                                            startDatumB = startDatumA
                                        datumStartB = startDatumB[:4]+startDatumB[4:6]+startDatumB[6:]
                                        if startDatumB >= startDatumA:
                                            try:
                                                datetime.strptime(datumStartB,"%Y%m%d")
                                                print(datumStartB)
                                                if comp == "2":
                                                    cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s BETWEEN '%s' AND '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[1],datumStartA,datumStartB,cltakenlijst[2])
                                                else:
                                                    cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s BETWEEN '%s' AND '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[1],datumStartA,datumStartB,cltakenlijst[2])
                                                cur.execute(cursel)
                                                selectieStartDatum = from_db_cursor(cur)
                                                selectieStartDatum.align = "l"
                                                selectieStartDatum.align[clteam[4]] = "r"
                                                selectieStartDatum.align[cltakenlijst[0]] = "m"
                                                selectieStartDatum.align[cltakenlijst[0][:3]] = "m"
                                                print(selectieStartDatum)
                                                startB = "N"
                                            except:
                                                print("Dat is geen geldige einddatum van je bereik, probeer het opnieuw.") # startDatumB
                                                del startDatumB
                                        else:
                                            print("De laatste Begindatum komt nu vóór de vroegste Begindatum, dat kan dus niet.")
                                if startB == "X":
                                    break
                            except:
                                print("Dat is geen geldige startdatum van je bereik, probeer het opnieuw.") # startDatumA
                                startDatumA = ""
                    if startA == "X":
                        selectie = "N"
                elif keuze == "2" or keuze[0].upper() == "E":
                    stopDatumA = ""
                    stopA = "Y"
                    while stopA == "Y":
                        if stopDatumA == "":
                            stopDatumA = input("Voer de %sVROEGSTE Einddatum%s van je bereik in (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                        if stopDatumA.upper() in afsluitlijst or stopDatumA.upper() in neelijst:
                            stopA = "X"
                        elif len(stopDatumA) == 2 and (stopDatumA[0].upper() in afsluitlijst or stopDatumA[0].upper() in neelijst) and stopDatumA[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            datumStopA = stopDatumA[:4]+stopDatumA[4:6]+stopDatumA[6:]
                            try:
                                datetime.strptime(datumStopA,"%Y%m%d")
                                print(datumStopA)
                                stopA = "N"
                                stopB = "Y"
                                while stopB == "Y":
                                    stopDatumB = input("Voer de %sLAATSTE Einddatum%s van je bereik in (YYYYMMDD of niets):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                                    if stopDatumB.upper() in afsluitlijst or stopDatumB.upper() in neelijst:
                                        stopA = "X"
                                    elif len(stopDatumB) == 2 and (stopDatumB[0].upper() in afsluitlijst or stopDatumB[0].upper() in neelijst) and stopDatumB[1].upper() in skiplijst:
                                        toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                        if toch.upper() in jalijst:
                                            print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                            exit()
                                    else:
                                        stopA = "N"
                                        stopB = "Y"
                                        if stopDatumB == "":
                                            stopDatumB = stopDatumA
                                        datumStopB = stopDatumB[:4]+stopDatumB[4:6]+stopDatumB[6:]
                                        if stopDatumB >= stopDatumA:
                                            try:
                                                datetime.strptime(datumStopB,"%Y%m%d")
                                                print(datumStopB)
                                                if comp == "2":
                                                    cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, SUBSTR(t.%s,1,2) %s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s BETWEEN '%s' AND '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[2],datumStopA,datumStopB,cltakenlijst[2])
                                                else:
                                                    cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s BETWEEN '%s' AND '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[2],datumStopA,datumStopB,cltakenlijst[2])
                                                cur.execute(cursel)
                                                selectieStopDatum = from_db_cursor(cur)
                                                selectieStopDatum.align = "l"
                                                selectieStopDatum.align[clteam[4]] = "r"
                                                selectieStopDatum.align[cltakenlijst[0]] = "m"
                                                selectieStopDatum.align[cltakenlijst[0][:3]] = "m"
                                                print(selectieStopDatum)
                                                stopB = "N"
                                            except:
                                                print("Dat is geen geldige einddatum van je bereik, probeer het opnieuw.") # stopDatumB
                                                del stopDatumB
                                        else:
                                            print("De laatste Einddatum komt nu vóór de vroegste Einddatum, dat kan dus niet.")
                                if stopB == "X":
                                    break
                            except:
                                print("Dat is geen geldige startdatum van je bereik, probeer het opnieuw.") # stopDatumA
                                stopDatumA = ""
                    if stopA == "X":
                        selectie = "N"
                elif keuze == "3" or keuze[0].upper() == "T":
                    taak = "Y"
                    while taak == "Y":
                        stukjeTaak = input("Voer (een fragment van) de gezochte %sTaakomschrijving%s in (* laat leeg voor alle Records):\n  : " % (col,ResetAll))
                        if stukjeTaak.upper() in afsluitlijst or stukjeTaak.upper() in neelijst:
                            taak = "X"
                        elif len(stukjeTaak) == 2 and (stukjeTaak[0].upper() in afsluitlijst or stukjeTaak[0].upper() in neelijst) and stukjeTaak[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            if comp == "2":
                                cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s LIKE '%%%s%%' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[3],stukjeTaak,cltakenlijst[2])
                            else:
                                cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s LIKE '%%%s%%' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[3],stukjeTaak,cltakenlijst[2])
                            cur.execute(cursel)
                            selectieTaak = from_db_cursor(cur)
                            selectieTaak.align = "l"
                            selectieTaak.align[clteam[4]] = "r"
                            selectieTaak.align[cltakenlijst[0]] = "m"
                            selectieTaak.align[cltakenlijst[0][:3]] = "m"
                            print(selectieTaak)
                            taak = "N"
                    if taak == "X":
                        selectie = "N"
                elif keuze == "4" or keuze[0].upper() == "V":
                    voor = "Y"
                    while voor == "Y":
                        stukjeVNaam = input("Voer (een fragment van) de gezochte %sVoornaam%s in (* laat leeg voor alle Records):\n  : " % (col,ResetAll))
                        if stukjeVNaam.upper() in afsluitlijst or stukjeVNaam.upper() in neelijst:
                            voor = "X"
                        elif len(stukjeVNaam) == 2 and (stukjeVNaam[0].upper() in afsluitlijst or stukjeVNaam[0].upper() in neelijst) and stukjeVNaam[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            cursel = "SELECT * FROM team WHERE %s LIKE '%%%s%%' ORDER BY %s ASC;" % (clteam[0],stukjeVNaam,clteam[0])
                            cur.execute(cursel)
                            VNaam = from_db_cursor(cur)
                            VNaam.align[clteam[0]] = "l"
                            VNaam.align[clteam[2]] = "l"
                            print(VNaam)
                            if comp == "2":
                                cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE t.%s LIKE '%%%s%%' ORDER BY t.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],clteam[0],stukjeVNaam,clteam[0])
                            else:
                                cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE t.%s LIKE '%%%s%%' ORDER BY t.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],clteam[0],stukjeVNaam,clteam[0])
                            cur.execute(cursel)
                            selectieVNaam = from_db_cursor(cur)
                            selectieVNaam.align = "l"
                            selectieVNaam.align[clteam[4]] = "r"
                            selectieVNaam.align[cltakenlijst[0]] = "m"
                            selectieVNaam.align[cltakenlijst[0][:3]] = "m"
                            print(selectieVNaam)
                            voor = "N"
                    if voor == "X":
                        selectie = "N"
                elif keuze == "5" or keuze[0].upper() == "A":
                    achter = "Y"
                    while achter == "Y":
                        stukjeANaam = input("Voer (een fragment van) de gezochte %sAchternaam%s in (* laat leeg voor alle Records):\n  : " % (col,ResetAll))
                        if stukjeANaam.upper() in afsluitlijst or stukjeANaam.upper() in neelijst:
                            achter = "X"
                        elif len(stukjeANaam) == 2 and (stukjeANaam[0].upper() in afsluitlijst or stukjeANaam[0].upper() in neelijst) and stukjeANaam[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            cursel = "SELECT %s, %s FROM team WHERE %s LIKE '%%%s%%' ORDER BY %s ASC;" % (clteam[2],clteam[0],clteam[2],stukjeANaam,clteam[2])
                            cur.execute(cursel)
                            ANaam = from_db_cursor(cur)
                            ANaam.align[clteam[0]] = "l"
                            ANaam.align[clteam[2]] = "l"
                            print(ANaam)
                            if comp == "2":
                                cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE t.%s LIKE '%%%s%%' ORDER BY t.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],clteam[2],stukjeANaam,clteam[2])
                            else:
                                cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE t.%s LIKE '%%%s%%' ORDER BY t.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],clteam[2],stukjeANaam,clteam[2])
                            cur.execute(cursel)
                            selectieANaam = from_db_cursor(cur)
                            selectieANaam.align = "l"
                            selectieANaam.align[clteam[4]] = "r"
                            selectieANaam.align[cltakenlijst[0]] = "m"
                            selectieANaam.align[cltakenlijst[0][:3]] = "m"
                            print(selectieANaam)
                            achter = "N"
                    if achter == "X":
                        selectie = "N"
                elif keuze == "6" or keuze[0].upper() == "P":
                    nummer = "Y"
                    while nummer == "Y":
                        Nr = input("Voer het %sPersoneelsNummer%s in:\n  : " % (col,ResetAll))
                        if Nr.upper() in afsluitlijst or Nr.upper() in neelijst:
                            nummer = "X"
                        elif len(Nr) == 2 and (Nr[0].upper() in afsluitlijst or Nr[0].upper() in neelijst) and Nr[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            if comp == "2":
                                cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE t.%s = '%s' ORDER BY t.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],clteam[4],Nr,clteam[4])
                            else:
                                cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE t.%s = '%s' ORDER BY t.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],clteam[4],Nr,clteam[4])
                            cur.execute(cursel)
                            selectieNr = from_db_cursor(cur)
                            selectieNr.align = "l"
                            selectieNr.align[clteam[4]] = "r"
                            selectieNr.align[cltakenlijst[0]] = "m"
                            selectieNr.align[cltakenlijst[0][:3]] = "m"
                            print(selectieNr)
                            nummer = "N"
                    if nummer == "X":
                        selectie = "N"
                # 7: status = default = else
                elif keuze == "8" or keuze[0].upper() == "O":
                    aant = "Y"
                    while aant == "Y":
                        stukjeAant = input("Voer (een fragment van) de gezochte %sOpmerking%s in (* laat leeg voor alle Records)\n  : " % (col,ResetAll))
                        if stukjeAant.upper() in afsluitlijst or stukjeAant.upper() in neelijst:
                            aant = "X"
                        elif len(stukjeAant) == 2 and (stukjeAant[0].upper() in afsluitlijst or stukjeAant[0].upper() in neelijst) and stukjeAant[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            if comp == "2":
                                cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,2) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s LIKE '%%%s%%' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[6],stukjeAant,cltakenlijst[2])
                            else:
                                cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s LIKE '%%%s%%' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[6],stukjeAant,cltakenlijst[2])
                            cur.execute(cursel)
                            selectieAant = from_db_cursor(cur)
                            selectieAant.align = "l"
                            selectieAant.align[clteam[4]] = "r"
                            selectieAant.align[cltakenlijst[0]] = "m"
                            selectieAant.align[cltakenlijst[0][:3]] = "m"
                            print(selectieAant)
                            aant = "N"
                    if aant == "X":
                        selectie = "N"
                elif keuze[0].upper() == "G":
                        if comp == "2":
                            cursel = "SELECT a.%s %s, SUBSTR(a.%s,5,4) %s, SUBSTR(a.%s,5,4) %s, SUBSTR(a.%s,1,19) %s, t.%s, t.%s, SUBSTR(a.%s,6,2) %s, SUBSTR(a.%s,1,5) %s FROM archief a INNER JOIN team t ON a.%s = t.%s;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4])
                        else:
                            cursel = "SELECT a.%s, a.%s, a.%s, a.%s, t.%s, t.%s, t.%s, a.%s, a.%s FROM archief a INNER JOIN team t ON a.%s = t.%s;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4])
                        cur.execute(cursel)
                        selectieArch = from_db_cursor(cur)
                        selectieArch.align = "l"
                        selectieArch.align[clteam[4]] = "r"
                        selectieArch.align[cltakenlijst[0]] = "m"
                        selectieArch.align[cltakenlijst[0][:3]] = "m"
                        print("%s##### ARCHIEF #####%s" % (col,ResetAll))
                        print(selectieArch)
                        print("%s##### ARCHIEF #####%s" % (col,ResetAll))
                # 7: status = default = else
                else:
                    staat = "Y"
                    while staat == "Y":
                        Staat = input("Kies uit één van de volgende %sStatussen%s:\n    %s\n%s  > %s%s\n    %s\n    %s\n    %s\n    %s\n  : " % (col,ResetAll,statuslijst[0],col,statuslijst[1],ResetAll,statuslijst[2],statuslijst[3],statuslijst[4],statuslijst[5]))
                        if Staat.upper() in afsluitlijst or Staat.upper() in neelijst:
                            staat = "X"
                        elif len(Staat) == 2 and (Staat[0].upper() in afsluitlijst or Staat[0].upper() in neelijst) and Staat[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            if Staat == "0":
                                Staat = statuslijst[0]
                                print(Staat)
                                staat = "N"
                            # 1: gestart = default = else
                            elif Staat == "2":
                                Staat = statuslijst[2]
                                print(Staat)
                                staat = "N"
                            elif Staat == "3":
                                Staat = statuslijst[3]
                                print(Staat)
                                staat = "N"
                            elif Staat == "4":
                                Staat = statuslijst[4]
                                print(Staat)
                                staat = "N"
                            elif Staat == "5":
                                Staat = statuslijst[5]
                                print(Staat)
                                staat = "N"
                            # 1: gestart = default = else
                            else:
                                Staat = statuslijst[1]
                                print(Staat)
                                staat = "N"
                            if comp == "2":
                                cursel = "SELECT m.%s %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,5,4) %s, SUBSTR(m.%s,1,19) %s, t.%s, t.%s, SUBSTR(m.%s,6,1) %s, SUBSTR(m.%s,1,5) %s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[0][:3],cltakenlijst[1],cltakenlijst[1],cltakenlijst[2],cltakenlijst[2],cltakenlijst[3],cltakenlijst[3][:10],clteam[1],clteam[3],cltakenlijst[5],cltakenlijst[5][:2],cltakenlijst[6],cltakenlijst[6][:3],cltakenlijst[4],clteam[4],cltakenlijst[5],Staat,cltakenlijst[5])
                            else:
                                cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s' ORDER BY m.%s ASC;" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[5],Staat,cltakenlijst[5])
                            cur.execute(cursel)
                            selectieStaat = from_db_cursor(cur)
                            selectieStaat.align = "l"
                            selectieStaat.align[clteam[4]] = "r"
                            selectieStaat.align[cltakenlijst[0]] = "m"
                            selectieStaat.align[cltakenlijst[0][:3]] = "m"
                            print(selectieStaat)
                            staat = "N"
                    if staat == "X":
                        selectie = "N"
            if selectie == "X":
                break
        if kijk == "X":
            functie = "N"

    # 3: WIJZIGEN
    elif functie == "3" or functie[0].upper() == "W":
        col = colwijzigen
        wijzig = "Y"
        while wijzig == "Y":
            if mot not in ["1","2"]:
                mot = input("%sWil je een Taak of een Medewerker wijzigen?%s\n%s  > 1: Taak%s\n    2: Medewerker\n%s  : " % (col,ResetAll,col,ResetAll,terug))
            if mot.upper() in afsluitlijst or mot.upper() in neelijst:
                functie = "N"
                wijzig = "X"
            elif len(mot) == 2 and (mot[0].upper() in afsluitlijst or mot[0].upper() in neelijst) and mot[1].upper() in skiplijst:
                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                if toch.upper() in jalijst:
                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                    exit()
            elif mot == "2" or mot.upper() == "M":
                cur.execute("SELECT %s FROM team;" % (clteam[4]))
                nummerLijstHaar = str(cur.fetchall())
                nummerLijstKaal = nummerLijstHaar.replace("[","").replace("]","").replace("(","").replace(",)","").replace("'","").split(", ")
                nLstring = []
                for i in nummerLijstKaal:
                    nLstring.append(str(i))
                mw = "Y"
                while mw == "Y":
                    iemAnder = input("Voer het %sPersoneelsNummer%s in van de medewerker die je wilt wijzigen, of \"?\" voor een lijst:\n  : " % (col,ResetAll))
                    if iemAnder.upper() in afsluitlijst or iemAnder.upper() in neelijst:
                        mw = "N"
                        mot = ""
                    elif len(iemAnder) == 2 and (iemAnder[0].upper() in afsluitlijst or iemAnder[0].upper() in neelijst) and iemAnder[1].upper() in skiplijst:
                        toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                        if toch.upper() in jalijst:
                            print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                            exit()
                    elif iemAnder == "?" or iemAnder == "":
                        cur.execute("SELECT * FROM team")
                        Lijst = from_db_cursor(cur)
                        Lijst.align = "l"
                        Lijst.align[clteam[4]] = "r"
                        print(Lijst.get_string(sort_key=operator.itemgetter(1, 0), sortby=clteam[0]))
                    elif iemAnder not in nummerLijstKaal:
                        print("Dat PersoneelsNummer staat niet in de lijst, kies een ander nummer.")
                    else:
                        cur.execute("SELECT * FROM team WHERE %s = '%s'" % (clteam[4],iemAnder))
                        watWas = from_db_cursor(cur)
                        watWas.align = "l"
                        watWas.align[clteam[4]] = "r"
                        print(watWas)
                        watAnder = input("%sWat%s wil je wijzigen?\n    1: %s\n    2: %s\n    3: %s\n    4: %s\n    5: %s\n    6: %s\n  : " % (col,ResetAll,clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
                        if watAnder.upper() in afsluitlijst or watAnder.upper() in neelijst:
                            nummer = "X"
                        elif len(watAnder) == 2 and (watAnder[0].upper() in afsluitlijst or watAnder[0].upper() in neelijst) and watAnder[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        elif watAnder == "1":
                            voor = "Y"
                            while voor == "Y":
                                nieuweVoornaam = input("Typ de nieuwe %sVoornaam%s:\n  : " % (col,ResetAll))
                                if nieuweVoornaam.upper() in afsluitlijst or nieuweVoornaam.upper() in neelijst:
                                    voor = "X"
                                elif len(nieuweVoornaam) == 2 and (nieuweVoornaam[0].upper() in afsluitlijst or nieuweVoornaam[0].upper() in neelijst) and nieuweVoornaam[1].upper() in skiplijst:
                                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                elif len(nieuweVoornaam) > 25:
                                    print("Deze Voornaam is te lang. Kort hem af.")
                                else:
                                    cur.execute("UPDATE team SET %s = '%s' WHERE %s = '%s'" % (clteam[0],nieuweVoornaam,clteam[4],iemAnder))
                                    con.commit()
                                    cur.execute("SELECT * FROM team WHERE %s = '%s'" % (clteam[4],iemAnder))
                                    andereVN = from_db_cursor(cur)
                                    andereVN.align = "l"
                                    andereVN.align[clteam[4]] = "r"
                                    print(andereVN)
                                    mot = "N"
                                    voor = "N"
                                    mw = "N"
                            if voor != "Y":
                                mw = "N" 
                        elif watAnder == "2":
                            vn = "Y"
                            while vn == "Y":
                                nieuweVN = input("Typ de nieuwe %sVN%s:\n  : " % (col,ResetAll))
                                if nieuweVN.upper() in afsluitlijst or nieuweVN.upper() in neelijst:
                                    vn = "X"
                                elif len(nieuweVN) == 2 and (nieuweVN[0].upper() in afsluitlijst or nieuweVN[0].upper() in neelijst) and nieuweVN[1].upper() in skiplijst:
                                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        print("\n%sBedankt, aan de slag, of neem een momentje vn jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                elif len(nieuweVN) > 2:
                                    print("Deze VN is te lang. Kort hem af.")
                                else:
                                    cur.execute("UPDATE team SET %s = '%s' WHERE %s = '%s'" % (clteam[1],nieuweVN,clteam[4],iemAnder))
                                    con.commit()
                                    cur.execute("SELECT * FROM team WHERE %s = '%s'" % (clteam[4],iemAnder))
                                    andereVN = from_db_cursor(cur)
                                    andereVN.align = "l"
                                    andereVN.align[clteam[4]] = "r"
                                    print(andereVN)
                                    mot = "N"
                                    vn = "N"
                                    mw = "N"
                            if vn != "Y":
                                mw = "N" 
                        elif watAnder == "3":
                            achter = "Y"
                            while achter == "Y":
                                nieuweAchternaam = input("Typ de nieuwe %sAchternaam%s:\n  : " % (col,ResetAll))
                                if nieuweAchternaam.upper() in afsluitlijst or nieuweAchternaam.upper() in neelijst:
                                    achter = "X"
                                elif len(nieuweAchternaam) == 2 and (nieuweAchternaam[0].upper() in afsluitlijst or nieuweAchternaam[0].upper() in neelijst) and nieuweAchternaam[1].upper() in skiplijst:
                                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                elif len(nieuweAchternaam) > 25:
                                    print("Deze Achternaam is te lang. Kort hem af.")
                                else:
                                    cur.execute("UPDATE team SET %s = '%s' WHERE %s = '%s'" % (clteam[2],nieuweAchternaam,clteam[4],iemAnder))
                                    con.commit()
                                    cur.execute("SELECT * FROM team WHERE %s = '%s'" % (clteam[4],iemAnder))
                                    andereAN = from_db_cursor(cur)
                                    andereAN.align = "l"
                                    andereAN.align[clteam[4]] = "r"
                                    print(andereAN)
                                    mot = "N"
                                    achter = "N"
                                    mw = "N"
                            if achter != "Y":
                                mw = "N" 
                        elif watAnder == "4":
                            an = "Y"
                            while an == "Y":
                                nieuweAN = input("Typ de nieuwe %sAN%s:\n  : " % (col,ResetAll))
                                if nieuweAN.upper() in afsluitlijst or nieuweAN.upper() in neelijst:
                                    an = "X"
                                elif len(nieuweAN) == 2 and (nieuweAN[0].upper() in afsluitlijst or nieuweAN[0].upper() in neelijst) and nieuweAN[1].upper() in skiplijst:
                                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                elif len(nieuweAN) > 2:
                                    print("Deze AN is te lang. Kort hem af.")
                                else:
                                    cur.execute("UPDATE team SET %s = '%s' WHERE %s = '%s'" % (clteam[3],nieuweAN,clteam[4],iemAnder))
                                    con.commit()
                                    cur.execute("SELECT * FROM team WHERE %s = '%s'" % (clteam[4],iemAnder))
                                    andereAN = from_db_cursor(cur)
                                    andereAN.align = "l"
                                    andereAN.align[clteam[4]] = "r"
                                    print(andereAN)
                                    mot = "N"
                                    an = "N"
                                    mw = "N"
                            if an != "Y":
                                mw = "N" 
                        elif watAnder == "5":
                            print("Let op dat er geen Taken op het \"oude\" PersoneelsNummer openstaan, of pas die alsnog aan.")
                            nummer = "Y"
                            while nummer == "Y":
                                nieuwNummer = input("Typ het nieuwe %sPersoneelsNummer%s:\n  : " % (col,ResetAll))
                                if nieuwNummer.upper() in afsluitlijst or nieuwNummer.upper() in neelijst:
                                    nummer = "X"
                                elif len(nieuwNummer) == 2 and (nieuwNummer[0].upper() in afsluitlijst or nieuwNummer[0].upper() in neelijst) and nieuwNummer[1].upper() in skiplijst:
                                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                elif nieuwNummer in nLstring:
                                    print("Dat PersoneelsNummer bestaat al.")
                                else:
                                    try:
                                        str(int(nieuwNummer))
                                        cur.execute("UPDATE team SET %s = '%s' WHERE %s = '%s'" % (clteam[4],nieuwNummer,clteam[4],iemAnder))
                                        con.commit()
                                        cur.execute("SELECT * FROM team WHERE %s = '%s'" % (clteam[4],nieuwNummer))
                                        anderNR = from_db_cursor(cur)
                                        anderNR.align = "l"
                                        anderNR.align[clteam[4]] = "r"
                                        print(anderNR)
                                        mot = "N"
                                        nummer = "N"
                                        mw = "N"
                                    except:
                                        print("Dat is geen geldig PersoneelsNummer.")
                        elif watAnder == "6":
                            aant = "Y"
                            while aant == "Y":
                                nieuwAant = input("Typ een nieuwe %sAantekening%s:\n  : " % (col,ResetAll))
                                if nieuwAant.upper() in afsluitlijst or nieuwAant.upper() in neelijst:
                                    aant = "X"
                                elif len(nieuwAant) == 2 and (nieuwAant[0].upper() in afsluitlijst or nieuwAant[0].upper() in neelijst) and nieuwAant[1].upper() in skiplijst:
                                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                else:
                                    cur.execute("UPDATE team SET %s = '%s' WHERE %s = '%s'" % (clteam[5],nieuwAant,clteam[4],iemAnder))
                                    con.commit()
                                    cur.execute("SELECT * FROM team WHERE %s = '%s'" % (clteam[5],nieuwAant))
                                    anderA = from_db_cursor(cur)
                                    anderA.align = "l"
                                    anderA.align[clteam[4]] = "r"
                                    print(anderA)
                                    mot = "N"
                                    aant = "N"
                                    mw = "N"
            else:
                wijzigTaak = "Y"
                while wijzigTaak == "Y":
                    cur.execute("SELECT %s FROM takenlijst;" % (cltakenlijst[0]))
                    reclist = str(cur.fetchall()).replace("[","").replace("(","").replace(")","").replace("]","").replace("'","").replace(" ","").split(",")
                    wijzigWelk = input("Welk %sRecord%s wil je %swijzigen%s?\n  : " % (col,ResetAll,col,ResetAll))
                    if wijzigWelk.upper() in afsluitlijst or wijzigWelk.upper() in neelijst:
                        wijzigTaak = "X"
                    elif len(wijzigWelk) == 2 and (wijzigWelk[0].upper() in afsluitlijst or wijzigWelk[0].upper() in neelijst) and wijzigWelk[1].upper() in skiplijst:
                        toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                        if toch.upper() in jalijst:
                            print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                            exit()
                    elif wijzigWelk not in reclist or wijzigWelk == "":
                        print("Dat recordnummer bestaat niet.")
                    else:
                        if wijzigWelk in reclist:
                            cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],wijzigWelk))
                            welk = from_db_cursor(cur)
                            welk.align = "l"
                            welk.align[cltakenlijst[0]] = "m"
                            welk.align[clteam[4]] = "r"
                            print(welk)
                            wat = "Y"
                            while wat == "Y":
                                Wat = input("Wat wil je %swijzigen%s?\n    1: %s\n    2: %s\n    3: %s\n    4: %s\n  > 5: %s\n    6: %s\n  : " % (col,ResetAll,cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
                                if Wat.upper() in afsluitlijst or Wat.upper() in neelijst:
                                    wat = "X"
                                elif len(Wat) == 2 and (Wat[0].upper() in afsluitlijst or Wat[0].upper() in neelijst) and Wat[1].upper() in skiplijst:
                                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                    if toch.upper() in jalijst:
                                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                        exit()
                                elif Wat == "1" or Wat.upper() == "B":
                                    start = "Y"
                                    while start == "Y":
                                        startDatum = input("Voer de %sBegindatum%s in (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                                        if startDatum.upper() in afsluitlijst or startDatum.upper() in neelijst:
                                            start = "N"
                                        elif len(startDatum) == 2 and (startDatum[0].upper() in afsluitlijst or startDatum[0].upper() in neelijst) and startDatum[1].upper() in skiplijst:
                                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                            if toch.upper() in jalijst:
                                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                                exit()
                                        else:
                                            try:
                                                datumStart = int(startDatum[:4]+startDatum[4:6]+startDatum[6:])
                                                datetime.strptime(str(datumStart),"%Y%m%d")
                                                cursel = "UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[1],datumStart,cltakenlijst[0],wijzigWelk)
                                                cur.execute(cursel)
                                                con.commit()
                                                cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],wijzigWelk))
                                                wijzigStart = from_db_cursor(cur)
                                                wijzigStart.align = "l"
                                                wijzigStart.align[cltakenlijst[0]] = "m"
                                                wijzigStart.align[clteam[4]] = "r"
                                                print(wijzigStart)
                                                wat = "N"
                                                start = "N"
                                            except:
                                                print("Dat is geen geldige datum, probeer het opnieuw.") # startDatum
                                elif Wat == "2" or Wat.upper() == "E":
                                    stop = "Y"
                                    while stop == "Y":
                                        stopDatum = input("Voer de %sEinddatum%s in (YYYYMMDD):\n  : " % (col,ResetAll)).replace(" ","").replace("-","").replace("/","")
                                        if stopDatum.upper() in afsluitlijst or stopDatum.upper() in neelijst:
                                            stop = "N"
                                        elif len(stopDatum) == 2 and (stopDatum[0].upper() in afsluitlijst or stopDatum[0].upper() in neelijst) and stopDatum[1].upper() in skiplijst:
                                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                            if toch.upper() in jalijst:
                                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                                exit()
                                        else:
                                            try:
                                                datumStop = int(stopDatum[:4]+stopDatum[4:6]+stopDatum[6:])
                                                datetime.strptime(str(datumStop),"%Y%m%d")
                                                cursel = "UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[2],datumStop,cltakenlijst[0],wijzigWelk)
                                                cur.execute(cursel)
                                                con.commit()
                                                cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],wijzigWelk))
                                                wijzigStop = from_db_cursor(cur)
                                                wijzigStop.align = "l"
                                                wijzigStop.align[cltakenlijst[0]] = "m"
                                                wijzigStop.align[clteam[4]] = "r"
                                                print(wijzigStop)
                                                wat = "N"
                                                stop = "N"
                                            except:
                                                print("Dat is geen geldige datum, probeer het opnieuw.") # stopDatum
                                elif Wat == "3" or Wat.upper() == "T":
                                    omschrijvingTaak = "Y"
                                    while omschrijvingTaak == "Y":
                                        taakOmschrijving = input("Voer een nieuwe %sTaakomschrijving%s van de taak in:\n  : " % (col,ResetAll))
                                        if taakOmschrijving.upper() in afsluitlijst or taakOmschrijving.upper() in neelijst:
                                            omschrijvingTaak = "N"
                                        elif len(taakOmschrijving) == 2 and (taakOmschrijving[0].upper() in afsluitlijst or taakOmschrijving[0].upper() in neelijst) and taakOmschrijving[1].upper() in skiplijst:
                                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                            if toch.upper() in jalijst:
                                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                                exit()
                                        elif len(taakOmschrijving) < 5:
                                            print("Taakomschrijving is verplicht, vul tenminste 5 posities (bij voorkeur uniek) in.")
                                        else:
                                            cursel = "UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[3],taakOmschrijving,cltakenlijst[0],wijzigWelk)
                                            cur.execute(cursel)
                                            con.commit()
                                            cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],wijzigWelk))
                                            wijzigTaak = from_db_cursor(cur)
                                            wijzigTaak.align = "l"
                                            wijzigTaak.align[cltakenlijst[0]] = "m"
                                            wijzigTaak.align[clteam[4]] = "r"
                                            print(wijzigTaak)
                                            wat = "N"
                                            omschrijvingTaak = "N"
                                elif Wat == "4" or Wat.upper() == "M":
                                    cur.execute("SELECT %s FROM team;" % (clteam[4]))
                                    nummerLijstHaar = str(cur.fetchall())
                                    nummerLijstKaal = nummerLijstHaar.replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","").split(",")
                                    nummer = "Y"
                                    while nummer == "Y":
                                        iemAnders = input("Voer het %sMedewerkerNummer%s van de andere medewerker in, of \"?\" voor een lijst:\n  : " % (col,ResetAll))
                                        if iemAnders.upper() in afsluitlijst or iemAnders.upper() in neelijst:
                                            nummer = "N"
                                        elif len(iemAnders) == 2 and (iemAnders[0].upper() in afsluitlijst or iemAnders[0].upper() in neelijst) and iemAnders[1].upper() in skiplijst:
                                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                            if toch.upper() in jalijst:
                                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                                exit()
                                        elif iemAnders == "?" or iemAnders == "":
                                            cur.execute("SELECT * FROM team")
                                            Lijst = from_db_cursor(cur)
                                            Lijst.align = "l"
                                            Lijst.align[clteam[4]] = "r"
                                            print(Lijst.get_string(sort_key=operator.itemgetter(1, 0), sortby=clteam[0]))
                                        if iemAnders not in nummerLijstKaal:
                                            print("Dat MedewerkerNummer staat niet in de lijst, kies een ander nummer.")
                                        else:
                                            cursel = "UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[4],iemAnders,cltakenlijst[0],wijzigWelk)
                                            cur.execute(cursel)
                                            con.commit()
                                            cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],wijzigWelk))
                                            wijzigIem = from_db_cursor(cur)
                                            wijzigIem.align = "l"
                                            wijzigIem.align[cltakenlijst[0]] = "m"
                                            wijzigIem.align[clteam[4]] = "r"
                                            print(wijzigIem)
                                            wat = "N"
                                            nummer = "N"
                                # 3: WIJZIGEN - 1: Taak - 5: status = default = else
                                elif Wat == "6" or Wat.upper() == "O":
                                    aantekeningTaak = "Y"
                                    while aantekeningTaak == "Y":
                                        taakOpmerking = input("Voer een nieuwe %sOpmerking%s in:\n  : " % (col,ResetAll))
                                        if taakOpmerking.upper() in afsluitlijst or taakOpmerking.upper() in neelijst:
                                            aantekeningTaak = "N"
                                        elif len(taakOpmerking) == 2 and (taakOpmerking[0].upper() in afsluitlijst or taakOpmerking[0].upper() in neelijst) and taakOpmerking[1].upper() in skiplijst:
                                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                            if toch.upper() in jalijst:
                                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                                exit()
                                        else:
                                            cursel = "UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[6],taakOpmerking,cltakenlijst[0],wijzigWelk)
                                            cur.execute(cursel)
                                            con.commit()
                                            cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],wijzigWelk))
                                            wijzigTaak = from_db_cursor(cur)
                                            wijzigTaak.align = "l"
                                            wijzigTaak.align[cltakenlijst[0]] = "m"
                                            wijzigTaak.align[clteam[4]] = "r"
                                            print(wijzigTaak)
                                            wat = "N"
                                            aantekeningTaak = "N"
                                # 3: WIJZIGEN - 1: Taak - 5: status = default = else
                                else:
                                    voortgang = "Y"
                                    while voortgang == "Y":
                                        preStatuslijst = []
                                        for i in statuslijst:
                                            preStatuslijst.append(i[5])
                                        preStatus = input("Kies uit één van de volgende %sStatussen%s:\n    %s\n    %s\n    %s\n    %s\n    %s\n    %s\n  : " % (col,ResetAll,statuslijst[0],statuslijst[1],statuslijst[2],statuslijst[3],statuslijst[4],statuslijst[5]))
                                        if preStatus not in preStatuslijst:
                                            if preStatus.upper() in afsluitlijst or preStatus.upper() in neelijst:
                                                break
                                            elif len(preStatus) == 2 and (preStatus[0].upper() in afsluitlijst or preStatus[0].upper() in neelijst) and preStatus[1].upper() in skiplijst:
                                                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                                                if toch.upper() in jalijst:
                                                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                                    exit()
                                            else:
                                                print("Daar kan ik geen Status van maken.")
                                        else:
                                            if preStatus == "0":
                                                Status = statuslijst[0]
                                            elif preStatus == "1":
                                                Status = statuslijst[1]
                                            elif preStatus == "2":
                                                Status = statuslijst[2]
                                            elif preStatus == "3":
                                                Status = statuslijst[3]
                                            elif preStatus == "4":
                                                Status = statuslijst[4]
                                            elif preStatus == "5":
                                                Status = statuslijst[5]
                                            cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s'" % (cltakenlijst[5],cltakenlijst[0],wijzigWelk))
                                            OudeStaat = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace("","").replace("'","").replace("\\x1b33m",colstat0).replace("\\x1b93m",colstat1).replace("\\x1b35m",colstat2).replace("\\x1b31m",colstat3).replace("\\x1b32m",colstat4).replace("\\x1b91m",colstat5).replace("\\x1b0m",ResetAll)
                                            cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s'" % (cltakenlijst[6],cltakenlijst[0],wijzigWelk))
                                            OudeAant = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace("","").replace("'","").replace("\\x1b33m",colstat0).replace("\\x1b93m",colstat1).replace("\\x1b35m",colstat2).replace("\\x1b31m",colstat3).replace("\\x1b32m",colstat4).replace("\\x1b91m",colstat5).replace("\\x1b96m",col).replace("\\x1b0m",ResetAll)
                                            if OudeStaat == Status:
                                                NieuweAant = OudeAant
                                            else:
                                                #NieuweAant = "%s: " % (nu[:4])+ "%s" % (OudeStaat)+ "%s -> %s" % (col,ResetAll)+  "%s" % (Status)+ " \"%s\"" % (OudeAant)
                                                NieuweAant = "%s: %s%s -> %s%s \"%s\"" % (nu[4:],OudeStaat,col,ResetAll,Status,OudeAant)
                                            cur.execute("UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[5],Status,cltakenlijst[0],wijzigWelk))
                                            cur.execute("UPDATE takenlijst SET %s = '%s' WHERE %s = '%s';" % (cltakenlijst[6],NieuweAant,cltakenlijst[0],wijzigWelk))
                                            con.commit()
                                            cur.execute("SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],wijzigWelk))
                                            wijzigStats = from_db_cursor(cur)
                                            wijzigStats.align = "l"
                                            wijzigStats.align[cltakenlijst[0]] = "m"
                                            wijzigStats.align[clteam[4]] = "r"
                                            print(wijzigStats)
                                            wat = "N"
                                            voortgang = "N"
                                    if voortgang == "X":
                                        break
                            if wat == "X":
                                wijzigTaak = "X"
                                break
                if wijzigTaak == "X":
                    break
            if wijzig == "X":
                functie = "N"

    # 4: VERWIJDEREN EN ARCHIVEREN
    elif functie == "4" or functie[0].upper() == "V":
        col = colverwijderen
        weg = "Y"
        while weg == "Y":
            if Wat not in ["1","2","3"]:
                Wat = input("%sWil je een Taak of een Medewerker VERWIJDEREN of een Taak ARCHIVEREN?%s\n    1: Taak verwijderen\n    2: Medewerker verwijderen\n%s  > 3: Archiveren (taak)%s\n%s  : " % (col,ResetAll,col,ResetAll,terug))
            if Wat.upper() in afsluitlijst or Wat.upper() in neelijst:
                weg = "X"
                break
            elif len(Wat) == 2 and (Wat[0].upper() in afsluitlijst or Wat[0].upper() in neelijst) and Wat[1].upper() in skiplijst:
                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                if toch.upper() in jalijst:
                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                    exit()
            if Wat == "1" or Wat.upper() == "T":
                cur.execute("SELECT %s FROM takenlijst;" % (cltakenlijst[0]))
                reclist = str(cur.fetchall()).replace("[","").replace("(","").replace(")","").replace("]","").replace("'","").replace(" ","").split(",")
                Welk = input("Geef het %sRecord%s in:\n  : " % (col,ResetAll))
                if Welk.upper() in afsluitlijst or Welk.upper() in neelijst:
                    break
                elif len(Welk) == 2 and (Welk[0].upper() in afsluitlijst or Welk[0].upper() in neelijst) and Welk[1].upper() in skiplijst:
                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                    if toch.upper() in jalijst:
                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                        exit()
                elif Welk not in reclist:
                    print("Dat recordnummer bestaat niet.")
                else:
                    cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],Welk)
                    cur.execute(cursel)
                    welkVerwijderen = from_db_cursor(cur)
                    welkVerwijderen.align = "l"
                    welkVerwijderen.align[clteam[4]] = "r"
                    welkVerwijderen.align[cltakenlijst[0]] = "m"
                    print(welkVerwijderen)
                    echtWeg = input("%sWeet je het zeker?%s\n%s    1: Ja%s\n  > 2: Nee\n  : " % (col,ResetAll,col,ResetAll))
                    if echtWeg == "1" or echtWeg.upper() in jalijst:
                        cur.execute("DELETE FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[0],Welk))
                        con.commit()
                        print("%sRecord %s is VERWIJDERD.%s" % (col,Welk,ResetAll))
                        weg = "N"
            elif Wat == "2" or Wat.upper() == "M":
                cur.execute("SELECT %s FROM team;" % (clteam[4]))
                teamlist = str(cur.fetchall()).replace("[","").replace("(","").replace(")","").replace("]","").replace("'","").replace(" ","").split(",")
                Wie = input("Geef het %sPersoneelsNummer%s in:\n  : " % (col,ResetAll))
                if Wie.upper() in afsluitlijst or Wie.upper() in neelijst:
                    break
                elif len(Wie) == 2 and (Wie[0].upper() in afsluitlijst or Wie[0].upper() in neelijst) and Wie[1].upper() in skiplijst:
                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                    if toch.upper() in jalijst:
                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                        exit()
                elif Wie not in teamlist:
                    print("Dat PersoneelsNummer bestaat niet.")
                else:
                    cursel = "SELECT %s, %s, %s FROM team WHERE %s = '%s';" % (clteam[0],clteam[2],clteam[4],clteam[4],Wie)
                    cur.execute(cursel)
                    wieVerwijderen = from_db_cursor(cur)
                    wieVerwijderen.align = "l"
                    wieVerwijderen.align[clteam[4]] = "r"
                    print(wieVerwijderen)
                    echtWeg = input("%sWeet je het zeker?%s\n%s    1: Ja%s\n  > 2: Nee\n  : " % (col,ResetAll,col,ResetAll))
                    if echtWeg == "1" or echtWeg.upper() in jalijst:
                        cur.execute("DELETE FROM team WHERE %s = '%s';" % (clteam[4],Wie))
                        con.commit()
                        print("%sMedewerker %s is VERWIJDERD.%s" % (col,Wie,ResetAll))
                        weg = "N"
            # 4: ARCHIVEREN - 3: taak = default = else
            else:
                cur.execute("SELECT %s FROM takenlijst;" % (cltakenlijst[0]))
                reclist = str(cur.fetchall()).replace("[","").replace("(","").replace(")","").replace("]","").replace("'","").replace(" ","").split(",")
                Welk = input("Geef het %sRecord%s in:\n  : " % (col,ResetAll))
                if Welk.upper() in afsluitlijst or Welk.upper() in neelijst:
                    break
                elif len(Welk) == 2 and (Welk[0].upper() in afsluitlijst or Welk[0].upper() in neelijst) and Welk[1].upper() in skiplijst:
                    toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                    if toch.upper() in jalijst:
                        print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                        exit()
                elif Welk not in reclist:
                    print("Dat recordnummer bestaat niet.")
                else:
                    cursel = "INSERT INTO archief(%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[0],Welk)
                    cur.execute(cursel)
                    con.commit()
                    print("Het record is succesvol gearchiveerd, je kunt het nu %sverwijderen%s uit de takenlijst." % (col,ResetAll))
                    cursel = "SELECT m.%s, m.%s, m.%s, m.%s, t.%s, t.%s, t.%s, m.%s, m.%s FROM takenlijst m INNER JOIN team t ON m.%s = t.%s WHERE m.%s = '%s';" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],clteam[0],clteam[2],clteam[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[4],clteam[4],cltakenlijst[0],Welk)
                    cur.execute(cursel)
                    welkVerwijderen = from_db_cursor(cur)
                    welkVerwijderen.align = "l"
                    welkVerwijderen.align[clteam[4]] = "r"
                    welkVerwijderen.align[cltakenlijst[0]] = "m"
                    print(welkVerwijderen)
                    echtWeg = input("%sWeet je het zeker?%s\n%s    1: Ja%s\n  > 2: Nee\n  : " % (col,ResetAll,col,ResetAll))
                    if echtWeg == "1" or echtWeg.upper() in jalijst:
                        cur.execute("DELETE FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[0],Welk))
                        con.commit()
                        print("%sRecord %s is VERWIJDERD.%s" % (col,Welk,ResetAll))
                        weg = "N"
        if weg == "X":
            functie = "N"
    # 5: KALENDER = Default = else
    # 6: RESET RECORDID & BACKUP
    elif functie == "6" or functie[0].upper() == "R":
        col = colreset
        if resetjn not in ["1","2","3","4","5","6","7","8","9"]:
            resetjn = input("Deze functie maakt of herstelt uit een %sbackup%s en maakt de %sRecordID's aansluitend%s.\n%s  > 1: Backup van alles en reset RecordID's%s\n    2: Backup alleen Takenlijst en reset RecordID's\n    3: Backup alleen Team\n    4: Backup alleen Archief\n    5: Backup alleen Algemene informatie (Team.txt)\n    6: Terugzetten backup Takenlijst\n    7: Terugzetten backup Team\n    8: Terugzetten backup Archief\n    9: Terugzetten backup Algemene informatie (Team.txt)\n%s  : " % (col,ResetAll,col,ResetAll,col,ResetAll,terug))
        if resetjn == "":
            resetjn = "1"
        if len(resetjn) == 2 and (resetjn[0].upper() in afsluitlijst or resetjn[0].upper() in neelijst) and resetjn[1].upper() in skiplijst:
            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
            if toch.upper() in jalijst:
                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                exit()
        if resetjn == "1":
            try:
                cur.execute("DROP TABLE backupvantakenlijst;")
            except(Exception) as error:
                #print(error)
                pass
            try:
                cur.execute("CREATE TABLE backupvantakenlijst AS SELECT * FROM takenlijst;")
                cur.execute("DROP TABLE takenlijst;")
                cur.execute("CREATE TABLE takenlijst (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
                cur.execute("INSERT INTO takenlijst (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvantakenlijst;" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],))
                con.commit()
                print("%sBackup van Takenlijst is sucesvol gemaakt en de RecordId's zijn weer aansluitend.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Takenlijst.%s" % (colslecht,ResetAll))
            try:
                cur.execute("DROP TABLE backupvanteam;")
            except(Exception) as error:
                #print(error)
                pass
            try:
                cur.execute("CREATE TABLE backupvanteam AS SELECT * FROM team;")
                cur.execute("DROP TABLE team;")
                cur.execute("CREATE TABLE team (%s VARCHAR(25), %s VARCHAR(2), %s VARCHAR(25), %s VARCHAR(2), %s INTEGER, %s VARCHAR(25));" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
                cur.execute("INSERT INTO team (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvanteam;" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5],clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
                con.commit()
                print("%sBackup van Team is sucesvol gemaakt.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Team.%s" % (colslecht,ResetAll))
            try:
                cur.execute("DROP TABLE backupvanarchief;")
            except(Exception) as error:
                #print(error)
                pass
            try:
                cur.execute("CREATE TABLE backupvanarchief AS SELECT * FROM archief;")
                cur.execute("DROP TABLE archief;")
                cur.execute("CREATE TABLE archief (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
                cur.execute("INSERT INTO archief (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvanarchief;" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],))
                con.commit()
                print("%sBackup van Archief is sucesvol gemaakt.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Archief.%s" % (colslecht,ResetAll))
            try:
                filename = folder+os.path.sep+"Team.txt" 
                filenamebu = folder+os.path.sep+"BackupVanTeam.txt" 
                subprocess.run(["cp",filename,filenamebu])
                print("%sBackup van Team.txt is succesvol gemaakt.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Team.txt.%s" % (colslecht,ResetAll))
        elif resetjn == "2":
            try:
                cur.execute("DROP TABLE backupvantakenlijst;")
            except(Exception) as error:
                #print(error)
                pass
            try:
                cur.execute("CREATE TABLE backupvantakenlijst AS SELECT * FROM takenlijst;")
                cur.execute("DROP TABLE takenlijst;")
                cur.execute("CREATE TABLE takenlijst (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
                cur.execute("INSERT INTO takenlijst (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvantakenlijst;" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],))
                con.commit()
                print("%sBackup van Takenlijst is sucesvol gemaakt en de RecordId's zijn weer aansluitend.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Takenlijst.%s" % (colslecht,ResetAll))
        elif resetjn == "3":
            try:
                cur.execute("DROP TABLE backupvanteam;")
            except(Exception) as error:
                #print(error)
                pass
            try:
                cur.execute("CREATE TABLE backupvanteam AS SELECT * FROM team;")
                cur.execute("DROP TABLE team;")
                cur.execute("CREATE TABLE team (%s VARCHAR(25), %s VARCHAR(2), %s VARCHAR(25), %s VARCHAR(2), %s INTEGER, %s VARCHAR(25));" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
                cur.execute("INSERT INTO team (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvanteam;" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5],clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
                con.commit()
                print("%sBackup van Team is sucesvol gemaakt.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Team.%s" % (colslecht,ResetAll))
        elif resetjn == "4":
            try:
                cur.execute("DROP TABLE backupvanarchief;")
            except(Exception) as error:
                #print(error)
                pass
            try:
                cur.execute("CREATE TABLE backupvanarchief AS SELECT * FROM archief;")
                cur.execute("DROP TABLE archief;")
                cur.execute("CREATE TABLE archief (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
                cur.execute("INSERT INTO archief (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvanarchief;" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],))
                con.commit()
                print("%sBackup van Archief is sucesvol gemaakt.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Archief.%s" % (colslecht,ResetAll))
        elif resetjn == "5":
            try:
                filename = folder+os.path.sep+"Team.txt" 
                filenamebu = folder+os.path.sep+"BackupVanTeam.txt" 
                subprocess.run(["cp",filename,filenamebu])
                print("%sBackup van Team.txt is succesvol gemaakt.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup te maken van Team.txt.%s" % (colslecht,ResetAll))
        elif resetjn == "6":
            try:
                cur.execute("SELECT * FROM backupvantakenlijst;")
                cur.execute("DROP TABLE takenlijst;")
                cur.execute("CREATE TABLE takenlijst (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
                cur.execute("INSERT INTO takenlijst (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvantakenlijst;" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],))
                con.commit()
                print("%sBackup van Takenlijst is succesvol teruggezet.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sEr is geen backup van Takenlijst gevonden.%s" % (colslecht,ResetAll))
        elif resetjn == "7":
            try:
                cur.execute("SELECT * FROM backupvanteam;")
                cur.execute("DROP TABLE team;")
                cur.execute("CREATE TABLE team (%s VARCHAR(25), %s VARCHAR(2), %s VARCHAR(25), %s VARCHAR(2), %s INTEGER, %s VARCHAR(25));" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
                cur.execute("INSERT INTO team (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvanteam;" % (clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5],clteam[0],clteam[1],clteam[2],clteam[3],clteam[4],clteam[5]))
                con.commit()
                print("%sBackup van Team is succesvol teruggezet.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sEr is geen backup van Team gevonden.%s" % (colslecht,ResetAll))
        elif resetjn == "8":
            try:
                cur.execute("SELECT * FROM backupvanarchief;")
                cur.execute("DROP TABLE archief;")
                cur.execute("CREATE TABLE archief (%s INTEGER PRIMARY KEY AUTOINCREMENT, %s INTEGER, %s INTEGER, %s VARCHAR(50), %s INTEGER, %s VARCHAR(11), %s VARCHAR(100));" % (cltakenlijst[0],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6]))
                cur.execute("INSERT INTO archief (%s,%s,%s,%s,%s,%s) SELECT %s,%s,%s,%s,%s,%s FROM backupvanarchief;" % (cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],cltakenlijst[1],cltakenlijst[2],cltakenlijst[3],cltakenlijst[4],cltakenlijst[5],cltakenlijst[6],))
                con.commit()
                print("%sBackup van Archief is succesvol teruggezet.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sEr is geen backup van Archief gevonden.%s" % (colslecht,ResetAll))
        elif resetjn == "9":
            try:
                filenamebu = folder+os.path.sep+"BackupVanTeam.txt" 
                filename = folder+os.path.sep+"Team.txt" 
                subprocess.run(["cp",filenamebu,filename])
                print("%sBackup Team.txt is succesvol teruggezet.%s" % (col,ResetAll))
            except(Exception) as error:
                #print(error)
                print("%sHet is niet gelukt een Backup van Team.txt terug te zetten. Bestaat het Backupbestand wel?%s" % (colslecht,ResetAll))

    # 7: DATABASE
    elif functie[0] == "7" or functie[0].upper() == "D":
        col = coldatabase
        subprocess.run(["sqlite3","-header","-column",db])
        print(ResetAll, end = "")
            
    # 8: ALGEMENE INFORMAteam
    elif functie[0] == "8" or functie[0].upper() == "A":
        col = colinformatie
        filename = folder+os.path.sep+"Team.txt" 
        print(col)
        subprocess.run(["vim", filename])
        print(ResetAll)

    # 9: MEETING
    elif functie[0] == "9" or functie[0].upper() == "M":
        col = colmeeting
        cur.execute("SELECT COUNT(%s) FROM presentie WHERE %s = '%s';" % (pl[1],pl[3],colgoed+"IN"+ResetAll+colcheck))
        countIN = int(str(cur.fetchone()).replace("(","").replace(",)",""))
        if countIN == 0:
            print("Er zijn %sgeen deelnemers%s aan deze meeting. Voeg deze eerst toe bij %s\"0: Presentielijst\"%s" % (colslecht,ResetAll,colcheck,ResetAll))
        elif countIN == 1:
            print("%sSolomeeting%s? Voeg eerst extra deelnemers toe bij %s\"0: Presentielijst\"%s" % (colslecht,ResetAll,colcheck,ResetAll))
        else:
            lijst = []
            cur.execute("SELECT %s FROM presentie WHERE %s = '%s';" % (pl[1],pl[3],colgoed+"IN"+ResetAll+colcheck))
            lijstplus = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","").replace("\"","").split(",")
            for i in lijstplus:
                lijst.append(i)
            if Extra.upper() != "N":
                erbij = "Y"
                while erbij == "Y":
                    Extra = input("Typ de Voornamen van eventuele %sExtra deelnemers%s of niets om door te gaan:\nAls de meeting al gestart is voegt \"%sE%s\" alsnog een Extra deelnemer toe.\n  : " % (col,ResetAll,col,ResetAll))
                    if Extra.upper() in afsluitlijst or Extra.upper() in neelijst or Extra.upper() == "":
                        erbij = "N"
                        break
                    elif len(Extra) == 2 and (Extra[0].upper() in afsluitlijst or Extra[0].upper() in neelijst) and Extra[1].upper() in skiplijst:
                        toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                        if toch.upper() in jalijst:
                            print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                            exit()
                    else:
                        lijst.append(Extra)
            lijstwillekeurig = []
            aantekeningleeg = ""
            Aantekeningenlijst = []
            while len(lijst) != 0:
                r = random.choice(lijst)
                lijstwillekeurig.append(r)
                Aantekeningenlijst.append(aantekeningleeg)
                lijst.remove(r)
            Willeke = PrettyTable(lijstwillekeurig)
            print(Willeke)
            meeting = "Y"
            while meeting == "Y":
                i = 0
                while i < len(lijstwillekeurig):
                    print(col,lijstwillekeurig[i],ResetAll)
                    Aantekening = input()
                    if Aantekening.upper() in afsluitlijst or Aantekening.upper() in neelijst:
                        meeting = "N"
                        break
                    elif len(Aantekening) == 2 and (Aantekening[0].upper() in afsluitlijst or Aantekening[0].upper() in neelijst) and Aantekening[1].upper() in skiplijst:
                        toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                        if toch.upper() in jalijst:
                            print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                            exit()
                    elif Aantekening.upper() == "E": 
                        Extra = input("Typ de naam van de %sExtra deelnemer%s:\n  : " % (col,ResetAll)) 
                        if Extra.upper() in afsluitlijst or Extra.upper() in neelijst:
                            meeting = "N"
                            break
                        elif len(Extra) == 2 and (Extra[0].upper() in afsluitlijst or Extra[0].upper() in neelijst) and Extra[1].upper() in skiplijst:
                            toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                            if toch.upper() in jalijst:
                                print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                                exit()
                        else:
                            lijstwillekeurig.append(Extra)
                            Aantekeningenlijst.append(aantekeningleeg)
                            print("Extra deelnemer %s is toegevoegd" % (col+Extra+ResetAll))
                            Willeke = PrettyTable(lijstwillekeurig)
                            print(Willeke)
                    elif Aantekening == "<":
                        i -= 1
                        print("De vorige aantekening van %s is %s\"%s\"%s." % (lijstwillekeurig[i],col,Aantekeningenlijst[i],ResetAll))
                    elif Aantekening == "<x":
                        i -= 1
                        print("De vorige aantekening van %s is gewist." % (lijstwillekeurig[i]))
                        Aantekeningenlijst[i] = aantekeningleeg
                    else:
                        Aantekeningenlijst[i] = Aantekeningenlijst[i]+Aantekening
                        i += 1
                Willeke.add_row(Aantekeningenlijst)
                print(Willeke)
                nogns = input("Wil je nog een rondje?\n  : ")
                if nogns.upper() not in jalijst:
                    break

    elif functie == "0" or functie.upper() == "P":
        col = colcheck
        check = "Y"
        while check == "Y":
            if togglewie.upper() != "R":
                try:
                    presenteam()
                except(Exception) as error:
                    mkPresenteam()
                    togglewie = "N"
            else:
                try:
                    cur.execute("DROP TABLE presentie;")
                    con.commit()
                    mkPresenteam()
                    togglewie = "N"
                except(Exception) as error:
                    #print(error)
                    mkPresenteam()
                    togglewie = "N"
            cur.execute("SELECT %s FROM presentie;" % (pl[0]))
            lijst = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").split(",")
            cur.execute("SELECT %s FROM presentie;" % (pl[1]))
            VNlijst = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").split(",")
            if togglewie.upper() != "R":
                togglewie = input("Typ het %s (toggle %s of %s), %sllemaal %sn, of %seset de hele lijst (%sit):\n  : " % (col+"ID"+ResetAll,colgoed+"IN"+ResetAll,colslecht+"UIT"+ResetAll,colgoed+"A"+ResetAll,colgoed+"I"+ResetAll,colslecht+"R"+ResetAll,colslecht+"U"+ResetAll))
            if togglewie.upper() in afsluitlijst or togglewie.upper() in neelijst or togglewie.upper() == "":
                break
            elif len(togglewie) == 2 and (togglewie[0].upper() in afsluitlijst or togglewie[0].upper() in neelijst) and togglewie[1].upper() in skiplijst:
                toch = input("Weet je het %s?\n  : " % (colslecht+"zeker"+ResetAll))
                if toch.upper() in jalijst:
                    print("\n%sBedankt, aan de slag, of neem een momentje voor jezelf.%s\n" % (LichtMagenta,ResetAll))
                    exit()
            elif togglewie[0].upper() in ["R","U"]:
                cur.execute("UPDATE presentie SET %s = '%s'" % (pl[3],colslecht+"UIT"+ResetAll+col))
                con.commit()
            elif togglewie[0].upper() in ["A","I"]:
                cur.execute("UPDATE presentie SET %s = '%s'" % (pl[3],colgoed+"IN"+ResetAll+col))
                con.commit()
            else:
                if togglewie in lijst:
                    cur.execute("SELECT %s FROM presentie WHERE %s = '%s'" % (pl[3],pl[0],togglewie))
                    tog = str(cur.fetchall()).replace("[('","").replace("',)]","")
                    if tog == "\\x1b[31mUIT\\x1b[0m\\x1b[94m":
                        cur.execute("UPDATE presentie SET %s = '%s' WHERE %s = '%s'" % (pl[3],colgoed+"IN"+ResetAll+col,pl[0],togglewie))
                        con.commit()
                    else:
                        cur.execute("UPDATE presentie SET %s = '%s' WHERE %s = '%s'" % (pl[3],colslecht+"UIT"+ResetAll+col,pl[0],togglewie))
                        con.commit()
                elif "\'"+togglewie+"\'" in VNlijst:
                    cur.execute("SELECT %s FROM presentie WHERE %s = '%s'" % (pl[3],pl[1],togglewie))
                    tog = str(cur.fetchall()).replace("[('","").replace("',)]","")
                    if tog == "\\x1b[31mUIT\\x1b[0m\\x1b[94m":
                        cur.execute("UPDATE presentie SET %s = '%s' WHERE %s = '%s'" % (pl[3],colgoed+"IN"+ResetAll+col,pl[1],togglewie))
                        con.commit()
                    else:
                        cur.execute("UPDATE presentie SET %s = '%s' WHERE %s = '%s'" % (pl[3],colslecht+"UIT"+ResetAll+col,pl[1],togglewie))
                        con.commit()
                else:
                    print("Dat nummer staat niet in de lijst.")

    # 5: KALENDER = Default = else
    # elif functie[0] == "5" or functie[0].upper() == "K":
    else:
        col = colkalender
        print(col)
        subprocess.run(["ncal","-3w"]) # on Raspbian
        #subprocess.run(["cal","-3w"]) # on Mageia
        print(ResetAll, end = "")
        try:
            VandaagMinDrie = datetime.today()-timedelta(days=3)
            VMD = int(str(datetime.strftime(VandaagMinDrie,"%Y%m%d"))[:10].replace("-",""))
            KaleBereik = VandaagMinDrie
            KaleKop = []
            while KaleBereik < datetime.strptime(nu,"%Y%m%d")+timedelta(days=12):
                KaleKop.append(datetime.strftime(KaleBereik,"%m%d"))
                KaleBereik = KaleBereik+timedelta(days=1)
            KaleKop[3] = "%s%s NU %s" % (col,Omkeren,ResetAll)
            cur.execute("SELECT %s FROM takenlijst WHERE (%s IS NOT '%s' AND %s IS NOT '%s');" % (cltakenlijst[0],cltakenlijst[5],statuslijst[3],cltakenlijst[5],statuslijst[4]))
            RecLijst = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","").split(",")
            RijLijst= []
            for i in RecLijst:
                KaleRij = []
                cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[1],cltakenlijst[0],i))
                begindatum = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","")
                cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[2],cltakenlijst[0],i))
                einddatum = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","")
                cur.execute("SELECT %s FROM takenlijst WHERE %s = '%s';" % (cltakenlijst[5],cltakenlijst[0],i))
                status = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","")[7]
                cur.execute("SELECT t.%s FROM team t INNER JOIN takenlijst m ON m.%s = t.%s WHERE m.%s = '%s';" % (clteam[1],cltakenlijst[4],clteam[4],cltakenlijst[0],i))
                VN = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","")
                cur.execute("SELECT t.%s FROM team t INNER JOIN takenlijst m ON m.%s = t.%s WHERE m.%s = '%s';" % (clteam[3],cltakenlijst[4],clteam[4],cltakenlijst[0],i))
                AN = str(cur.fetchall()).replace("[","").replace("]","").replace("(","").replace(",)","").replace(" ","").replace("'","")
                med = VN[0]+AN
                Datum = VandaagMinDrie
                if status == "0":
                    col = colstat0
                elif status == "1":
                    col = colstat1
                elif status == "2":
                    col = colstat2
                elif status == "5":
                    col = colstat5
                if datetime.strptime(einddatum,"%Y%m%d") >= datetime.today()+timedelta(days=12):
                    einddatum = str(datetime.today()+timedelta(days=12))[:10].replace("-","")
                while Datum < datetime.strptime(begindatum,"%Y%m%d"):
                    KaleRij.append("")
                    Datum = Datum+timedelta(days=1)
                while datetime.strptime(begindatum,"%Y%m%d") < Datum < datetime.strptime(einddatum,"%Y%m%d")+timedelta(days=1):
                    KaleRij.append(col+i+med+ResetAll)
                    Datum = Datum+timedelta(days=1)
                while datetime.strptime(einddatum,"%Y%m%d")+timedelta(days=1) < Datum < datetime.today()+timedelta(days=11):
                    if col == colstat5:
                        KaleRij.append(col+i+" !!"+ResetAll)
                        Datum = Datum+timedelta(days=1)
                    else:
                        KaleRij.append(col+i+ResetAll)
                        Datum = Datum+timedelta(days=1)
                KaleRij = KaleRij[:15] # TODO: Als de Begin EN Eind buiten het bereik vallen zit er een record teveel in de lijst
                RijLijst.append(KaleRij)
            Kalender = PrettyTable(KaleKop)
            for i in RijLijst:
                Kalender.add_row(i)
            print(Kalender)
        except(Exception) as error:
            #print(error)
            print("%sDe Kalender bevat geen geplande, gestarte of verlopen taken.\nGepauzeerde, afgebroken en afgesloten taken worden niet getoond.%s" % (col,ResetAll))

