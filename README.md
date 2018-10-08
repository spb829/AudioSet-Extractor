# AudioSet-Extractor

[Forked from album-splitter](https://github.com/crisbal/album-splitter)

## How to install

0. Install `ffmpeg`
    * [Download](http://ffmpeg.org/releases/ffmpeg-3.4.2.tar.bz2) `v3.4.2`
    * [For Windows 64-bit](https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-20180227-fa0c9d6-win64-static.zip)
    * [For macOS 64-bit](https://ffmpeg.zeranoe.com/builds/macos64/static/ffmpeg-20180227-fa0c9d6-macos64-static.zip)
1. Install ```Python 3```
2. Install ```pip3```
3. Install ```virtualenv``` (optional)
4. Fork/Clone/Download this repository
5. ```virtualenv -p /usr/bin/python3 venv``` (optional)
    * ```source venv/bin/activate```
6. Install the required packages via pip
    * ```pip install -r requirements/prod.txt```

## Quick guide

1. Run the script
    * Basic usage: ```python main.py```
    * Specify Label Name: ```python main.py -label LABELNAME```
    * Specify Label ID: ```python main.py -id LABELID```
2. Wait for the splitting process to complete
3. You will find your audio files in the `results` folder which sorted by label

## Need help?

If you need any help just create an Issue or send me an email at the address you can find on my profile.

## Want to help?

If you want to improve the code and submit a pull request feel free to do so.

## Licence

GPL v3


