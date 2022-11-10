import pandas as pd
import numpy as np
dfAlbums = pd.read_csv('DATA/clean/albums.csv')
dfAlbums.reset_index(drop=True, inplace=True)

cpt1970 = 0 #annees 1970
cpt1980 = 0 #annees 1980
cpt1990 = 0 #annees 1990
cpt2000 = 0 #annees 2000
cpt2010 = 0 #annees 2010

#Decade
new_col = []
for i in range(len(dfAlbums['_id'])):
    elt = dfAlbums['publicationDate'][i]
    if (pd.isna(elt) or elt == '????') :
        new_col.append(0)
    else:
        elt = int(elt)
        if (elt < 1980) :
            cpt1970 += 1
            new_col.append(1970)
            continue
        elif (1980 <= elt < 1990) :
            cpt1980 += 1
            new_col.append(1980)
            continue

        elif (1990 <= elt < 2000) :
            cpt1990 += 1
            new_col.append("1990")
            continue

        elif (2000 <= elt < 2010) :
            cpt2000 += 1
            new_col.append(2000)
            continue
        else :
            cpt2010 += 1
            new_col.append(2010)
            continue
dfAlbums.insert(loc=len(dfAlbums.columns), column="decade", value=new_col)
    
print(cpt1970)
print(cpt1980)
print(cpt1990)
print(cpt2000)
print(cpt2010)

alias = {"dubstep":"electronic", "synthpop":"electronic", "drum and bass":"rock"}
genre_clusters = ["hip hop", "pop rock", "rock", "metal", "electronic", "pop", "country", "blues", "soul", "classical", "techno", "jazz", "punk", "funk", "disco", "reggae", "R&B", "gospel", "dupstep", "rap", "folk", "bossa nova"]

mycolumns = list(dfAlbums.columns) + ["decade","sousGenre", "genreCluster"]
myDf = pd.DataFrame(columns= mycolumns)
print(dfAlbums.head)
'''for i in range (len(dfAlbums['publicationDate'])) :
    for j in range(len(dfAlbums['genre'][i])) :
        if dfAlbums['genre'][i][j] in alias :
            dfAlbums['genre'][i][j] = alias[dfAlbums['genre'][i][j]]
        if dfAlbums['genre'][i][j] not in genre_clusters :
            dfAlbums['genre'][i][j] = 'other'''

