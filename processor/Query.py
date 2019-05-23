#!/usr/bin/python3
import collections
import json
import operator

import spacy
import re
from processor.Paragraph import Paragraph

MAX_FEATURES = 10000

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
    nlp = spacy.load("en_core_web_sm")
    qry = split_doc('../corpus/CISI_dev.QRY')
    docs = []
    for q in qry:
        qry[q].generate_model()
        qry[q].filter_stop_words()
        docs.append(qry[q].filtered)
        # print("\n\n\nBody:" + qry[q].body)
        # print("Filtered: ", qry[q].filtered, "\n\n\n")
        qry[q].generate_vect()

    qry_idx = 5
    tfidf_vect = json.loads(open("../results/results.json", "r").read())
    res_dict = {}
    qurey = qry[qry_idx]
    for kwd in qurey.qry_vect.keys():
        if kwd in tfidf_vect.keys():
            for doc_num, doc_score in tfidf_vect[kwd]:
                if doc_num in res_dict.keys():
                    res_dict[doc_num] += qurey.qry_vect[kwd] * doc_score
                else:
                    res_dict[doc_num] = qurey.qry_vect[kwd] * doc_score

    sorted_x = sorted(res_dict.items(), key=operator.itemgetter(1))
    sorted_dict = collections.OrderedDict(sorted_x)
    print(sorted_dict.keys())
    # qurey.qry_vect    tfidf_vect

    # for keyword in qurey.qry_vect.keys():
    #     if keyword in tfidf_vect.keys():
    #         pass


