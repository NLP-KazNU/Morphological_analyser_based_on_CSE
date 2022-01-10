import re
import os
import xlrd, xlwt

def stemming_with_lexicon(text_fn, affixes_fn, stopwords_fn, stems_fn):
    def splitting_by_words(text):
        result = re.findall(r'\w+', text)
        return result

    def sorting_affixes(file_name):
        affixes_wb = xlrd.open_workbook(affixes_file_name)
        affixes_sh = affixes_wb.sheet_by_index(0)
        affixes = []
        for rownum in range(affixes_sh.nrows-1):
            affix = affixes_sh.cell(rownum+1,0).value
            if '\ufeff' in affix:
                affix = affix.replace('\ufeff', '')
            affixes.append(affix)

        sorted_affixes = sorted(affixes, key=len, reverse=True)

        return sorted_affixes

    def stem(word, affixeslst, sfile_name):

# добавить with

        stop_stem_file = open(sfile_name, 'r', encoding="utf-8")
        stop_stem_file = stop_stem_file.read()
        stop_stems = splitting_by_words(stop_stem_file)
        
        word_len = len(word)
        min_len_of_word = 2
        stems = []
        affixes = []
        

        if word_len > min_len_of_word:
            n = word_len - min_len_of_word

            if word.lower() in stop_stems:
                stems.append(word)
                affixes.append("")

            else:
                is_found = False
                for i in range(n+1, 0, -1):
                    if is_found:
                        break
                    word_affix = word[word_len - (i-1):]
                    stem = word[:word_len-len(word_affix)]
                    lastletter = stem[-1]
                
                    for affix in affixeslst:
                        if is_found:
                            break
                        if word_affix == affix:
                            if stem.lower() in stop_stems:
                                if lastletter == 'г':
                                    stem = stem[0:-1] + 'к'
                                elif lastletter == 'б':
                                    stem = stem[0:-1] + 'п'
                                elif lastletter == 'ғ':
                                    stem = stem[0:-1] + 'қ'
                                stems.append(stem)
                                affixes.append(word_affix)
                                is_found = True
                            else:
                                break
                    if word_affix == '':
                        if stem.lower() in stop_stems:
                            stems.append(word)
                            affixes.append(word_affix)
                        else:
                            for j in range(n+1, 0, -1):
                                word_affix = word[word_len - (j-1):]
                                stem = word[:word_len-len(word_affix)]
                                lastletter = stem[-1]
                                for affix in affixes:
                                    if word_affix == affix:
                                        if lastletter == 'г':
                                            stem = stem[0:-1] + 'к'
                                        elif lastletter == 'б':
                                            stem = stem[0:-1] + 'п'
                                        elif lastletter == 'ғ':
                                            stem = stem[0:-1] + 'қ'
                                        stems.append(stem)
                                        affixes.append(word_affix)
                                if word_affix == '':
                                    stems.append(word)
                                    affixes.append('')
        else:
            word_affix=""
            stems.append(word)
            affixes.append(word_affix)
                            
        return stems[0], affixes[0]
        

    def stemming(tfile_name, affixes, stopwords_file_name, sfile_name):
        text_file = open(tfile_name, 'r', encoding="utf-8")
        text_file = text_file.read()

        with open(stopwords_file_name, "r", encoding="utf-8") as f:
            stopwords_file = f.readlines()
        stop_words = []
        for stop_word in stopwords_file:
            if "\n" in stop_word:
                stop_word = stop_word.replace("\n", "")
            stop_words.append(stop_word)
        #print(stop_words)
            
        text = splitting_by_words(text_file)
        res_text = []

        rim_cifry = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx', 'xxi']

        for word in text:
            if word not in res_text:
                if word.isnumeric() or word.lower() in rim_cifry:
                    continue
                res_text.append(word)
        #print(res_text)
        
        result_words  = [word for word in res_text if word.lower() not in stop_words]
        #print(result_words)
        
        stem_text = {}
        for word in result_words:
            stemm, affixx = stem(word, affixes, sfile_name)
            stem_text.update({word: [stemm, affixx]})
        #print(stem_text)

        for i in stem_text.keys():
            word = str(i)
            stemm = str(stem_text[i])
            value_list = stem_text[word]
            stemm = value_list[0]
            affixx = value_list[1]
            #print(word, stemm, affixx)

            #for j in range(len(text_file)):
                #print(text_file[j])
            if word in text_file:
                if word == stemm+affixx:
                    if affixx != "":
                        text_file = re.sub((rf"\b{word}\b"), rf"{stemm}~{affixx}", text_file)
                    else:
                        text_file = re.sub((rf"\b{word}\b"), stemm, text_file)
                else:
                    break
        
        #print(text_file)
        #print(stem_text)    
        return text_file

  
    affixes = sorting_affixes(affixes_fn)
    #print(affixes)

    stem_text = stemming(text_fn, affixes, stopwords_fn, stems_fn)
    #print("\n")
    #print(text)
            
    output_file_name = "text_after_stemming.txt"
    output_file = open(output_file_name, 'w', encoding="utf-8")
    output_file.write(stem_text)
    output_file.close()

    #print("The results of the stemming process are written to a file " + output_file_name + " and saved in the folder where this python file is located")
    return stem_text


###-----------------------------------------------------------------###
    
def segmentation(text, affixes_fn):
    text_fseg = re.findall(r'\w+\~\w+', text)
    #print(text_fseg)
    
    seg_affixes = {}
    for word in text_fseg:
        stem = re.findall(r'\w+\~', word)
        stem = str(stem).replace('~', '')
        affix = re.findall(r'\~\w+', word)
        affix = str(affix).replace('~', '')
        #print(str(stem) + '--' + str(affix))

        affixes_wb = xlrd.open_workbook(affixes_fn)
        affixes_sh = affixes_wb.sheet_by_index(0)
        for roww in range(affixes_sh.nrows-1):
            if affix == rf"['{affixes_sh.cell_value(roww+1, 0)}']":
                affix0 = affixes_sh.cell_value(roww+1, 0)
                affix1 = affixes_sh.cell_value(roww+1, 1)
                seg_affixes.update({affix0: affix1})

    #print(seg_affixes)
    
    seg_text = text.replace('~', '+ ')
    #print(seg_text)
    
    for i in seg_affixes.keys():
        affix0 = str(i)
        affix1 = str(seg_affixes[i])
        if affix0 in text:
            seg_text = re.sub((rf"\b{affix0}\b"), affix1, seg_text)
    #print(seg_text)
        
    output_file_name1 = "text_after_morph_analysis.txt"
    output_file1 = open(output_file_name1, 'w', encoding="utf-8")
    output_file1.write(seg_text)
    output_file1.close()

    print("The results of the morphological analysis process are written to a file " + output_file_name1 + " and saved in the folder where this python file is located")
    return seg_text



#******************** main ********************#

text_file_name = "text.txt" #or # input("Name of the text file: ") #"text.txt"
affixes_file_name = "affixes.xls" #or # input("Name of the affix file: ") #"affixes.xls"
stopwords_file_name = "stop_words.txt" #or # input("Name of the stop-words file: ") #"stop_words.txt"
stems_file_name = "truestems.txt" #or #input("Name of the vocabulary of correct stems: ") #"truestems.txt"

### 1-st process "Stemming"
text = stemming_with_lexicon(text_file_name, affixes_file_name, stopwords_file_name, stems_file_name)
#print("\nText after Stemming:\n" + text)

### 2-nd process "Segmentation or Morph analyze"
result_text = segmentation(text, affixes_file_name)
#print("\nText after Morph_analysis:\n" + result_text)

