#!/usr/bin/python3
versie = "1.68"
datum = "20240211"
import locale, os, ast, pathlib, subprocess, random, textwrap, calendar
from datetime import *
from dateutil.relativedelta import *
from time import sleep

key = "emailadres"
#key = "personeelsnummer"
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
coldatum = LichtCyaan
colover = LichtGrijs
coltoevoegen = LichtGroen
colbekijken = LichtGeel
colwijzigen = LichtCyaan
colverwijderen = LichtRood
colmeeting = LichtMagenta
colinformatie = Wit
colterug = DonkerGrijs
colgoed = Groen
colslecht = Rood
statcol = [Geel,LichtGeel,Magenta,Rood,Groen,LichtRood,DonkerGrijs]
iocol = [Rood,Groen]
logocol = [coltoevoegen,colbekijken,colwijzigen,colverwijderen,colmeeting,colinformatie]

TeamLogo = """ .______.  
 |/ \/ \|__.   _. ___. _.    
    ||  //_\\\\ 6_\\\\|| \V \\\\   
    || ||'   // |||| || ||   
   _/\_ \\\\_/|\\\\/|\/\ || /\\   """
lenlijst = 0
try:
    while len(TeamLogo) > 0:
        for i in logocol:
            sleep(0.0125)
            print(i,end = "")
            print(TeamLogo[logocol.index(i)+lenlijst], end = "", flush = True)
            TeamLogo = TeamLogo[0:]
        lenlijst += len(logocol)
except:
    print(ResetAll)

nu = datetime.strftime(datetime.today(),"%Y%m%d")
afsluitlijst = ["X","Q",":X",":Q"]
jalijst = ["J","JA","Y","YES","OK","K","SURE","JAZEKER","ZEKER","INDERDAAD","IDD"]
neelijst = ["N"]
skiplijst = ["!",">","S","D"] # Skip, Standaard, Default
inputindent = "  : "
dagenlijstEN = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
maandlijstEN = ["January","February","March","April","May","June","July", "August", "September","October","November","December"]
dagenlijstNL = ["maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag","zondag"]
maandlijstNL = ["januari","februari","maart","april","mei","juni","juli", "augustus", "september","oktober","november","december"]
scopenunu = {}
wi = 66
forcwi = ("{:^%s}" % wi).format
vim = """# NL:
#     Ga naar schrijfmodus met "i", verlaat schrijfmodus met "Esc"
#     Opslaan met ":w"+"Enter", verlaat Vim met ":q"+"Enter"
# EN:
#     Enter input mode with "i", leave input mode with "Esc"
#     Save/write with ":w"+"Enter", exit/quit Vim with ":q"+"Enter"
"""
print()

lang = False
while lang == False:
    qlang = input("Kies uw taal | Choose your language:\n  > 1: NL\n    2: EN\n%s" % inputindent)
    if qlang.upper() in afsluitlijst:
        exit()
    elif qlang == "2":
        lang = "EN"
    else:
        lang = "NL"

if lang == "EN":
    checklijst = ["OUT","IN"]
    weg = "%s  Q!: Exit%s" % (ResetAll+colterug,ResetAll)
    terug = "%s  Q : Back%s" % (ResetAll+colterug,ResetAll)
    statuslijst = ["Planned","Started","Paused","Aborted","Completed","Overdue","Absent"]
    taakverdeling = ["Start","Due","TaskDescription","Name","Note","Status"]
    if key == "emailadres":
        teamverdeling = ["EMail address","Given Name","Last Name","Check","Note"]
    else:
        teamverdeling = ["Agent Number","Given Name","Last Name","Check","Note"]
else:
    checklijst = ["UIT","IN"]
    weg = "%s  Q!: Afsluiten%s" % (ResetAll+colterug,ResetAll)
    terug = "%s  Q : Terug%s" % (ResetAll+colterug,ResetAll)
    statuslijst = ["Gepland","Gestart","Gepauzeerd","Afgebroken","Afgerond","Verlopen","Afwezig"]
    taakverdeling = ["Start","Eind","Taakomschrijving","Naam","Aantekening","Status"]
    if key == "emailadres":
        teamverdeling = ["EMailadres","VoorNaam","AchterNaam","Check","Aantekening"]
    else:
        teamverdeling = ["Personeelsnummer","VoorNaam","AchterNaam","Check","Aantekening"]

def printdag():
    todaag = datetime.strftime(datetime.today(),"%A %Y%m%d")
    week = datetime.strftime(datetime.today(),"%W")
    if lang == "EN":
        dag = "Today is %s." 
        for i in range(len(dagenlijstNL)):
            todaag = todaag.replace(dagenlijstNL[i],dagenlijstEN[i])
        print(dag % (coldatum+todaag+" week "+week+ResetAll))
    else:
        dag = "Het is vandaag %s."
        for i in range(len(dagenlijstEN)):
            todaag = todaag.replace(dagenlijstEN[i],dagenlijstNL[i])
        print(dag % (coldatum+todaag+" week "+week+ResetAll))

# Veel formaten niet in gebruik, maar handig om mee te testen
forc2 = "{:^2}".format
forl2 = "{:<2}".format
forr2 = "{:>2}".format
for0r2 = "{:0>2}".format
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

def printstuff():
    if lang == "EN":
        ve = "Version:"
        da = "Date:"
        stuff1 = textwrap.wrap("\"TEAM\" is a simple planning tool for team leads and managers. Check Agents IN or OUT, register personal talents and expertise, assign Tasks and organize meetings.", width = wi)
        stuff2 = textwrap.wrap("Tasks and Agents are assigned an ad hoc ID on which operations can be performed. An additional Agent called \"Whole Team\" is present by default with ID \"0\", not shown in the overviews. If it is deleted (if the alphabetically sorted first Agent has ID \"0\"), you can add this \"Agent\" with Agent Number or EMail address \"00000\" manually. Agents can be combined into SubTeams. Remember that Tasks assigned to a SubTeam do not appear with the involved individual Agents.", width = wi)
        stuff3 = textwrap.wrap("Confirm every choice with \"Enter\", go back with \"Q\" or leave the program immediately with \"Q!\". The option \"Notepad (Vim)\" uses the application \"Vim\". Make sure it is installed.\n", width = wi)
    else:
        ve = "Versie:"
        da = "Datum:"
        stuff1 = textwrap.wrap("\"TEAM\" is een simpele planningstool voor leidinggevenden en managers. Check Medewerkers IN of UIT, registreer persoonlijke talenten en expertise, verdeel Taken en organiseer vergaderingen.", width = wi)
        stuff2 = textwrap.wrap("Alle Taken en Medewerkers krijgen ad hoc een ID waarop de bewerkingen kunnen worden uitgevoerd. Een extra medewerker \"Hele Team\" is standaard aanwezig met ID \"0\", die in de overzichten niet wordt getoond. Als deze \"Medewerker\" werd verwijderd (als de alfabetisch gesorteerd eerste Medewerker ID \"0\" heeft), dan kunt u die handmatig toevoegen met PersoneelsNummer of EMailadres \"00000\". Medewerkers kunnen worden gecombineerd tot SubTeams. Denk eraan dat aan een SubTeam toegewezen Taak niet te zien is bij de betrokken individuele Medewerkers.", width = wi)
        stuff3 = textwrap.wrap("Bevestig iedere keuze met \"Enter\", ga terug met \"Q\" of verlaat het programma direct met \"Q!\". De optie \"Kladblok (Vim)\" maakt gebruik van de applicatie \"Vim\". Installeer dat eerst.", width = wi)
    print()
    print(colover+forl8(ve)+versie+ResetAll)
    print(colover+forl8(da)+datum+ResetAll)
    print()
    for i in stuff1:
        print(colover+i+ResetAll)
    for i in stuff2:
        print(colover+i+ResetAll)
    for i in stuff3:
        print(colover+i+ResetAll)
    print()


def eindroutine():
    if lang == "EN":
        zeker = "Are you %ssure%s?\n%s" % (colslecht,ResetAll,inputindent)
        bedankt = "\n%sThank you, back to work, or take a moment for yourself.%s\n" % (LichtMagenta,ResetAll)
    else:
        zeker = "Weet u het %szeker%s?\n%s" % (colslecht,ResetAll,inputindent)
        bedankt = "\n%sBedankt, aan de slag, of neem een momentje voor uzelf.%s\n" % (LichtMagenta,ResetAll)
    toch = input(zeker)
    if toch.upper() in jalijst:
        print(bedankt)
        exit()

def statusshow():
    for i in statuslijst:
        col = statcol[statuslijst.index(i)]
        ID = statuslijst.index(i)+1
        print("  %s : " % (ID)+col+forl15(i)+ResetAll)

def team():
    try:
        with open("teamlijst","r") as t:
            teamlijst = sorted(ast.literal_eval(t.read()))
        with open("teamlijst","w") as t:
            print(teamlijst, end = "", file = t)
    except:
        if lang == "EN":
            teamlijst = [['00000','Whole','Team',2,'Whole Team']]
        else:
            teamlijst = [['00000','Hele','Team',2,'Hele Team']]
        with open("teamlijst","w") as t:
            print(teamlijst, end = "", file = t)
    return teamlijst

def nepecht():
    teamlijst = team()
    nep = []
    echt = []
    for i in teamlijst:
        if i[0] == "00000" or i[0][0] == "~":
            nep.append(i)
    for i in teamlijst:
        if i not in nep:
            echt.append(i)
    return teamlijst,nep,echt

def taak():
    try:
        with open("takenlijst","r") as t:
            takenlijst = ast.literal_eval(t.read())
    except:
        takenlijst = []
        with open("takenlijst","w") as t:
            print(takenlijst, end = "", file = t)
    return takenlijst

def hoeveeltaken():
    takenlijst = taak()
    if len(takenlijst) == 1:
        if lang == "EN":
            print("There is %s Task in the list." % len(takenlijst))
        else:
            print("Er staat %s Taak in de lijst." % len(takenlijst))
    else:
        if lang == "EN":
            print("There are %s Tasks in the list." % len(takenlijst))
        else:
            print("Er staan %s Taken in de lijst." % len(takenlijst))

def checkstatusdatum():
    takenlijst = taak()
    oeilijst = []
    for i in takenlijst:
        if datetime.strptime(str(i[0]),"%Y%m%d") > datetime.strptime(nu,"%Y%m%d") and i[5] not in [3,4,5,7]:
            i[5] = 1
        if datetime.strptime(str(i[0]),"%Y%m%d") <= datetime.strptime(nu,"%Y%m%d") and i[5] == 1:
            i[5] = 2
        if datetime.strptime(str(i[1]),"%Y%m%d") < datetime.strptime(nu,"%Y%m%d") and i[5] == 2:
            i[5] = 6
        if i[5] == 6:
            oeilijst.append(i)
    if len(oeilijst) == 1:
        if lang == "EN":
            verlopentaak = "There is 1 Task Overdue."
        else:
            verlopentaak = "Er is 1 Verlopen Taak."
        print(statcol[5]+verlopentaak+ResetAll)
    elif len(oeilijst) > 1:
        if lang == "EN":
            verlopentaken = "There are %s Tasks Overdue." % len(oeilijst)
        else:
            verlopentaken = "Er zijn %s Verlopen Taken." % len(oeilijst)
        print(statcol[5]+verlopentaken+ResetAll)
    takenlijst = sorted(takenlijst)
    with open("takenlijst","w") as t:
        print(takenlijst, end = "", file = t)
    return oeilijst
    print()
    
