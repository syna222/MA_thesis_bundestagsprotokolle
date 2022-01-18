import csv
from gensim.test.utils import get_tmpfile
from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from gensim.scripts import word2vec2tensor
from HanTa import HanoverTagger as HT
from multiprocessing import cpu_count
import nltk
import numpy as np
import os
import pandas as pd
import re
import string
#initially needed:
#nltk.download('punkt')

## --- INPUT: (party_folders) = Ordner, der 5 Parteiordner enthält (BÜNDNIS90DIEGRÜNEN, CDUCSU, FDP, PDSLINKE, SPD), in denen pro Parteijahr eine Textdatei vorliegt
## --- ZIEL:  (word2vec_folder) = Für jede der 5 Parteien ein WEM-Modell (aus den Dateien Sentence-Listen, aus Sentence-Listen Token-Listen --> Modell) ##

###PARAMS: --------------------------------------------------------------------------------------------------------------------------------------
party_folders = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\3tagged\ZZZZZ_gensim_originals_2"
word2vec_folder = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\WEM_MODELS\WEM_2\model"
kv_folder = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\WEM_MODELS\WEM_2\kv"

###FUNCTIONS: -----------------------------------------------------------------------------------------------------------------------------------
def create_speakerlist(party_folders):                              #list alle der 7 partei-ordner
    os.chdir(party_folders)
    speaker_list = os.listdir(party_folders)      
    return speaker_list

def create_filelist(party_folders, speaker): 
    speaker_path = os.path.join(party_folders, speaker)
    file_list = os.listdir(speaker_path)
    return speaker_path, file_list                                  #callable w/ -->   my_var1, my_var2 = create_filelist(x_1, x_2)

def read_file(speaker_path, item):                                  #item aus file_list
    file_path = os.path.join(speaker_path, item)
    file = open(file_path, "r", encoding="utf-8")
    file_data = file.read()
    file.close()
    return file_data

def tokenize_sent(file_data):
    pre_list_of_sent = nltk.sent_tokenize(file_data, language="german")
    list_of_sentences = []
    #remove satzzeichen und großschreibung around here:
    for item in pre_list_of_sent:
        new_item = re.sub("[\.!\?,;:\-\(\)\[\)]", "", item)
        list_of_sentences.append(new_item.lower())                  
    return list_of_sentences

def tokenize_words(list_of_sentences):
    file_2D_list = []
    #each sentence is tokenized, put in list --> list appended to file_2D_list:
    for sentence in list_of_sentences:
        list_of_words = nltk.word_tokenize(sentence)                 #each list_of_words = 1 sentence
        file_2D_list.append(list_of_words)
    return file_2D_list                                              #oberliste: sätze, unterliste:nomen-token

def word2vec_model_to_keyedvectors(word2vec_model_path, party_name):
    model = Word2Vec.load(word2vec_model_path)
    model_name = "keyedvec_" + party_name + ".kv"
    model.wv.save_word2vec_format(model_name)
    
def kv_model_to_tensorflow(kv_model_path, party_name):
    #!darf nicht ".model" sein, sondern muss ".kv"-endung besitzen:
    word2vec2tensor.word2vec2tensor(kv_model_path, party_name) 

def create_model_word_vec_file(kv_model_path, party_name):
    model = KeyedVectors.load_word2vec_format(kv_model_path)
    #df aller wort-vektoren (aber ohne angabe, um welches wort es sich handelt):
    vec_df = pd.DataFrame(model.vectors)
    word_list = []
    #durch df laufen, vektor erhalten, vektor nachschlagen, wort erhalten:
    #wort an liste anhängen, liste als indexe der rows in vec_df:
    for i in vec_df.iloc:
        my_vec = i.to_numpy()
        simi_vec = model.most_similar(positive=[my_vec,])
        word = simi_vec[0][0]
        word_list.append(word)
    #wort-liste als indexe setzen, speichern:
    vec_df.index = word_list
    vec_df.to_csv(party_name + "_wörtervekt.csv") 

