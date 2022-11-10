import pandas as pd
import numpy as np
import re

dfSongs = pd.read_csv('../../DATA/songs_parallelCoord.csv')
dfSongs.reset_index(drop=True, inplace=True)

dfAlbums = pd.read_csv('../../DATA/albums.csv')
dfAlbums.reset_index(drop=True, inplace=True)

dfArtists = pd.read_csv('../../DATA/artists.csv')
dfArtists.reset_index(drop=True, inplace=True)


# Fonction qui transforme la liste des genres dans un format exploitable et split les lignes des genres
def tranformListGenre() : 
    global dfSongs
    nans = dfSongs['genre'].isnull()
    for i in range(1000):
        print(i)
        if not nans[i]:
            dfSongs['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
            dfSongs['genre'][i] = dfSongs['genre'][i].replace("list(", "").replace("list(", "").replace(")","").replace("\"", "").split(", ")

        else:
            dfSongs['genre_infere'][i] = dfSongs['genre_infere'][i].split(",")
    
    dfSongs = dfSongs.explode('genre')
    dfSongs = dfSongs.explode('genre_infere')

# Fonction qui rajoute le nom de l'artiste et de l'album correspondant à chaque chanson
def addArtistAndAlbumName() : 
    global dfSongs
    global dfArtists
    dfSongs['artist_name'] = ""
    dfSongs['album_name'] = ""
    for i in range(1000):
        print(i)
        id_album = dfSongs['id_album'][i]
        id_artist = dfAlbums.loc[dfAlbums['_id'] == id_album]["id_artist"].values[0]
        dfSongs['artist_name'] = dfArtists.loc[dfArtists['_id'] == id_artist]["name"].values[0]
        dfSongs['album_name'] = dfAlbums.loc[dfAlbums['_id'] == id_album]["title"].values[0]

# Fonction qui remplaces les données nulles par "Unknown"
def cleanDataFrame():
    global dfSongs
    dfSongs = dfSongs.replace(np.nan, 'Unknown', regex=True)


            

if __name__ == '__main__' :
    
    #tranformListGenre()

    addArtistAndAlbumName()
    cleanDataFrame()
    
    dfSongs = dfSongs.drop(columns=['publicationDate','releaseDate',"_id","Unnamed: 0","id_album"])
    
    songs_csv_data = dfSongs.to_csv('../../DATA/songs_parallelCoord.csv', index = True)




