# Search Engine NLP

This project's objective is to build a text search engine. The implementation is evaluated on a provided dataset. A subset of 30 queries is provided in order to tune the system. The entire system is then evaluated using the entire dataset.

## Provided data
1. CISI.ALLnettoye is a collection of about 1460 books and papers descriptions ;
2. CISI.QRY is a set of 30 queries related to that collection ;
3. CISI.REL contains the relevance judgements for the documents w.r.t. the queries.

A tool that aims to evaluate your search engine performances — eval.pl
Documents are separated from their neighbours in the collection with a special marker ; they all have a personal number, and are composed of a title and an abstract. A sample is given and explicited below.

```
.I 1
18 Editions of the Dewey Decimal Classifications
The present study is a history of the DEWEY Decimal
Classification. The first edition of the DDC was published
in 1876, the eighteenth edition in 1971, and future editions
will continue to appear as needed. In spite of the DDC’s
long and healthy life, however, its full story has never
been told. There have been biographies of Dewey
that briefly describe his system, but this is the first
attempt to provide a detailed history of the work that
more than any other has spurred the growth of
librarianship in this country and abroad.
.I 2
Use Made of Technical Libraries
This report is an analysis of 6300 acts of use
in 104 technical libraries in the United Kingdom.
Library use is only one aspect of the wider pattern of
information use. Information transfer in libraries is
restricted to the use of documents. It takes no
account of documents used outside the library, still
less of information transferred orally from person
to person. The library acts as a channel in only a
proportion of the situations in which information is
transferred.
Taking technical information transfer as a whole,
there is no doubt that this proportion is not the
major one. There are users of technical information
```

## Step 1 : collection indexing
For each document, identified by its .I field, the indexing of both title and abstract is produced through:
1. a tokenization : this treatment isolates words within the sequences of letters and symbols in the document. During this process, you choose what vocabulary you want to keep and do the associate processing (stemming, use of stopword list, etc..) ;
2. a choice of indexing terms : elaborate a policy to choose the indexing terms among all the dis- tinct words or stems (all the terms, only the most frequent ones, only the most discriminative ones, etc.). This choice mostly relies on a count of occurrences ;
3. define a weighting strategy for terms in the documents (e.g. TF.IDF) ;
4. the production of a representation vector for each document (a list of the weighted indexing
terms). Note that this item has to be considered together with the following one ;
5. the production of inverted files for your system, for efficiency reasons. Thus an inverted file, corresponding to the structure indexing term → list of couples (document containing this term, weight), has to be produced from the above representation.

## Step 2 : build the search engine
1. query indexing : to index the queries, use the same methodology and the same weighting schemes as for documents.
2. implementation of a search engine to answer the queries : a similarity measure between the indexing vectors of the queries and the documents has to be chosen and implemented. The expected output is a ranked list of documents calculated by the system in response to a given query.

## Step 3 : evaluation
The performance of your IR system has to be evaluated, a script to do the evaluation is provided. This script output the next measures for each separated query as well as the overall result :

* Precision : the percentage of relevant documents among the ones provided by your system : ability to provide relevant documents ;
* Recall : percentage of relevant document provided by your system w.r.t. to the list expected in the database : ability to retrieve all the relevant documents ;
* F1 : a mix of the two previous measures ;
* Precision@1 : is the first ranked document relevant ? ;
* Precision@5 : percentage of relevant documents among the five first ranked documents.

## Reference links / sources 
* natural language toolkit
* okapi bm25
         
Stop words: https://medium.com/@makcedward/nlp-pipeline-stop-words-part-5-d6770df8a936
Stemming: https://stackabuse.com/python-for-nlp-tokenization-stemming-and-lemmatization-with-spacy-library/

https://www.dataquest.io/blog/tutorial-text-classification-in-python-using-spacy/

https://nlpforhackers.io/complete-guide-to-spacy/

http://dsgeek.com/2018/02/19/tfidf_vectors.html

https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

https://spacy.io/api/tokenizer#_title

http://kavita-ganesan.com/extracting-keywords-from-text-tfidf/#.XNLSsS-B29Y

http://kavita-ganesan.com/tfidftransformer-tfidfvectorizer-usage-differences/#.XNLgUi-B29a

https://nlp.stanford.edu/IR-book/html/htmledition/inverse-document-frequency-1.html


http://blog.christianperone.com/2013/09/machine-learning-cosine-similarity-for-vector-space-models-part-iii/


## Result of the 1st paragraph from the entire corpus

```
Index: 2472 Score:  0.40788527272875663
Index: 2025 Score:  0.35386917177255645
Index: 2224 Score:  0.31174397713890434
Index: 3358 Score:  0.23727335871537572
Index: 3304 Score:  0.20686207018952035
Index: 2493 Score:  0.20686207018952035
Index: 6546 Score:  0.18797992989306214
Index: 1055 Score:  0.18797992989306214
Index: 6625 Score:  0.18190123844002745
Index: 86 Score:  0.18190123844002745
Index: 386 Score:  0.17693458588627822
Index: 6535 Score:  0.16909778959660393
Index: 6901 Score:  0.16588924187949433
Index: 2052 Score:  0.15385320068927616
Index: 144 Score:  0.1340151317784521
Index: 1151 Score:  0.1288923689397833
Index: 4121 Score:  0.12525481755065282
Index: 2191 Score:  0.12265845672394918
Index: 1902 Score:  0.12086168449945872
Index: 4113 Score:  0.12028816499690359
Index: 1802 Score:  0.11917612609761814
Index: 4184 Score:  0.11810770797653576
Index: 3240 Score:  0.1120290165235011
Index: 717 Score:  0.10637267725419462
Index: 3104 Score:  0.10286311906920802
Index: 5620 Score:  0.1014060247004454
Index: 1438 Score:  0.10029398580115993
Index: 865 Score:  0.09443410010414155
Index: 4643 Score:  0.07610678896976798
Index: 7561 Score:  0.07577253728950867
Index: 5597 Score:  0.07511609178633374
Index: 2162 Score:  0.07313593839024955
Index: 5419 Score:  0.07027584860172299
Index: 6663 Score:  0.06671760198524603
Index: 6830 Score:  0.056945821569986885
```

## ===Keywords===
```edition 0.408
ddc 0.354
dewey 0.312
history 0.237
healthy 0.207
eighteenth 0.207
spur 0.188
biography 0.188
story 0.182
1876 0.182
abroad 0.177
spite 0.169
tell 0.166
decimal 0.154
1971 0.134
briefly 0.129
life 0.125
detailed 0.123
country 0.121
librarianship 0.12
continue 0.119
long 0.118
growth 0.112
appear 0.106
future 0.103
publish 0.101
classification 0.1
attempt 0.094
need 0.076
work 0.076
provide 0.075
describe 0.073
present 0.07
study 0.067
system 0.057```
