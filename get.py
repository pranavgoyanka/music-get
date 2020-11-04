import json
import os
import requests
import tqdm
import subprocess
import sys
from termcolor import colored, cprint

class music_get:
    def __init__(self):
        try: 
            os.stat('./.config').st_size

        except:
            cprint("It seems like you are running music-get for the first time.", "yellow")
            cprint("Running config fix.", "yellow")
            # os.system('python ./.config.py')
            subprocess.check_call([sys.executable, "./config.py"])

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
        self.artistName = input("Artist Name: ")
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


mdl = music_get()
mdl.start()
mdl.metadata_fetch()
mdl.youtube_dl()
mdl.fix_names()




