import glob
import os
import time
import xml.etree.ElementTree as ET

#------------------------------------------------------------------------------------------------
# Get all documents in a directory as a list.
documents = []
def listDocuments():
	os.chdir("xml")
	for document in glob.glob("*.xml"):
		# print('Reading '+document)
		documents.append(document)
	#print documents
#------------------------------------------------------------------------------------------------
# Parse each document and write the text into corresponding text file.
def parseDocuments():
	for document in documents:
		#print("Converting "+str(document))

		tree = ET.parse(document)
		root = tree.getroot()

		for pub in root.iter('pub'):
			date = pub.find('date')
			year = date.find('year')
			pub_year = year.text
			break		

		xmlDoc = open(document, 'r')
		out_file = getOutputFilename(document, pub_year)
		
		actual_data = ""
		dirty = False
		body_start = False

		figure_start = False
		table_start = False
		st_start = False

		for line in xmlDoc:
			if "<bdy>" not in line and body_start == False:
				#print("bdy not found yet.")
				continue

			elif "<bdy>" in line:
				#print("Body found.")
				body_start = True
				continue

			elif "</bdy>" in line:
				#print("bdy ends, so breaking")
				break				

			elif "<st" in line:
				#print("st starts")
				section_start = True
				continue
			elif "</st>" in line:
				#print("st ends.")
				section_start = False
				continue

			elif "<p>" and "</p>" in line and table_start == False and figure_start == False and section_start == False:
				#print("p starts and ends.")
				out_line = getData(line)
				out_line = out_line.strip()
				out_line = out_line+'\n'
				out_file.write(out_line)
				continue

			elif "<p>" in line and "</p>" not in line and table_start == False and figure_start == False and section_start == False:
				#print("p starts.")
				out_line = getData(line)
				out_line = out_line.strip()
				out_line = out_line+'\n'
				out_file.write(out_line)
				dirty = True
				continue

			elif "<p>" not in line and "</p>" in line and table_start == False and figure_start == False and section_start == False:
				#print("p ends.")
				out_line = getData(line)
				out_line = out_line.strip()
				out_line = out_line+'\n'
				out_file.write(out_line)
				dirty = False
				continue

			elif dirty == True and table_start == False and figure_start == False and section_start == False:
				#print("Text to be ")
				out_line = getData(line)
				out_line = out_line.strip()
				out_line = out_line+'\n'
				out_file.write(out_line)
				continue

			elif "<fig" in line:
				#print("Figure found.")
				#print line
				figure_start = True
				continue

			elif "</fig>" in line:
				#print("Figure ends.")
				figure_start = False
				continue

			elif "<tbl" in line:
				#print("Table starts.")
				table_start = True
				continue

			elif "</tbl>" in line:
				#print("Table ends.")
				table_start = False
				continue
		xmlDoc.close()
		out_file.close()
#------------------------------------------------------------------------------------------------
# Function to create and open a text file for writing.
def getOutputFilename(document, pub_year):
	tokens = document.split('.')
	doc_name = tokens.pop(0)
	text_doc_name = "../text/"+str(pub_year)+"_"+doc_name+".txt"
	
	out_file = open(text_doc_name, 'w')
	return out_file

#------------------------------------------------------------------------------------------------
# Function to parse a line and extract only text
def getData(line):
	dirty = False
	out_line = ""
	for c in line:
		if c == '<':
			dirty = True
			continue
		elif c == '>':
			dirty = False
			continue
		elif dirty == False:
			out_line = out_line+c
		else:
			continue
	#print(out_line)
	return out_line+'\n'
#------------------------------------------------------------------------------------------------
def main():
	
	print("Building text corpus from xml corpus. This may take around 30 minutes. Please wait...")
	listDocuments()

	start_time = time.time()
	parseDocuments()
	end_time = time.time()

	print("Xml to Text conversion is done.")
	print("Time taken for execution : "+ str(end_time - start_time)+" seconds")	
#------------------------------------------------------------------------------------------------
main()
