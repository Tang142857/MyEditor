"""
text book checker debug file
@author: tang142857
Copyright(c) DFSA Software Develop Center
"""
from time import time
import re


def timer(fun):
    def reFunction(*args, **kwargs):
        startTime = time()
        print('Running...')
        fun(*args, **kwargs)
        print(f'Down used {time()-startTime}seconds')

    return reFunction


def makeBookName(Paths: str):
    """Make the formated book name."""
    baseFileName = re.split(r'[\\/]', Paths)[-1]  # To get the file name.
    fileExtendName = '.' + re.split(r'\.', baseFileName)[-1]  # To get the extend name.
    newFileName = '$' + baseFileName.replace(fileExtendName, '$' + fileExtendName)
    return Paths.replace(baseFileName, newFileName)


def normalDecoder(path: str):
    with open(path, 'r', encoding='utf-8') as files:
        strBook = files.read()
    # Load the book's text end

    print('Normal book, without and format.')
    book = Book()  # Initialize the book object.
    chapterSpliter = re.compile(r'第<\d*>章')  # Split the chapter with re.
    r = chapterSpliter.split(strBook)
    # Text manage end.

    book.addInfo('name', r[0])
    del r[0]
    for chapterText in r:
        book.addChapter(chapterText)
    return book


class Book(object):
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


if __name__ == "__main__":
    print(makeBookName('D:/calibre_factions/DFSA/Threebody (8)/Threebody - DFSA.txt'))
    b = Book()
    b.addChapter('hello world 1')
    b.addChapter('hello world 2')
    b.addInfo('author', 'tang142857')
    print(b)
    b = normalDecoder('E:/PY/TextbookChecker/resource/test_book.txt')
    input()