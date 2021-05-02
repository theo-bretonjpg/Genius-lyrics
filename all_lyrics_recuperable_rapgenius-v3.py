#-------------------------------------------------------------------------------------------
# Fonction : Code qui permet de recuperer tout les lyrics d'un artistes present sur Genius 
# 		     utilise un fichier de configuration pour le client id, token,
# Entree   : nom de m'artiste
# Sortie   : tout les tracks et lyrics de l'artiste
# Auteur   : Theo Breton
# date     : 4/29/2021
# Version  : V3
#-------------------------------------------------------------------------------------------


import lyricsgenius   #la librairie pour manipuler l'api rapgenius
import simplejson as json  #pour manipuler les réponses json 
import json
from CONFIG_RAP_GENIUS import * #le fichier config
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import shutil

path = os.getcwd()

#Recuperation du token de l'API Genius 
token= lyricsgenius.API(client_access_token, response_format='plain', timeout=10, sleep_time=0.2, retries=5)

print(token)

session = requests.session() 

nom_inputted=input("Input artist name : ")

if token :
	#Recherche pour recuperer l'id de l'artiste entree 
	songs=token.search_songs(nom_inputted,per_page=1,page=None)	
	print(type(songs))
	
	#print("..................................................")
	#print(json.dumps(songs))
	#print("..................................................")
	
	#Recuperation de l'id de l'artiste
	artistid=songs['hits'][0]['result']['primary_artist']['id']
	artist_name=songs['hits'][0]['result']['primary_artist']['name']  
	print(artistid)
 
	page = 1
	full_length = 0

	os.mkdir(artist_name)

	path = "ENTER ARTIST NAME FILE LOCATION HERE"+artist_name

	#On fais un while qui va chercher tout les url des tracks d'un artiste

	while page:
		artist_tracks = token.artist_songs(artistid,sort='popularity',per_page=50,page=page)
		
		#print("..................................................")
		#print(request)
		#print("..................................................")
		length = len(artist_tracks['songs'])
		print(length)
		full_length= full_length + length

		for i in artist_tracks['songs'] :
			
			trackname=i['title']
			artistname=i['primary_artist']['name']
			full_track=trackname + " - " + artistname
			print(trackname + " - " + artistname)
			track_url=i['url']

			#Apres avoir recupe rer tout les url de tout les tracks de l'artiste on utilise beautifulSoup pour recuperer les lyrics de l'artiste
			
			session = requests.session()
			response = session.get(track_url) 
			soup = BeautifulSoup(response.text, 'html.parser')

			lyrics_loc = soup.find('div',attrs={"class":"lyrics"})

			#On fais des if pour les deux cas possible apres la recuperation  de la page html
			#le premier cas ou tout se passe bien est la page reste pareil a la recuperation

			if lyrics_loc :
				
				pinsidediv = lyrics_loc.find('p')
				lyrics = pinsidediv.text
	
								
				if pinsidediv :

					
					completename=os.path.join(path, full_track+".txt")
					with open(completename,"w",encoding="utf-8") as text_file :
						text_file.write(str(lyrics)) 
									
	
			#le deuxieme cas ou on recois une deuxieme page avec une differente structure
			
			if not lyrics_loc :
				
				lyrics_loc2 = soup.find('div',attrs={"class":"Lyrics__Container-sc-1ynbvzw-6 krDVEH"})
				
				lyrics_loc2text = lyrics_loc2.text
				#print(lyrics_loc2text)

					
				if lyrics_loc2 :
					completename2=os.path.join(path, full_track+".txt")
					with open(completename2,"w", encoding="utf-8") as text_file2:
						text_file2.write(str(lyrics_loc2text))	
					
		print(full_length)
		page = artist_tracks['next_page']
		#Je cherche le nombre total des tracks de l'artist_name
