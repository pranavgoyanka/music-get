# music-get
Download music

## Disclaimer: This project is intended for educational purposes only. Please support artists by getting your music from official sources. 

## To do
- Build a UI
- Improve error handling

## Usage

1. Install all the dependencies with

    ``` python2 install.py ```

2. Run the script with 

    ``` python3 get.py ```
    This will run a config file for the first time to make sure you the required binaries installed.

3. Enter the Album URL from youtube.com. For example:
``` youtube.com/playlist?list=OLAK5uy_lq9J1oCESyYOIiuMAmoSMgLanM35g2L2Q ```

4. Enter Album and Artist Names. Make sure that the spellings are correct. The case doesn't matter.

5. The album will be downloaded and stored at  ```./<artist_name>/<album_name>```

Note: If you get an error similar to ```Cannot extract video data```, then try again after a few minutes.
