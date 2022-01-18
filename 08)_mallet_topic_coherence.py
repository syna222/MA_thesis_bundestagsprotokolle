import csv
import os
import xml.etree.ElementTree as ET

## --- INPUT: (model_diagn_path) = Ordner, der für jedes MALLET-Modell eine XML-Diagnose-Datei enthält (diagnostics-file)
## --- ZIEL:  (csv-file) avg word length, coherence, specificity und exclusivity-Werte (für die topics) jedes MALLET-modells erhalten ##

###PARAMS: --------------------------------------------------------------------------------------------------------------------------------
model_diagn_path = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\ALL_MODELS\diag"

###FUNCTIONS: -----------------------------------------------------------------------------------------------------------------------------
def get_model_avg_wordlength(root):
    wlen_list = []
    counter = 0
    for elem in root.iter():
        if elem.tag == "topic":
            counter += 1
            wlen_val = float(elem.attrib.get("word-length"))
            wlen_list.append(wlen_val)
    wlen_sum = 0
    for item in wlen_list:
        wlen_sum = wlen_sum + item
    wlen_mean = wlen_sum /counter
    return wlen_mean

def get_avg_topic_length(root):                             #num tokens
    toke_len_list = []
    counter = 0
    for elem in root.iter():
        if elem.tag == "topic":
            counter += 1
            toke_val = float(elem.attrib.get("tokens"))
            toke_len_list.append(toke_val)
    toke_sum = 0
    for item in toke_len_list:
        toke_sum = toke_sum + item
    toke_mean = toke_sum /counter
    return toke_mean

def get_model_coherence(root):                              #coh_vals werden nicht normalisiert durch anzahl wörter in entspr. topics
    coh_list = []
    counter = 0
    for elem in root.iter():
        if elem.tag == "topic":
            counter += 1
            coh_val = float(elem.attrib.get("coherence"))
            coh_list.append(coh_val)        
    coh_sum = 0
    for item in coh_list:
        coh_sum = coh_sum + item
    coh_mean = coh_sum / counter
    return coh_mean

def get_model_specificity(root):
    spec_list = []
    counter = 0
    for elem in root.iter():
        if elem.tag == "topic":
            counter += 1
            spec_val = float(elem.attrib.get("uniform_dist"))
            spec_list.append(spec_val)
    spec_sum = 0
    for item in spec_list:
        spec_sum = spec_sum + item
    spec_mean = spec_sum / counter
    return spec_mean

def get_model_exclusivity(root):
    exclu_list = []
    counter = 0
    for elem in root.iter():
        if elem.tag == "topic":
            counter += 1
            exclu_val = float(elem.attrib.get("exclusivity"))
            exclu_list.append(exclu_val)
    exclu_sum = 0
    for item in exclu_list:
        exclu_sum = exclu_sum + item
    exclu_mean = exclu_sum / counter
    return exclu_mean

def get_model_entropy(root):
    entro_list = []
    counter = 0
    for elem in root.iter():
        if elem.tag == "topic":
            counter += 1
            entro_val = float(elem.attrib.get("document_entropy"))
            entro_list.append(entro_val)
    entro_sum = 0
    for item in entro_list:
        entro_sum = entro_sum + item
    entro_mean = entro_sum / counter
    return entro_mean

###MAIN: ----------------------------------------------------------------------------------------------------------------------------------
def main_methode(model_diagn_path):
    #create overall-csv with header as list:
    header = ["MODEL/FILE-NAME", "avg topic avg wordlength", "topic token avg", "topic coherence mean", "topic specific. mean", "topic exclus. mean", "topic entropy mean"]
    csv_title = "comparison_MODEL_metrics.csv"
    with open(csv_title, "a", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)                                 
        folder_list = os.listdir(model_diagn_path)
        for folder in folder_list:
            folder_path = os.path.join(model_diagn_path, folder)
            file_list = os.listdir(folder_path)
            for item in file_list:
                #create file_path:
                file_path = os.path.join(folder_path, item)
                #create doc-tree:
                my_tree = ET.parse(file_path)
                #determine doc-root:
                root = my_tree.getroot()
                #get doc-tm-values:
                avg_wordlength_mean = get_model_avg_wordlength(root)  #the higher the better
                toke_mean = get_avg_topic_length(root)            
                coherence_mean = get_model_coherence(root)          
                specificity_mean = get_model_specificity(root)
                exclusivity_mean = get_model_exclusivity(root)
                entropy_mean = get_model_entropy(root)
                #ITEM == MODEL NAME
                # write item, and values as a line to overall-csv: 
                #create list for row:
                row_list = [item, avg_wordlength_mean, toke_mean, coherence_mean, specificity_mean, exclusivity_mean, entropy_mean]
                writer.writerow(row_list)
                print(row_list)

###RUN: -----------------------------------------------------------------------------------------------------------------------------------
main_methode(model_diagn_path)