def wijzigoei(oeilijst):
    print()
    takenlijst = taak()
    for i in oeilijst:
        if i in takenlijst:
            indi = takenlijst.index(i)+1
            if lang == "EN":
                print("Change the Due date or the Status of Task %s" % statcol[5]+str(indi)+ResetAll)
            else:
                print("Wijzig de Einddatum of de Status van Taak %s" % statcol[5]+str(indi)+ResetAll)
    print()

def teamnieuw():
    teamshowbasis()
    if lang == "EN":
        nieuwevoornaam = "Type the GivenNamem, or IDs as CSV (for a SubTeam):\n%s" % inputindent
        eindsubteam = "End adding Agents to the SubTeam with \"~\"."
        nieuweachternaam = "Type the LastName:\n%s" % inputindent
        if key == "emailadres":
            nieuwemail = "Type the EMail:\n%s" % inputindent
            nietuniek = "This EMail already exists."
        else:
            nieuwpersoneelsnummer = "Type the AgentNumber:\n%s" % inputindent
            nietuniek = "This AgentNumber already exists."
        nieuweaantekening = "Type a Note (opt):\n%s" % inputindent
    else:
        nieuwevoornaam = "Typ de VoorNaam, of ID's als CSV (voor een SubTeam):\n%s" % inputindent
        eindsubteam = "Beëindig het toevoegen van Medewerkers aan dit SubTeam met \"~\"."
        nieuweachternaam = "Typ de AchterNaam:\n%s" % inputindent
        if key == "emailadres":
            nieuwemail = "Typ het EMailadres:\n%s" % inputindent
            nietuniek = "Dit EMailadres bestaat al."
        else:
            nieuwpersoneelsnummer = "Typ het PersoneelsNummer:\n%s" % inputindent
            nietuniek = "Dit Personeelsnummer bestaat al."
        nieuweaantekening = "Typ een Aantekening (opt):\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    subteamvoornaam = "~"
    voornaam = False
    while voornaam == False:
        VN = input(nieuwevoornaam)
        if VN.upper() in afsluitlijst:
            uit = True
            return uit
        elif len(VN) == 2 and VN[0].upper() in afsluitlijst and VN[1].upper() in skiplijst:
            eindroutine()
        try:
            VNCSV = VN.replace(" ","").split(",")
            for i in VNCSV:
                if int(i)-1 in range(len(echt)):
                    subteamvoornaam += echt[int(i)-1][1]+"~"
            print(subteamvoornaam)
            print(colover+forcwi(eindsubteam)+ResetAll)
        except:
            if VN == "~":
                AN = subteamvoornaam
                print(AN)
                if lang == "EN":
                    VN = "SubTeam"
                else:
                    VN = "SubTeam"
            if key == "emailadres":
                EM = subteamvoornaam
            else:
                PN = subteamvoornaam
            if len(VN) == 0:
                pass
            else:
                voornaam = True
    try:
        print(AN)
    except:
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
        if key == "emailadres":
            email = False
            while email == False:
                EM = input(nieuwemail)
                if EM.upper() in afsluitlijst:
                    uit = True
                    return uit
                elif len(EM) == 2 and EM[0].upper() in afsluitlijst and EM[1].upper() in skiplijst:
                    eindroutine()
                elif len(EM) < 1:
                    pass
                else:
                    u = True
                    for i in teamlijst:
                        if EM == i[0]:
                            u = False
                    if u == False:
                        print(colslecht+nietuniek+ResetAll)
                    else:
                        email = True
        else:
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
                    u = True
                    for i in teamlijst:
                        if PN == i[0]:
                            u = False
                    if u == False:
                        print(colslecht+nietuniek+ResetAll)
                    else:
                        personeelsnummer = True
    AT = input(nieuweaantekening)
    if AT.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(AT) == 2 and AT[0].upper() in afsluitlijst and AT[1].upper() in skiplijst:
        eindroutine()
    if key == "emailadres":
        nieuwteam = [EM,VN,AN,0,AT]
    else:
        nieuwteam = [PN,VN,AN,0,AT]
    teamlijst.append(nieuwteam)
    teamlijst = sorted(teamlijst)
    with open("teamlijst","w") as t:
        print(teamlijst, end = "", file = t)
    print()

def teamshowbasis():
    if lang == "EN":
        tpmofukt = "Type the ID to view the Tasks of that Agent ir SubTeam:\n%s" % inputindent
    else:
        tpmofukt = "Typ de ID om de taken van die Medewerker of dat SubTeam te zien:\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    lijn = "+--+----------+----------+--------------------+-----+------------+"
    if lang == "EN":
        if key == "emailadres":
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("EMail")[:10],forc10("GivenName")[:10],forc20("LastName")[:20],forc5("Chk")[:5],forc12("Note")[:12])
        else:
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("AN")[:10],forc10("GivenName")[:10],forc20("LastName")[:20],forc5("Chk")[:5],forc12("Note")[:12])
    else:
        if key == "emailadres":
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("EMail")[:10],forc10("VoorNaam")[:10],forc20("AchterNaam")[:20],forc5("Chk")[:5],forc12("Aantekening")[:12])
        else:
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("PN")[:10],forc10("VoorNaam")[:10],forc20("AchterNaam")[:20],forc5("Chk")[:5],forc12("Aantekening")[:12])
    print(colbekijken+lijn+ResetAll)
    print(kop)
    print(lijn)
    for i in teamlijst:
        if i[0] != "00000":
            ID = teamlijst.index(i)
            if i[0][0] == "~":
                print(forr3(ID),forc10(i[0])[:10],forr10(i[1])[:10],forl20(i[2])[:20],forc5(""),forl12(i[4])[:12])
            else:
                print(forr3(ID),forc10(i[0])[:10],forr10(i[1])[:10],forl20(i[2])[:20],iocol[int(forc5(i[3]))]+forc5(checklijst[int(forc5(i[3]))])[:5]+ResetAll,forl12(i[4])[:12])
    print(colbekijken+lijn+ResetAll)
    print()

def teamshowbasisecht():
    if lang == "EN":
        tpmofukt = "Type the ID to view the Tasks of that Agent ir SubTeam:\n%s" % inputindent
    else:
        tpmofukt = "Typ de ID om de taken van die Medewerker of dat SubTeam te zien:\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    lijn = "+--+----------+----------+--------------------+-----+------------+"
    if lang == "EN":
        if key == "emailadres":
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("EMail")[:10],forc10("GivenName")[:10],forc20("LastName")[:20],forc5("Chk")[:5],forc12("Note")[:12])
        else:
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("AN")[:10],forc10("GivenName")[:10],forc20("LastName")[:20],forc5("Chk")[:5],forc12("Note")[:12])
    else:
        if key == "emailadres":
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("EMail")[:10],forc10("VoorNaam")[:10],forc20("AchterNaam")[:20],forc5("Chk")[:5],forc12("Aantekening")[:12])
        else:
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("PN")[:10],forc10("VoorNaam")[:10],forc20("AchterNaam")[:20],forc5("Chk")[:5],forc12("Aantekening")[:12])
    print(colbekijken+lijn+ResetAll)
    print(kop)
    print(lijn)
    for i in echt:
        if i[0] != "00000":
            ID = echt.index(i)+1
            print(forr3(ID),forc10(i[0])[:10],forr10(i[1])[:10],forl20(i[2])[:20],iocol[int(forc5(i[3]))]+forc5(checklijst[int(forc5(i[3]))])[:5]+ResetAll,forl12(i[4])[:12])
    print(colbekijken+lijn+ResetAll)
    print()


def teamshowkort():
    lenlist = 0
    numin = 0
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    for i in echt:
        numin += i[3]
        lenlist += 1
    if numin == 1:
        col = iocol[1]
        if lang == "EN":
            aanin = "There is %s Agent - of %s - checked %sIN%s." % (col+str(numin)+ResetAll,str(lenlist),iocol[1],ResetAll)
        else:
            aanin = "Er is %s Medewerker - van %s - %sIN%sgecheckt." % (col+str(numin)+ResetAll,str(lenlist),iocol[1],ResetAll)
    elif numin == 0:
        col = iocol[0]
        if lang == "EN":
            aanin = "%s - of %s - is checked %sIN%s." % (col+"No-one"+ResetAll,str(lenlist),iocol[1],ResetAll)
        else:
            aanin = "%s - van %s - is %sIN%sgecheckt." % (col+"Niemand"+ResetAll,str(lenlist),iocol[1],ResetAll)
    elif numin == lenlist:
        col = iocol[1]
        if lang == "EN":
            aanin = "%s - of %s - is checked %sIN%s." % (col+"Everyone"+ResetAll,str(lenlist),iocol[1],ResetAll)
        else:
            aanin = "%s - van %s - is %sIN%sgecheckt." % (col+"Iedereen"+ResetAll,str(lenlist),iocol[1],ResetAll)
    else:
        col = iocol[1]
        if numin == 0:
            col = iocol[0]
        if lang == "EN":
            aanin = "There are %s Agents - of %s - checked %sIN%s." % (col+str(numin)+ResetAll,str(lenlist),iocol[1],ResetAll)
        else:
            aanin = "Er zijn %s Medewerkers - van %s - %sIN%sgecheckt." % (col+str(numin)+ResetAll,str(lenlist),iocol[1],ResetAll)
    print(aanin)
 
