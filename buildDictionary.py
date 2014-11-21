import gensim
import glob
import os
import time

#------------------------------------------------------------------------------------------------------------
# Function to split line into list of words.
def split_line(text):
    words = text.split()
    out = []
    for word in words:
        out.append(word)
    return out

#------------------------------------------------------------------------------------------------------------
# Overwriting get_texts method to create corpus out of all documents in a directory.
class MyCorpus(gensim.corpora.TextCorpus):
    def get_texts(self):
        for filename in self.input:
            yield split_line(open(filename).read())

#------------------------------------------------------------------------------------------------------------
# Function to list all document names as list.
documents = []
def listDocuments():
	os.chdir("text")
	for document in glob.glob("*.txt"):
		documents.append(document)
	print documents

#------------------------------------------------------------------------------------------------------------
stop_word_file = open('data/stopwords.txt', 'r')
stop_word_list = stop_word_file.read()

global stoplist
stoplist = set(stop_word_list.split())

# Function to create dictionary out of all the documents.
def createDictionary(minFrequency):
	myCorpus = MyCorpus(documents)
	dictionary = myCorpus.dictionary

	stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
		            if stopword in dictionary.token2id]
	once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < minFrequency]
	dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
	dictionary.compactify() # remove gaps in id sequence after words that were removed

	# Save the dictionary in a file for future reference.
	dictionary.save('../data/BioMedDictionary.dict')

	print('BioMedDictionary created in data directory.')
#------------------------------------------------------------------------------------------------------------

def main():
	listDocuments()
	minFrequency = input("Enter the minimum required frequency for words: ")
	
	print("Building dictionary. This may take several minutes. Please wait...")
	start = time.time()
	createDictionary(minFrequency)
	end = time.time()

	print("Time taken for execution : "+str(end - start)+" seconds.")

#------------------------------------------------------------------------------------------------------------
main()
