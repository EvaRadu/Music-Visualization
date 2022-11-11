import pandas as pd
import numpy as np
import re

dfSongs = pd.read_csv('../../DATA/songs_parallelCoord.csv')
dfSongs.reset_index(drop=True, inplace=True)
#dfSongs.set_index('_id', inplace=True)

dfAlbums = pd.read_csv('../../DATA/albums.csv')
dfAlbums.reset_index(drop=True, inplace=True)

dfArtists = pd.read_csv('../../DATA/artists.csv')
dfArtists.reset_index(drop=True, inplace=True)


# Fonction qui transforme la liste des genres dans un format exploitable et split les lignes des genres
def tranformListGenre() : 
    global dfSongs
    nans = dfSongs['genre'].isnull()
    for i in range(len(dfSongs)):
        print("nb : ", i)
        if not nans[i]:
            dfSongs['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
            dfSongs['genre'][i] = dfSongs['genre'][i].replace("list(", "").replace("list(", "").replace(")","").replace("\"", "").split(", ")
           
        else:
            dfSongs['genre_infere'][i] = dfSongs['genre_infere'][i].split(",")
              

            #print(len(dfSongs['genre_infere'][i].split(",")))
           
    #newDf.to_csv('../../DATA/songs_parallelCoord.csv', index = False)
    dfSongs.drop(columns=["Unnamed: 0"])
    dfSongs = dfSongs.explode('genre')
    dfSongs.drop(columns=["Unnamed: 0"])
    dfSongs = dfSongs.explode('genre_infere')
    #print(dfSongs)

# Fonction qui rajoute le nom de l'artiste et de l'album correspondant à chaque chanson
def addArtistAndAlbumName() : 
    global dfSongs
    global dfArtists
    dfSongs['artist_name'] = ""
    dfSongs['album_name'] = ""
    for i in range(len(dfSongs)):
        print(i)
        id_album = dfSongs['id_album'][i]
        id_artist = dfAlbums.loc[dfAlbums['_id'] == id_album]["id_artist"].values[0]
        dfSongs['artist_name'][i] = dfArtists[dfArtists['_id'] == id_artist]['name'].values[0]
        dfSongs['album_name'][i] = dfAlbums[dfAlbums['_id'] == id_album]['title'].values[0]


# Fonction qui remplaces les données nulles par "Unknown"
def cleanDataFrame():
    global dfSongs
    dfSongs = dfSongs.replace(np.nan, 'Unknown', regex=True)

def splitCol():
    #print(dfSongs.columns)
    #print(dfSongs["Nom artist"].unique())
    #print(dfSongs[dfSongs["Nom artist"] == "Tricky"])
    
    for i in dfSongs["Nom artist"].unique():
        newDf = dfSongs[dfSongs["Nom artist"] == i]

               
        newDf.to_csv('../../DATA/ParCoordCsv/'+i.replace("/","").replace('"',"").replace("*","").replace(">","").replace("'","").replace("<","").replace('\\',"").replace(':',"").replace("?","").replace('|',"") +'.csv',  index=False)





            

if __name__ == '__main__' :
    
    #tranformListGenre()

    #addArtistAndAlbumName()
    #cleanDataFrame()
    
    #dfSongs.reset_index(drop = True).head()
    
    '''
    print(dfSongs.columns)
    dfSongs = dfSongs.drop(columns=['Unnamed: 0', 'id_album', 'publicationDate', 'releaseDate'])
    dfSongs.reset_index(drop=True, inplace=True)
    print(dfSongs)
    '''
    
    #songs_csv_data = dfSongs.to_csv('../../DATA/songs_parallelCoord.csv',  index=False)

    '''
    newDf =  pd.DataFrame()
    newDf['Nom artist'] = dfSongs['artist_name']
    newDf['Titre'] = dfSongs['title']
    newDf['Genre'] = dfSongs['genre']
    newDf['Genre inféré'] = dfSongs['genre_infere']
    newDf['Nom Album'] = dfSongs['album_name']
    newDf['Langue'] = dfSongs['language']

    songs_csv_data = newDf.to_csv('../../DATA/songs_parallelCoord.csv',  index=False)
    '''
    splitCol()




