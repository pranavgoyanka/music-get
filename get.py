import json
import os
import requests
from mutagen.easyid3 import EasyID3
# import tqdm

class music_get:
    def __init__(self):
        self.url = ""
        self.albumName = ""
        self.artistName = ""
        self.output = ""
        self.yt_dl = ""
        self.last_fm = ""
        self.songs = []
        self.files = []
    
    def start(self):
        self.url = input('Enter Album URL from YT Music: ')
        self.albumName = input("Album Name: ")
        self.albumName = self.albumName.capitalize()
        self.artistName = input("Artist Name: ")
        self.artistName = self.artistName.capitalize()
        self.output = '"./' + self.artistName.replace('+', ' ') + '/' + self.albumName.replace('+', ' ') + '/%(playlist_index)s.%(ext)s" ' 
        self.output = '"./' + self.artistName.replace('+', ' ') + '/' + self.albumName.replace('+', ' ') + '/%(playlist_index)s.%(ext)s" ' 
        self.yt_dl = "youtube-dl -x --audio-format mp3 --audio-quality 0 --prefer-ffmpeg  -o" + self.output
        self.lastFM = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=ebd06f4e0ef7f4affadd430237a839b1&artist="+self.artistName+"&album="+self.albumName+"&format=json"

    def metadata_fetch(self):
        r = requests.get(self.lastFM)
        data = json.loads(r.text)
        # tracks = data['album']['tracks']['track']
        print("The following tracks will be downloaded:")
        for i in data['album']['tracks']['track']:
            print(i['name'])
            self.songs.append(i['name'])

    def youtube_dl(self):
        try:
            os.chdir('./' + self.artistName)
            os.chdir('..')
        except:
            os.mkdir('./' + self.artistName)
        
        try:
            os.chdir('./' + self.artistName + '/' + self.albumName)
            os.chdir('..')
            os.chdir('..')
        except: 
            os.mkdir('./' + self.artistName + '/' + self.albumName)
        os.system(self.yt_dl + self.url)

    def fix_names(self):
        # Sanitize titles
        for title in self.songs:
            bad_chars = '<>:"/\|?*'
            for c in bad_chars:
                title = title.replace(c, ';')
            title = title.replace('.', '')
        # Rename files
        os.chdir('./' + self.artistName.replace('+', ' ') + '/' + self.albumName.replace('+', ' ') + '/')
        for filename in sorted(os.listdir('./')):
            self.files.append(filename)

        for i in range(0,len(self.songs)):
            os.rename(self.files[i], self.songs[i] + '.mp3')
        
    def fix_tag(self):
        API_key = "ebd06f4e0ef7f4affadd430237a839b1"
        url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=" + API_key + "&artist="+self.artistName+"&album=" + self.albumName + "&format=json"
        # Example: http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=ebd06f4e0ef7f4affadd430237a839b1&artist=Abba&album=Arrival&format=json
        r = requests.get(url)
        r = json.loads(r.text)

        for i in r['album']['tracks']['track']:
            data = EasyID3('./' + self.artistName + '/' + self.albumName + '/' + os.listdir('./' + self.artistName + '/' + self.albumName + '/')[int(i['@attr']['rank'])- 1])
            # data = mutagen.File('./Song/' + os.listdir('./Song/')[int(i['@attr']['rank'])- 1] )
            # print(data)
            # mutagen.File('')
            # os.rename(''./2001 - Amnesiac/' + os.listdir('./2001 - Amnesiac')[int(i['@attr']['rank'])- 1]', i['name'])
            data['title'] = i['name']
            data['album'] = r['album']['name']
            data['tracknumber'] = i['@attr']['rank']
            data['albumartist'] = r['album']['artist']
            data['artist'] = r['album']['artist']
            data.save()



mdl = music_get()
mdl.start()
mdl.metadata_fetch()
mdl.youtube_dl()
mdl.fix_tag()
mdl.fix_names()