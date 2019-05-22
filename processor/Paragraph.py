#!/usr/bin/python3
import spacy
nlp = spacy.load("en_core_web_sm")

class Paragraph:
    def __init__(self, text: str):
        self.title, self.body = Paragraph.process_text(text)
        self.model = None
        self.filtered = ""
        self.qry_vect = {}

    @staticmethod
    def process_text(text):
        lines = text.split("\n")
        # lines = [line.strip for line in full_lines]
        title = lines[0]
        body = lines[1:]
        for line in body:
            line = line.strip()
        body = " ".join(body)
        return title, body

    def generate_model(self):
        self.model = nlp(self.body)

    def filter_stop_words(self):
        # stop_words = spacy.lang.en.stop_words.STOP_WORDS
        filtered_sent = []
        for word in self.model:
            if (not word.is_stop) and (not word.is_space) and (not word.is_punct):
                filtered_sent.append(word.lemma_.lower().strip())
        self.filtered = " ".join(filtered_sent)
        # bow_vector = CountVectorizer(tokenizer = spacy_tokenizer, ngram_range=(1,1))   bag of words

    def generate_vect(self):
        words = self.filtered.split(" ")
        print("Filtered: ", self.filtered)
        # max_freq = -1
        for word in words:
            if word in self.qry_vect.keys():
                self.qry_vect[word] += 1
                # if self.qry_vect[word] > max_freq:
                #     max_freq = self.qry_vect[word]
            else:
                self.qry_vect[word] = 1
        # for vec in self.qry_vect.keys():
        #     self.qry_vect[vec] = self.qry_vect[vec] / max_freq
        print(self.qry_vect)