def teamshow():
    if lang == "EN":
        tpmofukt = "View Agent or SubTeam's details or Tasks:\n  1 : Details\n >2 : Tasks:\n%s" % inputindent
        tpmidq = "Type an Agent or SubTeam's ID:\n%s" % inputindent
    else:
        tpmofukt = "Bekijk details of Taken van een Medewerker of SubTeam:\n  1 : Details\n >2 : Taken:\n%s" % inputindent
        tpmidq = "Typ de ID van een Medewerker of SubTeam:\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    lijn = "+--+----------+----------+--------------------+-----+------------+"
    if lang == "EN":
        if key == "emailadres":
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("EMail")[:10],forc10("GivenName")[:10],forc20("LastName")[:20],forc5("Chk")[:5],forc12("Note")[:12])
        else:
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("AN")[:10],forc10("GivenName")[:10],forc20("LastName")[:20],forc5("Chk")[:5],forc12("Note")[:12])
    else:
        if key == "emailadres":
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("EMail")[:10],forc10("VoorNaam")[:10],forc20("AchterNaam")[:20],forc5("Chk")[:5],forc12("Aantekening")[:12])
        else:
            kop = "%s %s %s %s %s %s" % (forr3("ID"),forc10("PN")[:10],forc10("VoorNaam")[:10],forc20("AchterNaam")[:20],forc5("Chk")[:5],forc12("Aantekening")[:12])
    print(colbekijken+lijn+ResetAll)
    print(kop)
    print(lijn)
    for i in teamlijst:
        if i[0] != "00000":
            ID = teamlijst.index(i)
            if i[0][0] == "~":
                print(forr3(ID),forc10(i[0])[:10],forr10(i[1])[:10],forl25(i[2])[:20],forc5(""),forl12(i[4])[:12])
            else:
                print(forr3(ID),forc10(i[0])[:10],forr10(i[1])[:10],forl25(i[2])[:20],iocol[int(forc5(i[3]))]+forc5(checklijst[int(forc5(i[3]))])[:5]+ResetAll,forl12(i[4])[:12])
    print(colbekijken+lijn+ResetAll)
    takenlijst = taak()
    tpm = input(tpmofukt)
    if tpm.upper() in afsluitlijst:
        return
    elif len(tpm) == 2 and tpm[0].upper() in afsluitlijst and tpm[1].upper() in skiplijst:
        eindroutine()
    elif tpm == "1":
        uitklapteam()
    else:
        tpmid = input(tpmidq)
        lijn = "+"+"-"*20+"+"+"-"*20
        try:
            tpmid = int(tpmid)
            mw = teamlijst[tpmid][1]+" "+teamlijst[tpmid][2]
            for i in takenlijst:
                if i[3] == mw:
                    print(lijn)
                    tv = 0
                    for j in i:
                        col = ResetAll
                        ij = j
                        if j == i[2] or j == i[5]:
                            col = statcol[i[5]-1]
                        if j == i[5]:
                            col = Omkeren+statcol[i[5]-1]
                            ij = statuslijst[j-1]
                        print(" "+forl20(taakverdeling[tv]),col+str(ij)+ResetAll)
                        tv +=1
                    print(lijn)
        except:
            pass
    print()
 
def taaknieuw():
    if lang == "EN":
        nok = "   >1 : New\n    2 : Copy\n  %s" % inputindent
        welk = "Give the ID of the Task you want to copy:\n%s" % inputindent
        maand = "m"
        startdatum = "Give the Start date (YYYYMMDD) or \"%s+0\" for thismonthfirstday:\n%s" % (maand,inputindent)
        nieuwestartdatum = "Give the new Start date (YYYYMMDD) or \"%s+0\" for thismonthfirstday:\n%s" % (maand,inputindent)
        einddatum = "Give the Due date (YYYYMMDD, or \"+N\" adds days to the Start date):\n%s" % inputindent
        omschrijving = "Give the TaskDescription:\n%s" % inputindent
        moetlanger = "Give at least 4 characters."
        wie = "Give the ID of the Agent or SubTeam:\n%s" % inputindent
        aantekening = "Give extra Info (opt):\n%s" % inputindent
        staten = "Give the ID of one of these Statuses:"
    else:
        nok = "   >1 : Nieuw\n    2 : Kopie\n  %s" % inputindent
        welk = "Geef de ID op van de Taak die u wilt kopiëren:\n%s" % inputindent
        maand = "m"
        startdatum = "Geef de Startdatum op (YYYYMMDD) of \"%s+0\" voor dezemaandeerstedag:\n%s" % (maand,inputindent)
        nieuwestartdatum = "Geef de nieuwe Startdatum op (YYYYMMDD) of \"%s+0\" voor dezemaandeerstedag:\n%s" % (maand,inputindent)
        einddatum = "Geef de Einddatum op (YYYYMMDD, of \"+N\" voegt dagen toe aan Startdatum):\n%s" % inputindent
        omschrijving = "Geef de Taakbeschrijving op:\n%s" % inputindent
        moetlanger = "Geef tenminste 4 karakters op."
        wie = "Geef de ID van de Medewerker of het SubTeam:\n%s" % inputindent
        aantekening = "Geef extra Informatie (opt):\n%s" % inputindent
        staten = "Geef de ID van één van deze Statusen:"
    takenlijst = taak()
    niko = input(nok)
    if niko.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(niko) == 2 and niko[0].upper() in afsluitlijst and niko[1].upper() in skiplijst:
        eindroutine()
    elif niko == "2":
        takensmal()
        kopie = False
        while kopie == False:
            uitklapofstatus = input(welk)
            if uitklapofstatus.upper() in afsluitlijst:
                return
            elif len(uitklapofstatus) == 2 and uitklapofstatus[0].upper() in afsluitlijst and uitklapofstatus[1].upper() in skiplijst:
                eindroutine()
            try:
                uitklap = int(uitklapofstatus)
                if 1 <= uitklap <= len(takenlijst):
                    uitklaptaak(uitklapofstatus)
                    start = str(takenlijst[uitklap-1][0])
                    eind =  str(takenlijst[uitklap-1][1])
                    startdat = datetime.strptime(start,"%Y%m%d")
                    einddat = datetime.strptime(eind,"%Y%m%d")
                    lent = einddat - startdat
                    helemaand = False
                    if start[6:] == "01" and start[:6] == eind[:6] and int(eind[6:]) == calendar.monthrange(int(eind[:4]),int(eind[4:6]))[1]:
                        helemaand = True
                    StartDatum = False
                    while StartDatum == False:
                        SD = input(nieuwestartdatum)
                        if SD.upper() in afsluitlijst:
                            return
                        elif len(SD) == 2 and SD[0].upper() in afsluitlijst and SD[1].upper() in skiplijst:
                            eindroutine()
                        try:
                            if SD[0] in ["+","-"]:
                                delta = eval(SD)
                                startdat = startdat + timedelta(days = delta)
                            else:
                                startdat = datetime.strptime(SD,"%Y%m%d")
                            StartDatum = True
                        except:
                            if len(SD) > 1 and SD[0].lower() == maand:
                                try:
                                    plus = eval(SD[1:])
                                    maandstart = datetime.strptime(datetime.strftime(datetime.today(),"%Y%m")+"01","%Y%m%d")
                                    startdat = datetime.strptime(datetime.strftime(maandstart+timedelta(days = 15 + (30*plus)),"%Y%m"+"01"),"%Y%m%d")
                                    StartDatum = True
                                except:
                                    pass
                            elif len(SD) == 1 and SD.lower() == maand:
                                startdat = datetime.strptime(datetime.strftime(datetime.today(),"%Y%m")+"01","%Y%m%d")
                                StartDatum = True
                            else:
                                startdat = date.today()
                                StartDatum = True
                    start = int(datetime.strftime(startdat,"%Y%m%d"))
                    if helemaand == True and str(start)[6:] == "01":
                        einddat = startdat + timedelta(days = (calendar.monthrange(int(str(start)[:4]),int(str(start)[4:6]))[1]-1))
                    else:
                        einddat = startdat + lent
                    eind = int(datetime.strftime(einddat,"%Y%m%d"))
                    kopie =  True

                else:
                    del uitklap
            except:
                pass
        kopietaak = [start,eind,takenlijst[uitklap-1][2],takenlijst[uitklap-1][3],takenlijst[uitklap-1][4],takenlijst[uitklap-1][5]]
        takenlijst.append(kopietaak)
        takenlijst = sorted(takenlijst)
        nieuwetaakindex = takenlijst.index(kopietaak)+1
        col = statcol[kopietaak[5]-1]
        if lang == "EN":
            print("The new Task has (for now) ID: %s" % col+str(nieuwetaakindex)+ResetAll)
        else:
            print("De nieuwe Taak heeft (voorlopig) ID: %s" % col+str(nieuwetaakindex)+ResetAll)
        lijn = "+"+"-"*20+"+"+"-"*20
        print(colbekijken+lijn+ResetAll)
        for i in range(len(kopietaak)):
            ij = kopietaak[i]
            if i == 5:
                ij = statuslijst[kopietaak[i]-1]
            if i == 2 or i == 5:
                print(" "+forl20(taakverdeling[i]),col+str(ij)+ResetAll)
            else:
                print(" "+forl20(taakverdeling[i]),str(ij))
        print(colbekijken+lijn+ResetAll)
        checkstatusdatum()
        with open("takenlijst","w") as t:
            print(takenlijst, end = "", file = t)
    else:
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
                    try:
                        startdat = datetime.strptime(SD,"%Y%m%d")
                    except:
                        if len(SD) > 1 and SD[0].lower() == maand:
                            try:
                                plus = eval(SD[1:])
                                maandstart = datetime.strptime(datetime.strftime(datetime.today(),"%Y%m")+"01","%Y%m%d")
                                startdat = datetime.strptime(datetime.strftime(maandstart+timedelta(days = 15 + (30*plus)),"%Y%m"+"01"),"%Y%m%d")
                            except:
                                pass
                        elif len(SD) == 1 and SD.lower() == maand:
                            startdat = datetime.strptime(datetime.strftime(datetime.today(),"%Y%m")+"01","%Y%m%d")
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
                    try:
                        einddat = datetime.strptime(ED,"%Y%m%d")
                    except:
                        if ED.lower() == maand:
                            maandstr = datetime.strftime(startdat,"%Y%m")
                            einddat = datetime.strptime(maandstr+str(calendar.monthrange(int(maandstr[:4]),int(maandstr[4:]))[1]),"%Y%m%d")
                eind = int(datetime.strftime(einddat,"%Y%m%d"))
                if eind >= start:
                    if lang == "EN":
                        print("The Due date is %s." % eind)
                    else:
                        print("De Einddatum is %s." % eind)
                    EindDatum = True
            except:
                einddat = startdat+timedelta(days = 6)
                eind = int(datetime.strftime(einddat,"%Y%m%d"))
                if lang == "EN":
                    print("The default Due date (Start date + 6 days: %s) is selected." % eind)
                else:
                    print("De standaardEinddatum (Startdatum + 6 dagen: %s) is geselecteerd." % eind)
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
        teamlijst = nepecht()[0]
        nep = nepecht()[1]
        echt = nepecht()[2]
        teamshowbasis()
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
                if 0 <= LL <= len(teamlijst):
                    die = teamlijst[LL]
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
        nieuwetaakindex = takenlijst.index(nieuwtaak)+1
        col = statcol[nieuwtaak[5]-1]
        if lang == "EN":
            print("The new Task has (for now) ID: %s" % Omkeren+col+str(nieuwetaakindex)+ResetAll)
        else:
            print("De nieuwe Taak heeft (voorlopig) ID: %s" % Omkeren+col+str(nieuwetaakindex)+ResetAll)
        lijn = "+"+"-"*20+"+"+"-"*20
        print(colbekijken+lijn+ResetAll)
        for i in range(len(nieuwtaak)):
            col = ResetAll
            ij = nieuwtaak[i]
            if i == 2:
                col = statcol[nieuwtaak[5]-1]
            if i == 5:
                col = Omkeren+statcol[nieuwtaak[5]-1]
                ij = statuslijst[nieuwtaak[i]-1]
            print(" "+forl20(taakverdeling[i]),col+str(ij)+ResetAll)
        print(colbekijken+lijn+ResetAll)
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
        print(forr3(ID),forc4(str(i[0]))[4:],forc4(str(i[1]))[4:],statcol[int(i[5])-1]+forl11(i[2])[:11]+ResetAll,forl11(i[3])[:11],forl11(i[4])[:11],Omkeren+statcol[int(i[5])-1]+forl10(statuslijst[int(i[5])-1])[:10]+ResetAll)
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
        print(forr3(ID),forc8(str(i[0]))[:8],forc8(str(i[1]))[:8],statcol[int(i[5])-1]+forl20(i[2])[:20]+ResetAll,forl20(i[3])[:20],forl20(i[4])[:20],Omkeren+statcol[int(i[5])-1]+forl15(statuslijst[int(i[5])-1])[:15]+ResetAll)
    print(colbekijken+lijn+ResetAll)
    print()

