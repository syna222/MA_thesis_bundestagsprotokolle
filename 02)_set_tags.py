import itertools
import os
import re

## --- INPUT      : (sourcefolder_1) = Ordner, der alle 18 Wahlperioden-Ordner mit ihren Protokollen (XML-Format) enthält
## --- ZIEL Part 1: (sourcefolder_2) = Je Wahlperiode alle XML-Dateien getagged nach Protokollteilen (Metadaten, Inhaltsangabe, Hauptteil, Anhang) ##

## --- INPUT      : (source_folder_2) = s.o.
## --- ZIEL Part 2: (targetfolder_2) = Je Wahlperiode alle (teilgetaggten) XML-Dateien getagged nach Sprechbeiträgen, Unterbrechungen + Interaktionen ##

###PARAMS: --------------------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = "C:\\Users\\vck\\Documents\\000MA Studium\\MA Thesis\\AAAtestordner\\taggables"
sourcefolder_2 = "C:\\Users\\vck\\Documents\\000MA Studium\\MA Thesis\\AAAtestordner\\3tagged\\taggable"
targetfolder_2 = "C:\\Users\\vck\\Documents\\000MA Studium\\MA Thesis\\AAAtestordner\\3tagged\\reden_tagged"

###FUNCTIONS: ----------------------------------------------------------------------------------------------------------------------------------
def create_wplist(needed_dir):                        #list alle wp-ordner
    os.chdir(needed_dir)
    wp_list = os.listdir(needed_dir)      
    return wp_list

def create_filelist(needed_dir, wp): 
    wp_path = os.path.join(needed_dir, wp)
    file_list = os.listdir(wp_path)
    return wp_path, file_list                         #callable w/ -->   my_var1, my_var2 = create_filelist(x_1, x_2)

def read_file(wp_path, item):                         #item aus file_list
    file_path = os.path.join(wp_path, item)
    file = open(file_path, "a+", encoding = "utf-8")  #a+ = appending+reading, braucht aber nächste zeile
    file.seek(0)                                      #trick um pointer an anfang zu setzen https://stackoverflow.com/questions/31794291/python-open-append-and-read-file-read-returns-empty-string
    file_data = file.read()
    return file_data

def write_new_xml(new_file_path, new_file_data):
    new_file = open(new_file_path, "w", encoding="utf-8")
    new_file.write(new_file_data)
    new_file.close()
    
def tag_mainparts(file_data):
    #set metadaten:
    file_data = re.sub("<WAHLPERIODE>.+</TITEL>", "<METADATEN>\n\g<0>\n</METADATEN>", file_data, flags=re.DOTALL)
    #set inhaltstag (öffn.):
    file_data = re.sub("<TEXT>", "\g<0>\n<INHALTSANGABE>\n", file_data)
    #set inhaltstag (schl.) + hauptteiltag (öffn.):
    file_data = re.sub("Beginn: \d{1,2}\.?.*Uhr", "</INHALTSANGABE>\n<HAUPTTEIL>\n\g<0>", file_data)
    #set hauptteiltag (schl.) + anhangtag (öffn.):
    file_data = re.sub("\((?:Schluß|Schluss|Ende).+\d{1,2}.+Uhr(?:\s\d{1,2}\sMinuten?\.?\s?)?\.?\)\.?", "\g<0>\n</HAUPTTEIL>\n<ANHANG>", file_data)
    #set anhangtag (schl.):
    file_data = re.sub("</TEXT>", "\n</ANHANG>\n\g<0>", file_data)
    return file_data

def get_ID(file_data):
    prot_ID = re.search("<NR>(.+)</NR>", file_data)
    prot_ID = prot_ID.group(1)
    return prot_ID

def get_date(file_data):
    date = re.search("<DATUM>(.+)</DATUM>", file_data)
    date = date.group(1)
    return date
    
