import pandas as pd
import numpy as np

songs = pd.read_csv("DATA/songs.csv")
albums = pd.read_csv("DATA/albums_all_artists_3000.csv")
artists = pd.read_csv("DATA/wasabi_all_artists_3000.csv")

print(len(artists))

songs_genre = songs[songs['genre'].notnull()]
songs_no_genre = songs[songs['genre'].isnull()]
songs_no_genre.reset_index()
songs_genre.reset_index()

print("Total:", len(songs))
print("Avec un genre:",len(songs_genre))
print("Sans genre:",len(songs_no_genre))

to_deduce = len(songs_no_genre)

for index, row in songs_no_genre.iterrows():
	alb_id = row["id_album"]

	album = albums[albums["_id"]==alb_id]
	album = album[album['genre'].notnull()]

	if len(album)>0:
		to_deduce -=1

print("Sans genre ni album genre:", to_deduce)