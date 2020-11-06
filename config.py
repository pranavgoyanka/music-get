import os
import requests
import subprocess
import sys
from tqdm import tqdm
import json
from termcolor import colored, cprint
import platform
import zipfile

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

os.system('cat ./banner')

print('Installing python dependancies')
install('youtube_dl')
install('requests')
install('termcolor')
install('tqdm')
install('mutagen')

ff = requests.get("https://ffbinaries.com/api/v1/version/latest")
ff = json.loads(ff.text)

if(platform.system() == "Linux"):
    ffmpeg = ff['bin']['linux-64']['ffmpeg']
elif(platform.system() == "Windows"):
    ffmpeg = ff['bin']['windows-64']['ffmpeg']

else:
    ffmpeg = ff['bin']['osx-64']['ffmpeg']

print('Fetching ffmpeg for ' + str(platform.system()))

r = requests.get(ffmpeg, stream=True)
size = int(r.headers.get('content-length'))
block_size = 1024 #1 Kibibyte
progress_bar = tqdm(total=size, unit='iB', unit_scale=True)
with open('ffmpeg.zip', 'wb') as file:
    for data in r.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
progress_bar.close()
if size != 0 and progress_bar.n != size:
    print("ERROR, something went wrong")
print('Done!')

with zipfile.ZipFile('ffmpeg.zip', 'r') as zip_ref:
    zip_ref.extractall('./')

# WRITE config
conf = open('.config', 'w')
conf.write('platform: ' + str(platform.system()))
conf.close()