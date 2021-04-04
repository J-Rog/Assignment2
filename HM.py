import pandas as pd
import numpy as np
import re

#Open the file
raw_corpus = pd.read_csv('Shakespeare_data.csv')

#Isolate the lines and convert them into a numpy array.
lines = raw_corpus['PlayerLine'].to_numpy()

lineOlines = []

for i in range(0,len(lines)):
    #Remove all punctuation and uppercase letters
    lines[i] = re.sub(r'[^\w\s]', '', lines[i]).lower()
    #Turn each sententce into a list
    target = lines[i].split()

    #Create a 1d array of all lines
    for j in target:
        lineOlines.append(j)

word_count = {}

#Gets each word count and a 1d object of every word
for i in lineOlines:
    if i in word_count:
        word_count[i] = word_count[i] + 1
    else:
        word_count[i]=1

x = np.array(word_count.keys())
