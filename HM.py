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

#Create a blank emission table of size 27381 x 27381
emission = np.zeros((len(x),len(x)))

startTime = datetime.now()

print("Begin raw emission table " + str(startTime))

#Populate the emission table with raw counts
for i in range(1,len(lineOlines)):

    current_index = np.where(x == lineOlines[i])[0][0]

    past_index = np.where(x == lineOlines[i-1])[0][0]

    emission[past_index][current_index] += 1

print("End raw emission table " + str(datetime.now() - startTime))


#Convert raw data into probabilities
startTime = datetime.now()
print("Begin probability table " + str(startTime))

for i in range(0,len(x)):

    row_total = sum(emission[i])

    for j in range(0,len(x)):

        emission[i][j] = emission[i][j]/row_total

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
            word[0] = x[np.argmax(emission[queary])]

            #Penalize duplicates
            if word[0] in word_list:
                temp = emission[queary][np.argmax(emission[queary])]
                emission[queary][np.argmax(emission[queary])] = 0
                word[0] = x[np.argmax(emission[queary])]
                emission[queary][np.argmax(emission[queary])] = temp

            word_list.append(word[0])

        print("Your new text is: ", end = " ")

        for i in range(0, number_of_words):
            print(word_list[i] + " ", end = " ")

        print(" ")


    if choice == 2:

        #Make a transition table
        #           |Novel| Previous | Degree2 |
        #Novel      |_.3__|___.45____|__.5_____|
        #Previous   |_.4__|___.5_____|__.55____|
        #Degree2    |_.35_|___.6_____|__.05____|
        #Assumption the next word is based only on previous word counts up to 2
        transition = np.array([[0.3,0.45,0.5],[0.4,0.5,0.55],[0.5,0.55,0.05]])

        #Get user input
        corpus = input("Please some text: ").split()

        #Initialize probability with any given word assuming even probability
        emmision_probability = 1/len(x)

        #Three states novel, previous, 2Degree (0,1,2) respectively
        state = 0
        previous_state = 0

        #Tracks probability
        probability_sum = 0

        novel = []
        previous = []
        degree2 = []



        for i in range(1, len(corpus)):

            try:
                queary = np.where(x == corpus[i-1])[0][0]
            except Exception:
                pass

            if corpus[i] in novel:
                state = 0; #Novel
                novel.remove(corpus[i])
                previous.append(corpus[i])

            elif corpus[i] in previous:
                state = 1 #Previous
                previous.remove(corpus[i])
                degree2.append(corpus[i])

            elif corpus[i] in degree2:
                state = 2 #Degree2

            elif corpus[i] in x:
                state = 0 #Novel
                novel.append(word)

            else: #corpus[i] not in Shakespeare_data
                state = 0 #Novel


            if state == 0:
                emmision_probability = 1/len(x)
            else:
                emmision_probability = [emission[queary][np.argmax(emission[queary])]]


            probability_sum = probability_sum + emmision_probability * \
                              transition[previous_state][state]

            previous_state = state

        #Corpus probability found

        prediction_num = int(input("How many words would you like to predict"))

        for i in range(0, prediction_num):




    if choice == 3:
        print("Choice 3: Exit")
        break
