import codecs
from HanTa import HanoverTagger as HT
import nltk
import os
#needed once:
nltk.download('punkt')

## --- INPUT: (sourcefolder_1) = Ordner, der für jede Partei einen Ordner mit Jahres-Textdateien enthält (in den Dateien die jew. Speeches d. Partei d. Jahres)
## --- ZIEL:  (targetfolder_1) = wie sourcefolder_1, aber tokenisiert, stoppwortlos, POS-getagged, lemmatisiert

#BUILD TAGGER:
tagger = HT.HanoverTagger("morphmodel_ger.pgz")

###PARAMS: --------------------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = "C:\\Users\\vck\\Documents\\000MA Studium\\MA Thesis\\AAAtestordner\\3tagged\\txt_per_PARTY_per_year"
targetfolder_1 = "C:\\Users\\vck\\Documents\\000MA Studium\\MA Thesis\\AAAtestordner\\3tagged\\NLTK_txt_per_PARTY_per_year"

###FUNCTIONS: -----------------------------------------------------------------------------------------------------------------------------------
def create_speakerlist(sourcefolder_1):                             #list alle sprecher-ordner
    os.chdir(sourcefolder_1)
    speaker_list = os.listdir(sourcefolder_1)      
    return speaker_list

def create_filelist(speaker_list, sourcefolder_1, speaker):
    speaker_path = os.path.join(sourcefolder_1, speaker)
    file_list = os.listdir(speaker_path)
    return speaker_path, file_list                                  #callable w/ -->   my_var1, my_var2 = create_filelist(x_1, x_2)

def read_file(speaker_path, item):                                  #item aus file_list
    file_path = os.path.join(speaker_path, item)
    file = open(file_path, "r", encoding="utf-8")
    file_data = file.read()
    file.close()
    return file_data

def tokenize_sent(file_data):
    sentence_list = nltk.sent_tokenize(file_data, language="german")
    return sentence_list

def toke_lemm_pos(sentence_list):
    tagged_2D_list = [] 
    for sentence in sentence_list:
        word_list = nltk.word_tokenize(sentence)
        lemma_tuplelist = tagger.tag_sent(word_list,taglevel= 1)     #lemmalist = tuple-liste
        lemma_listoflists = [list(elem) for elem in lemma_tuplelist] #sentence-list von word-lists
        for elem in lemma_listoflists:                               #jedes element: [Fehlern, Fehler, NN]
            tagged_2D_list.append(elem)
    return tagged_2D_list                                               
    
def write_new_txt(targetfolder_1, speaker, item, tagged_2D_list):
    new_file_path = os.path.join(targetfolder_1, speaker, item)
    new_file = open(new_file_path, "a", encoding="utf-8")  
    for elem in tagged_2D_list:
        new_file.write(str(elem) + "\n")                             #nimmt nur strings
    new_file.close()
    
###MAIN: ----------------------------------------------------------------------------------------------------------------------------------------  
def main_method(sourcefolder_1, targetfolder_1):
    speaker_list = create_speakerlist(sourcefolder_1)
    #speaker = ordner von partei o. amtsinhaber
    for speaker in speaker_list:
        #list alle files/speaker:
        speaker_path, file_list = create_filelist(speaker_list, sourcefolder_1, speaker)
        #für jede file in jedem speaker-ordner:
        for item in file_list:
            #file einlesen:
            file_data = read_file(speaker_path, item)
            #sätze tokenisieren:
            sentence_list = tokenize_sent(file_data)
            #wörter tokenisieren:
            tagged_2D_list = toke_lemm_pos(sentence_list)
            #in neue datei schreiben:
            write_new_txt(targetfolder_1, speaker, item, tagged_2D_list)
        
###RUN: ----------------------------------------------------------------------------------------------------------------------------------------- 
main_method(sourcefolder_1, targetfolder_1)