def takenlijn(scopenunu):
    scope = scopenunu["scope"]
    nunu = scopenunu["nunu"]
    lijn = "+"+"----+"*scope
    eerstedatum = datetime.strptime(nu,"%Y%m%d")-timedelta(days = nunu)
    laatstedatum = eerstedatum + timedelta(days = scope)
    print(colbekijken+lijn+ResetAll)
    datumbereik = []
    for i in range(scope):
        ij = eerstedatum + timedelta(days = i)
        j = datetime.strftime(ij,"%y%m")
        datumbereik.append(j)
        wdcol = ResetAll
        if ij.weekday() in [5,6]:
            wdcol = DonkerGrijs
        if i == nunu-1:
            if lang == "EN":
                dij = "yd"
                j = statcol[5]+forc4(dij[:2])+ResetAll
            else:
                dij = "gi"
                j = statcol[5]+forc4(dij[:2])+ResetAll
        if i == nunu:
            if lang == "EN":
                j = coldatum+forc4("NOW")+ResetAll
            else:
                j = coldatum+forc4("NU")+ResetAll
        if i == nunu+1:
            if lang == "EN":
                dij = "tm"
                j = statcol[0]+forc4(dij[:2])+ResetAll
            else:
                dij = "mo"
                j = statcol[0]+forc4(dij[:2])+ResetAll
        print(" "+wdcol+j+ResetAll, end = "")
    print()
    for i in range(scope):
        ij = eerstedatum + timedelta(days = i)
        j = datetime.strftime(ij,"%m%d")
        datumbereik.append(j)
        wdcol = ResetAll
        if ij.weekday() in [5,6]:
            wdcol = DonkerGrijs
        if lang == "EN":
            dij = datetime.strftime(ij,"%A")
            for d in range(len(dagenlijstNL)):
                dij = dij.replace(dagenlijstNL[d],dagenlijstEN[d])
            j = forc4(dij[:2]+j[2:])
        else:
            dij = datetime.strftime(ij,"%A")
            for d in range(len(dagenlijstEN)):
                dij = dij.replace(dagenlijstEN[d],dagenlijstNL[d])
            j = forc4(dij[:2]+j[2:])
        print(" "+wdcol+j+ResetAll, end = "")
    print()
    print(lijn)
    takenlijst = taak()
    taakinlijst = []
    for i in takenlijst:
        startdatum = datetime.strptime(str(i[0]),"%Y%m%d")
        einddatum = datetime.strptime(str(i[1]),"%Y%m%d")
        lentaak = einddatum - startdatum
        if einddatum < eerstedatum:
        # Scenario 1 : Einddatum ligt voor eerstedatum
            taakinlijst.append("<")
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll)
        elif startdatum < eerstedatum and einddatum == eerstedatum:
        # Scenario 2 : Startdatum ligt voor eerstedatum en Einddatum ligt op eerstedatum
            taakinlijst.append("<")
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll+statcol[i[5]-1]+i[2][:4-len(str(takenlijst.index(i)+1))]+"|"+ResetAll)
        elif startdatum < eerstedatum and einddatum < laatstedatum:
        # Scenario 3 : Startdatum ligt voor eerstedatum en Einddatum ligt voor of op laatstedatum
            taakinlijst.append("<")
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll+statcol[i[5]-1]+i[2][:5-len(str(takenlijst.index(i)+1))]+ResetAll)
            lendezetaak = lentaak.days - (eerstedatum - startdatum).days
            for j in range(lendezetaak-1):
                taakinlijst.append(statcol[i[5]-1]+"....."+ResetAll)
            taakinlijst.append(i[3][:4].replace(" ","_")+statcol[i[5]-1]+"|"+ResetAll)
        elif startdatum < eerstedatum and einddatum >= laatstedatum:
        # Scenario 4 : Startdatum ligt voor eerstedatum en Einddatum ligt na laatstedatum
            taakinlijst.append("<")
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll+statcol[i[5]-1]+i[2][:5-len(str(takenlijst.index(i)+1))]+ResetAll)
            lendezetaak = lentaak.days - (eerstedatum - startdatum).days - (einddatum - laatstedatum).days
            for j in range(lendezetaak-2):
                taakinlijst.append(statcol[i[5]-1]+"....."+ResetAll)
            taakinlijst.append(i[3][:4].replace(" ","_"))
            taakinlijst.append(statcol[i[5]-1]+">"+ResetAll)
        elif eerstedatum <= startdatum == einddatum <= (laatstedatum - timedelta(days = 1)):
        # Scenario 5 : Startdatum ligt op of na eerstedatum en Einddatum == Startdatum ligt voor of op laatstedatum
            taakinlijst.append(" ")
            for j in range((startdatum - eerstedatum).days):
                taakinlijst.append(statcol[i[5]-1]+"     "+ResetAll)
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll+statcol[i[5]-1]+i[2][:4-len(str(takenlijst.index(i)+1))]+"|"+ResetAll)
        elif eerstedatum <= startdatum and einddatum < laatstedatum:
        # Scenario 6 : Startdatum ligt op of na eerstedatum en Einddatum ligt voor of op laatstedatum
            taakinlijst.append(" ")
            for j in range((startdatum - eerstedatum).days):
                taakinlijst.append(statcol[i[5]-1]+"     "+ResetAll)
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll+statcol[i[5]-1]+i[2][:5-len(str(takenlijst.index(i)+1))]+ResetAll)
            lendezetaak = lentaak.days
            for j in range(lendezetaak-1):
                taakinlijst.append(statcol[i[5]-1]+"....."+ResetAll)
            taakinlijst.append(i[3][:4].replace(" ","_")+statcol[i[5]-1]+"|"+ResetAll)
        elif eerstedatum <= startdatum < laatstedatum - timedelta(days = 1) and einddatum >= laatstedatum:
        # Scenario 7 : Startdatum ligt op of na eerstedatum en Einddatum ligt na laatstedatum
            taakinlijst.append(" ")
            for j in range((startdatum - eerstedatum).days):
                taakinlijst.append(statcol[i[5]-1]+"     "+ResetAll)
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll+statcol[i[5]-1]+i[2][:5-len(str(takenlijst.index(i)+1))]+ResetAll)
            lendezetaak = lentaak.days - (einddatum - laatstedatum).days
            for j in range(lendezetaak-2):
                taakinlijst.append(statcol[i[5]-1]+"....."+ResetAll)
            taakinlijst.append(i[3][:4].replace(" ","_"))
            taakinlijst.append(statcol[i[5]-1]+">"+ResetAll)
        elif startdatum == laatstedatum - timedelta(days = 1) <= einddatum:
        # Scenario 8 : Startdatum ligt op laatstedatum en Einddatum ligt na laatstedatum
            taakinlijst.append(" ")
            for j in range((startdatum - eerstedatum).days):
                taakinlijst.append(statcol[i[5]-1]+"     "+ResetAll)
            taakinlijst.append(Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll+statcol[i[5]-1]+i[2][:5-len(str(takenlijst.index(i)+1))-1]+ResetAll)
            taakinlijst.append(statcol[i[5]-1]+">"+ResetAll)
        elif startdatum >= laatstedatum:
        # Scenario 9 : Startdatum ligt na laatstedatum
            taakinlijst.append(" ")
            for j in range((laatstedatum - eerstedatum).days-1):
                taakinlijst.append(statcol[i[5]-1]+"     "+ResetAll)
            taakinlijst.append(" "*(4-len(str(takenlijst.index(i)+1)))+Omkeren+statcol[i[5]-1]+str(takenlijst.index(i)+1)+ResetAll)
            taakinlijst.append(statcol[i[5]-1]+">"+ResetAll)
        for j in taakinlijst:
            print(j, end = "")
        print()
        taakinlijst = []
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
        print(forr3(i)+" : "+statcol[collijst[tel-1]]+forl15(j[:12])+ResetAll,end = "")
        if breed == breedte or tel == len(takendict):
            print()
            breed = 0

def filterstatustaak(uitklapofstatus):
    takenlijst = taak()
    if uitklapofstatus.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(uitklapofstatus) == 2 and uitklapofstatus[0].upper() in afsluitlijst and uitklapofstatus[1].upper() in skiplijst:
        eindroutine()
    uitklapofstatuslijst = uitklapofstatus.replace(" ","").split(",")
    try:
        print()
        for i in takenlijst:
            if statuslijst.index(uitklapofstatus) == i[5]-1:
                lijn = "+"+"-"*20+"+"+"-"*20
                print(colbekijken+lijn+ResetAll)
                tv = 0
                print(" "+statcol[i[5]-1]+forr20("ID:")+ResetAll+" "+Omkeren+statcol[i[5]-1]+forc20(takenlijst.index(i)+1)+ResetAll)
                for j in i:
                    col = ResetAll
                    ij = j
                    if j == i[2]:
                        col = statcol[i[5]-1]
                    if j == i[5]:
                        col = Omkeren+statcol[i[5]-1]
                        ij = statuslijst[j-1]
                    print(" "+forl20(taakverdeling[tv]),col+str(ij)+ResetAll)
                    tv +=1
                print(colbekijken+lijn+ResetAll)
        print()
    except:
        pass

def filteromschrijvingtaak(uitklapofstatus):
    takenlijst = taak()
    if uitklapofstatus.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(uitklapofstatus) == 2 and uitklapofstatus[0].upper() in afsluitlijst and uitklapofstatus[1].upper() in skiplijst:
        eindroutine()
    uitklapofstatuslijst = uitklapofstatus.replace(" ","").split(",")
    lijn = "+"+"-"*20+"+"+"-"*20
    for i in takenlijst:
        if uitklapofstatus.lower() in i[2].lower():
            print(colbekijken+lijn+ResetAll)
            tv = 0
            print(" "+statcol[i[5]-1]+forr20("ID:")+ResetAll+" "+Omkeren+statcol[i[5]-1]+forc20(takenlijst.index(i)+1)+ResetAll)
            for j in i:
                col = ResetAll
                ij = j
                if j == i[2]:
                    col = statcol[i[5]-1]
                if j == i[5]:
                    col = Omkeren+statcol[i[5]-1]
                    ij = statuslijst[j-1]
                print(" "+forl20(taakverdeling[tv]),col+str(ij)+ResetAll)
                tv +=1
    print(colbekijken+lijn+ResetAll)
    print()

