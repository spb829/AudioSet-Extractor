import json
import os
from subprocess import call
from shutil import copyfile

ontologyData = json.load(open('ontology.json'))
trainedData = json.load(open('balanced_train_segments.json'))
resultFolder = "./results/"

def ontologyFindByID(id):
    for ontology in ontologyData:
        if ontology['id'] == id:
            return ontology

for data in trainedData:
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
        labels = data['positive_labels'].split(',')
        
        for label in labels:
            found = ontologyFindByID(label)

            folder = resultFolder + found['name']
            dst = folder + "/" + data['YTID'] + ".mp3"

            # create destination folder
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            copyfile(src, dst)