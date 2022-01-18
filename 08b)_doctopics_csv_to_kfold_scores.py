import csv
import os
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
import sklearn.metrics as skm

## --- INPUT: (sourcefolder_1) = Ordner, der von verschiedenen MALLET-Modellen Doc-Topic-CSVs enthält
## --- ZIEL: (targetfolder_1) = Ordner, der CSV-Datei enthält, in der für jedes MALLET-Modell die Werte einer Kfold-Cross-Val-Klassification nach Parteien stehen ##

## --- INPUT: (targetfolder_1)
## --- ZIEL:  Mittelwerte aller Kfold-Werte (Klassification) jedes MALLET-Modells ##

###PARAMS: -----------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\ALL_MODELS\MODELS_2000_w\fertige_CSV_COMPS"
targetfolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\ALL_MODELS\MODELS_2000_w\comparison_scores"

###FUNCTIONS: --------------------------------------------------------------------------------------------------------------------------
def create_file_list(sourcefolder_1):                                    #list alle csv-dateien
    os.chdir(sourcefolder_1)
    file_list = os.listdir(sourcefolder_1)      
    return file_list

def csv_to_dataframe(path, item):
    csv_file_path = os.path.join(path, item)
    data_frame = pd.read_csv(csv_file_path, encoding = "ISO-8859-1")   
    return data_frame

def get_Xy_from_dataframe(data_frame):
    X = data_frame.iloc[:, :-1]                                      #enthält alle rows, aber ohne die letzte column (die ist das label "speaker", auf dem trainiert wird)
    #OCCURING label-realisations (die vorher ausgelassene speaker-column):
    y = data_frame.iloc[:, -1]                                       #enthält alle rows, aber NUR die letzte column (label "speaker")
    return X, y                                                      #X.shape = (119868, num_topics), y.shape = (119868, )
    
def write_scores_to_csv(kfold_classif_scores, targetfolder_1, file_name):
    #transfer to list-type, convert values:
    value_list = []
    for elem in kfold_classif_scores:
        value_list.append(float(elem))   
    #file_name is used to label the model:
    model_name = file_name.replace("compheader.csv", "")
    value_list.append(model_name)
    #change dir to targetfolder_1:
    os.chdir(targetfolder_1)
    #create row from value-list, append to global csv for all models:
    with open("comparison_tmodels_SVM.csv", "a", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(value_list)

def get_csv(targetfolder_1, item):
    file_path = os.path.join(targetfolder_1, item)
    csv_file = open(file_path, "r")
    return csv_file

def get_line_float_list(line):
    line_list = line.split(",")
    #label(model_name) auf letzter zeilen-position entfernen:           
    model_name = line_list[-1] 
    line_list = line_list[:-1]
    float_list = []
    for item in line_list:
        float_list.append(float(item))
    return model_name, float_list
    
def get_mean_from_model(float_list):
    score_sum = 0.0
    for item in float_list:
        score_sum = score_sum + item
    score_mean = score_sum / len(float_list)
    return score_mean

###MAIN: -------------------------------------------------------------------------------------------------------------------------------
def main_part_1(sourcefolder_1, targetfolder_1):
    file_list = create_file_list(sourcefolder_1)
    for item in file_list:                                                #csv!
        fitola_df = csv_to_dataframe(sourcefolder_1, item)                #fitola = file, topic, label
        #datenreihe u. vorkommende labels erhalten:
        X, y = get_Xy_from_dataframe(fitola_df)      
        #create classifier:
        clf = LinearSVC()
        #SVC() was too slow, other possib:
        #get list of k scores from kfold cross validation classification:
        scorer = skm.make_scorer(skm.f1_score, average = "weighted")
        kfold_classif_scores = cross_val_score(clf, X, y, scoring=scorer, cv = 14)        #(classifier-model, data, labels, number k of folds for cross validation)
        #write this list to a global comparison csv of all models:
        write_scores_to_csv(kfold_classif_scores, targetfolder_1, item)                   #item is needed as the model name

def main_part_2(targetfolder_1):
    file_list = create_file_list(targetfolder_1)
    model_dict = {}
    for item in file_list:
        csv_file = get_csv(targetfolder_1, item)
        for line in csv_file:
            model_name, line_float_list = get_line_float_list(line)
            mean = get_mean_from_model(line_float_list)
            #append model_name and mean to dictionary:
            pair = {model_name : mean}
            model_dict.update(pair)
    #modell + seinen mittelwert zeigen:       
    for pair in model_dictionary.items():
    print(pair)        

###RUN: --------------------------------------------------------------------------------------------------------------------------------
main_part_1(sourcefolder_1, targetfolder_1)
main_part_2(targetfolder_1)





























