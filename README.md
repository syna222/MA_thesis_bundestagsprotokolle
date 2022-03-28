# MA_Thesis

Dieses Repository beinhaltet die Skripte zu folgendem Teil meiner Master-Thesis:

Die in rudimentärem XML ausgezeichneten Bundestagsprotokolle der Jahre 1949-2017 wurden zunächst heruntergeladen und kurz analysiert (Längen. Parteien etc.).

Mittels eigens erstelltem XML-Schema und regulären Ausdrücken wurden alle vorliegenden Protokolle mit Markup versehen, sodass jedes Protokoll hinterher mit einer XML-Auszeichnung nach Datum, Inhaltsteilen, Sprecherbeiträgen samt Sprechername, Funktion/Partei existiert und somit semantisch durchsuchbar ist.

Die ausgezeichneten Protokolle wurden darauffolgend in verschiedene Unterkorpora sortiert (Parteien und Jahre) und mittels NLP-Verfahren (Natural Language Processing) weiterverarbeitet.

Anschließend wurden Methoden des Topic Modelings und der Word Embeddings genutzt, um einen automatisierten Überblick über Themen der Parteien und Wahlperioden zu erlangen sowie einen Einblick in mögliche politische Positionierungen.



![alt text](https://github.com/syna222/MA_Thesis/blob/main/1_Grafik_Preprocessing_Steps.png?raw=true)

![alt text](https://github.com/syna222/MA_Thesis/blob/main/2_Grafik_Modelling_Process.png?raw=true)
