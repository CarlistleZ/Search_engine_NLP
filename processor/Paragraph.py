#!/usr/bin/python3


class Paragraph:
    def __init__(self, text: str):
        self.title, self.body = Paragraph.process_text(text)

    @staticmethod
    def process_text(text):
        lines = text.split("\n")
        title = lines[0]
        body = lines[1:]
        return title, body

    def get_text(self):
        return " ".join(self.body)