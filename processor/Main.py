#!/usr/bin/python3
import spacy
import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from processor.Paragraph import Paragraph
from collections import Counter

MAX_FEATURES = 10000
MAX_DF = 0.85

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
    paragraphs = split_doc('../corpus/CISI_small.ALLnettoye')
    docs = []
    for p in paragraphs:
        # print('\n\n*************** Paragraph ' + str(p) + ' ***************')
        paragraphs[p].generate_model()
        paragraphs[p].filter_stop_words()
        docs.append(paragraphs[p].filtered)
        paragraphs[p].generate_freq()
        # print(paragraphs[p].filtered)

    cv = CountVectorizer(max_df=MAX_DF, max_features=MAX_FEATURES)
    word_count_vector = cv.fit_transform(docs)
    # print(word_count_vector.shape)
    keyword_list = list(cv.vocabulary_.keys())
    # print("\n\nKeywords:", len(keyword_list), "\n", keyword_list)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    # print(tfidf_transformer.idf_)
    tf_idf_vector = tfidf_transformer.transform(cv.transform(docs))

    keyword_dict = {}
    for i in range(len(docs)):
        coo_items = sort_coo(tf_idf_vector[i].tocoo())
        keywords = extract_topn_from_vector(cv.get_feature_names(), coo_items, 200)
        # print("====Paragraph ", str(i), "====")
        print(keywords, "\n\n")
        for k in keywords:
            if k in paragraphs[i + 1].qry_vect:
                tf_coeff = paragraphs[i + 1].qry_vect[k]
            else:
                tf_coeff = 1
            p = (i + 1, keywords[k]) #* tf_coeff)
            # print("p= ", p, "k= ", k, " ", keywords[k])
            if k in keyword_dict.keys():
                keyword_dict[k].append(p)
            else:
                keyword_dict[k] = [p]

    # for key in keyword_dict:
    #     print(key, " : ", keyword_dict[key])

    idf_dict_str = json.dumps(keyword_dict)
    # print(idf_dict_str)

    my_file = open('../results/inv_vector_small.json', 'w')
    my_file.write(idf_dict_str)
    my_file.close()
