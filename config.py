import os
import requests
import subprocess
import sys
from tqdm import tqdm

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

os.system('cat ./banner')

windows = input("Are you using Windows? (y/n) ")

print('Installing python dependancies')
install('youtube_dl')
install('requests')
install('tqdm')

if(windows.lower() == 'y'):
    print('Fetching ffmpeg')
    r = requests.get('https://srv-store1.gofile.io/download/GytNuJ/ffmpeg.exe', stream=True)
    size = int(r.headers.get('content-length'))
    block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=size, unit='iB', unit_scale=True)
    with open('ffmpeg.exe', 'wb') as file:
        for data in r.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if size != 0 and progress_bar.n != size:
        print("ERROR, something went wrong")
    print('Done!')

else:
    print("\n\033[93m[WARNING]: Installing ffmpeg for Linux and macOS is currently not supported.")
    print("Please install them manually if it is not installed.\n")

