#!/usr/bin/python3
import json
import operator
import spacy
import re
from processor.Paragraph import Paragraph

MAX_OUTPUT = 150

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

    vec_json_file = open("../results/inv_vector.json", "r")
    tfidf_vect = json.loads(vec_json_file.read())
    vec_json_file.close()
    output_file = open("../results/result.REL", "w+")
    res_dict = {}
    for qry_idx in range(1, len(qry) + 1):
    # for qry_idx in range(5, 6):
        qurey = qry[qry_idx]
        # print("\n\n\nFiltered query: ", qry_idx, " ", qurey.filtered)
        # print("Query vector: ", qurey.qry_vect)
        for kwd in qurey.qry_vect.keys():
            if kwd in tfidf_vect.keys():
                print("\n\n\nKeyword: ", kwd)
                # print("tfidf vector: ", str(tfidf_vect[kwd]))
                for doc_num, doc_score in tfidf_vect[kwd]:
                    # print("Doc num: ", str(doc_num), " doc score: ", str(doc_score))
                    if doc_num in res_dict:
                        print("Adding to doc ", str(doc_num))
                        res_dict[doc_num] += qurey.qry_vect[kwd] * doc_score
                    else:
                        res_dict[doc_num] = qurey.qry_vect[kwd] * doc_score

        sorted_res_dict = sorted(res_dict.items(), key=operator.itemgetter(1), reverse=True)
        # print("Query", qry_idx, "\n", sorted_res_dict, "\n\n\n\n")
        ctr = 0
        for doc_freq_tuple in sorted_res_dict:
            if ctr < MAX_OUTPUT:
                str_to_write = str(qry_idx) + " " + str(doc_freq_tuple[0]) + " " + str(doc_freq_tuple[1]) + "\n"
                output_file.write(str_to_write)
                ctr += 1
            else:
                break
    output_file.close()