def get_hauptteil(file_data):
    hauptteil_match = re.search("<HAUPTTEIL>.+</HAUPTTEIL>", file_data, re.DOTALL)  #only finds 1st instance
    hauptteil_text= hauptteil_match.group(0) #mit tags
    return hauptteil_text

##für jedes Dok: enthält alle sprecher eines doks m. jew. partei
def create_local_MdBList(hauptteil_text):
    #liste aller parties:
    party_list = ["Alterspräsident", "Alterspräsidentin", "BP", "Bundeskanzler", "Bundeskanzlerin", "BÜNDNIS 90/DIE GRÜNEN", "BÜNDNIS 90/GRÜNE", "CDU", "CSU", "CDU/CSU", "DIE GRÜNEN", "DIE LINKE", "DP", "DRP", "FDP", "fraktionslos", "FU", "FVP", "GB/BHE", "GRÜNE", "KPD", "NR", "NS", "parteilos", "PDS", "PDS/Linke Liste", "Präsident", "Präsidentin", "SPD", "SSW", "Vizepräsident", "Vizepräsidentin", "WAV", "Z"]
    #liste erstellen m. allen MdB-Namen der laufenden file (für erneute nennungen im text):
    TUPLE_MdB_list = []
    #für jede partei:
    for party in party_list:
        MdB_regex = "(.+)\s\((" + party + ")\)\s?:"
        party_TUPLE_MdB_list = re.findall(MdB_regex, hauptteil_text, flags=re.MULTILINE)  #returns list of tuples(!) w/ all matches (if sth in (), only that - if ()>1 than dim = amount of ()) 
        #alle Abg. mit selber Party an große Liste hängen:
        for item in party_TUPLE_MdB_list:
            TUPLE_MdB_list.append(item)   
    #duplikate löschen:
    TUPLE_MdB_list = list(set(TUPLE_MdB_list))
    local_MdB_list = [list(entry) for entry in TUPLE_MdB_list]                            #tuple-liste konvertieren --> liste von listen (für nächsten schritt)
    #TEST:
    print(local_MdB_list)
    return local_MdB_list

##gilt für jede wp einzeln: --in mdb_list sind (i. idealfall) alle sprecher einer wp m. jew. partei
def append_to_MdB_list(MdB_list, local_MdB_list):
    for entry in local_MdB_list:
        entry[0] = entry[0].strip("() .,;:-!?/\[]_")
        #append each minilist [Abgeordneter, Partei] to MdB_list (for each wp):
        MdB_list.append(entry)
    #remove duplicates from MdB_list:
    MdB_list.sort()
    MdB_list = list(MdB_list for MdB_list,_ in itertools.groupby(MdB_list))
    return MdB_list

def tag_speakers(hauptteil_text, prot_ID, date):                                                    #used by tag_speechparts(file_data)!
    #tags setzen für sprecher (anfangs und end <speech>-tag werden durch repair_ends() gesetzt):    #re.MULTILINE treats each line as a separate string (^ matches line starts)
    new_hauptteil_text = re.sub("^[A-Z]?.*([A-Z].+)\s\((.+)\)\s?:", "</SPEECH>\n<SPEECH PARTY=\"\g<2>\" NAME=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\" OTEXT=\"\g<0>\">", hauptteil_text, flags=re.MULTILINE)
    new_hauptteil_text = re.sub("^(Präsidenti?n?).+:", "</SPEECH>\n<SPEECH PARTY=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\" OTEXT=\"\g<0>\">", new_hauptteil_text, flags=re.MULTILINE) 
    new_hauptteil_text = re.sub("^(Vizepräsidenti?n?).+:", "</SPEECH>\n<SPEECH PARTY=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\" OTEXT=\"\g<0>\">", new_hauptteil_text, flags=re.MULTILINE)
    new_hauptteil_text = re.sub("^(Bundeskanzleri?n?).+:", "</SPEECH>\n<SPEECH PARTY=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\" OTEXT=\"\g<0>\">", new_hauptteil_text, flags=re.MULTILINE)
    new_hauptteil_text = re.sub("^(Alterspräsidenti?n?).+:", "</SPEECH>\n<SPEECH PARTY=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\" OTEXT=\"\g<0>\">", new_hauptteil_text, flags=re.MULTILINE)
    return new_hauptteil_text
    
