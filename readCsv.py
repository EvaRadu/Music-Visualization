import pandas as pd
import numpy as np
import re

dfSongs = pd.read_csv('DATA/wasabi_csv/songs.csv')
dfArtists = pd.read_csv('DATA/wasabi_csv/wasabi_all_artists_3000.csv')
dfAlbums = pd.read_csv('DATA/wasabi_csv/albums_all_artists_3000.csv')
dfAlbums.reset_index(drop=True, inplace=True)
dfArtists.reset_index(drop=True, inplace=True)
dfSongs.reset_index(drop=True, inplace=True)
dfArtists.rename(columns={'genres':'genre'}, inplace=True)

def tri_genre(df) : 
    global genre_set
    nans = df['genre'].isnull()
    for i in range(len(df['genre'])):
        if not nans[i]:
            l = df['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
            genre_set |= set(l)
        #df['genre'][i] = df['genre'][i].replace("list(", "").replace("list(", "").replace(")","").replace("\"", "").split(", ")
            #print(df['genre'][i])
    #print(df['genre'][1001])

def cluster_genre(df):
    global alias, genre_clusters
    nans = df['genre'].isnull()
    new_column = []
    for i in range(len(df['genre'])):
        clustered_genre = set() 
        if not nans[i]:
            l = df['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
            for genre in l:
                for a in alias.keys():
                    if a in genre.lower():
                        clustered_genre.add(alias[a])
                for cluster in genre_clusters:
                    if cluster in genre.lower():
                        clustered_genre.add(cluster)
                        continue
        new_column.append(list(clustered_genre))
    df.insert(loc=len(df.columns), column="genre_cluster", value=new_column)

def complete(dfAlbums, dfArtists):
    nansAlb = dfAlbums['genre'].isnull()
    new_column = []
    for i in range(len(dfAlbums)):
        print(i)
        if nansAlb[i] :
            print("A")

            new_column.append(np.array(dfArtists[dfArtists['_id'] == dfAlbums['id_artist'][i]]['genre'])[0])
        else :
            print("B")
            print(dfAlbums['genre'][i])
            new_column.append(dfAlbums['genre'][i])
        print()
    print(new_column)


if __name__ == '__main__' :

    alias = {"dubstep":"electronic", "synthpop":"electronic", "drum and bass":"rock"}
    genre_clusters = ["hip hop", "pop rock", "rock", "metal", "electronic", "pop", "country", "blues", "soul"
    "classical", "techno", "jazz", "punk", "funk", "disco", "reggae", "R&B", "gospel"
    "dupstep", "rap", "folk", "bossa nova"]
    genre_set = set()
 
    cluster_genre(dfSongs)
    #print(dfSongs["genre"][:20])
    #print(dfSongs["genre_cluster"][:20])
    #print(genre_set)

    complete(dfAlbums, dfArtists)