##methode, die wort einliest, und aus allen modellen ähnlichste zurückgibt:
def word_sim_all_models(kv_folder, word):
    model_list = os.listdir(kv_folder)
    for model_name in model_list:
        model_path = os.path.join(kv_folder, model_name)
        model = KeyedVectors.load_word2vec_format(model_path)
        try:
            result = model.most_similar(word)
            print("Parteimodell: ", model_name, " Wort: ", word)
            print("Ähnlichste Wörter: ")
            for i in result:
                print(i)
            print("\n")
        except Exception as message:
            print("Exception occured!: ", message, " model name is: ", model_name)

###MAIN: ----------------------------------------------------------------------------------------------------------------------------------------
def main_create_word2vec_folder(party_folders):
    speaker_list = create_speakerlist(party_folders)    
    for speaker in speaker_list:   
        speaker_path, file_list = create_filelist(party_folders, speaker)
        #übergeordnete liste für jew. sprecher, in der wort-listen für jeden satz sind:
        speaker_2D_wordlist = []
        for item in file_list:
            #print("file name: ", item)
            #get text from each speaker-file:
            file_data = read_file(speaker_path, item)
            #get all sentences of speaker-file:
            list_of_sentences = tokenize_sent(file_data)
            #jedes elem in list_of_sentences tokenizieren --> get 2D_liste für entspr. file! (in unterlisten aber nur noch nomen):
            file_2D_list = tokenize_words(list_of_sentences) 
            #innere listen (jede liste alle token für je 1 satz) an speaker_2D_wordlist anhängen:
            for liste in file_2D_list:
                speaker_2D_wordlist.append(liste)      
        #speaker_2D_wordlist übergeben an gensim --> daraus modell:    
        model = Word2Vec(speaker_2D_wordlist, window=10, workers=cpu_count()-1, iter=10)           #Defaults result vector size = 100, default for min_count (for words) = 5, default for window=5
        model_name = "word2vec_" + speaker + "_nn.model"
        model.save(model_name)
        print(speaker)

def main_convert_models_to_kv(word2vec_folder, model_filenames_list):
    for file_name in model_filenames_list:
        path = os.path.join(word2vec_folder, file_name)
        try:
            party_name = re.search("_([A-Z]*[0-9]{0,2}[A-Z]*)_", file_name).group(1)
            word2vec_model_to_keyedvectors(path, party_name)
        except Exception as message:
            print("Exception occured!: ", message, " filename is: ", file_name)      

def main_convert_kvmodels_to_tensorflow(kv_folder, kv_model_filenames_list):
    for file_name in kv_model_filenames_list:
        kv_model_path = os.path.join(kv_folder, file_name)
        try:
            party_name = re.search("_([A-Z]*[0-9]{0,2}[A-Z]*)\.kv", file_name).group(1)
            print(party_name)
            create_model_word_vec_file(kv_model_path, party_name)
            kv_model_to_tensorflow(kv_model_path, party_name)
        except Exception as message:
            print("Exception occured!: ", message, " filename is: ", file_name)

##RUN: -------------------------------------------------------------------------------------------------------------------------------------------
model_filenames_list = ["word2vec_BUENDNIS90DIEGRUENEN_2.model", "word2vec_CDUCSU_2.model", "word2vec_DIELINKE_2.model", "word2vec_FDP_2.model", "word2vec_SPD_2.model"]
kv_model_filenames_list = ["keyedvec_BUENDNIS90DIEGRUENEN.kv", "keyedvec_CDUCSU.kv", "keyedvec_DIELINKE.kv", "keyedvec_FDP.kv", "keyedvec_SPD.kv"]

main_create_word2vec_folder(party_folders)
main_convert_models_to_kv(word2vec_folder, model_filenames_list)
main_convert_kvmodels_to_tensorflow(kv_folder, kv_model_filenames_list)

#Ähnlichkeitsberechnung:
word_sim_all_models(kv_folder, "asyl")



