def tag_interaction(new_hauptteil_text, prot_ID, date):                                             #used by tag_speechparts(file_data)!
    #tags setzen für interactions:
    new_hauptteil_text = re.sub("\(.*(Beifall).*\.?\)", "<INTERACTION TYPE=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\">\g<0></INTERACTION>", new_hauptteil_text)
    new_hauptteil_text = re.sub("\(.*(Zurufe?).*\.?\)", "<INTERACTION TYPE=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\">\g<0></INTERACTION>", new_hauptteil_text)
    new_hauptteil_text = re.sub("\(.*(Lachen).*\.?\)", "<INTERACTION TYPE=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\">\g<0></INTERACTION>", new_hauptteil_text)
    new_hauptteil_text = re.sub("\(.*(Widerspruch).*\.\)", "<INTERACTION TYPE=\"\g<1>\" ID=\"" + prot_ID + "\" DATE=\"" + date + "\">\g<0></INTERACTION>", new_hauptteil_text)
    return new_hauptteil_text

#methode, um in tag_interruptions() falsche abgeordneten-values zu korrigieren (s.u.)
def own_replace(text):
    i = 0
    bool = "False"
    for t in text:
        if t == "(" or t == "[":
            bool = "True"
            break
        i += 1
    if bool == "True":
        newly = text[:i] + "\\" + text[i:]
    else:
        newly = text  
    return newly
    
def tag_interruption(MdB_list, new_hauptteil_text, prot_ID, date):
    for entry in MdB_list:
        #PROBLEM: wenn ( oder ) vorkommen wirft er errors - daher vorher replacen: --> geht nicht ohne trick mit eigener methode, weil immer escaped wird!
        abgeo = own_replace(entry[0])
        mention_regex_1 = "\(.*(" + abgeo + ")\s?:(.+)\)"       #abgeordnete ohne erneute parteinennung
        mention_regex_2 = "\((.+)\[([A-Z]{2}.+)\]\s?:(.+)\)"    #unterbrechungen in anderem format (mit parteiangabe)
        new_hauptteil_text = re.sub(mention_regex_1, "<INTERRUPTION PARTY=\""+entry[1]+"\" NAME=\"\g<1>\" ID=\"" +prot_ID+ "\" DATE=\"" +date+ "\" OTEXT=\"\g<0>\">\g<2></INTERRUPTION>", new_hauptteil_text) #erstmal ohne re.MULTILINE
        new_hauptteil_text = re.sub(mention_regex_2, "<INTERRUPTION PARTY=\"\g<2>\" NAME=\"\g<1>\" ID=\"" +prot_ID+ "\" DATE=\"" +date+ "\" OTEXT=\"\g<0>\">\g<3></INTERRUPTION>", new_hauptteil_text)
    return new_hauptteil_text

def repair_ends(new_hauptteil_text):
    #remove first </SPEECH>-tag:
    new_hauptteil_text = re.sub("</SPEECH>", "", new_hauptteil_text, count=1)
    #add last </SPEECH>-tag:
    new_hauptteil_text = re.sub("</HAUPTTEIL>", "</SPEECH>\n</HAUPTTEIL>", new_hauptteil_text, count=1)
    return new_hauptteil_text

def correct_doubletag(new_hauptteil_text):
    new_hauptteil_text = re.sub("<SPEECH.+(<SPEECH.+)", "\g<1>", new_hauptteil_text)
    new_hauptteil_text = re.sub("</SPEECH>.</SPEECH>", "</SPEECH>", new_hauptteil_text, flags=re.DOTALL)
    return new_hauptteil_text

