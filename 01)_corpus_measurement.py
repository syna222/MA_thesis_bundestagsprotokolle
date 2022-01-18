import os
import xml.etree.ElementTree as ET

## --- INPUT: Ordner, der alle 18 Wahlperioden-Ordner mit ihren jeweiligen Protokollen (XML-Format) enthält
## --- ZIEL:  Auszählung aller Dateien (Anzahl Dateien, Anzahl Wörter gesamt, Median u. Mittelwert Wörter/Datei, Wörter/Wahlperiode, Anzahl Redevorkommen/Partei) ##

###PARAMS: --------------------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\BundesProtokolle"

###FUNCTIONS: -----------------------------------------------------------------------------------------------------------------------------------
def create_wplist(sourcefolder_1):                    #list alle wahlperioden-ordner
    os.chdir(sourcefolder_1)
    wp_list = os.listdir(sourcefolder_1)              
    return wp_list

def create_filelist(wp_list, sourcefolder_1, wp):
    wp_path = os.path.join(sourcefolder_1, wp)
    file_list = os.listdir(wp_path)
    return wp_path, file_list                         #callable w/ -->   my_var_1, my_var_2 = create_filelist(x_1, x_2)

def read_file(wp_path, item):                         #item aus file_list
    file_path = os.path.join(wp_path, item)
    file = open(file_path, "a+", encoding = "utf-8")  #a+ = appending+reading, braucht aber nächste zeile
    file.seek(0)                                      #trick um pointer an anfang der datei zu setzen https://stackoverflow.com/questions/31794291/python-open-append-and-read-file-read-returns-empty-string
    file_data = file.read()
    file.close()
    return file_data

def count_parties(party_list, party_dict, file_data):
    for party in party_list:
        #vorkommnis der partei in jeder file zählen:
        search_count = file_data.count(party)
        #Klammern weg:
        raw_party = party.replace("(", "")
        raw_party = raw_party.replace(")", "")
        raw_party = raw_party.replace("[", "")
        raw_party = raw_party.replace("]", "")
        #vorherige vorkommnis-zahl erhalten:
        value_var = party_dict.get(raw_party)            
        if value_var is not None:                    
            value_var = value_var + search_count
            #vorkommnis-zahl updaten:
            party_dict[raw_party] = value_var
    return party_dict                                

def count_words(file_data):                         
    datei_list = file_data.split()
    word_count = len(datei_list)
    return word_count

def get_median(median_list):
    median_list.sort()
    #auf gerade anzahl testen:
    if len(median_list) % 2 == 0:
        pos1 = int(len(median_list) / 2 - 1)
        pos2 = pos1 + 1
        median = (median_list[pos1] + median_list[pos2]) / 2
    else:
        pos1 = int(len(median_list) / 2)
        median = median_list[pos1]
    return median

def print_results(file_counter, data_wordcount, data_mean_wordcount, median, wp_wordcount_list, party_dict):
    print("Anzahl Dateien insgesamt: ", file_counter)
    print("Anzahl Wörter insgesamt: ", data_wordcount)
    print("Mittelwert Dateilänge (in Wörtern): ", data_mean_wordcount)
    print("Median Dateilänge (in Wörtern): ", median)
    print("Anzahl Sprechvorkommen nach Partei: ", party_dict)
  
###MAIN: ----------------------------------------------------------------------------------------------------------------------------------------
def main_method(source_folder_1):
    wp_list = create_wplist(sourcefolder_1)
    ##variables:
    party_list = ["(BP)", "(BÜNDNIS 90/DIE GRÜNEN)", "(CDU)", "(CSU)", "(CDU/CSU)", "(DIE GRÜNEN)", "(DIE LINKE)", "(DP)", "(DRP)", "(FDP)", "(FU)", "(FVP)", "(GB/BHE)", "(GRÜNE)", "(KPD)", "(PDS)", "(PDS/Linke Liste)", "(SPD)", "(SSW)", "(WAV)", "(Z)",
                  "[BP]", "[BÜNDNIS 90/DIE GRÜNEN]", "[CDU]", "[CSU]", "[CDU/CSU]", "[DIE GRÜNEN]", "[DIE LINKE]", "[DP]", "[DRP]", "[FDP]", "[FU]", "[FVP]", "[GB/BHE]", "[GRÜNE]", "[KPD]", "[PDS]", "[PDS/Linke Liste]", "[SPD]", "[SSW]", "[WAV]", "(Z]"]
    party_dict = {"BP": 0, "BÜNDNIS 90/DIE GRÜNEN": 0, "CDU": 0, "CSU": 0, "CDU/CSU": 0, "DIE GRÜNEN": 0, "DIE LINKE": 0, "DP": 0, "DRP": 0, "FDP": 0, "FU": 0, "FVP": 0, "GB/BHE": 0, "GRÜNE": 0, "KPD": 0, "PDS": 0, "PDS/Linke Liste": 0, "SPD": 0, "SSW": 0, "WAV": 0, "Z": 0}
    file_counter = 0
    wp_wordcount = 0
    data_wordcount = 0
    wp_wordcount_list = []
    median_list = []
    for wp in wp_list:
        #liste aller files/wahlp.
        wp_path, file_list = create_filelist(wp_list, sourcefolder_1, wp) 
        for item in file_list:
                #update counter:
                file_counter += 1
                #file einlesen:
                file_data = read_file(wp_path, item)
                #Datei nach Parteien-Sprechern durchsuchen + Vorkommn. zählen, upgedatetes dict erhalten:
                party_dict = count_parties(party_list, party_dict, file_data)
                #wörter in datei zählen:
                file_wordcount = count_words(file_data)
                #update wp_wordcount:
                wp_wordcount = wp_wordcount + file_wordcount
                #an median_list anhängen:
                median_list.append(file_wordcount)
                #update data_wordcount (overall sum):
                data_wordcount = data_wordcount + file_wordcount      
        #update global wp_count w/ wp_sum + reset wp_sum:
        wp_wordcount_list.append(wp_wordcount)
        wp_wordcount = 0
    #mittelwert aller filelängen (in words) erhalten:
    data_mean_wordcount = data_wordcount/file_counter
    #median ermitteln:
    median = get_median(median_list)
    #anzeigen:
    print_results(file_counter, data_wordcount, data_mean_wordcount, median, wp_wordcount_list, party_dict)

###RUN: -----------------------------------------------------------------------------------------------------------------------------------------
main_method(source_folder_1)
