from collections import Counter
import os

## --- INPUT: (sourcefolder_1) = Ordner, der für jede Partei einen Ordner mit Jahres-Textdateien enthält (nur Lemmata von Verben/Nomen/Adjektiven - ohne Named Entities)
## --- ZIEL: (targetfolder_1) = wie sourcefolder_1, aber Stoppwörter und Hapax Legomena entfernt ##

##NOTES: -------------------------------------------------------------------------------------------------------------------------------
# main_part_1(): für jeden sprecher wird liste d. 200 häufigsten wörter (ohne zählangabe) ermittelt, schnittmenge aller sprecher-listen --> result
#                --> methode wird nicht angewendet, da deren resultat hier in main_part_2() enthalten

# main_part_2(): für jede file jedes sprechers wird liste d. 100 häufigsten wörter ermittelt + häufigkeiten normalisiert (durch länge files),
#                daraus überliste + häufigk. normalisiert (durch anzahl files/spr.),
#                elemente d. überliste an liste für alle sprecher angehängt + nach häufigk. sortiert, davon später die n häufigsten wörter als stopwords

##PARAMS: ------------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = r"E:\4_PARTY_YEAR_txts"           
targetfolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\3tagged\4_PARTY_YEAR_txts"

##FUNCTIONS: ---------------------------------------------------------------------------------------------------------------------------
def create_speakerlist(sourcefolder_1):                         #list alle sprecher-ordner
    os.chdir(sourcefolder_1)
    speaker_list = os.listdir(sourcefolder_1)                       
    return speaker_list

def create_filelist(sourcefolder_1, speaker):
    speaker_path = os.path.join(sourcefolder_1, speaker)
    file_list = os.listdir(speaker_path)
    return speaker_path, file_list

def read_file(speaker_path, item):                              #item aus file_list
    file_path = os.path.join(speaker_path, item)
    file = open(file_path, "r", encoding="utf-8")
    file_data = file.read()
    file.close()
    return file_data

def intersection(list1, list2):
    sub_intersec_list = [elem for elem in list1 if elem in list2]
    return sub_intersec_list
    
def give_intersec_list(SUPER_freqlist):
    #zuerst mit 1. liste initialisieren, von dieser läuft schnittmengenabgleich weiter
    intersec_list = SUPER_freqlist[0]
    for liste in SUPER_freqlist:
        intersec_list = intersection(intersec_list, liste)
    return intersec_list
        
def get_most_freq_words(word_list, amount):
    CounterVariable = Counter(word_list)
    list_most_occur = CounterVariable.most_common(amount)
    return list_most_occur

def normalize_list(liste, normalizer):
    normalized_list = []
    for item in liste:
        word_freq = item[1]                            #häufigkeit d. wortes
        norm_val = word_freq/normalizer                #normalis. häufigk. d. wortes
        normalized_list.append([item[0], norm_val])    #unterliste von ['wort', normalis. häufigk.] an oberliste hängen
    return normalized_list
     
def get_super_norm_list(list_to_be_added, SUPER_norm_list):
    for elem in list_to_be_added:                      #elem = ['word', value]
        SUPER_norm_list.append(elem)
        for e in SUPER_norm_list:
            if e[0] == elem[0] and e[1] != elem[1]:    #damit nicht dasselbe tuple genommen wird
                e[1] = e[1] + elem[1]
                SUPER_norm_list.remove(elem)           
    #SUPER_norm_list aufsteigend sortieren:
    SUPER_norm_list.sort(key=lambda tup: tup[1])
    return SUPER_norm_list

def get_least_common_words(word_list):                #wörter die nur 1mal vorkommen
    CounterVariable = Counter(word_list)
    list_freq = CounterVariable.most_common()         #list of tuples with (word, freq)
    #liste für wörter, die nur einmal vorkommen:
    onesies_list = []
    for item in list_freq:
        if item[1] == 1:
            onesies_list.append(item[0])
    return onesies_list

def write_list_to_new_file(new_file_path, file_wörter):
    #liste wird in neue datei geschrieben:
    with open(new_file_path, "a", encoding="utf-8") as new_file:            
        for elem in file_wörter:
            new_file.write(elem)
            new_file.write("\n")
    new_file.close()
    
##MAIN:---------------------------------------------------------------------------------------------------------------------------------
# def main_part1(sourcefolder_1): 
#     SUPER_freqlist = []
#     speaker_list = create_speakerlist(sourcefolder_1)
#     for speaker in speaker_list:
#         speaker_path, file_list = create_filelist(sourcefolder_1, speaker)
#         speaker_wordlist = []
#         #alle files von speaker durchlaufen:
#         for item in file_list:
#             file_data = read_file(speaker_path, item)
#             #create liste aller wörter (lemmata) der file:
#             split_list = file_data.split()
#             #liste an übergreifende liste des sprechers anhängen:
#             for elem in split_list:
#                 speaker_wordlist.append(elem)
#         #für den sprecher häufigste 200 wörter ermitteln:
#         CounterVariable = Counter(speaker_wordlist)
#         most_occur = CounterVariable.most_common(200)            #list of tuples: ['wort', zählangabe]
#         #zählangaben von most_occur weg, nur wörter --> neue liste:
#         freq_list = []
#         for lemm in most_occur:
#             freq_list.append(lemm[0]) 
#         #freq_listen an SUPER_freqlist hängen (200 häufigsten wörter jedes sprechers):
#         SUPER_freqlist.append(freq_list)    
#     #ermittle schnittmenge aller sprecherlisten in SUPER_freqlist:
#     intersec_list = give_intersec_list(SUPER_freqlist)
#     return intersec_list                                         #hier: ['sein', 'haben', 'wollen', 'frage', 'möchten']       
                                             
