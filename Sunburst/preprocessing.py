import pandas as pd
import numpy as np
import json
import csv

# Read the csv files
dfSongs = pd.read_csv('DATA/wasabi_csv/songs.csv')
dfArtists = pd.read_csv('DATA/wasabi_csv/wasabi_all_artists_3000.csv')
dfAlbums = pd.read_csv('DATA/wasabi_csv/albums_all_artists_3000.csv')
dfAlbums.reset_index(drop=True, inplace=True)
dfArtists.reset_index(drop=True, inplace=True)
dfSongs.reset_index(drop=True, inplace=True)
dfArtists.rename(columns={'genres':'genre'}, inplace=True)

cpt1970 = 0 #annees 1970
cpt1980 = 0 #annees 1980
cpt1990 = 0 #annees 1990
cpt2000 = 0 #annees 2000
cpt2010 = 0 #annees 2010

# Adding a decade columnn
# counting the number of albums released in each decade
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

# adding the name of the artist to the album dataframe
new_col = []
for i in range(len(dfAlbums['_id'])):
    id_artist = dfAlbums['id_artist'][i]
    print(id_artist)


    b = np.array(pd.isnull(dfArtists[dfAlbums['_id'] == dfArtists['id_artist'][i]]['name']))[0] #genre_inféré
    elt = np.array(dfAlbums[dfAlbums['_id'] == dfSongs['id_album'][i]]['genre'])[0] #genre

    name = dfArtists[dfArtists['_id'] == id_artist]['name'].values[0]
    print(name)
    new_col.append(dfArtists['name'][id_artist])
print(new_col)



alias = {"dubstep":"electronic", "synthpop":"electronic", "drum and bass":"rock"}
genre_clusters = ["hip hop", "pop rock", "rock", "metal", "electronic", "pop", "country", "blues", "soul", "classical", "techno", "jazz", "punk", "funk", "disco", "reggae", "R&B", "gospel", "dupstep", "rap", "folk", "bossa nova"]

mycolumns = list(dfAlbums.columns) + ["decade","sousGenre", "genreCluster"]
myDf = pd.DataFrame(columns= mycolumns)
print(dfAlbums.head)



sub_genres = {}  # Pour chaque genre majeur, un ensemble de sous-genre
artist_subgenres = {}  # Pour genre, un ensemble d'artistes
for genre in genre_clusters:
	sub_genres[genre] = set({})


# Ici on parcours le dataset pour lister tous les genres, et les relier à leurs sous-genres
nans = dfArtists['genre'].isnull()
for i in range(len(dfArtists)):
	if not nans[i]:
		artist_genres = dfArtists['genre'][i].replace("list(", "").replace(
			")", '').replace('"', '').replace("Dub(", "").split(', ')
		artist_name = dfArtists["name"][i]

		# On relie chaque genre majeur à un ensemble de sous-genres
		for genre in artist_genres:
			for a in alias.keys():
				if a.lower() in genre.lower() and a.lower()!=genre.lower():
					sub_genres[alias[a]].update((a,))
					if artist_subgenres.get(a) is None:
						artist_subgenres[a] = set()
						artist_subgenres[a].add(artist_name)
					else:
						artist_subgenres[a].update((artist_name,))
					continue
			for cluster in genre_clusters:
				if cluster.lower() in genre.lower():
					sub_genres[cluster].update((genre,))
					if artist_subgenres.get(genre) is None:
						artist_subgenres[genre] = set()
						artist_subgenres[genre].add(artist_name)
					else:
						artist_subgenres[genre].update((artist_name,))
					continue
print(sub_genres)

hierachy = {"name": "Major Genres", "children": []}
liste = []

years = [1970, 1980, 1990, 2000, 2010]

#GENRE ET SOUS GENRE
for year in years :
    cpt = globals()['cpt'+str(year)]
    liste.append([year, year, "", cpt ])
    for genre in genre_clusters:
        hierachy["children"].append({"name": genre, "children": []})
        children = list(sub_genres[genre])
        liste.append([genre + str(year), genre, year, len(children)])
        for c in children:
            if (c!="R&B") :
                hierachy["children"][-1]["children"].append({"name":c})
                liste.append([c + str(year), c, genre + str(year), 1])
            else :
                continue

'''print("Saving hierachy json...")
# Sauvegarder en json
with open("sunburst_hierachy.json", "w") as outfile:
    json.dump(hierachy, outfile)
'''

fields = ["ids","labels", "parents", "values"]
rows = liste

with open('sunburst.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
      
    write.writerow(fields)
    write.writerows(rows)
'''for i in range (len(dfAlbums['publicationDate'])) :
    for j in range(len(dfAlbums['genre'][i])) :
        if dfAlbums['genre'][i][j] in alias :
            dfAlbums['genre'][i][j] = alias[dfAlbums['genre'][i][j]]
        if dfAlbums['genre'][i][j] not in genre_clusters :
            dfAlbums['genre'][i][j] = 'other'''

