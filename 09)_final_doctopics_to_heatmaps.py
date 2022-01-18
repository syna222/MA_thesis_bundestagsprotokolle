import adjustText as aT
import csv
import copy
import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as shc
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA

## --- INPUT: (speakeryear_file_path) = CSV-Datei eines MALLET-Modells (CSV enthält pro Zeile einen Dok-Pfad, dessen Werte pro Topic, die Partei, das Jahr), erstellt durch "08a)_mallet_doctopics_to_CSV.py"
## --- ZIEL:  DataFrames, die Mittelwert für jedes Topic in jeder Untergruppe (Parteien oder Wahlperioden) anzeigen,
## ---        seaborn-Heatmaps(herausragendste Topics für Parteien oder Wahlperiode),
## ---        Partei-Ranking für Topics u. Wahlperioden-Ranking für Topics

##PARAMS: ----------------------------------------------------------------------------------------------------------------------------
speakeryear_file_path = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\ALL_MODELS\MODELS_2000_w\cleaned_100_5000_2000_compheader_speakeryear.csv"

##FUNCTIONS: -------------------------------------------------------------------------------------------------------------------------
#erstellt df das jede partei mit ihren mittelwerten für jedes topic zeigt:
def create_speaker_mean_df(speakeryear_file_path):
    tm_df = pd.read_csv(speakeryear_file_path, encoding="ISO-8859-1")        
    #eliminate label-column "year":
    tm_df= tm_df.drop(columns="year")    
    #umbenennung der label-werte vor grouping:
    tm_df["speaker"].replace({"Alterspräsident":"AlterspräsidentIn", "Alterspräsidentin": "AlterspräsidentIn", "Bundeskanzler":"BundeskanzlerIn", "Bundeskanzlerin":"BundeskanzlerIn", "CDU":"CDUCSU", "CSU":"CDUCSU", "PDS":"PDSLinkeListe", "Präsident":"PräsidentIn", "Präsidentin":"PräsidentIn", "Vizepräsident":"VizepräsidentIn", "Vizepräsidentin":"VizepräsidentIn"}, inplace=True)
    ##DataFrameGroupBy-Object
    group_obj = tm_df.groupby("speaker")                                     #"speaker" ist column-name
    #find mean val of all groups (in all columns):
    mean_df = group_obj.mean()
    return mean_df

#erstellt df das jede wahlperiode mit ihren mittelwerten für jedes topic zeigt:
def create_year_mean_df(speakeryear_file_path): 
    tm_df = pd.read_csv(speakeryear_file_path, encoding="ISO-8859-1")
    #label-column "speaker" löschen:
    tm_df= tm_df.drop(columns="speaker")
    #umbenennung der label-werte vor grouping:
    tm_df["year"].replace({1949: "01", 1950:"01", 1951:"01", 1952:"01", 1953:"01", 1954:"02", 1955:"02", 1956:"02", 1957:"02", 1958:"03", 1959:"03", 1960:"03",
                                             1961:"03", 1962: "04", 1963:"04", 1964: "04", 1965:"04", 1966: "05", 1967:"05", 1968: "05", 1969:"05", 1970: "06", 1971:"06", 1972: "06",
                                             1973:"07", 1974:"07", 1975:"07", 1976:"07", 1977:"08", 1978:"08", 1979:"08", 1980:"08", 1981:"09", 1982:"09", 1983:"09", 1984:"10",
                                             1985:"10", 1986:"10", 1987:"11", 1988:"11", 1989:"11", 1990:"11", 1991:"12", 1992:"12", 1993:"12", 1994:"12", 1995:"13",
                                             1996: "13", 1997:"13", 1998:"13", 1999:"14", 2000:"14", 2001:"14", 2002:"14", 2003:"15", 2004:"15", 2005:"15", 2006:"16",
                                             2007: "16", 2008:"16", 2009:"16", 2010:"17", 2011:"17", 2012:"17", 2013:"17", 2014:"18", 2015:"18", 2016:"18", 2017:"18"}, inplace=True)
    ##DataFrameGroupBy-Object
    group_obj = tm_df.groupby("year")
    #mittelwert jeder untergruppe finden (in allen columns):
    mean_df = group_obj.mean()
    mean_df = mean_df.rename_axis("election term", axis="index")
    return mean_df

