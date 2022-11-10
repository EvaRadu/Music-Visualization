import pandas as pd
import numpy as np
import re
import json 
from math import ceil

dfSongs = pd.read_csv('DATA/wasabi_csv/songs.csv')
dfArtists = pd.read_csv('DATA/wasabi_csv/wasabi_all_artists_3000.csv')
dfAlbums = pd.read_csv('DATA/wasabi_csv/albums_all_artists_3000.csv')
dfAlbums.reset_index(drop=True, inplace=True)
dfArtists.reset_index(drop=True, inplace=True)
dfSongs.reset_index(drop=True, inplace=True)
dfArtists.rename(columns={'genres':'genre'}, inplace=True)

artists_name = list(dfArtists["name"])
artists_name = np.array([a for a in artists_name if type(a)==type(" ") and len(a)<60 and '"' not in a])

np.savetxt("artists_name.txt", artists_name, delimiter=",", fmt='"%s",')

alias = {"dubstep":"electronic", "synthpop":"electronic", "drum and bass":"rock"}
genre_clusters = ["hip hop", "pop rock", "rock", "metal", "electronic", "pop", "country", "blues", "soul"
	"classical", "techno", "jazz", "punk", "funk", "disco", "reggae", "R&B", "gospel", "rap", "folk", "bossa nova"]


sub_genres = {} # Pour chaque genre majeur, un ensemble de sous-genre
artist_subgenres = {} # Pour genre, un ensemble d'artistes
for genre in genre_clusters:
	sub_genres[genre] = set({})


# Ici on parcours le dataset pour lister tous les genres, et les relier à leurs sous-genres
nans = dfArtists['genre'].isnull()
for i in range(len(dfArtists)):
	if not nans[i]:
		artist_genres = dfArtists['genre'][i].replace("list(", "").replace(")", '').replace('"', '').replace("Dub(", "").split(', ')
		artist_name = dfArtists["name"][i]

		# On relie chaque genre majeur à un ensemble de sous-genres
		for genre in artist_genres:
			for a in alias.keys():
				if a.lower() in genre.lower():
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

albums_infos = {}

# Ici on relie chaque artiste a sa liste d'albums
nans_genre = dfAlbums['genre'].isnull()
nans_artist = dfAlbums['id_artist'].isnull()
album_artist_dict = {}
for i in range(len(dfAlbums)):
	if not nans_artist[i]:
		album = dfAlbums["title"][i]
		artist = dfArtists[dfArtists["_id"]==dfAlbums["id_artist"][i]]["name"].to_numpy()[0]

		if dfAlbums["title"][i]=="Other Songs":
			album = artist+"-"+album

		albums_infos[album] = {
			"Title": album,
			"Year": dfAlbums["publicationDate"][i],
			 "Genre(s)":dfAlbums["genre"][i],
			 "Songs":[]
		}

		if album_artist_dict.get(artist) is not None:
			album_artist_dict[artist].append(album)
		else:
			album_artist_dict[artist] = [album]



# Ici on relie chaque album a sa liste de chansons
nans_genre = dfSongs['genre'].isnull()
nans_album = dfSongs['id_album'].isnull()
song_album_dict = {}
for i in range(len(dfSongs)):
	if not nans_album[i]:
		album = dfAlbums[dfAlbums["_id"]==dfSongs["id_album"][i]]["title"].to_numpy()[0]

		song_artist = dfArtists[dfArtists["_id"]==dfAlbums[dfAlbums["_id"]==dfSongs["id_album"][i]]["id_artist"].to_numpy()[0]]["name"].to_numpy()[0]

		if album == "Other Songs":
			album = song_artist+"-"+"Other Songs"
		if nans_genre[i]:
			albums_infos[album]["Songs"].append({
				"Title":dfSongs["title"][i],
				"Genres": "undocumented",
				"Publication": dfSongs["publicationDate"][i]
			})
		else:
			albums_infos[album]["Songs"].append({
				"Title":dfSongs["title"][i],
				"Genres": dfSongs["genre"][i],
				"Publication": dfSongs["publicationDate"][i]
			})

		#print("Album found: ", album)
		if song_album_dict.get(album) is not None:
			song_album_dict[album].append(dfSongs["title"][i])
		else:
			song_album_dict[album] = [dfSongs["title"][i]]
	else:
		print("Song without album: ", fSongs["title"][i])



# On créé la hierachie : Dans le cas où on a plus de 50 childrens, les grouper par ordre alphabetique pr sous-ensembles de taille 50 
hierachy = {"name": "Major Genres", "children": []}
for genre in genre_clusters:
	hierachy["children"].append({"name":genre, "children":[]})
	children = list(sub_genres[genre])
	for c in children:
		hierachy["children"][-1]["children"].append({"name":c})
		artists = list(artist_subgenres[c])
		artists.sort()
		num_groups = ceil(len(artists)/50)
		hierachy["children"][-1]["children"][-1]["children"] = []
		print(c)
		for g in range(num_groups):
			hierachy["children"][-1]["children"][-1]["children"].append({"name":artists[g*50]+"-"+artists[min(g*50+50-1, len(artists)-1)], "children":[]})
			for a in range(g*50, min(g*50+50, len(artists))):
				hierachy["children"][-1]["children"][-1]["children"][-1]["children"].append({"name":artists[a], "children":[]})
				for album in album_artist_dict[artists[a]]:
					hierachy["children"][-1]["children"][-1]["children"][-1]["children"][-1]["children"].append({"name":album, "children":[]})
					'''
					try:
						for song in song_album_dict[album]:
							hierachy["children"][-1]["children"][-1]["children"][-1]["children"][-1]["children"][-1]["children"].append(song)
						#print("Album sucessfully associated with songs: ", album)
					except:
						print("Album not found: ", album)
					'''
						


		'''
		for a in artists:
			if hierachy["children"][-1]["children"][-1].get("children") is None:
				hierachy["children"][-1]["children"][-1]["children"] = [{"name":a}]
			else:
				hierachy["children"][-1]["children"][-1]["children"].append({"name":a})
		'''


'''
m = 3
for major in hierachy["children"]:
	print("MAJOR GENRE: ", major["name"])
	for minor in major["children"]:
		print("MINOR: ", minor["name"])
		for artist in minor["children"]:
			print("artist:", artist["name"])
			if m==0:
				m=3
				break
			m-=1
'''

print("Saving hierachy json...")
# Sauvegarder en json
with open("graph_hierachy.json", "w") as outfile:
    json.dump(hierachy, outfile)


with open("albums_infos.json", "w") as outfile:
    json.dump(albums_infos, outfile)