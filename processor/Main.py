#!/usr/bin/python3
import spacy
import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from processor.Paragraph import Paragraph

MAX_FEATURES = 500

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

if __name__ == '__main__':
    nlp = spacy.load("en_core_web_sm")
    paragraphs = split_doc('../corpus/CISI_small.ALLnettoye')
    docs = []
    for p in paragraphs:
        # print('\n\n*************** Paragraph ' + str(p) + ' ***************')
        paragraphs[p].generate_model()
        paragraphs[p].filter_stop_words()
        docs.append(paragraphs[p].filtered)
        # print(paragraphs[p].filtered)

    cv = CountVectorizer(max_df=0.85, max_features=MAX_FEATURES)
    word_count_vector = cv.fit_transform(docs)
    # print(word_count_vector)
    keyword_list = list(cv.vocabulary_.keys())
    # print("\n\nKeywords:", len(keyword_list), "\n", keyword_list)

    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    tf_idf_vector = tfidf_transformer.transform(cv.transform([docs[1]]))

    coo_items = sort_coo(tf_idf_vector.tocoo())
    for idx, score in coo_items:
        print('Index: ' + str(idx) + ' Score: ', str(score))

    idx_dict = {}
    idx_dict[0] = ['']

    for keyword in keyword_list:
        exist_paragraphs = []
        for p in paragraphs:
            if keyword in paragraphs[p].body:
                exist_paragraphs.append(p)
        idx_dict[keyword] = exist_paragraphs
        # print("Keyword: ", keyword, " \t\tin paragraphs: ", exist_paragraphs)


    json_string = json.dumps(idx_dict)
    # print(json_string)
    with open('../results/data.json', 'w') as outfile:
        json.dump(json_string, outfile)


