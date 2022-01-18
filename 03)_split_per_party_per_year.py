import os
import re
import shutil
import xml.etree.ElementTree as ET

## --- INPUT: (sourcefolder_1) = Ordner, der alle 18 Wahlperioden-Ordner mit ihren getaggten XML-Dateien enthält
## --- ZIEL:  (targetfolder_1) = Ordner, der für jede Partei einen Ordner mit Jahres-Textdateien enthält (in den Dateien die jew. Speeches d. Partei d. Jahres) ##

###PARAMS: ------------------------------------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = "C:\\Users\\vck\\Documents\\000MA Studium\\MA Thesis\\AAAtestordner\\3tagged\\ausgelagert"
targetfolder_1 = "C:\\Users\\vck\\Documents\\000MA Studium\\MA Thesis\\AAAtestordner\\3tagged\\txt_per_PARTY_per_year"

###FUNCTIONS: ---------------------------------------------------------------------------------------------------------------------------------------------------
def create_wplist(needed_dir):                       #list alle wp-ordner
    os.chdir(needed_dir)
    wp_list = os.listdir(needed_dir)      
    return wp_list

def create_filelist(wp_list, needed_dir, wp):
    wp_path = os.path.join(needed_dir, wp)
    file_list = os.listdir(wp_path)
    return wp_path, file_list                        #callable w/ -->   my_var1, my_var2 = create_filelist(x_1, x_2)

def get_treeroot(file_path):
    file_tree = ET.parse(file_path)
    root = file_tree.getroot()
    return root   

def get_txt_filename(elem):
    #rausgenommen: DEUTSCHE ZENTRUMSPARTEI, ZENTRUM, BÜNDNIS 90, LINKSPARTEI.PDS --> in entsprech. parteinamen konvertiert
    party_list = ["Alterspräsident", "Alterspräsidentin", "BP", "Bundeskanzler", "Bundeskanzlerin", "BÜNDNIS 90/DIE GRÜNEN", "BÜNDNIS 90/GRÜNE", "CDU", "CSU", "CDU/CSU", "DIE GRÜNEN", "DIE LINKE", "DP", "DRP", "FDP", "fraktionslos", "FU", "FVP", "GB/BHE", "GRÜNE", "KPD", "NR", "NS", "parteilos", "PDS", "PDS/Linke Liste", "Präsident", "Präsidentin", "SPD", "SSW", "Vizepräsident", "Vizepräsidentin", "WAV", "Z"]
    txt_filename = ""
    file_check = True
    for party in party_list:
        party_val = elem.attrib.get("PARTY")         #elem.attrib = dict #partei aus speech-tag
        year = elem.attrib.get("DATE")[6:10]         #jahreszahl
        if party_val == party:
            party = party.replace("/", "")           #sonderzeichen aus parteinamen killen (für ordnernamen)
            party = party.replace(".", "")
            party_year = party + "_" + year
            txt_filename = party_year + ".txt"       
            break                                    #damit party value stehenbleibt
    #ERROR test:
    if txt_filename == "":
        file_check = False
    return party, txt_filename, file_check

def get_txt_path(elem):
    #file_check zum checken, ob party-eintrag existiert!
    party, txt_filename, file_check = get_txt_filename(elem)
    #ERROR test:
    if file_check == False:
        raise Exception("Partei gibt es nicht")
    #pfad von parteiordner erhalten:
    subfolder_path = os.path.join(targetfolder_1, party)         #subfolder im Vorhinein erstellt!
    txt_filepath = os.path.join(subfolder_path, txt_filename)
    return txt_filepath
    
def write_txt(elem, txt_filepath):
    txt_file = open(txt_filepath, "a", encoding="utf-8")
    txt_file.write(elem.text)
    #text nach child-elementen von speech bekommen (sonst nur bis zu erstem child-elem):
    for child in elem:
        txt_file.write(child.tail)
    txt_file.write("\n")
    txt_file.close()

###MAIN: --------------------------------------------------------------------------------------------------------------------------------------------------------
def main_method(sourcefolder_1, targetfolder_1):
    wp_list = create_wplist(sourcefolder_1)
    error_liste = []
    for wp in wp_list:
        #liste aller files pro Wahlp.:
        wp_path, file_list = create_filelist(wp_list, sourcefolder_1, wp)
        #für jede file in jedem wp-ordner:
        for item in file_list:
            file_path = os.path.join(wp_path, item)            
            try:
                #file einlesen mit ET, root erhalten:
                root = get_treeroot(file_path)
            except Exception as message:
                print("Exception occured!", message, " with item: ", item)                              
            #durch tree-root (durch jedes speech-elem) laufen:
            for elem in root.iter():
                if elem.tag == "SPEECH":
                    #checken von welcher partei u. dafür entspr. txt.file-path erhalten (ordner im vorfeld erstellt)                    
                    try:           
                        txt_filepath = get_txt_path(elem)
                    except Exception as message:
                        print("Exception occurs!", message)
                        error_liste.append(item)                       
                    #checken, ob file für partei u. jahr schon existiert:
                    if os.path.isfile(txt_filepath) == False:
                        #create new file:        
                        new_file = open(txt_filepath, "w", encoding="utf-8")  
                        new_file.close()
                    #so oder so hiernach:
                    write_txt(elem, txt_filepath)                 
                
###RUN: ---------------------------------------------------------------------------------------------------------------------------------------------------------       
main_method(sourcefolder_1, targetfolder_1)                        
                        
        
        
        
        
        
        
        
        
        