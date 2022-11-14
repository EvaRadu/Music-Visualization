import pandas as pd
import numpy as np
import json
import csv

# Read the csv files
dfSongs = pd.read_csv('DATA/clean/songs.csv')
dfArtists = pd.read_csv('DATA/clean/artists.csv')
dfAlbums = pd.read_csv('DATA/clean/albums.csv')
dfAlbums.reset_index(drop=True, inplace=True)
dfArtists.reset_index(drop=True, inplace=True)
dfSongs.reset_index(drop=True, inplace=True)
dfArtists.rename(columns={'genres':'genre'}, inplace=True)

cpt0 = 0
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
    name = np.array(dfArtists[dfArtists['_id'] == dfAlbums['id_artist'][i]]['name'])[0]
    new_col.append(name)
dfAlbums.insert(loc=len(dfAlbums.columns), column="artist_name", value=new_col)


alias = {"dubstep":"electronic", "synthpop":"electronic", "drum and bass":"rock"}
genre_clusters = ["hip hop", "pop rock", "rock", "metal", "electronic", "pop", "country", "blues", "soul", "classical", "techno", "jazz", "punk", "funk", "disco", "reggae", "R&B", "gospel", "dupstep", "rap", "folk", "bossa nova"]

mycolumns = list(dfAlbums.columns) + ["decade","sousGenre", "genreCluster", "artist_name"]
myDf = pd.DataFrame(columns= mycolumns)
#print(dfAlbums.head)



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



dfSousGenreAlbums = pd.DataFrame(columns=["idAlbums", "sousGenre"])


hierachy = {"name": "Major Genres", "children": []}
liste = []

years = [0, 1970, 1980, 1990, 2000, 2010]


#counting the number of albums per genre in each decade
filtered_values = dfAlbums.loc[(dfAlbums['decade']==1970) & pd.isna(dfAlbums['genre'])]
print(filtered_values["_id"].count())


#GENRE ET SOUS GENRE
print("HERE")
test = 0
bool = False
idees = []
for year in years :
    print(year)
    valYear = globals()['cpt'+str(year)]
    
    for genre in genre_clusters: #genre majeur
        
        hierachy["children"].append({"name": genre, "children": []})
        
        children = list(sub_genres[genre])
        valGenre = 0
        
        for c in children: #sous genre
            if (c!="R&B") : 
                  
                hierachy["children"][-1]["children"].append({"name":c})
                
                #counting the number of albums per genre in each decade 
                filtered_values = dfAlbums.loc[(dfAlbums['decade']==year) & (dfAlbums['genre'].isin(list(sub_genres[genre])))] 
                count = filtered_values["_id"].count()
                #print(filtered_values["genre"])
                #not a genre but a genre_infere
                '''if count == 0 : 
                    myDf = dfAlbums.loc[(dfAlbums['decade']==year)]
                    for i in myDf.index:
                        if (not pd.isna(myDf["genre_infere"][i])) :
                            list_genre = (myDf["genre_infere"][i]).split(',')
                            #print(list_genre)
                            for j in list_genre:
                                #print(j)
                                if j in list(sub_genres[genre]) :
                                    count += 1
                                    break
                     '''    
                
                #if  (c + str(year) not in idees)  :   
                #liste.append([c + str(year), c, genre + str(year), count])
                 #   idees.append(c + str(year))
                
                counting = 0
                for i in filtered_values['artist_name'].unique():
                    art = filtered_values[filtered_values['artist_name'] == i]
                    counting += art["artist_name"].count()

                for i in filtered_values['artist_name'].unique():
                    art = filtered_values[filtered_values['artist_name'] == i]
                    counting = art["artist_name"].count()
                    #if (i + str(year)) not in idees :
                    liste.append([i + str(year), i, genre + str(year),counting])
                        #idees.append(i + str(year))
                
                valGenre += count
            else :
                continue
        
        liste.append([genre + str(year), genre, year,valGenre])
        valYear += valGenre
    
    unknown = dfAlbums.loc[(dfAlbums['decade']==year) & pd.isna(dfAlbums['genre'])]
    unknownCount = unknown["_id"].count()
    liste.append(["unknown"+str(year), "Unknown", year, unknownCount])

    if (year !=0) : 
        liste.append([year, year, "", valYear + unknownCount])
    else :
        liste.append([year, "UnknownYear", "", valYear + unknownCount])

    



'''print("Saving hierachy json...")
# Sauvegarder en json
with open("sunburst_hierachy.json", "w") as outfile:
    json.dump(hierachy, outfile)
'''

fields = ["ids","labels", "parents", "values"]
rows = liste

print("Writing the csv file...")
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

