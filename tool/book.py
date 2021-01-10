"""
text book checker book object file
@author: tang142857
Copyright(c) DFSA Software Develop Center
"""
import os
import re


class Book(object):
    """Book object for Editor to edit book file."""
    def __init__(self):
        self.data = {'info': {}, 'body': []}
        # Initialize book object finish.

    def __str__(self):
        """Override the str function to pretty print."""
        string = self.data['info']
        return 'INFO:' + str(string)

    def addInfo(self, infoName, newInformation):
        self.data['info'][infoName] = newInformation

    def addChapter(self, chapter: str):
        self.data['body'].append(chapter)

    def getChapter(self, chapterIndex: int):
        return self.data['body'][chapterIndex]

    def getInfo(self, informationName):
        return self.data['info'][informationName]


def __textDecoder(path: str, book: Book):
    """pass path to load file,save the content into book"""
    with open(path, 'r', encoding='utf-8') as files:
        strBook = files.read()
    # Load the book's text end

    print('Normal book, without and format.')
    chapterSpliter = re.compile(r'第<\d*>章')  # Split the chapter with re.
    results = chapterSpliter.split(strBook)
    # Text manage end.

    book.addInfo('name', results[0])
    del results[0]  # Delete the first part of the book(may be it is its description)
    for chapterText in results:
        book.addChapter(chapterText)
    return book


def decodeBook(path: str):
    data = Book()  # Create book
    extendName = path.split('.')[-1]  # Get the file's extend name.
    if extendName == 'ftb':
        pass  # TODO ftb file decoder
    elif extendName == 'txt':
        __textDecoder(path, data)  # using text decoder to decode the book
    return data


if __name__ == "__main__":
    book=decodeBook('E:/PY/TextbookChecker/resource/test_book.txt')
    print(book)