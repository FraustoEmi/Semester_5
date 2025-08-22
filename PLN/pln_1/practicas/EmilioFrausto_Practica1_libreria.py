#Emilio Frausto

import nltk 
#nltk.download()

from nltk.book import *

#ntlk.data.path

print(len(set(text1))) #palabras unicas en este libro
print(len(text1))      #todas las palabras que tiene
print(text1[-20])      #la 20° ultima palabra del libro

print(text1.concordance('monstrous'))
