import pandas as pd
import numpy as np
import re
from datetime import datetime
import random

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

    #Create a 1d list of all lines
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

#Create a blank transition table of size 27381 x 27381
transition = np.zeros((len(x),len(x)))

print("Transition shape is " + str(np.shape(transition)))

startTime = datetime.now()

print("Begin raw transition table " + str(startTime))

#Populate the transition table with raw counts
for i in range(1,len(lineOlines)):

    current_index = np.where(x == lineOlines[i])[0][0]

    past_index = np.where(x == lineOlines[i-1])[0][0]

    transition[past_index][current_index] += 1

print("End raw transition table " + str(datetime.now() - startTime))


#Convert raw data into probabilities
startTime = datetime.now()
print("Begin probability table " + str(startTime))

for i in range(0,len(x)):

    row_total = sum(transition[i])

    for j in range(0,len(x)):

        transition[i][j] = transition[i][j]/row_total

print("End probability table " + str(datetime.now() - startTime))



choice = 0
while(True):
    print("1: Generate New Text")
    print("2: Text Prediction")
    print("3: Exit")
    choice = int(input("Please Select an option: "))

    if choice == 1:
        #Get a random word to begin the sequence
        seed = random.randint(0,len(x)-1)

        #Get how many words the user wants
        number_of_words = int(input("How many words would you like: "))

        #Word is an np array so the where command works later
        word = np.array([x[seed]])
        word_list = [word[0]]

        for i in range(0, number_of_words - 1):

            try:
                queary = np.where(x == word[0])[0][0]
            except Exception:
                pass
            print(queary)
            word[0] = x[np.argmax(transition[queary])]
            word_list.append(word[0])

        print("Your new text is: ", end = " ")

        for i in range(0, number_of_words):
            print(word_list[i] + " ", end = " ")

        print(" ")






    if choice == 2:
        print("Choice 2: Predict Text")
    if choice == 3:
        print("Choice 3: Exit")
        break
