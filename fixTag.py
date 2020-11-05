import mutagen
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
import requests
import os
import json

albumName = input("Album Name: ")
albumName = albumName.capitalize()
artistName = input("Artist Name: ")
artistName = artistName.capitalize()

API_key = "ebd06f4e0ef7f4affadd430237a839b1"
url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=" + API_key + "&artist="+artistName+"&album=" + albumName + "&format=json"
# http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=ebd06f4e0ef7f4affadd430237a839b1&artist=Abba&album=Arrival&format=json
r = requests.get(url)
r = json.loads(r.text)

print(r['album']['image'][-2]['#text'])

# for i in r['album']['tracks']['track']:
#     data = EasyID3('./' + artistName + '/' + albumName + '/' + os.listdir('./' + artistName + '/' + albumName + '/')[int(i['@attr']['rank'])- 1])
#     # data = mutagen.File('./Song/' + os.listdir('./Song/')[int(i['@attr']['rank'])- 1] )
#     print(data)
#     # mutagen.File('')
#     # os.rename(''./2001 - Amnesiac/' + os.listdir('./2001 - Amnesiac')[int(i['@attr']['rank'])- 1]', i['name'])
#     data['title'] = i['name']
#     data['album'] = r['album']['name']
#     data['tracknumber'] = i['@attr']['rank']
#     data['albumartist'] = r['album']['artist']
#     data['artist'] = r['album']['artist']
#     data.save()