def kalender():
    takenlijst = taak()
    kaltaken = []
    kaltaak = []
    for i in takenlijst:
        tindex = takenlijst.index(i)+1
        kaltaak.append(tindex)
        tstart = datetime.strptime(str(i[0]),"%Y%m%d")
        kaltaak.append(str(i[0]))
        teinde = datetime.strptime(str(i[1]),"%Y%m%d")
        kaltaak.append(str(i[1]))
        tlengt = (teinde - tstart + timedelta(days = 1)).days
        kaltaak.append(tlengt)
        tstcol = Omkeren+statcol[i[5]-1]
        kaltaak.append(tstcol)
        kaltaken.append(kaltaak)
        kaltaak = []
    if lang == "EN":
        dagenlijst = dagenlijstEN
    else:
        dagenlijst = dagenlijstNL
    nuyyyymm0 = datetime.strftime(date.today(),"%Y%m")
    dzmnd0 = datetime.strftime(datetime.strptime(nuyyyymm0,"%Y%m")+timedelta(days = 15+30*0),"%B")
    nuyyyymm1 = datetime.strftime(datetime.strptime(nuyyyymm0,"%Y%m")+timedelta(days = 15+30*1),"%Y%m")
    dzmnd1 = datetime.strftime(datetime.strptime(nuyyyymm0,"%Y%m")+timedelta(days = 15+30*1),"%B")
    nuyyyymm2 = datetime.strftime(datetime.strptime(nuyyyymm0,"%Y%m")+timedelta(days = 15+30*2),"%Y%m")
    dzmnd2 = datetime.strftime(datetime.strptime(nuyyyymm0,"%Y%m")+timedelta(days = 15+30*2),"%B")
    dezemaand0 = nuyyyymm0[:4]+" "+dzmnd0
    dezemaand1 = nuyyyymm1[:4]+" "+dzmnd1
    dezemaand2 = nuyyyymm2[:4]+" "+dzmnd2
    if lang == "EN":
        for i in maandlijstNL:
            if i == dzmnd0:
                dezemaand0 = dzmnd0.replace(dzmnd0,maandlijstEN[maandlijstNL.index(i)])+" "+nuyyyymm0[:4]
            if i == dzmnd1:
                dezemaand1 = dzmnd1.replace(dzmnd1,maandlijstEN[maandlijstNL.index(i)])+" "+nuyyyymm1[:4]
            if i == dzmnd2:
                dezemaand2 = dzmnd2.replace(dzmnd2,maandlijstEN[maandlijstNL.index(i)])+" "+nuyyyymm2[:4]
    else:
        for i in maandlijstEN:
            if i == dzmnd0:
                dezemaand0 = dzmnd0.replace(dzmnd0,maandlijstNL[maandlijstEN.index(i)])+" "+nuyyyymm0[:4]
            if i == dzmnd1:
                dezemaand1 = dzmnd1.replace(dzmnd1,maandlijstNL[maandlijstEN.index(i)])+" "+nuyyyymm1[:4]
            if i == dzmnd2:
                dezemaand2 = dzmnd2.replace(dzmnd2,maandlijstNL[maandlijstEN.index(i)])+" "+nuyyyymm2[:4]
    weeklijn0 = []
    weeklijn1 = []
    weeklijn2 = []
    weeklijn3 = []
    weeklijn4 = []
    weeklijn5 = []
    for i in range(7*3):
        weeklijn0.append(" .")
        weeklijn1.append(" .")
        weeklijn2.append(" .")
        weeklijn3.append(" .")
        weeklijn4.append(" .")
        weeklijn5.append(" .")
    tel0 = calendar.monthrange(int(nuyyyymm0[:4]),int(nuyyyymm0[4:]))[0]
    tal0 = calendar.monthrange(int(nuyyyymm0[:4]),int(nuyyyymm0[4:]))[1]
    tel1 = calendar.monthrange(int(nuyyyymm1[:4]),int(nuyyyymm1[4:]))[0]
    tal1 = calendar.monthrange(int(nuyyyymm1[:4]),int(nuyyyymm1[4:]))[1]
    tel2 = calendar.monthrange(int(nuyyyymm2[:4]),int(nuyyyymm2[4:]))[0]
    tal2 = calendar.monthrange(int(nuyyyymm2[:4]),int(nuyyyymm2[4:]))[1]
    weeklijn = weeklijn0
    dag0 = 1
    dag1 = 1
    dag2 = 1
    while weeklijn == weeklijn0 and dag0 <= tal0:
        weeklijn[7*0+tel0] = for0r2(dag0)
        for i in kaltaken:
            if i[1] == nuyyyymm0+for0r2(dag0):
                weeklijn[7*0+tel0] = i[4]+forr2(i[0])+ResetAll
        dag0 += 1
        tel0 += 1
        if tel0 == 7:
            break
    while weeklijn == weeklijn0 and dag1 <= tal1:
        weeklijn[7*1+tel1] = for0r2(dag1)
        for i in kaltaken:
            if i[1] == nuyyyymm1+for0r2(dag1):
                weeklijn[7*1+tel1] = i[4]+forr2(i[0])+ResetAll
        dag1 += 1
        tel1 += 1
        if tel1 == 7:
            break
    while weeklijn == weeklijn0 and dag2 <= tal2:
        weeklijn[7*2+tel2] = for0r2(dag2)
        for i in kaltaken:
            if i[1] == nuyyyymm2+for0r2(dag2):
                weeklijn[7*2+tel2] = i[4]+forr2(i[0])+ResetAll
        dag2 += 1
        tel2 += 1
        if tel2 == 7:
            weeklijn = weeklijn1
            tel0 = 0
            tel1 = 0
            tel2 = 0
    while weeklijn == weeklijn1 and dag0 <= tal0:
        weeklijn[7*0+tel0] = for0r2(dag0)
        for i in kaltaken:
            if i[1] == nuyyyymm0+for0r2(dag0):
                weeklijn[7*0+tel0] = i[4]+forr2(i[0])+ResetAll
        dag0 += 1
        tel0 += 1
        if tel0 == 7 or dag0 > tal0:
            break
    while weeklijn == weeklijn1 and dag1 <= tal1:
        weeklijn[7*1+tel1] = for0r2(dag1)
        for i in kaltaken:
            if i[1] == nuyyyymm1+for0r2(dag1):
                weeklijn[7*1+tel1] = i[4]+forr2(i[0])+ResetAll
        dag1 += 1
        tel1 += 1
        if tel1 == 7 or dag1 > tal1:
            break
    while weeklijn == weeklijn1 and dag2 <= tal2:
        weeklijn[7*2+tel2] = for0r2(dag2)
        for i in kaltaken:
            if i[1] == nuyyyymm2+for0r2(dag2):
                weeklijn[7*2+tel2] = i[4]+forr2(i[0])+ResetAll
        dag2 += 1
        tel2 += 1
        if tel2 == 7 or dag2 > tal2:
            weeklijn = weeklijn2
            tel0 = 0
            tel1 = 0
            tel2 = 0
    while weeklijn == weeklijn2 and dag0 <= tal0:
        weeklijn[7*0+tel0] = for0r2(dag0)
        for i in kaltaken:
            if i[1] == nuyyyymm0+for0r2(dag0):
                weeklijn[7*0+tel0] = i[4]+forr2(i[0])+ResetAll
        dag0 += 1
        tel0 += 1
        if tel0 == 7 or dag0 > tal0:
            break
    while weeklijn == weeklijn2 and dag1 <= tal1:
        weeklijn[7*1+tel1] = for0r2(dag1)
        for i in kaltaken:
            if i[1] == nuyyyymm1+for0r2(dag1):
                weeklijn[7*1+tel1] = i[4]+forr2(i[0])+ResetAll
        dag1 += 1
        tel1 += 1
        if tel1 == 7 or dag1 > tal1:
            break
    while weeklijn == weeklijn2 and dag2 <= tal2:
        weeklijn[7*2+tel2] = for0r2(dag2)
        for i in kaltaken:
            if i[1] == nuyyyymm2+for0r2(dag2):
                weeklijn[7*2+tel2] = i[4]+forr2(i[0])+ResetAll
        dag2 += 1
        tel2 += 1
        if tel2 == 7 or dag2 > tal2:
            weeklijn = weeklijn3
            tel0 = 0
            tel1 = 0
            tel2 = 0
    while weeklijn == weeklijn3 and dag0 <= tal0:
        weeklijn[7*0+tel0] = for0r2(dag0)
        for i in kaltaken:
            if i[1] == nuyyyymm0+for0r2(dag0):
                weeklijn[7*0+tel0] = i[4]+forr2(i[0])+ResetAll
        dag0 += 1
        tel0 += 1
        if tel0 == 7 or dag0 > tal0:
            break
    while weeklijn == weeklijn3 and dag1 <= tal1:
        weeklijn[7*1+tel1] = for0r2(dag1)
        for i in kaltaken:
            if i[1] == nuyyyymm1+for0r2(dag1):
                weeklijn[7*1+tel1] = i[4]+forr2(i[0])+ResetAll
        dag1 += 1
        tel1 += 1
        if tel1 == 7 or dag1 > tal1:
            break
    while weeklijn == weeklijn3 and dag2 <= tal2:
        weeklijn[7*2+tel2] = for0r2(dag2)
        for i in kaltaken:
            if i[1] == nuyyyymm2+for0r2(dag2):
                weeklijn[7*2+tel2] = i[4]+forr2(i[0])+ResetAll
        dag2 += 1
        tel2 += 1
        if tel2 == 7 or dag2 > tal2:
            weeklijn = weeklijn4
            tel0 = 0
            tel1 = 0
            tel2 = 0
    while weeklijn == weeklijn4 and dag0 <= tal0:
        weeklijn[7*0+tel0] = for0r2(dag0)
        for i in kaltaken:
            if i[1] == nuyyyymm0+for0r2(dag0):
                weeklijn[7*0+tel0] = i[4]+forr2(i[0])+ResetAll
        dag0 += 1
        tel0 += 1
        if tel0 == 7 or dag0 > tal0:
            break
    while weeklijn == weeklijn4 and dag1 <= tal1:
        weeklijn[7*1+tel1] = for0r2(dag1)
        for i in kaltaken:
            if i[1] == nuyyyymm1+for0r2(dag1):
                weeklijn[7*1+tel1] = i[4]+forr2(i[0])+ResetAll
        dag1 += 1
        tel1 += 1
        if tel1 == 7 or dag1 > tal1:
            break
    while weeklijn == weeklijn4 and dag2 <= tal2:
        weeklijn[7*2+tel2] = for0r2(dag2)
        for i in kaltaken:
            if i[1] == nuyyyymm2+for0r2(dag2):
                weeklijn[7*2+tel2] = i[4]+forr2(i[0])+ResetAll
        dag2 += 1
        tel2 += 1
        if tel2 == 7 or dag2 > tal2:
            weeklijn = weeklijn5
            tel0 = 0
            tel1 = 0
            tel2 = 0
    while weeklijn == weeklijn5 and dag0 <= tal0:
        weeklijn[7*0+tel0] = for0r2(dag0)
        for i in kaltaken:
            if i[1] == nuyyyymm0+for0r2(dag0):
                weeklijn[7*0+tel0] = i[4]+forr2(i[0])+ResetAll
        dag0 += 1
        tel0 += 1
        if tel0 == 7 or dag0 > tal0:
            break
    while weeklijn == weeklijn5 and dag1 <= tal1:
        weeklijn[7*1+tel1] = for0r2(dag1)
        for i in kaltaken:
            if i[1] == nuyyyymm1+for0r2(dag1):
                weeklijn[7*1+tel1] = i[4]+forr2(i[0])+ResetAll
        dag1 += 1
        tel1 += 1
        if tel1 == 7 or dag1 > tal1:
            break
    while weeklijn == weeklijn5 and dag2 <= tal2:
        weeklijn[7*2+tel2] = for0r2(dag2)
        for i in kaltaken:
            if i[1] == nuyyyymm2+for0r2(dag2):
                weeklijn[7*2+tel2] = i[4]+forr2(i[0])+ResetAll
        dag2 += 1
        tel2 += 1
        if tel2 == 7 or dag2 > tal2:
            weeklijn = weeklijn5
            tel0 = 0
            tel1 = 0
            tel2 = 0
    print(coldatum+Omkeren+forc20(dezemaand0)+ResetAll+" | "+Omkeren+forc20(dezemaand1)+ResetAll+" | "+Omkeren+forc20(dezemaand2)+ResetAll)
    col = ResetAll
    for i in dagenlijst:
        if i == dagenlijst[5] or i == dagenlijst[6]:
            col = LichtGrijs
        print(col+i[:2]+ResetAll,end = " " )
    col = ResetAll
    print("| ",end = "")
    for i in dagenlijst:
        if i == dagenlijst[5] or i == dagenlijst[6]:
            col = LichtGrijs
        print(col+i[:2]+ResetAll,end = " " )
    col = ResetAll
    print("| ",end = "")
    for i in dagenlijst:
        if i == dagenlijst[5] or i == dagenlijst[6]:
            col = LichtGrijs
        print(col+i[:2]+ResetAll,end = " " )
    print()
    for i in range(len(weeklijn0)):
        col = LichtGrijs
        if (i-5) % 7 == 0 or (i-6) % 7 == 0:
            col = DonkerGrijs
        if i % 7 == 0 and i != 0:
            col = LichtGrijs
            print("| ", end = "")
        if for0r2(weeklijn0[i]) == datetime.strftime(date.today(),"%d") and i < 7:
            col = coldatum
        print(col+weeklijn0[i]+ResetAll,end = " ")
    print()
    for i in range(len(weeklijn1)):
        col = LichtGrijs
        if (i-5) % 7 == 0 or (i-6) % 7 == 0:
            col = DonkerGrijs
        if i % 7 == 0 and i != 0:
            col = LichtGrijs
            print("| ", end = "")
        if for0r2(weeklijn1[i]) == datetime.strftime(date.today(),"%d") and i < 7:
            col = coldatum
        print(col+weeklijn1[i]+ResetAll,end = " ")
    print()
    for i in range(len(weeklijn2)):
        col = LichtGrijs
        if (i-5) % 7 == 0 or (i-6) % 7 == 0:
            col = DonkerGrijs
        if i % 7 == 0 and i != 0:
            col = LichtGrijs
            print("| ", end = "")
        if for0r2(weeklijn2[i]) == datetime.strftime(date.today(),"%d") and i < 7:
            col = coldatum
        print(col+weeklijn2[i]+ResetAll,end = " ")
    print()
    for i in range(len(weeklijn3)):
        col = LichtGrijs
        if (i-5) % 7 == 0 or (i-6) % 7 == 0:
            col = DonkerGrijs
        if i % 7 == 0 and i != 0:
            col = LichtGrijs
            print("| ", end = "")
        if for0r2(weeklijn3[i]) == datetime.strftime(date.today(),"%d") and i < 7:
            col = coldatum
        print(col+weeklijn3[i]+ResetAll,end = " ")
    print()
    for i in range(len(weeklijn4)):
        col = LichtGrijs
        if (i-5) % 7 == 0 or (i-6) % 7 == 0:
            col = DonkerGrijs
        if i % 7 == 0 and i != 0:
            col = LichtGrijs
            print("| ", end = "")
        if for0r2(weeklijn4[i]) == datetime.strftime(date.today(),"%d") and i < 7:
            col = coldatum
        print(col+weeklijn4[i]+ResetAll,end = " ")
    print()

    alldots = True
    for i in weeklijn5:
        if i != " .":
            alldots = False
    if alldots == False:
        col = LichtGrijs
        for i in range(len(weeklijn5)):
            if (i-5) % 7 == 0 or (i-6) % 7 == 0:
                col = DonkerGrijs
            if i % 7 == 0 and i != 0:
                col = LichtGrijs
                print("| ", end = "")
            if for0r2(weeklijn5[i]) == datetime.strftime(date.today(),"%d") and i < 7:
                col = coldatum
            print(col+weeklijn5[i]+ResetAll,end = " ")
    print()
    print()

