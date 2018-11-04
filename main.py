import json
import os
from subprocess import call
from shutil import copyfile
import argparse

ontologyData = json.load(open('ontology.json', 'rb'))
trainedData = json.load(open('balanced_train_segments.json', 'rb'))
resultFolder = "./results/"

def ontologyFindById(id):
    for ontology in ontologyData:
        if ontology['id'] == id:
            return ontology

def ontologyFindByLabel(label):
    for ontology in ontologyData:
        if ontology['name'] == label:
            return ontology

def download(mode, value):
  for data in trainedData:
      flag = False
      if mode is 'id':
          labelIds = data['positive_labels'].split(',')
          for labelId in labelIds:
                if labelId == value:
                    flag = True
                    break
          if flag is False:
              continue
      elif mode is 'label':
          labelIds = data['positive_labels'].split(',')
          for labelId in labelIds:
              found = ontologyFindById(labelId)
              if found['name'] == value:
                  flag = True
                  break
          if flag is False:
              continue

      src = "./splits/" + data['YTID'] + "/01 - " + data['YTID'] + ".mp3"
      if os.path.exists(src):
          continue

      url = "https://www.youtube.com/watch?v=" + data['YTID']
      f = open("tracks.txt", 'w')

      startSeconds = data['start_seconds']
      min = int(startSeconds / 60)
      seconds = int(startSeconds % 60)
      line = str(min) + ":" + str(seconds) + " " + data['YTID'] + "\n"
      f.write(line)

      startSeconds += 10
      min = int(startSeconds / 60)
      seconds = int(startSeconds % 60)
      line = str(min) + ":" + str(seconds) + " sample1"
      f.write(line)

      f.close()

      call(["python", "split.py", "-yt", url])

      if os.path.exists(src):
          labelIds = data['positive_labels'].split(',')
          
          for labelId in labelIds:
              found = ontologyFindById(labelId)

              folder = resultFolder + found['name']
              dst = folder + "/" + data['YTID'] + ".mp3"

              # create destination folder
              if not os.path.exists(folder):
                  os.makedirs(folder)
              
              copyfile(src, dst)
							
if __name__ == "__main__":
    # arg parsing
    parser = argparse.ArgumentParser(description='Download audioes from AudioSet')
    parser.add_argument(
        "-id", 
        help="The id you want to download. Default: None", 
        metavar="label_id",
				type=str,
        default=None
    )
    parser.add_argument(
        "-label",
        help="Specify the label that you want to download. Default: None",
        metavar="label",
				type=str,
        default=None
    )

    args = parser.parse_args()
    LABELID = args.id
    LABEL = args.label

    if LABELID is not None:
      if ontologyFindById(LABELID) is None:
        print("Error> No Matching ID !")
      else:
        download('id', LABELID)
    elif LABEL is not None:
      if ontologyFindByLabel(LABEL) is None:
        print("Error> No Matching Label !")
      else:
        download('label', LABEL)
    else:
      download(None, None)