def create_speaker_year_mean_df(speakeryear_file_path):
    tm_df = pd.read_csv(speakeryear_file_path, encoding="ISO-8859-1")   
    #umbenennung der label-werte vor grouping:
    tm_df["speaker"].replace({"Alterspräsident":"AlterspräsidentIn", "Alterspräsidentin": "AlterspräsidentIn", "Bundeskanzler":"BundeskanzlerIn", "Bundeskanzlerin":"BundeskanzlerIn", "CDU":"CDUCSU", "CSU":"CDUCSU", "PDS":"PDSLinkeListe", "Präsident":"PräsidentIn", "Präsidentin":"PräsidentIn", "Vizepräsident":"VizepräsidentIn", "Vizepräsidentin":"VizepräsidentIn"}, inplace=True)
    tm_df["year"].replace({1949: "01", 1950:"01", 1951:"01", 1952:"01", 1953:"01", 1954:"02", 1955:"02", 1956:"02", 1957:"02", 1958:"03", 1959:"03", 1960:"03",
                                             1961:"03", 1962: "04", 1963:"04", 1964: "04", 1965:"04", 1966: "05", 1967:"05", 1968: "05", 1969:"05", 1970: "06", 1971:"06", 1972: "06",
                                             1973:"07", 1974:"07", 1975:"07", 1976:"07", 1977:"08", 1978:"08", 1979:"08", 1980:"08", 1981:"09", 1982:"09", 1983:"09", 1984:"10",
                                             1985:"10", 1986:"10", 1987:"11", 1988:"11", 1989:"11", 1990:"11", 1991:"12", 1992:"12", 1993:"12", 1994:"12", 1995:"13",
                                             1996: "13", 1997:"13", 1998:"13", 1999:"14", 2000:"14", 2001:"14", 2002:"14", 2003:"15", 2004:"15", 2005:"15", 2006:"16",
                                             2007: "16", 2008:"16", 2009:"16", 2010:"17", 2011:"17", 2012:"17", 2013:"17", 2014:"18", 2015:"18", 2016:"18", 2017:"18"}, inplace=True)  
    #DataFrameGroupBy-Object
    group_obj = tm_df.groupby(["speaker","year"])            #turn around?? originally: ["speaker", "year"]
    #mittelwert jeder untergruppe finden (in allen columns):
    speaker_year_mean_df = group_obj.mean()
    return speaker_year_mean_df   

def df_to_mean_normalized_df(original_df, mean_series, norm_filename):
    column_labels = original_df.columns.values
    #kopie von speaker_mean_df erstellen:                                #niemals kopieren mit new = old! Change of new will also change old (CALL-BY-OBJECT-REFERENCE IN PYTHON)!
    norm_df = copy.deepcopy(original_df)
    #norm_df (zu anfang noch gleich wie original) wird durchlaufen, einzelne werte werden durch subtraktion des mittelwertes für das jew. topic erneuert:
    for i in range(len(column_labels)):                                  #damit gleichzeitig column_labels und mean_series durchlaufen werden (haben selbe länge)
        for index_label, row_series in norm_df.iterrows():
            norm_df.at[index_label, column_labels[i]] = row_series[column_labels[i]] - mean_series[i] 
    #save normalized df to csv-file:
    norm_df.to_csv(norm_filename)
    return column_labels, norm_df

def df_to_heatmap(norm_df, xlabels, ylabels):                            #xlabels, ylabels müssen = numpy.ndarray
    sns.set(font_scale=0.4)
    heat_map = sns.heatmap(norm_df, xticklabels = xlabels, yticklabels = ylabels, linewidths=0.5, linecolor="black")      
    plt.show()

def df_to_topic_ranking(norm_df, csv_name):
    #topics als ndarray erhalten:
    topics = norm_df.columns.values
    topic_2D = []    
    for i in topics:
        topic_df = norm_df[[i]]
        #sortieren:
        topic_df = topic_df.sort_values(i, ascending=False)
        #2darray erstellen aus allen topic_df.index.values:
        topic_2D.append(list(topic_df.index.values))
    #aus topic_2D u. topics --> neuer df --> csv:
    ranking_df = pd.DataFrame(topic_2D, index=topics)
    ranking_df.to_csv(csv_name)
    ranking_transposed_df = ranking_df.transpose()
    return ranking_transposed_df

def make_dendrogram(norm_df):
    plt.figure(figsize=(10, 7))  
    plt.title("Dendrograms")  
    dend = shc.dendrogram(shc.linkage(norm_df, method='ward'))
    plt.show()
    
