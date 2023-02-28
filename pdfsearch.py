# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 12:15:30 2023

@author: Prakash
"""

import pytesseract

from pdf2image import convert_from_path

# convert pdf to image
images = convert_from_path('example.pdf', 500, poppler_path=r'C:\Program Files\poppler-0.68.0\bin')

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
# extract text from image
text = []
for image in images:
    text.append(pytesseract.image_to_string(image))

# print the text
print(text)