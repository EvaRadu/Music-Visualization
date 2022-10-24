import pandas as pd
import numpy as np
import re

dfSongs = pd.read_csv('DATA/wasabi_csv/songs.csv').dropna()
dfArtists = pd.read_csv('DATA/wasabi_csv/wasabi_all_artists_3000.csv').dropna()
dfAlbums = pd.read_csv('DATA/wasabi_csv/albums_all_artists_3000.csv').dropna()
dfSongs.reset_index(drop=True, inplace=True)
dfArtists.reset_index(drop=True, inplace=True)
dfSongs.reset_index(drop=True, inplace=True)
dfArtists.rename(columns={'genres':'genre'}, inplace=True)


#print(df['genre'][0])

def tri_genre_beta() :
    my_liste = []
    genre = df['genre'].unique()
    my_method = lambda x: x.replace("\"", "").replace("list(", "").replace(")","").split(", ")
    #np.stack(np.vectorize(lambda x: x.replace("\"", "").replace("list(", "").replace(")","").split(", ")))(genre)
    #print(map(my_method,genre))
    for a in genre:
        if not(np.nan(a)) :
            my_liste.append(my_method(a))
        else :
            my_liste.append(a)
    #print((genre[4]).find("list"))
    #set(genre)
    #frequent = max(set(genre), key = genre.count)
    #print(frequent)
    return genre

def tri_genre(df) : 
    global genre_set
    for i in range(len(df['genre'])):
        l = df['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
        genre_set |= set(l)
        #df['genre'][i] = df['genre'][i].replace("list(", "").replace("list(", "").replace(")","").replace("\"", "").split(", ")
            #print(df['genre'][i])
    #print(df['genre'][1001])

def cluster_genre(df):
    new_column = []
    for i in range(len(df['genre'])):
        clustered_genre = set() 
        l = df['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
        for genre in l:
            for cluster in genre_clusters:
                if cluster in genre.lower():
                    clustered_genre.add(cluster)
                    continue
        new_column.append(list(clustered_genre))
    df.insert(loc=len(df.columns), column="genre_cluster", value=new_column)


alias = {"dubstep":"electronic", "synthpop":"electronic", "drum and bass":"rock"}
genre_clusters = ["hip hop", "pop rock", "rock", "metal", "electronic", "pop", "country", "blues", "soul"
    "classical", "techno", "jazz", "punk", "funk", "disco", "reggae", "R&B", "gospel"
    "dupstep", "rap", "folk", "bossa nova"]
genre_set = set()


if __name__ == '__main__' :
    tri_genre(dfSongs)
    tri_genre(dfArtists)
    tri_genre(dfAlbums)
    cluster_genre(dfSongs)
    print(dfSongs["genre"][:20])
    print(dfSongs["genre_cluster"][:20])
    print(genre_set)



