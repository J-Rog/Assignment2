import pandas as pd
import numpy as np
import re
from datetime import datetime

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

#Now I have every word mapped to a unique index
x = np.array(list(word_count.keys()))

#Create a blank transition table
transition = np.zeros((len(x),len(x)))

print("Begin raw transition table " + str(transition.shape))

startTime = datetime.now()

#Populate the transition table with raw counts
for i in range(1,len(lineOlines)):

    current_index = np.where(x == lineOlines[i])[0][0]

    past_index = np.where(x == lineOlines[i-1])[0][0]

    transition[current_index][past_index] += 1

print("End raw transition table " + str(datetime.now() - startTime))

choice = 0
while(True):
    print("1: Generate New Text")
    print("2: Text Prediction")
    print("3: Exit")
    choice = int(input("Please Select an option: "))

    if choice == 1:
        print("Choice 1")
        break
    if choice == 2:
        print("Choice 2")
        break
    if choice == 3:
        print("Choice 3")
        break
