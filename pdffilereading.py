# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:31:28 2023

@author: Prakash
"""

from PyPDF2 import PdfReader

# open the PDF file
with open("example_1.pdf", "rb") as file:
    # create a PdfFileReader object
    pdf = PdfReader(file)

    # iterate through all the pages
    for page in range(len(pdf.pages)):
        # extract the text from the page
        text = pdf.pages[page].extract_text()

        # print the text
        print(text)
        

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# tokenize the text
text = "This is an example sentence. It contains words to tokenize."
tokens = word_tokenize(text)

# stem the tokens
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(token) for token in tokens]

# remove stop words
stop_words = set(stopwords.words("english"))
filtered_tokens = [token for token in stemmed_tokens if token not in stop_words]

# print the filtered tokens
print(filtered_tokens)