def takenshow():
    if lang == "EN":
        sob = "View:\n >1 : Narrow (60 chars)\n  2 : Wide (100 chars)\n  3 : Timeline ( 7+1 days: Narrow)\n  4 : Timeline (14+1 days: Normal)\n  5 : Timeline (31+1 days: Wide)\n  6 : Timeline (Give days)\n  7 : Compact block\n  0 : Calendar\n%s" % inputindent
        geentaken = "There are no tasks."
        hoelang = "Give the number of days of the length of your timeline (default 3):\n%s" % inputindent
        vanaf = "Give the number of days in the past (default 1):\n%s" % inputindent
        ukos = textwrap.wrap("To expand Tasks, give the Task ID's in CSV style, the exact Status, a search string in the Task description, or \"*\" for all:", width = wi)
    else:
        sob = "Toon:\n >1 : Smal (60 tekens)\n  2 : Breed (100 tekens)\n  3 : Tijdlijn ( 7+1 dagen: Smal)\n  4 : Tijdlijn (14+1 dagen: Normaal)\n  5 : Tijdlijn (31+1 dagen: Breed)\n  6 : Tijdlijn (Geef dagen)\n  7 : Compact blok\n  0 : Kalender\n%s" % inputindent
        geentaken = "Er zijn geen taken."
        hoelang = "Geef het aantal dagen op van de lengte van de tijdlijn (standaard 3):\n%s" % inputindent
        vanaf = "Geef het aantal dagen in het verleden op (standaard 1):\n%s" % inputindent
        ukos = textwrap.wrap("Om Taken uit te klappen, geef de Taak-ID's op in CSV-stijl, de precieze Status, een zoektekst in de Taakomschrijving, of \"*\" voor alle:", width = wi)
    takenlijst = taak()
    if len(takenlijst) == 0:
        print(geentaken)
        return
    now = input(sob)
    if now.upper() in afsluitlijst:
        return
    elif len(now) == 2 and now[0].upper() in afsluitlijst and now[1].upper() in skiplijst:
        eindroutine()
    if now == "2":
        takenbreed()
    elif now == "3":
        scopenunu["scope"] = 7+1
        scopenunu["nunu"] = 1
        takenlijn(scopenunu)
    elif now == "4":
        scopenunu["scope"] =14+1
        scopenunu["nunu"] = 3
        takenlijn(scopenunu)
    elif now == "5":
        scopenunu["scope"] = 31+1
        scopenunu["nunu"] = 7
        takenlijn(scopenunu)
    elif now == "6":
        try:
            scopein = input(hoelang).strip()
            if scopein.upper() in afsluitlijst:
                return
            elif len(scopein) == 2 and scopein.upper() in afsluitlijst and scopein.upper() in skiplijst:
                eindroutine()
            if scopein == "":
                scopein = "3"
            scope = int(scopein)
            if scope < 3:
                scope = 3
            scopenunu["scope"] = scope
            nunuin = input(vanaf).strip()
            if nunuin.upper() in afsluitlijst:
                return
            elif len(nunuin) == 2 and nunuin.upper() in afsluitlijst and nunuin.upper() in skiplijst:
                eindroutine()
            if nunuin == "":
                nunuin = "1"
            nunu = int(nunuin)
            if nunu < 1:
                nunu = 1
            scopenunu["nunu"] = nunu
        except:
            scopenunu["scope"] = 3
            scopenunu["nunu"] = 1
        takenlijn(scopenunu)
    elif now == "7":
        takenblok()
    elif now == "0":
        kalender()
    else: # now == "1":
        takensmal()
    for i in ukos:
        print(i)
    uitklapofstatus = input(inputindent).capitalize()
    if uitklapofstatus.upper() in afsluitlijst:
        return
    elif len(uitklapofstatus) == 2 and uitklapofstatus[0].upper() in afsluitlijst and uitklapofstatus[1].upper() in skiplijst:
        eindroutine()
    if uitklapofstatus == "":
        return
    elif uitklapofstatus == "*":
        uitklapofstatus =  ""
    if uitklapofstatus in statuslijst:
    # als zoekterm precies een statusnaam is:
        filterstatustaak(uitklapofstatus)
    else:
    # als zoekterm een CSV van ID's is:
        try:
            isidcsv = uitklapofstatus.replace(" ","").split(",")
            for i in isidcsv:
                i = int(i)
            uitklaptaak(uitklapofstatus)
        except:
    # als zoekterm in omschrijving voorkomt:
            inoms = False
            for i in takenlijst:
                if uitklapofstatus.lower() in i[2].lower():
                    inoms = True
            if inoms == True:
                filteromschrijvingtaak(uitklapofstatus)

