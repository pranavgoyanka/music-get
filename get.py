import json
import os
import requests
import tqdm
import subprocess
import sys
from termcolor import colored, cprint
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import urllib3

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
        self.albumName = self.albumName.title()
        self.artistName = input("Artist Name: ")
        self.artistName = self.artistName.title()
        self.output = '"./' + self.artistName.replace('+', ' ') + '/' + self.albumName.replace('+', ' ') + '/%(playlist_index)s.%(ext)s" ' 
        self.output = '"./' + self.artistName.replace('+', ' ') + '/' + self.albumName.replace('+', ' ') + '/%(playlist_index)s.%(ext)s" ' 
        self.yt_dl = "youtube-dl -x --audio-format mp3 --audio-quality 0 --prefer-ffmpeg  -o" + self.output
        self.lastFM = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=ebd06f4e0ef7f4affadd430237a839b1&artist="+self.artistName+"&album="+self.albumName+"&format=json"

    def metadata_fetch(self):
        r = requests.get(self.lastFM)
        data = json.loads(r.text)
        # tracks = data['album']['tracks']['track']
        print("\nThe following tracks will be downloaded:-")
        sno=1
        for i in data['album']['tracks']['track']:
            print(str(sno) + ". " + i['name'])
            self.songs.append(i['name'])
            sno+=1

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
        API_key = "ebd06f4e0ef7f4affadd430237a839b1"
        art_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=" + API_key + "&artist="+self.artistName+"&album=" + self.albumName + "&format=json"
        res = requests.get(art_url)
        res = json.loads(res.text)
        
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

        print("\n\nAdding Album art and renaming songs....  ")

        
        http = urllib3.PoolManager()
        albumart = http.request('GET', res['album']['image'][-2]['#text']).data

        for i in range(0,len(self.songs)):
            data = EasyID3(self.files[i])
            data['title'] = self.songs[i]
            data['album'] = self.albumName
            data['tracknumber'] = str(i+1)
            data['albumartist'] = self.artistName
            data['artist'] = self.artistName
            data.save()

            data = ID3(self.files[i])

            data['APIC'] = APIC(
                                encoding=3, # 3 is for utf-8
                                mime='image/png', # image/jpeg or image/png
                                type=3, # 3 is for the cover image
                                desc=u'Cover',
                                data=albumart
                            )
            data.save()

            os.rename(self.files[i], self.songs[i] + '.mp3')

        print("\nSuccessfully downloaded album \"" + self.albumName + "\" by " + self.artistName)

mdl = music_get()
mdl.start()
mdl.metadata_fetch()
mdl.youtube_dl()
mdl.fix_names()