import os

## --- INPUT: (sourcefolder_1) = Ordner, der für jede Partei einen Ordner mit Jahres-Textdateien enthält (nur Lemmata von Verben/Nomen/Adjektiven - ohne NE, Stoppwörter und Hapax Legomena entfernt)
## --- ZIEL: (targetfolder_1) = Ordner, der für jede Partei einen Ordner mit Textdateien enthält (jede Textdatei hat ca. 2000 Lemmata, ist der Partei, dem Jahr + einer Nummer zugeordnet --> meist mehrere Dateien pro Partei + Jahr) ##

###PARAMS: -------------------------------------------------------------------------------------------------------------------------------------------------
sourcefolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\3tagged\4_PARTY_YEAR_txts"
targetfolder_1 = r"C:\Users\vck\Documents\000MA_Studium\MA_Thesis\AAAtestordner\3tagged\000_aufgeteilte_DOKS_2000"

###FUNCTIONS: ----------------------------------------------------------------------------------------------------------------------------------------------
def create_speakerlist(sourcefolder_1):                         #list alle sprecher-ordner
    os.chdir(needed_dir)
    speaker_list = os.listdir(needed_dir)                       
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

###MAIN: ---------------------------------------------------------------------------------------------------------------------------------------------------
def main_method(sourcefolder_1, targetfolder_1):
    speaker_list = create_speakerlist(sourcefolder_1)
    for speaker in speaker_list:
        speaker_path, file_list = create_filelist(sourcefolder_1, speaker)
        for item in file_list:
            file_data = read_file(speaker_path, item)
            #aus jeder datei liste aller lemmata machen:
            split_list = file_data.split()
            #counter-vars initialisieren:
            counter = 0
            number_file = 0
            #new doc - durch splitlist laufen bis pos erreicht ist:
            #create first file for initial split_list input:
            path_new_file = os.path.join(targetfolder_1, speaker, item[:len(item)-4] + "_" + str(number_file) + ".txt")   #also bspw. C:\....\SPD\finalSPD_1949_0.txt
            new_file = open(path_new_file, "a+", encoding="utf-8")
            new_file.seek(0)
            for elem in split_list:
                #if pos is reached, create new file:
                if counter > 1998:                 
                    number_file += 1
                    new_file_path = os.path.join(targetfolder_1, speaker, item[:len(item)-4] + "_" + str(number_file) + ".txt")
                    new_file = open(new_file_path, "a+", encoding="utf-8")
                    new_file.seek(0)
                    new_file.write(elem)          #andere new_file als in "else:"!
                    new_file.write("\n")
                    counter = 0
                #ansonsten weiter in initiale datei schreiben:
                else:
                    new_file.write(elem)          
                    new_file.write("\n")
                counter += 1

###RUN: ----------------------------------------------------------------------------------------------------------------------------------------------------
main_method(sourcefolder_1, targetfolder_1)