def cluster_speaker_topic_deviation(norm_speaker_mean_df, num_clusters):
    cluster = AgglomerativeClustering(n_clusters=num_clusters, affinity='euclidean', linkage='ward')
    norm_speaker_mean_df["clusters"] = cluster.fit_predict(norm_speaker_mean_df)                     #row ["clusters"] hinzufügen
    #PCA für dimensionsreduktion:
    reduced_data = PCA(n_components=2).fit_transform(norm_speaker_mean_df)                           
    results_df = pd.DataFrame(reduced_data, columns=["pca1","pca2"])
    plot_1 = sns.scatterplot(x="pca1", y="pca2", data=results_df)          
    plt.title("Clustering with 2 dimensions")
    #speaker labels hinzufügen für datenpunkte:
    texts = [plt.text(results_df.pca1[line]+0.2, results_df.pca2[line], norm_speaker_mean_df.index.values[line], horizontalalignment='right', size='medium', color='black', weight='semibold') for line in range(0,norm_speaker_mean_df.shape[0])]
    #speaker labels anpassen:
    aT.adjust_text(texts)
    plt.show()
    
##MAIN: ------------------------------------------------------------------------------------------------------------------------------
def main_method(speakeryear_file_path):
    #df für parteien (pro partei deren 100 topic-mittelwerte):
    speaker_mean_df = create_speaker_mean_df(speakeryear_file_path)
    #df für jahre (pro wahlperiode deren 100 topic-mittelwerte):
    year_mean_df = create_year_mean_df(speakeryear_file_path)
    #df für wahlperioden innerhalb d. parteien:
    speaker_period_mean_df = create_speaker_year_mean_df(speakeryear_file_path)

    #gesamt-mittelwerte für jedes topic:
    #mw für jedes topic über alle parteien:
    mean_topics_speaker_means = speaker_mean_df.mean(axis=0)    #für mean normalization der parteien
    #mw für jedes topic über alle wahlperioden:                     
    mean_topics_year_means = year_mean_df.mean(axis=0)          #für mean normalization der wahlperioden

    #parteien-werte normalisieren durch topic-mittelwerte:
    speaker_filename = "norm_cleaned_100_5000_2000_speakermean.csv"
    column_labels_1, norm_speaker_mean_df = df_to_mean_normalized_df(speaker_mean_df, mean_topics_speaker_means, speaker_filename)

    #wahlperioden-werte normalisieren durch topic-mittelwerte:
    year_filename = "norm_cleaned_100_5000_2000_yearmean.csv"
    column_labels_2, norm_year_mean_df = df_to_mean_normalized_df(year_mean_df, mean_topics_year_means, year_filename)

    ##wahlperioden-werte innerhalb d. parteien normalisieren:
    speaker_period_filename = "norm_cleaned_100_5000_2000_speakerperiodmean.csv"
    column_labels_3, norm_speakerperiod_mean_df = df_to_mean_normalized_df(speaker_period_mean_df, mean_topics_year_means, speaker_period_filename)

    #labels + heatmap erstellen:
    speaker_labels = speaker_mean_df.index.values
    year_labels = year_mean_df.index.values
    speakerperiod_labels = norm_speakerperiod_mean_df.index.values    

    #für parteien:
    df_to_heatmap(norm_speaker_mean_df, column_labels_1, speaker_labels)
    #für wahlperioden:
    df_to_heatmap(norm_year_mean_df, column_labels_2, year_labels)
    #für speaker in wahlperioden:
    df_to_heatmap(norm_speakerperiod_mean_df, column_labels_3, speakerperiod_labels)

    #ranking erstellen für topic-party u. topic-years:
    ranking_speakers = df_to_topic_ranking(norm_speaker_mean_df, "topic_party_ranking.csv")
    ranking_years = df_to_topic_ranking(norm_year_mean_df, "topic_year_ranking.csv")

    #konvertieren --> absolute-value-dataframe:
    norm_speaker_mean_abs = norm_speaker_mean_df.abs()
    #für jede partei summe der standardabweichungs-beträge:  
    speaker_standev_sum = norm_speaker_mean_abs.sum(axis=1)
    #ranking:
    speaker_standev_sum = speaker_standev_sum.sort_values(ascending=False)

    #dendrogramm --> cluster anzahl ermitteln:
    make_dendrogram(norm_speaker_mean_df)
    #clustern:
    cluster_speaker_topic_deviation(norm_speaker_mean_df, 2)

##RUN: -------------------------------------------------------------------------------------------------------------------------------
main_method(speakeryear_file_path)