def wijzigtaak():
    if lang == "EN":
        startdatum = "Give the Start date (YYYYMMDD), or \"+N\" to start N days later:\n%s" % inputindent
        einddatum = "Give the Due date (YYYYMMDD), or \"+N\" for N days more:\n%s" % inputindent
        omschrijving = "Give the TaskDescription:\n%s" % inputindent
        moetlanger = "Give at least 4 characters."
        wie = "Give the ID of the Agent or SubTeam:\n%s" % inputindent
        aantekening = "Give extra Info (opt):\n%s" % inputindent
        staten = "Give the ID of one of these Statuses:"
        welk = "Give the ID of the Task you want to change:\n%s" % inputindent
        wat = "Give the ID of what you want to change:"
    else:
        startdatum = "Geef de Startdatum op (YYYYMMDD), of \"+N\" om N dagen later te starten:\n%s" % inputindent
        einddatum = "Geef de Einddatum op (YYYYMMDD), of \"+N\" voor N dagen méér:\n%s" % inputindent
        omschrijving = "Geef de Taakbeschrijving op:\n%s" % inputindent
        moetlanger = "Geef tenminste 4 karakters op."
        wie = "Geef de ID van de Medewerker of het SubTeam:\n%s" % inputindent
        aantekening = "Geef extra Informatie (opt):\n%s" % inputindent
        staten = "Geef de ID van één van deze Statusen:"
        welk = "Geef de ID op van de Taak die u wilt wijzigen:\n%s" % inputindent
        wat = "Geef de ID op van wat u wilt wijzigen:"
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
                            if eind >= start:
                                if lang == "EN":
                                    print("The Due date is %s." % eind)
                                else:
                                    print("De Einddatum is %s." % eind)
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
                    teamlijst = nepecht()[0]
                    nep = nepecht()[1]
                    echt = nepecht()[2]
                    teamshowbasis()
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
        kies = "Choose an Agent or SubTeam to %sCHANGE%s:" % (colwijzigen, ResetAll)
        wie = "Give the ID of the Agent or SubTeam:\n%s" % inputindent
        if key == "emailadres":
            keyhere = "EMail address"
        else:
            keyhere = "Agent Number"
        wat = "What do you want to change?:\n  1 : %s\n  2 : Given Name\n  3 : Last Name\n  4 : Check\n  5 : Note\n%s" % (keyhere,inputindent)
        nietuniek = "This %s already exists." % keyhere
        tog = "Check these Agents OUT or IN:\n  0 : OUT\n  1 : IN\n >2 : Invert\n%s" % inputindent
    else:
        kies = "Kies een Medewerker of SubTeam om te %sWIJZIGEN%s:" % (colwijzigen, ResetAll)
        wie = "Geef de ID van de Medewerker of het SubTeam:\n%s" % inputindent
        if key == "emailadres":
            keyhere = "EMailadres"
        else:
            keyhere = "PersoneelsNummer"
        wat = "Wat wilt u Wijzigen?:\n  1 : %s\n  2 : VoorNaam\n  3 : AchterNaam\n  4 : Check\n  5 : Aantekening\n%s" % (keyhere,inputindent)
        nietuniek = "Dit %s bestaat al." % keyhere
        tog = "Check deze Medewerkers UIT of IN:\n  0 : UIT\n  1 : IN\n >2 : Omkeren\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    print(kies)
    teamshowbasis()
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
            if 0 <= LL <= len(teamlijst):
                die = teamlijst[LL]
                welk = input(wat)
                if welk.upper() in afsluitlijst:
                    return
                elif len(welk) == 2 and welk[0].upper() in afsluitlijst and welk[1].upper() in skiplijst:
                    eindroutine()
                if welk == "1":
                    if key == "emailadres":
                        emailadres = False
                        while emailadres == False:
                            EM = input()
                            if EM.upper() in afsluitlijst:
                                return
                            elif len(EM) == 2 and EM[0].upper() in afsluitlijst and EM[1].upper() in skiplijst:
                                eindroutine()
                            elif len(EM) < 1:
                                pass
                            else:
                                u = True
                                for i in teamlijst:
                                    if EM == i[0]:
                                        u = False
                                if u == False:
                                    print(colslecht+nietuniek+ResetAll)
                                else:
                                    print(die)
                                    print(EM)
                                    if die[0][0] == "~" and EM[0] != "~":
                                        teamlijst[LL][0] = "~"+EM
                                    else:
                                        teamlijst[LL][0] = EM
                                    emailadres = True
                    else:
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
                                u = True
                                for i in teamlijst:
                                    if PN == i[0]:
                                        u = False
                                if u == False:
                                    print(colslecht+nietuniek+ResetAll)
                                else:
                                    print(die)
                                    print(PN)
                                    if die[0][0] == "~" and PN[0] != "~":
                                        teamlijst[LL][0] = "~"+PN
                                    else:
                                        teamlijst[LL][0] = PN
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
                            teamlijst[LL][1] = VN
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
                            teamlijst[LL][2] = AN
                            achternaam = True
                    teamlijst[LL][2] = AN
                elif welk == "4":
                    toggleall = input(tog)
                    if toggleall == "0":
                        teamlijst[LL][3] = 0
                    elif toggleall == "1":
                        teamlijst[LL][3] = 1
                    else:
                        if teamlijst[LL][3] == 0:
                            teamlijst[LL][3] = 1
                        else:
                            teamlijst[LL][3] = 0
                elif welk == "5":
                    AT = input()
                    if AT.upper() in afsluitlijst:
                        return
                    elif len(AT) == 2 and AT[0].upper() in afsluitlijst and AT[1].upper() in skiplijst:
                        eindroutine()
                    teamlijst[LL][4] = AT
                with open("teamlijst","w") as t:
                    print(teamlijst, end = "", file = t)
                teamlijst = nepecht()[0]
                nep = nepecht()[1]
                echt = nepecht()[2]
        except:
            pass
        pisang = True
    print()

def wijzigteam():
    if lang == "EN":
        sel = "Select the IDs of the Agents or SubTeams you want to %sCHANGE%s,\nin CSV style (separated by commas), or * for all:\n%s" % (colwijzigen,ResetAll,inputindent)
        tog = "Check these Agents or SubTeams OUT or IN:\n  0 : OUT\n  1 : IN\n >2 : Invert\n%s" % inputindent
        wat = "What do you want to change?\n >1 : Check this group OUT or IN\n  2 : Change Note for everyone in this group\n%s" % inputindent
        nieuweaantekening = "Type or clear the Note:\n%s" % inputindent
    else:
        sel = "Selecteer ID's van de Medewerkers of SubTeams die u wilt %sWIJZIGEN%s,\nin CSV-stijl (gescheiden door een komma), of * voor alle:\n%s" % (colwijzigen,ResetAll,inputindent)
        tog = "Check deze Medewerkers of SubTeams UIT of IN:\n  0 : UIT\n  1 : IN\n >2 : Omkeren\n%s" % inputindent
        wat = "Wat wilt u wijzigen?\n >1 : Check deze groep UIT of IN\n  2 : Wijzig Aantekening voor iedereen in deze groep\n%s" % inputindent
        nieuweaantekening = "Typ of wis de Aantekening:\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    teamshowbasis()
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
                medewerkerlijst.append(teamlijst[i])
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
        else:
            for i in medewerkerlijst:
                if i[3] == 0:
                    i[3] = 1
                else:
                    i[3] = 0
    with open("teamlijst","w") as t:
        print(teamlijst, end = "", file = t)
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    print()

def vergadering():
    if lang == "EN":
        ingecheckt = "These Agents are checked %sIN%s and can participate:" % (iocol[1],ResetAll)
        naamkop = colmeeting+forc10("Name:")+ResetAll
        meetingstart = "Comments are collected and shown but not stored.\n%sThe meeting has started.%s End with \"Q\"." % (colmeeting,ResetAll)
        extradeelnemer = "Add extra participants by typing their names, or\ntype the IDs of any indisposed Agent(s) (csv style).\nLeave empty to continue:\n%s" % inputindent
        geendeelnemers = "Check in participating Agents, or add participants manually."
        perdeelnemer = "Noted comments grouped per participant:"
        eindevergadering = "Here ends the Meeting."
    else:
        ingecheckt = "Deze Medewerkers zijn %sIN%sgecheckt en kunnen deelnemen:" % (iocol[1],ResetAll)
        naamkop = colmeeting+forc10("Naam:")+ResetAll
        meetingstart = "Opmerkingen worden verzameld en getoond maar niet opgeslagen.\n%sDe vergadering is gestart.%s Beëindig met \"Q\"." % (colmeeting,ResetAll)
        extradeelnemer = "Voeg extra deelnemers toe door hun namen te typen, of\ngeef de ID's van verhinderde Medewerkers (csv-stijl).\nLaat leeg om door te gaan:\n%s" % inputindent
        geendeelnemers = "Check deelnemende Medewerkers in, of voeg handmatig deelnemers toe."
        perdeelnemer = "Genoteerde opmerkingen gegroepeerd per Deelnemer:"
        eindevergadering = "Hier stopt de vergadering."
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    teamshowbasisecht()
    meelijst = []
    numin = 0
    for i in teamlijst:
        numin += i[3]
        if i[3] == 1:
            meelijst.append(i[1])
    if len(meelijst) > 0:
        print(ingecheckt)
        indie = 1
        for i in meelijst:
            print(forr3(indie)+" : "+iocol[1]+i+ResetAll)
            indie += 1
    print()
    gast = False
    while gast == False:
        extra = input(extradeelnemer).replace(" ","")
        try:
            extraint = int(extra.replace(",",""))
            extralijst = extra.split(",")
            extralijst = sorted(extralijst, reverse = True)
            for i in extralijst:
                del meelijst[int(i)-1]
            del extra
            indie = 1
            for i in meelijst:
                print(forr3(indie)+" : "+iocol[1]+i+ResetAll)
                indie += 1
        except:
            if extra.upper() in afsluitlijst:
                gezellig = False
                return
            elif len(extra) == 2 and extra[0].upper() in afsluitlijst and extra[1].upper() in skiplijst:
                eindroutine()
            elif extra == "":
                gast = True
            else:
                extralijst = extra.split(",")
                for i in extralijst:
                    meelijst.append(i)
                indie = 1
                for i in meelijst:
                    print(forr3(indie)+" : "+iocol[1]+i+ResetAll)
                    indie += 1
    meetingdictrandom = {}
    while len(meelijst) > 0:
        r = random.choice(meelijst)
        meetingdictrandom[r]= []
        meelijst.remove(r)
    if len(meetingdictrandom) == 0:
        print(colslecht+geendeelnemers+ResetAll)
        return
    lijn = "   +"+"----------+"*(len(meetingdictrandom)+1)
    print(meetingstart)
    print()
    print(colmeeting+lijn+ResetAll)
    print("    %s " % naamkop, end = "")
    for i in meetingdictrandom:
        if len(i) <= 10:
            j = forl10(i)
        else:
            j = i[:10]
        print(j, end = " ")
    print()
    print(colmeeting+lijn+ResetAll)
    puttel = 1
    gezellig = True
    while gezellig == True:
        for i,j in meetingdictrandom.items():
            print(forr2(puttel),forr10(i[:10]),": ", end = "")
            put = input()
            if put.upper() in afsluitlijst:
                meetingdictrandom[i].append(str(puttel)+": "+eindevergadering)
                print()
                gezellig = False
                break
            elif len(put) == 2 and put[0].upper() in afsluitlijst and put[1].upper() in skiplijst:
                eindroutine()
            meetingdictrandom[i].append(str(puttel)+": "+put)
        print(lijn)
        puttel += 1
    print(perdeelnemer)
    try:
        tel = 0
        for i,j in meetingdictrandom.items():
            print("    "+colmeeting+forl10(i[:10])+":"+ResetAll,end = "")
            print(" "+colmeeting+j[0]+" "+ResetAll)
            for k in j[1:]:
                print("                "+colmeeting+k+" "+ResetAll)
            tel += 1
    except:
        print()
    print(colmeeting+lijn+ResetAll)
    print()

def archiveerteam(medewerkerlijst):
    if lang == "EN":
        archop = "\nArchived on %s:" % nu
        archok = "Agent(s) or SubTeam(s) archived successfully."
    else:
        archop = "\nGearchiveerd op %s:" % nu
        archok = "Medewerker(s) of SubTeam(s)succesvol gearchiveerd."
    with open("team.txt","a+") as t:
        try:
            for i in medewerkerlijst:
                if i[0] != "00000":
                    lijn = "+"+"-"*20+"+"+"-"*20
                    print(archop, file = t)
                    print(lijn, file = t)
                    tv = 0
                    for j in i:
                        ij = j
                        if j == i[3]:
                            ij = checklijst[int(i[3])]
                        print(" "+forl20(teamverdeling[tv]),str(ij), file = t)
                        tv +=1
                    print(lijn, file = t)
            print(archok)
        except:
            pass
    print()

def verwijderteam(medewerkerlijst):
    if lang == "EN":
        verwok = "Agent(s) or SubTeam(s) deleted successfully."
    else:
        verwok = "Medewerker(s) of SubTeam(s) succesvol verwijderd."
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    for i in medewerkerlijst:
        if i[0] != "00000":
            teamlijst.remove(i)
    with open("teamlijst","w") as t:
        print(teamlijst, end = "", file = t)
    print(verwok)
    print()

