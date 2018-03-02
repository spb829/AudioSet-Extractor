import json
from subprocess import call
from pprint import pprint

ontologyData = json.load(open('ontology.json'))
trainedData = json.load(open('balanced_train_segments.json'))
resultFolder = "./results/"

def ontologyFindByID(id):
    for ontology in ontologyData:
        if ontology['id'] == id:
            return ontology

#call(["python", "split.py", "-yt", "https://www.youtube.com/watch?v=-0DLPzsiXXE"])
found = ontologyFindByID("/m/07qwdck")
pprint(found)

# create destination folder
if not os.path.exists(resultFolder):
    os.makedirs(resultFolder)