"""
This program was written to take all csv files in a directory (will be specified by the user in a later iteration) and merge all of it together down the row. The program will also append the name of the file for each row.

4/30/14
Basic structure of the program is complete. Will need to create some basic UI for user interaction. The follwing is a list of things to make:
-Ask if the directory is correct
-Ask if to include the filenames at the end
-Ask for a filename to export to
-If exporting file name already exists, ask for a new filename or complex string to overwrite that file

"""

import sys
import glob
import csv
import pprint
import re

#Processes a CSV file by loading all rows into individual lists, grouped in to a big list of lists
def processCsv(filename):
	csvDic = []
	with open(filename, newline='') as f:
		reader = csv.reader(f)
		i = 0
		for row in reader:
			#Skip over all headers
			if (i < 4):
				i += 1
				continue
			#Largest Row number minus 1
			elif (i > 46):
				break
			#All other rows loaded into a list
			else:
				csvDic.append(row)
				i += 1
	return csvDic

#Writes all the content into a combinedBook.csv
def writeCsvFile(csvLines):
	with open('combinedBook.csv', "w") as f:
		for line in csvLines:
			for item in line:
				#Takes out extra commas in currency and names
				item = re.sub("[,]","", item)
				#Checks if number is a currency value
				if re.match("[$]", item) is not None:
					#If is currency, take away $ sign
					item = re.sub("[$]", "", item)
					item = minusDotAfter(item)
				#Add comma to separate out values in CSV
				current = str(item) + ","
				#Write to file
				f.write(current)
			#Separates row by adding newline
			f.write("\n")

#Deletes the period and anything after it and returns the string
def minusDotAfter(string):
	string = re.match(r'^.*?\.', string).group(0)
	string = re.sub("[.]", "", string)
	return string

if __name__ == "__main__":
	csvDic = []
	#Gets all csv files from the current directory
	csvFilenames = glob.glob("*.csv")
	#Takes all csv files and processes then write everything in memory to the combined csv file
	for filename in csvFilenames:
		csvDicPart = processCsv(filename)
		for row in csvDicPart:
			#Adds the name of the file to the csv row to differentiate between where the row came from
			row.append(minusDotAfter(filename))
			csvDic.append(row)
	writeCsvFile(csvDic)