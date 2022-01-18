import csv
import os
import re

## --- INPUT: (all_doc_topic_files) = Ordner, der von verschiedenen MALLET-Modellen die Comp-Textdateien (output-doc-topics) enthält
## --- ZIEL:  Jede Datei (output-doc-topics) jedes MALLET-Modells zu je einer CSV-Datei konvertieren (CSV enthält pro Zeile einen Dok-Pfad, dessen Werte pro Topic, die Partei, das Jahr) ##

###PARAMS: --------------------------------------------------------------------------------------------------------------
all_doc_topic_files = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\ALL_MODELS\MODELS_2000_w\all_comps"
targetfolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\ALL_MODELS\MODELS_2000_w"

###FUNCTIONS: -----------------------------------------------------------------------------------------------------------
def create_file_list(all_doc_topic_files):                      #list alle comp-dateien
    os.chdir(all_doc_topic_files)
    file_list = os.listdir(all_doc_topic_files)      
    return file_list

def get_labels(doc_path):
    #get speaker:
    label_s = re.search("DOKS_2000/(.+)/final", doc_path)       #suchbegriff passt nur auf bestimmte dok-namen, muss sonst angepasst werden!
    #print("get_name_and_label, label = ", label)
    label_s = label_s.group(1)
    #get year:
    label_y = re.search("(\d{4})_\d{1,3}\.txt", doc_path)       #suchbegriff passt nur auf bestimmte dok-namen, muss sonst angepasst werden!
    label_y = label_y.group(1)
    return label_s, label_y                 

def get_list_of_line(line):
    #zeile in separate werte splitten:
    split_list = line.split()
    #pfad von entspr. datei erhalten:
    doc_path = split_list[1]
    #partei, jahr rausfiltern:
    label_s, label_y = get_labels(doc_path) 
    #neue liste:
    end_list = []
    #exclude pos 1+2, convert text-numbers to float:
    for elem in split_list[2:]:
        conv = float(elem)
        end_list.append(conv)    
    #partei, jahr anhängen:
    end_list.append(label_s)                                    #aufbau end_list: -- topics 1 to n, name of file, label "speaker", label "year" --
    end_list.append(label_y)
    return end_list

def create_header(item):                                     
    num_topics = re.search("[0-9]{2,3}", item)                  #zieht aus titel der txt-file die anzahl der topics
    num_topics = int(num_topics.group(0))
    count = 0
    header =[]
    while count < num_topics:
        header_field = "top_" + str(count)
        header.append(header_field)
        count += 1
    #add label:
    header.append("speaker")
    header.append("year")         
    return header

def write_comp_to_csv(targetfolder_1, item, super_list):
    #überschrift erstellen:
    header = create_header(item)
    #change dir zu zielordner:
    os.chdir(targetfolder_1)
    #dateinamen erstellen:
    csv_title = item + "header_speakeryear.csv"        
    csv_title = csv_title.replace(".txt", "")
    #csv schreiben:
    with open(csv_title, "a", newline = '') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(super_list)
    csv_file.close()
    
###MAIN: ----------------------------------------------------------------------------------------------------------------
def main(all_doc_topic_files, targetfolder_1):
    file_list = create_file_list(all_doc_topic_files)
    #walk through files:
    for item in file_list:
        #create list for all line_lists in file:
        super_list = []
        #create file_path:
        file_path = os.path.join(all_doc_topic_files, item)
        #visit:
        file = open(file_path, "r", encoding = "utf-8") 
        #walk through lines:
        for line in file:
            line_list = get_list_of_line(line)
            #append to SUPER_list:
            super_list.append(line_list)
        #create csv:
        write_comp_to_csv(targetfolder_1, item, super_list)
        #close file:
        file.close()

###RUN: -----------------------------------------------------------------------------------------------------------------
main(all_doc_topic_files, targetfolder_1)













