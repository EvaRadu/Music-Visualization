import pandas as pd
import numpy as np
import re

df = pd.read_csv('DATA/wasabi_csv/songs.csv')

#print(df.columns)
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

def tri_genre() : 
    for i in range(len(df['genre'])):
        if type(df['genre'][i])!=float:
            df['genre'][i] = df['genre'][i].replace("list(", "").replace("list(", "").replace(")","").replace("\"", "").split(", ")
            #print(df['genre'][i])
    print(df['genre'][1001])

if __name__ == '__main__' :
    tri_genre()
