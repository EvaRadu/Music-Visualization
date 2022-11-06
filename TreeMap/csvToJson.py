import csv
import json

csvList = []   # each element of the list = one row of the csv file



def nbGenre(L, genre):
    nb = 0
    for i in range(len(L)):
        if L[i][2] == genre:
            nb += 1
    return nb

def listGenre(L,genre):
    L2 = []
    for i in range(len(L)):
        if L[i][2] == genre:
            L2.append(L[i][1])
    return L2

def createDico(L):
    D = {}
    for i in range(len(L)):
        D[L[i][2]] = [nbGenre(L,L[i][2]),listGenre(L,L[i][2])]
    return D


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

dico = createDico(csvList)
jsonString2 = '['

for key, value in dico.items():
    jsonString2 += "{'name': '"+ key + "', "
    jsonString2 += "'value': '"+ str(value[0]) + "', "
    jsonString2 += "'children': ["
    for i in range(len(value[1])):
      jsonString2 += "{ 'name': '"+ value[1][i] + "', 'value': 1},"
    jsonString2 = jsonString2[:-1] + "]},"

print(jsonString2[:-1] + ']')


jsonString2 = jsonString2[:-1] + ']'
 
# Writing to test.txt
with open("test.txt", "w") as outfile:
    outfile.write(jsonString)


# Writing to test2.txt
with open("test2.txt", "w") as outfile:
    outfile.write(jsonString2)

