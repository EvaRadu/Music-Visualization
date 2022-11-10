import pandas as pd
import numpy as np
import re

dfSongs = pd.read_csv('../../DATA/songs.csv')
dfSongs.reset_index(drop=True, inplace=True)

# Fonction qui transforme la liste des genres dans un format exploitable et split les lignes des genres
def tranformListGenre() : 
    global dfSongs
    nans = dfSongs['genre'].isnull()
    for i in range(len(dfSongs['genre'])):
        print(i)
        if not nans[i]:
            dfSongs['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
            dfSongs['genre'][i] = dfSongs['genre'][i].replace("list(", "").replace("list(", "").replace(")","").replace("\"", "").split(", ")

        else:
            dfSongs['genre_infere'][i] = dfSongs['genre_infere'][i].split(",")
    
    dfSongs = dfSongs.explode('genre')
    dfSongs = dfSongs.explode('genre_infere')






            

if __name__ == '__main__' :
    
    tranformListGenre()
    songs_csv_data = dfSongs.to_csv('../../DATA/songs_parallelCoord.csv', index = True)




