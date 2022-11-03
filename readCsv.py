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


def completeGenreAlbums(dfAlbums, dfArtists):
    nansAlb = dfAlbums['genre'].isnull()
    new_column = []
    for i in range(len(dfAlbums)):
        if nansAlb[i] :
            new_column.append(np.array(dfArtists[dfArtists['_id'] == dfAlbums['id_artist'][i]]['genre'])[0])
        else :
            new_column.append(np.nan)
    dfAlbums.insert(loc=len(dfAlbums.columns), column="genre_infere", value=new_column)


def completeGenreSongs(dfSongs, dfAlbums):
    nansSongs = dfSongs['genre'].isnull()
    new_column = []
    for i in range(len(dfSongs)):
        if nansSongs[i] :
            if i%100==0 :
                print(i)
            b = np.array(pd.isnull(dfAlbums[dfAlbums['_id'] == dfSongs['id_album'][i]]['genre_infere']))[0]
            elt = np.array(dfAlbums[dfAlbums['_id'] == dfSongs['id_album'][i]]['genre'])[0]
            if (b):
                new_column.append(np.array(dfAlbums[dfAlbums['_id'] == dfSongs['id_album'][i]]['genre_infere'])[0])
            else :
                new_column.append(elt)
        else :
            new_column.append(np.nan)
    dfSongs.insert(loc=len(dfSongs.columns), column="genre_infere", value=new_column)


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

    completeGenreAlbums(dfAlbums, dfArtists)
    completeGenreSongs(dfSongs, dfAlbums)
    print(dfAlbums.tail(20))
    print(dfSongs.tail(20))




