#!/usr/bin/python3

def split_doc(file_name):
    word_dict[][str:int]
    i = 0
    j = 0
    nb_paragraphe = 0
    
    for line in open(file_name).readlines():
        # print('line ' + str(i) +': ' +line)
        i += 1
        j = 0
        for word in line.split(' '):
            if word[:2] == '.I':
                nb_paragraphe += 1
                # print( 'No.' + str(nb_paragraphe) + ' paragraphe')                
                continue
            if len(word) == 0:
                continue
            if word[-1] == ',' or word[-1] == '.':
                word = word[:-1]
            word = word.lower()            
            # print('No.' + str(j) + 'word: ' + word)
            word_dict[i][word] = word_dict[i][word] + 1            
            j += 1
        if i >= 20:
            break
    return word_dict
        


splitted_dict = split_doc('./dataFiles/CISI.ALLnettoye')
