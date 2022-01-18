import csv
import gzip
import matplotlib.pyplot as plt
import os
import pandas as pd
import pyLDAvis
import shutil
import sklearn.preprocessing
from wordcloud import WordCloud
#CODE zum größten Teil hierher: https://jeriwieringa.com/2018/07/17/pyLDAviz-and-Mallet/ (übersetzt, angepasst)

## --- INPUT: (state_file_path) = Datei-Pfad zu MALLET-Modell-Datei (.gz)
## --- ZIEL:  einzelne DataFrames, sodass passend für pyLDA-Visualisierung (speichern der Vis. funktioniert nicht)

## --- INPUT: (topic_groups_csv) = CSV-Datei, die Themenbereiche + ihren Anteil am Modell enthält
## --- ZIEL:  Bar-Chart für Topic-Übergruppen erstellen aus CSV (muss manuell gespeichert werden)

###PARAMS: ----------------------------------------------------------------------------------------------------
state_file_path = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\ALL_MODELS\MODELS_2000_w\_2000\cleaned_100_5000_2000_state.gz"                                
topic_groups_csv = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\8_TM_Themenkomplexe.csv"

###FUNCTIONS: -------------------------------------------------------------------------------------------------
#zieht alpha- u. betawerte aus modell-datei (state_file) --> tuple (alphawert-liste, beta)
def extract_params(state_file_path):
    with gzip.open(state_file_path, "r") as state:                                    #.readlines() --> line_list
        params = [x.decode("utf8").strip() for x in state.readlines()[1:3]]           #params = ['#alpha : 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5', '#beta : 0.01']
        print(type(params))
        print(params)
    return (list(params[0].split(":")[1].split(" ")), float(params[1].split(":")[1]))

#modell-datei (state-file) in df konvertieren, modell-datei ist tab-separated, die ersten zwei zeilen enthalten alpha u. beta hyperparams
def state_to_df(state_file_path):
    df = pd.read_csv(state_file_path, compression="gzip", sep=" ", skiprows=[1,2])
    return df                                                                         #df= topic zuweisung für jedes wort in jedem dok des modells

#konvertiert df zu matrix:
def pivot_and_smooth(df, smooth_value, rows_variable, cols_variable, values_variable):
    # args:
        #df (dataframe): aggregated dataframe 
        #smooth_value (float): value to add to the matrix to account for the priors
        #rows_variable (str): name of dataframe column to use as the rows in the matrix
        #cols_variable (str): name of dataframe column to use as the columns in the matrix
        #values_variable(str): name of the dataframe column to use as the values in the matrix
    matrix = df.pivot(index=rows_variable, columns=cols_variable, values=values_variable).fillna(value=0)
    matrix = matrix.values + smooth_value
    normed = sklearn.preprocessing.normalize(matrix, norm='l1', axis=1)
    return pd.DataFrame(normed)                                                       #df: pandas matrix normalisiert auf Reihen                                                       

def topicgroups_to_barchart(csv_file):
    tgroup_df = pd.read_csv(csv_file, header=0, encoding="utf-8")
    #erste column als indexe nutzen, column entfernen:
    indexes = list(tgroup_df["Themenkomplex"])
    tgroup_df = tgroup_df.drop(columns=["Themenkomplex"])
    tgroup_df.index = indexes    
    #bar chart erstellen:
    tgroup_df.plot.barh()
    plt.yticks(fontsize=13)
    plt.xticks(fontsize=13)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

###MAIN: ------------------------------------------------------------------------------------------------------
def main_method(state_file_path, topic_groups_csv):
    #alpha- u. betawerte erhalten:
    params = extract_params(state_file_path)
    #auspacken:
    alpha = [float(x) for x in params[0][1:]]
    beta = params[1]
    #print(alpha, beta)

    #modell in df konvertieren (jedes wort in jedem dok gelistet, lauter wort-mehrfachnennungen):
    df = state_to_df(state_file_path)
    df["type"] = df.type.astype(str)                                                             #zur Sicherheit, damit kein -nan- in "type"-column
    #print(df[:10])

    #dok-längen erhalten:
    docs = df.groupby("#doc")["type"].count().reset_index(name="doc_length")                     #[row-indexes = numbers, COLUMNS: "#doc (num"), "doc_lenght"]
    #print(docs[:10])

    #wörter + ihre häufigkeiten erhalten :
    vocab = df["type"].value_counts().reset_index()                                              #[row-indexes = doc nums, COLUMNS: "type", "term_freq"]
    vocab.columns = ["type", "term_freq"]
    vocab = vocab.sort_values(by="type", ascending=True)
    #print(vocab[:10])

    #pro topic alle seine wörter + die häufigkeiten der wörter im topic:
    phi_df = df.groupby(["topic", "type"])["type"].count().reset_index(name ="token_count")      #zählt wie oft jedes wort in jedem topic vorkommt
    phi_df = phi_df.sort_values(by="type", ascending=True)
    #print(phi_df[:10])                                                                          #[row-indexes = doc nums, COLUMNS: "topic", "type", "token_count"]

    #pro topic alle wörter - topic-term-matrix (transponiert, werte durch beta geglättet, nicht mehr aggregiert, keine wörter mehr, nur ids):
    phi = pivot_and_smooth(phi_df, beta, "topic", "type", "token_count")                         #[]
    #print(phi[:10])                                                                              

    #pro dok alle topics mit jew. worthäufigkeiten im dok:
    theta_df = df.groupby(["#doc", "topic"])["topic"].count().reset_index(name ="topic_count")   
    #print(theta_df[:10])

    #pro dok alle seine topics mit norm. worthäufigk. im dok - doc-topic-matrix (transponiert, werte durch alpha geglättet, nur noch ids sichtbar):
    theta = pivot_and_smooth(theta_df, alpha, "#doc", "topic", "topic_count")
    #print(theta[:10])

    #alle daten an pyLDAvis übergeben:
    data = {'topic_term_dists': phi, 
            'doc_topic_dists': theta,
            'doc_lengths': list(docs['doc_length']),
            'vocab': list(vocab['type']),
            'term_frequency': list(vocab['term_freq'])
           }
    vis_data = pyLDAvis.prepare(**data, sort_topics=False)
    pyLDAvis.show(vis_data)                                      #wenn nicht funktioniert: pyLDAvis.display(vis_data)
    pyLDAvis.save_html(vis_data, 'cleaned_100_5000_2000.html')  #funktioniert leider nicht!

    #Anteile d. Topic-Übergruppen (Topic-Werte zsgerechnet aus pyLDA-Visualisierung) als bar chart:
    topicgroups_to_barchart(topic_groups_csv)

###RUN: -------------------------------------------------------------------------------------------------------
main_method(state_file_path, topic_groups_csv)



