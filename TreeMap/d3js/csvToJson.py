import csv
import json

csvList = []   # each element of the list = one row of the csv file
genre_clusters = ["hip hop", "pop rock", "rock", "metal", "electronic", "pop", "country", "blues", "soul"
    "classical", "techno", "jazz", "punk", "funk", "disco", "reggae", "R&B", "gospel"
    "dupstep", "rap", "folk", "bossa nova"]

with open("../../DATA/artists.csv", encoding="utf8") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    for row in csvreader:
        csvList.append(row)

csvList = csvList[1:]   # remove the first row (header)

jsonString = '['

print(list(csvList[0][3]))

'''
def nbCluster(data, genre):
    nb = 0
    for i in range(len(data)):
        if genre in data[i]:
            nb += 1
    return nb
'''

for i in range(len(genre_clusters)):
    jsonString += "{ 'name': '" + genre_clusters[i] + "',"
    #for i in range(len(csvList)):


#for i in range(len(csvList)):
#    jsonString += "{'name': '"+ csvList[i][1] + "', "
#    jsonString += "'value': '"+ str(i) + "', "
#    jsonString += "'children': [ { 'name': '"+ csvList[i][2] + "', 'value': 1}]},"

jsonString = jsonString[:-1] + ']'

#print(jsonString)



