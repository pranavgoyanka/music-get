import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

print('Installing python dependancies')
install('youtube_dl')
install('requests')
install('termcolor')
install('tqdm')
install('mutagen')