def tag_speechparts(file_data, MdB_list):                       #braucht new_file_data von tag_mainparts()! ABER HIER: ÜBER ZWISCHENSCHRITT IN DIRECTORIES!
    #Protokoll-Nr. rausfiltern:
    prot_ID = get_ID(file_data)
    #Datum rausfiltern:
    date = get_date(file_data)
    #hauptteil rausfiltern:
    hauptteil_text= get_hauptteil(file_data)
    #liste erstellen m. allen MdB-Namen der akt. file (für erneute nennungen im text):
    local_MdB_list = create_local_MdBList(hauptteil_text)
    #diese liste an MdB_liste aus MAIN appenden:                                    
    MdB_list = append_to_MdB_list(MdB_list, local_MdB_list)     #hier wird neue MdB_list (ohne duplicates) zurückgegeben
    #tags setzen sprecher (anfangs und end <speech>-tag erst durch repair_ends())      
    new_hauptteil_text = tag_speakers(hauptteil_text, prot_ID, date)
    #tags setzen interactions:
    new_hauptteil_text = tag_interaction(new_hauptteil_text, prot_ID, date)
    #erneute in-speech-mentions taggen: z.B.:  \(.*Adenauer.*\)
    #FOLGENDES TESTWEISE REMOVE:
    new_hauptteil_text = tag_interruption(MdB_list, new_hauptteil_text, prot_ID, date)
    #erstes </SPEECH> entfernen, letztes </SPEECH> setzen:
    new_hauptteil_text = repair_ends(new_hauptteil_text)
    #unvermeidliche tagging-fehler entfernen:
    new_hauptteil_text = correct_doubletag(new_hauptteil_text)
    #replace hauptteil in file_data
    new_file_data = file_data.replace(hauptteil_text, new_hauptteil_text)
    return new_file_data

###MAIN: ---------------------------------------------------------------------------------------------------------------------------------------
#PART 1: hauptteile taggen:
def main_part_1(sourcefolder_1, sourcefolder_2):
    #liste d. wahlperioden-ordner
    wp_list = create_wplist(sourcefolder_1)
    for wp in wp_list:
        #list alle files/wahlp.:
        wp_path, file_list = create_filelist(wp_list, sourcefolder_1, wp)  
        #create neue ordner für getaggte files jeder wahlp.:
        newfolder_path = os.path.join(sourcefolder_2, wp)
        os.mkdir(newfolder_path)
        #für jede file in altem wp-ordner:
        for item in file_list:
            #file einlesen --> daten raus:
            file_data = read_file(wp_path, item)
            #3 hauptteile taggen:
            new_file_data = tag_mainparts(file_data)
            #neuer text --> neue file --> in neuen wp-ordner:
            new_file_name = "3tagged" + item
            new_file_path = os.path.join(newfolder_path, new_file_name)
            write_new_xml(new_file_path, new_file_data)

#PART 2: alles übrige taggen:
def main_part_2(sourcefolder_2, targetfolder_2):
    #liste d. wahlperioden-ordner
    wp_list = create_wplist(sourcefolder_2)
    for wp in wp_list:
        #list alle files/wahlp.:
        wp_path, file_list = create_filelist(wp_list, sourcefolder_2, wp)
        #create neue uordner je wp für final getaggte files:
        newfolder_path = os.path.join(targetfolder_2, wp)
        os.mkdir(newfolder_path)
        #create übergreifende list for each WahlP: alle MdB-mentions/speaker:
        MdB_list = []
        #für jede file in altem wp-ordner:
        for item in file_list:
            #file einlesen --> daten raus:
            file_data = read_file(wp_path, item)
            #speech-teile taggen:
            new_file_data = tag_speechparts(file_data, MdB_list)
            #neuer text --> neue file --> in neuen wp-ordner:
            new_file_name = "final" + item
            new_file_path = os.path.join(newfolder_path, new_file_name)
            write_new_xml(new_file_path, new_file_data)

##RUN: ------------------------------------------------------------------------------------------------------------------------------------------
main_part_1(sourcefolder_1)
main_part_2(sourcefolder_2, targetfolder_2)