def archiveertaak(taaklijst):
    if lang == "EN":
        archop = "\nArchived on %s:" % nu
        archok = "Task(s) archived successfully."
        archnok = "%sTask(s) NOT archived successfully.%s Is the status %s?" % (statcol[5],ResetAll,Omkeren+statcol[5]+statuslijst[5]+ResetAll)
    else:
        archop = "\nGearchiveerd op %s:" % nu
        archok = "Ta(a)k(en) succesvol gearchiveerd."
        archnok = "%sTa(a)k(en) NIET succesvol gearchiveerd.%s Is de status %s?" % (statcol[5],ResetAll,Omkeren+statcol[5]+statuslijst[5]+ResetAll)
    with open("team.txt","a+") as t:
        try:
            for i in taaklijst:
                if i[5] == 5+1:
                    print(archnok)
                    return "nok"
                else:
                    lijn = "+"+"-"*20+"+"+"-"*20
                    print(archop, file = t)
                    print(lijn, file = t)
                    tv = 0
                    for j in i:
                        ij = j
                        if j == i[5]:
                            ij = statuslijst[j-1]
                        print(" "+forl20(taakverdeling[tv]),str(ij), file = t)
                        tv +=1
                    print(lijn, file = t)
                    print(archok)
        except:
            pass
    print()

def verwijdertaak(taaklijst):
    if lang == "EN":
        verwok = "Task(s) deleted successfully."
    else:
        verwok = "Ta(a)k(en) succesvol verwijderd."
    takenlijst = taak()
    for i in taaklijst:
        takenlijst.remove(i)
    with open("takenlijst","w") as t:
        print(takenlijst, end = "", file = t)
    print(verwok)
    print()

def archiveerofverwijdertaak():
    if lang == "EN":
        sel = "Give the IDs of the Tasks that you want to %sARCHIVE and/or DELETE%s,\nin CSV style (separated by commas), or * for all:\n%s" % (colverwijderen, ResetAll, inputindent)
        archov = "Select:\n  1 : Only Archive (append to Notepad)\n  2 : Only Delete\n >3 : Archive and Delete\n%s" % inputindent
    else:
        sel = "Geef ID's op van de Taken die u wilt %sARCHIVEREN en/of VERWIJDEREN%s,\nin CSV-stijl (gescheiden door een komma), of * voor alle:\n%s" % (colverwijderen, ResetAll, inputindent)
        archov = "Selecteer:\n  1 : Alleen Archiveren (toevoegen aan Kladblok)\n  2 : Alleen Verwijderen\n >3 : Archiveren en Verwijderen\n%s" % inputindent
    takenlijst = taak()
    takenblok()
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
    aov = input(archov)
    if aov.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(aov) == 2 and aov[0].upper() in afsluitlijst and aov[1].upper() in skiplijst:
        eindroutine()
    if aov == "1":
        archiveertaak(taaklijst)
        uit = True
        return uit
    elif aov == "2":
        verwijdertaak(taaklijst)
        takenlijst = taak()
        uit = True
        return uit
    else:
        arch = archiveertaak(taaklijst)
        if arch == "nok":
            uit = True
            return uit
        verwijdertaak(taaklijst)
        takenlijst = taak()
        uit = True
        return uit

def archiveerofverwijdermedewerker():
    if lang == "EN":
        sel = "Select the IDs of the Agents or SubTeams that you want to %sARCHIVE and/or DELETE%s,\nin CSV style (separated by commas), or * for all:\n%s" % (colverwijderen, ResetAll, inputindent)
        archov = "Select:\n  1 : Only Archive (append to Notepad)\n  2 : Only Delete\n >3 : Archive and Delete\n%s" % inputindent
    else:
        sel = "Selecteer ID's van de Medewerkers of SubTeams die u wilt %sARCHIVEREN en/of VERWIJDEREN%s,\nin CSV-stijl (gescheiden door een komma), of * voor alle:\n%s" % (colverwijderen, ResetAll, inputindent)
        archov = "Selecteer:\n  1 : Alleen Archiveren (toevoegen aan Kladblok)\n  2 : Alleen Verwijderen\n >3 : Archiveren en Verwijderen\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
    teamshowbasis()
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
                medewerkerlijst.append(teamlijst[i])
        except:
            pass
    aov = input(archov)
    if aov.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(aov) == 2 and aov[0].upper() in afsluitlijst and aov[1].upper() in skiplijst:
        eindroutine()
    if aov == "1":
        archiveerteam(medewerkerlijst)
        uit = True
        return uit
    elif aov == "2":
        verwijderteam(medewerkerlijst)
        teamlijst = nepecht()[0]
        nep = nepecht()[1]
        echt = nepecht()[2]
        uit = True
        return uit
    else:
        archiveerteam(medewerkerlijst)
        verwijderteam(medewerkerlijst)
        teamlijst = nepecht()[0]
        nep = nepecht()[1]
        echt = nepecht()[2]
        uit = True
        return uit

def uitklapteam():
    if lang == "EN":
        welk = "Give the ID of the Agent or SubTeam you want to expand:\n%s" % inputindent
    else:
        welk = "Geef de ID op van de Medewerker of het SubTeam om uit te klappen:\n%s" % inputindent
    teamlijst = nepecht()[0]
    nep = nepecht()[1]
    echt = nepecht()[2]
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
            lijn = "+"+"-"*20+"+"+"-"*20
            if 0 <= welke <= len(teamlijst):
                print(lijn)
                die = teamlijst[welke]
                for i in range(len(die)):
                    j = die[i]
                    if i == 3:
                        if die[0][0] == "~":
                            j = ""
                        else:
                            j = iocol[die[3]]+checklijst[die[3]]+ResetAll
                    print(" "+forl20(teamverdeling[i]),j)
                print(lijn)
        except:
            pass
    print()

def uitklaptaak(uitklapofstatus):
    takenlijst = taak()
    if uitklapofstatus.upper() in afsluitlijst:
        uit = True
        return uit
    elif len(uitklapofstatus) == 2 and uitklapofstatus[0].upper() in afsluitlijst and uitklapofstatus[1].upper() in skiplijst:
        eindroutine()
    uitklapofstatuslijst = uitklapofstatus.replace(" ","").split(",")
    try:
        for k in uitklapofstatuslijst:
            uitklapofstatus = int(k)-1
            lijn = "+"+"-"*20+"+"+"-"*20
            for i in takenlijst:
                if uitklapofstatus == takenlijst.index(i):
                    print(colbekijken+lijn+ResetAll)
                    tv = 0
                    print(" "+statcol[i[5]-1]+forr20("ID:")+ResetAll+" "+Omkeren+statcol[i[5]-1]+forc20(takenlijst.index(i)+1)+ResetAll)
                    for j in i:
                        col = ResetAll
                        ij = j
                        if j == i[2]:
                            col = statcol[i[5]-1]
                        if j == i[5]:
                            col = Omkeren+statcol[i[5]-1]
                            ij = statuslijst[j-1]
                        print(" "+forl20(taakverdeling[tv]),col+str(ij)+ResetAll)
                        tv +=1
            print(colbekijken+lijn+ResetAll)
    except:
        pass
    print()

baas = True
while baas == True:
    printdag()
    try:
        with open("team.txt","r") as t:
            pass
    except:
        with open("team.txt","w") as t:
            print(vim, file = t)
    oeilijst = checkstatusdatum()
    if len(oeilijst) > 0:
        wijzigoei(oeilijst)
    kalender()
    hoeveeltaken()
    teamshowkort()
    print()
    if lang == "EN":
        keuzeopties = "Choose from the following options:\n  0 : %sAbout this program%s\n  1 : %sAdd%s\n >2 : %sView%s\n  3 : %sChange%s\n  4 : %sArchive and Delete%s\n  5 : %sMeeting%s\n  6 : %sNotepad (Vim)%s\n%s\n%s" % (colover,ResetAll,coltoevoegen,ResetAll,colbekijken,ResetAll,colwijzigen,ResetAll,colverwijderen,ResetAll,colmeeting,ResetAll,colinformatie,ResetAll,weg,inputindent)
        toetom = "%sADD%s a Task or an Agent or SubTeam:\n >1 : Task\n  2 : Agent or SubTeam\n%s\n%s" % (coltoevoegen,ResetAll,terug,inputindent)
        zietom = "%sVIEW%s Tasks or Agents or SubTeams:\n >1 : Tasks\n  2 : Agents or SubTeams\n%s\n%s" % (colbekijken,ResetAll,terug,inputindent)
        andiot = "%sCHANGE%s a Task or Team data:\n  1 : Task\n  2 : One Agent or SubTeam\n >3 : Group\n%s\n%s" % (colwijzigen,ResetAll,terug,inputindent)
        watweg = "%sARCHIVE and/or DELETE%s a Task or an Agent or SubTeam:\n >1 : Task\n  2 : Agent or SubTeam\n%s\n%s" % (colverwijderen,ResetAll,terug,inputindent)
    else:
        keuzeopties = "Kies uit de volgende opties:\n  0 : %sOver dit programma%s\n  1 : %sToevoegen%s\n >2 : %sBekijken%s\n  3 : %sWijzigen%s\n  4 : %sArchiveren en Verwijderen%s\n  5 : %sVergadering%s\n  6 : %sKladblok (Vim)%s\n%s\n%s" % (colover,ResetAll,coltoevoegen,ResetAll,colbekijken,ResetAll,colwijzigen,ResetAll,colverwijderen,ResetAll,colmeeting,ResetAll,colinformatie,ResetAll,weg,inputindent)
        toetom = "%sVOEG%s een Taak of een Medewerker of SubTeam %sTOE%s:\n >1 : Taak\n  2 : Medewerker of SubTeam\n%s\n%s" % (coltoevoegen,ResetAll,coltoevoegen,ResetAll,terug,inputindent)
        zietom = "%sBEKIJK%s Taken of Medewerkers of SubTeams:\n >1 : Taken\n  2 : Medewerkers of SubTeams\n%s\n%s" % (colbekijken,ResetAll,terug,inputindent)
        andiot = "%sWIJZIG%s een Taak of Team gegevens:\n  1 : Taak\n  2 : Één Medewerker of SubTeam\n >3 : Groep\n%s\n%s" % (colwijzigen,ResetAll,terug,inputindent)
        watweg = "%sARCHIVEER en/of VERWIJDER%s een Taak of een Medewerker of SubTeam:\n >1 : Taak\n  2 : Medewerker of SubTeam\n%s\n%s" % (colverwijderen,ResetAll,terug,inputindent)
    keuze = input(keuzeopties)
    if keuze.upper() in afsluitlijst:
        eindroutine()
    elif len(keuze) == 2 and keuze[0].upper() in afsluitlijst and keuze[1].upper() in skiplijst:
        eindroutine()
    if keuze == "0":
        printstuff()
    elif keuze == "1":
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
                uit = archiveerofverwijdermedewerker()
                if uit == True:
                    veme = False
        else:
            veta = True
            while veta == True:
                uit = archiveerofverwijdertaak()
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
        else:
            takenshow()
