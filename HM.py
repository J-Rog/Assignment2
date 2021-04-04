import pandas as pd
import numpy as np
import re

#Open the file
raw_corpus = pd.read_csv('Shakespeare_data.csv')

#Isolate the lines and convert them into a numpy array.
lines = raw_corpus['PlayerLine'].to_numpy()

#Remove all punctuation
for i in range(0,len(lines)):
    lines[i] = re.sub(r'[^\w\s]', '', lines[i])
