import pandas as pd

#Download the file
raw_corpus = pd.read_csv('Shakespeare_data.csv')

#Isolate the lines
lines = raw_corpus['PlayerLine']

print(lines.head())
