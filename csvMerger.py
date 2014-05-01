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

#Checks if directory exists, make sure user wants that particular directory
def dirCheck(directory):
	while (len(directory) < 1):
		directory = raw_input("Please input a directory or restart program with a directory argument:\n")
	if (os.path.isdir(directory) is True):
		raw_input("The CSV is in is: " + str(directory) + "\nPress enter to continue or end program with Ctrl + C.")
	else:
		print("The directory does not exist. Please try again. Ending Program")
		sys.exit()
	return directory

def wantName():
	includeName = raw_input("Do you want the filename to be included at the last column in each row? Y/N:\n")
	while (len(includeName) > 1):
		raw_input("Not a valid answer. Please only use Y or N.\n")
	if re.match("y|Y") is not None:
		return True
	elif re.match("n|N") is not None:
		return False
	else:
		

if __name__ == "__main__":
	csvDic = []
	directory = argv[0]
	directory = dirCheck(directory)
	#Gets all csv files from the current directory
	csvFilenames = glob.glob("*.csv")
	#Ask user if they want to include the filename in the CSV output
	includeName = wantName()
	#Takes all csv files and processes then write everything in memory to the combined csv file
	for filename in csvFilenames:
		csvDicPart = processCsv(filename)
		for row in csvDicPart:
			#Adds the name of the file to the csv row to differentiate between where the row came from
			row.append(minusDotAfter(filename))
			csvDic.append(row)
	writeCsvFile(csvDic)