#STOPPWORT-LISTE ERMITTELN:              
def main_part2(sourcefolder_1):
    SUPER_norm_list = []
    speaker_list = create_speakerlist(sourcefolder_1)
    for speaker in speaker_list:
        speaker_path, file_list = create_filelist(sourcefolder_1, speaker)
        speaker_norm_list = []
        #alle files von speaker durchlaufen:
        for item in file_list:
            file_data = read_file(speaker_path, item)
            #liste aller wörter der file erstellen:
            split_list = file_data.split()
            #für jede file d. sprechers häufigste 100 wörter ermitteln:
            file_most_occur = get_most_freq_words(split_list, 100)
            #normalisieren durch länge der files: 
            #neue liste f. wörter + file-normalis. häufigkeiten:
            file_norm_list = normalize_list(file_most_occur, len(split_list))
            #in file_norm_list sind die häufigsten wörter jeder file
            #file_norm_list an speaker_norm_list hängen, sodass 2D-list!:
            for val in file_norm_list:
                speaker_norm_list.append(val)
                #speaker_norm_list enthält die 100 häufigsten Wörter jeder file des speakers! #entspricht nicht anzahl der files eines sprechers/100, weil nicht alle files 100 most freq word besitzen...
        #normalisieren durch anzahl der files pro speaker (listenname bleibt):
        speaker_norm_list = normalize_list(speaker_norm_list, len(file_list))                 
        #speaker_norm_list = von jeder file die häufigsten 100 wörter (normalisiert durch file, normalisiert durch sprecher)
        #an SUPER_norm_list aller speaker anhängen:   
        #damit dieselben wörter nicht mehrfach gelistet werden --> normalis. häufigkeiten addiert, duplikate gelöscht:      
        SUPER_norm_list = get_super_norm_list(speaker_norm_list, SUPER_norm_list)   
    return(SUPER_norm_list)                                                                   #len(SUPER_norm_list) = 3255
        
#UNIKAT-LISTE ERSTELLEN:
def main_part3(sourcefolder_1):
    onesies_ALL_list = []
    speaker_list = create_speakerlist(sourcefolder_1)
    for speaker in speaker_list:
        speaker_path, file_list = create_filelist(sourcefolder_1, speaker)
        onesies_speaker_list = []
        #alle files von speaker durchlaufen:
        for item in file_list:
            file_data = read_file(speaker_path, item)
            #create liste aller wörter der file:
            split_list = file_data.split()           
            #für jede file d. sprechers die mit 1-häufigk. ermitteln:
            onesies_list = get_least_common_words(split_list)
            #append to speakerlist (mit duplicates):
            onesies_speaker_list[0:0] = onesies_list
        #append to overall list (mit dupl.):
        onesies_ALL_list[0:0] = onesies_speaker_list
        print(len(onesies_ALL_list))
        #get words that only appear once in corpus (reuse method from above):
        true_onesies = get_least_common_words(onesies_ALL_list)
    return true_onesies

#STOPWORDS UND UNIKALE WÖRTER ENTFERNEN FÜR TEIL PER_PARTY_PER_YEAR:
def main_part_4(SUPER_norm_list, onesies_list, sourcefolder_1, targetfolder_1): 
    #die 100 meistgebrauchten wörter als stoppwörter nehmen ("grüne" wird rausgenommen, weil partei, dafür wort an 3154. stelle):
    teil_liste = SUPER_norm_list[3154:]    #zweidim.! ['word', value]
    #zum eindim. stoppwort-liste machen:
    stop_word_list = []
    for tup in teil_liste:
        stop_word_list.append(tup[0])
    #stop_word_list.remove("grüne")
    speaker_list = create_speakerlist(sourcefolder_1)
    #für jeden speaker-ordner:
    for speaker in speaker_list:
        speaker_path, file_list = create_filelist(sourcefolder_1, speaker)
        #alle files von speaker durchlaufen:
        for item in file_list:
            file_data = read_file(speaker_path, item)
            #hieraus liste erstellen mit allen wörtern:
            file_wörter = file_data.split()                       
            #liste erstellen für wörter, die nicht in stop_word_list: und nicht in onesies_list:
            pos_liste = []
            #alle wörter aus file_wörter, die nicht stoppwörter sind, werden an pos_liste gehängt:
            for elem in file_wörter: 
                if elem not in stop_word_list and elem not in onesies_list:                     #positive selektion 
                    #elem an dritte liste anhängen:
                    pos_liste.append(elem)                                                                       
            #neue datei erstellen + file_wörter reinschreiben:
            new_file_path = os.path.join(targetfolder_1, speaker, "final" + item)
            write_list_to_new_file(new_file_path, pos_liste)             
 
##RUN: ---------------------------------------------------------------------------------------------------------------------------------  
stoppwort_liste = main_part2(sourcefolder1_)
onesies_liste = main_part3(sourcefolder_1)
main_part_4(stoppwort_liste, onesies_liste, sourcefolder_1, targetfolder_1)
main_part_5(onesies_liste, sourcefolder_1, targetfolder_1)



