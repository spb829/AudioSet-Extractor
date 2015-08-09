from pydub import AudioSegment
import eyed3
import re
import os
import argparse


def timeToSeconds(time):
  parts = time.split(":")

  seconds = None
  if len(parts) == 3: #h:m:s
    seconds = int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])
  elif len(parts) == 2: #m:s
    seconds = int(parts[0])*60 + int(parts[1])

  return seconds


if __name__ == "__main__":
  print("Starting")

  
  #arg parsing
  parser = argparse.ArgumentParser(description='Split a single-file MP3 Album into its single tracks.')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("-mp3", help="The MP3 file you want to split.", metavar="mp3_file")
  group.add_argument("-yt", help="The YouTube video you want to download and split.", metavar="youtube_url")
  parser.add_argument("-a", "--artist", help="Specify the artist that the mp3s will be ID3-tagged with. Default: no tag", default=None)
  parser.add_argument("-A",  "--album", help="Specify the album that the mp3s will be ID3-tagged with. Default: no tag", default=None)
  parser.add_argument("-t", "--tracks", help="Specify the tracks file. Default: tracks.txt", default="tracks.txt")
  parser.add_argument("-f", "--folder", help="Specify the folder the mp3s will be put in. Default: splits/", default="splits")
  args = parser.parse_args()
  TRACKS_FILE =  args.tracks
  FILENAME = args.mp3
  YT_URL = args.yt
  ALBUM = args.album
  ARTIST = args.artist
  FOLDER = args.folder

  #create destination folder
  if not os.path.exists(FOLDER):
    os.makedirs(FOLDER)

  tracksStarts = []
  tracksTitles = []

  regex = re.compile("(?P<start>.+)\s*\-\s*(?P<title>.+)")

  print("Parsing " + TRACKS_FILE)
  with open(TRACKS_FILE) as tracksF:
    for i, line in enumerate(tracksF):
      m = regex.match(line)
      
      tStart = timeToSeconds(m.group('start').strip())
      tTitle = m.group('title').strip()

      tracksStarts.append(tStart*1000)
      tracksTitles.append(tTitle) 
  print("Tracks file parsed")

  print("Loading MP3")
  album = AudioSegment.from_mp3("album.mp3")
  print("MP3 Loaded")

  tracksStarts.append(len(album)) #we need this for the last track/split
  tracksTitles.append("END") 

  print("Starting to split")
  for i, track in enumerate(tracksTitles):
    if i != len(tracksTitles)-1:
      print("\t" + str(i+1) + ") " + track)
      start = tracksStarts[i]
      end = tracksStarts[i+1]
      duration = end-start
      album[start:][:duration].export( FOLDER + "/" + track + ".mp3", format="mp3")

      print("\t\tTagging")
      song = eyed3.load(FOLDER + "/" + track + ".mp3")
      if ARTIST:
        song.tag.artist = ARTIST.decode('utf-8')
      if ALBUM:
        song.tag.album = ALBUM.decode('utf-8')

      song.tag.title = track.decode('utf-8')
      song.tag.track_num = i+1
      song.tag.save()
  print("All Done")