#!/usr/bin/python3
import spacy
import re
import os
from Paragraph import Paragraph

def split_doc(file_name):
    word_dict = {}
    paragraph_to_append = 1
    for line in open(file_name).readlines():
        x = re.search("^\.I\s\d+$", line)
        if x:
            p_num = int(line[3:])
            word_dict[p_num] = ''
            paragraph_to_append = p_num
        else:
            word_dict[paragraph_to_append] += line
    for num in word_dict:
        word_dict[num] = Paragraph(word_dict[num])
    return word_dict
        

if __name__ == '__main__':
    paragraphs = split_doc('./CISI_small.ALLnettoye')
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        os.system('python -m spacy download en_core_web_sm')
        nlp = spacy.load("en_core_web_sm")
    # stop_words = spacy.lang.en.stop_words.STOP_WORDS
    # for word in stop_words:
    #     print(word)
    # stop_words.add('fml')
    for p in paragraphs:
        paragraphs[p] = nlp(paragraphs[p].get_text())
        res = paragraphs[p]
        print('*************** Paragraph ' + str(p) + ' ***************')
        for token in paragraphs[p]:
            if token.is_stop:
                print(token.text + ' STOP')
            else:
                print(token.text + '\t-> pos:' + token.pos_ + '\tdep:' + token.dep_ + '\thead: ' +
                      token.head.text + '\tlem: ' + token.lemma_)



# Stop words: https://medium.com/@makcedward/nlp-pipeline-stop-words-part-5-d6770df8a936
# Stemming: https://stackabuse.com/python-for-nlp-tokenization-stemming-and-lemmatization-with-spacy-library/