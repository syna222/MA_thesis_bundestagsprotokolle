import codecs
import os
import re

## --- INPUT: (sourcefolder_1) = Ordner, der für jede Partei einen Ordner mit Jahres-Textdateien enthält (tokenisiert, stoppwortlos, POS-getagged, lemmatisiert)
## --- ZIEL:  (target_folder_1) = Ordner, der für jede Partei einen Ordner mit Jahres-Textdateien enthält (nur Lemmata von Verben/Nomen/Adjektiven - ohne Named Entities) ##

###PARAMS: --------------------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\3tagged\NLTK_txt_per_PARTY_per_year"
targetfolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\3tagged\neue_FINAL_FILES"

###FUNCTIONS: -----------------------------------------------------------------------------------------------------------------------------------
def create_speakerlist(sourcefolder_1):                         #list alle sprecher-ordner
    os.chdir(sourcefolder_1)
    speaker_list = os.listdir(sourcefolder_1)                       
    return speaker_list

def create_filelist(speaker_list, sourcefolder_1, speaker):
    speaker_path = os.path.join(sourcefolder_1, speaker)
    file_list = os.listdir(speaker_path)
    return speaker_path, file_list                              

def read_file(speaker_path, item):                              #item aus file_list
    file_path = os.path.join(speaker_path, item)
    file = open(file_path, "r", encoding="utf-8")
    file_data = file.read()
    file.close()
    return file_data

def get_word(elem_list):                                        #kein 'NE'-Label (Named Entity)
    POS_of_interest = ["ADJA", "ADJD", "NA", "NN", "VAFIN", "VAIMP", "VAINF", "VAPP",    
                       "VMFIN", "VMINF", "VMPP", "VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP"]
    tag = re.sub("\W", "", elem_list[2])                        #löscht alle non-alphanumeric chars aus tag
    word = ""
    if tag in POS_of_interest:
        word = re.sub("\W", "", elem_list[1])                   #gibt lemma zurück, frei von non-alphanumerics
    return word

def write_word_file(words_string, targetfolder_1, speaker, item):
    new_file_path = os.path.join(targetfolder_1, speaker, item)
    new_file = open(new_file_path, "w", encoding="utf-8")
    new_file.write(words_string)
    new_file.close()      
    
###MAIN: ----------------------------------------------------------------------------------------------------------------------------------------
def main_part_1 (sourcefolder_1, targetfolder_1):
    speaker_list = create_speakerlist(sourcefolder_1)
    #speaker = ordner von partei o. amtsinhaber
    for speaker in speaker_list:
        #list aller files/speaker:
        speaker_path, file_list = create_filelist(speaker_list, sourcefolder_1, speaker)
        #für jede file in jedem speaker-ordner:
        for item in file_list:
            #file einlesen --> daten raus:
            file_data = read_file(speaker_path, item)
            #var, in der verwendete wörter landen:
            words_string = ""
            #file_data (string) zu liste von einzelstrings:
            file_string_array = file_data.splitlines()               #jeder entry: ['allein', 'allein', 'ADV']
            #durch file_string_array-entries iterate + collect:
            for elem in file_string_array:                           #elems sind noch strings, bei denen an jeder pos ein char, deshalb...
                elem_list = elem.split(",")                          #jeder entry: ['allein   -oder-  'allein'  -oder-  'ADV']
                #gibt wort zurück, wenn sein POS-tag korrekt ist:
                word = get_word(elem_list)
                #case abfangen, dass word leer:
                if word != "":
                    #anhängen:
                    words_string = words_string + "\n" + word.lower()       
            #in neue datei (braucht bestandteile für path):
            write_word_file(words_string, targetfolder_1, speaker, item)    
    
###RUN: ----------------------------------------------------------------------------------------------------------------------------------------
main_part_1(sourcefolder_1, targetfolder_1)












