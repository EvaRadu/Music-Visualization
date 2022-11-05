import csv
import json

csvList = []   # each element of the list = one row of the csv file

with open("./test.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    csvList.append(row)

csvList = csvList[1:]   # remove the first row (header)

jsonString = '['

for i in range(len(csvList)):
    jsonString += "{'name': '"+ csvList[i][1] + "', "
    jsonString += "'value': '"+ str(i) + "', "
    jsonString += "'children': [ { 'name': '"+ csvList[i][2] + "', 'value': 1}]},"

jsonString = jsonString[:-1] + ']'
 
# Writing to test.txt
with open("test.txt", "w") as outfile:
    outfile.write(jsonString)
