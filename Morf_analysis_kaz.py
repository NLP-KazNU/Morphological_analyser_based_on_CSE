import re
import os
import pandas as pd

with open("text1.txt",  encoding="utf-8") as f:
    tmp_text_lines = f.readlines()

with open("stop-words_32601", "r", encoding="utf-8") as f:
    tmp_stoplines = f.readlines()

endings = pd.read_excel("Endings.xlsx", header=None, names=['endings','endings_morph'])

endingsnew = list()
endingsnew_probel = list()

for i, row in endings.iterrows():
    endingsnew.append(row['endings'])
    endingsnew_probel.append(row['endings_morph'])

new_words = []
stoplines = []
for i in tmp_stoplines:
    if "\n" in i:
        i = i.replace("\n", "")
    stoplines.append(i)
j = 0

new_text_lines = ""

for line in tmp_text_lines:
    tmp_words = ""
    words = line.split()
    for word in words:
        j = 0
        found_in_stoplines = False
        for z in range(len(word), 1, -1):
            tubir=word[0:z]
            affix=word[z:]
            if tubir.lower() in stoplines:
                found_in_stoplines = True
                if affix in endingsnew:
                    index = endingsnew.index(affix)
                    affix = endingsnew_probel[index]
                    tmp_words += tubir + " + " + affix
                    new_text_lines += tmp_words
                    tmp_words = " "
                    j += 1
                else:
                    tmp_words += tubir + affix + " "
                    new_text_lines += tmp_words
                    tmp_words = " "
                    j += 1
                break
        if word == '.':
            new_text_lines += " ."
    new_text_lines += "\n"

output_lines = new_text_lines.split('\n')

with open("output.txt", "w", encoding="utf-8") as f:
    for line in new_text_lines:
        f.write('%s'%line)
f.close()
