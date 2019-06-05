#!/usr/bin/python3
import json
import operator
import spacy
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from processor.Paragraph import Paragraph

MAX_OUTPUT = 135
MAX_FEATURES = 10000
MAX_DF = 0.95

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

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


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
        # qry[q].generate_vect_uniform()

    vec_json_file = open("../results/inv_vector.json", "r")
    tfidf_vect = json.loads(vec_json_file.read())
    vec_json_file.close()
    output_file = open("../results/result.REL", "w+")

    cv = CountVectorizer(max_df=MAX_DF, max_features=MAX_FEATURES)
    word_count_vector = cv.fit_transform(docs)
    # print(word_count_vector.shape)
    keyword_list = list(cv.vocabulary_.keys())
    # print("\n\nKeywords:", len(keyword_list), "\n", keyword_list)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    # print(tfidf_transformer.idf_)
    tf_idf_vector = tfidf_transformer.transform(cv.transform(docs))

    for i in range(len(docs)):
        coo_items = sort_coo(tf_idf_vector[i].tocoo())
        keywords = extract_topn_from_vector(cv.get_feature_names(), coo_items, 200)
        # print("====Paragraph ", str(i), "====")
        qry[i + 1].generate_vect(keywords)

    res_dict = {}
    for qry_idx in range(1, len(qry) + 1):
    # for qry_idx in range(5, 6):
        qurey = qry[qry_idx]
        # print("\n\n\nFiltered query: ", qry_idx, " ", qurey.filtered)
        # print("Query vector: ", qurey.qry_vect)
        for kwd in qurey.qry_vect.keys():
            if kwd in tfidf_vect.keys():
                # print("\n\n\nKeyword: ", kwd, " score: ", qurey.qry_vect[kwd])
                # print("tfidf vector: ", str(tfidf_vect[kwd]))
                for doc_num, doc_score in tfidf_vect[kwd]:
                    # print("Doc num: ", str(doc_num), " doc score: ", str(doc_score))
                    if doc_num in res_dict:
                        # print("Adding to doc ", str(doc_num))
                        res_dict[doc_num] += qurey.qry_vect[kwd] * doc_score
                    else:
                        # print("Create new doc ", str(doc_num))
                        res_dict[doc_num] = qurey.qry_vect[kwd] * doc_score
                    # print("Res_dict: ", str(res_dict), "\n\n")

        sorted_res_dict = sorted(res_dict.items(), key=operator.itemgetter(1), reverse=True)
        # print("Query", qry_idx, "\n", sorted_res_dict, "\n\n\n\n")
        ctr = 0
        stop_list = [4, 6, 16, 17, 23, 25, 26, 29]
        for doc_freq_tuple in sorted_res_dict:
            max_freq = doc_freq_tuple[1]
            break
        for doc_freq_tuple in sorted_res_dict:
            if ctr < MAX_OUTPUT and qry_idx not in stop_list: # and doc_freq_tuple[1] > 0.05 and doc_freq_tuple[1] > 0.05 * max_freq:
                str_to_write = str(qry_idx) + " " + str(doc_freq_tuple[0]) + " " + str(doc_freq_tuple[1]) + "\n"
                output_file.write(str_to_write)
                ctr += 1
            else:
                break
    output_file.close()





