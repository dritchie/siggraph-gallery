import argparse
import csv
import json
import os

__config = None
def loadconfig():
    global __config
    if __config is None:
        dirPath = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dirPath, 'config.json')
        with open(filename) as f:
            __config = json.load(f)
    return __config

def loadjson():
    dirPath = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirPath, 'database.json')
    if not os.path.exists(filename):
        return {}
    else:
        with open(filename) as f:
            return json.load(f)

def savejson(jsonData):
    dirPath = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirPath, 'database.json')
    with open(filename, 'w') as f:
        json.dump(jsonData, f, sort_keys=True, indent=3)

def csv2json(csvFilename):
    assert os.path.exists(csvFilename)
    jsonData = {}
    with open(csvFilename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['Key']
            entry = dict(row)
            entry['Authors'] = entry['Authors'].split(',')
            del entry['Key']
            jsonData[key] = entry
    return jsonData

def update(csvFilename):
    currJson = loadjson()
    newJson = csv2json(csvFilename)

    # Figure out which new entries have been added
    newEntries = {}
    for name in newJson:
        if not name in currJson:
            newEntries[name] = newJson[name]

    # Make thumbnails for these new images

    # Upload these new images + thumbnails to S3
    
    # Save the new entries to disk as JSON
    savejson(newJson)

    # Write the new JSON into the HTML of the webpage itself

if __name__ == '__main__':
    parser = argparse.ArgumentParser();
    parser.add_argument('csvFilename',
        type=str,
        help='CSV file downlaoded from "Database" Google Sheet');
    args = parser.parse_args()

    update(args.csvFilename)