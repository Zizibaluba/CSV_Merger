import sys
import glob
import csv
import pprint
import re
import os

#Processes a CSV file by loading all rows into individual lists, grouped in to a big list of lists
def processCsv(filename):
	csvDic = []
	with open(filename) as f:
		reader = csv.reader(f)
		i = 0
		for row in reader:
			#Skip over header
			if (i < 1):
				i += 1
				continue
			else:
				csvDic.append(row)
				i += 1
	return csvDic

#Writes all the content into a combinedBook.csv
def writeCsvFile(csvLines, filename):
	with open(filename, "w") as f:
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

#Checks if directory exists, make sure user wants that particular directory
def dirCheck(directory):
	while (len(directory) < 1):
		directory = raw_input("Please input a directory or restart program with a directory argument:\n")
	if (os.path.isdir(directory) is True):
		raw_input("\nThe CSV is in is: " + str(directory) + "\n\nPress enter to continue or end program with Ctrl + C.\n")
	else:
		print("The directory does not exist. Please try again. Ending Program")
		sys.exit()
	return directory

#Asks the user if they want to include the file name to the last column of each of the rows they're merging
def choice(choiceItem):
	includeItemChoice = raw_input("Do you want " + choiceItem + " Y/N:\n")
	while True:
		if (len(includeItemChoice) > 1):
			includeItemChoice = raw_input("\nNot a valid answer. Please only use Y or N.\n")
		else:
			if re.match("y|Y", includeItemChoice) is not None:
				return True
			elif re.match("n|N", includeItemChoice) is not None:
				return False
			else:
				includeItemChoice = "bad"

#Gives the user a chance to name their file, continues until a suitable name is created
def nameFile(directory):
	while True:
		filename = raw_input("\nWhat would you like the merged file to be called? \n(If none is entered, the file will be called mergedCSV)\n")
		if (filename == ""):
			filename = "mergedCSV.csv"
		else:
			filename += ".csv"
		fileExist = checkExist(filename, directory)
		if fileExist == True:
			overwriteYN = choice("to overwrite the file?")
			if(overwriteYN == False):
				continue
			else:
				return filename
		else:
			return filename

#Checks if a file already exist within the directory
def checkExist(name, directory):
	if (os.path.exists(directory + "/" + name) == True):
		print "The file already exists."
		return True
	return False			

if __name__ == "__main__":
	csvDic = []
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	else:
		directory = ""
	directory = dirCheck(directory)
	os.chdir(directory)
	#Gets all csv files from the current directory
	csvFilenames = glob.glob("*.csv")
	#Ask user if they want to include the filename in the CSV output
	includeName = choice("the filenames to be included at the last column in each row?")
	#Takes all csv files and processes then write everything in memory to the combined csv file
	for filename in csvFilenames:
		csvDicPart = processCsv(filename)
		for row in csvDicPart:
			#Adds the name of the file to the csv row to differentiate between where the row came from if includName is True
			if (includeName == True):
				row.append(minusDotAfter(filename))
			csvDic.append(row)
	filename = nameFile(directory)
	writeCsvFile(csvDic, filename)
	print("\n=====\nDone!\n=====\n")
