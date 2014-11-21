from gensim import corpora, models, similarities
import glob
import os
import time

#------------------------------------------------------------------------------------------------
documents = []
def listDocuments():
	os.chdir("text")
	for document in glob.glob("*.txt"):
		# print('Reading '+document)
		documents.append(document)
	print documents

#------------------------------------------------------------------------------------------------
# For each document do the following
# Now that we have a dictionary having all unique words represented by id's, parse each document
# and find out 'no_of_unique_words', 'unique_word_id' and 'frequency' of each word and output to a
# file like following format
#
# no_of_unique_words unique_word_id:frequency unique_word_id:frequency unique_word_id:frequency ...

def createDatFile():
	output_file = open('data/biomed-mult.dat', 'a')
	dictionary = corpora.Dictionary.load('data/BioMedDictionary.dict')
	stop_word_file = open('data/stopwords.txt', 'r')
	stop_word_list = stop_word_file.read()
	stoplist = set(stop_word_list.split())

	# Populate the list of documents	
	listDocuments()

	for document in documents:
		temp_file = open(document, 'r')	
		whole_text = temp_file.read()
	
		doc_as_list = whole_text.lower().split()

		# remove stop words from the document
		words = [word for word in doc_as_list if word not in stoplist]

		# get id for every unique word from the dictionary.
		# Note that words with less frequency (1) will be removed here.
		document_vector = dictionary.doc2bow(words)

		no_of_unique_words = len(document_vector)

		# print(no_of_unique_words)
		output_file.write(str(no_of_unique_words))

		for element in document_vector:
			values = str(element).strip('()')
			wordid_and_frequency = values.split(',')
			word_id = int(wordid_and_frequency.pop(0))
			frequency = int(wordid_and_frequency.pop(0))
			# write the 'unique_word_id:frequency' to the dat file.
			output_file.write(' '+str(word_id)+':'+str(frequency))

		# Iterate for next document
		output_file.write('\n')
	print("biomed-mult.dat file generated in data directory.")
#------------------------------------------------------------------------------------------------
# Main function to call other functions
def main():
	
	print("Building .dat file. This may take several minutes. Please wait...")
	start = time.time()
	createDatFile()
	end = time.time()

	print("Time taken for execution : "+str(end - start)+" seconds.")
#------------------------------------------------------------------------------------------------
main()
