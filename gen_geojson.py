from __future__ import print_function
from future.standard_library import install_aliases
import json
import numpy as np
import math
from datetime import datetime
import pprint

install_aliases()
from urllib.parse import urlparse, parse_qs

def parseCoordinates(coordinates):
    floats_list_coordinates = []
    items = coordinates.split(',')
    floats_list_coordinates.append(float(items[1]))
    floats_list_coordinates.append(float(items[0]))

    return floats_list_coordinates


def getNewLine(from_coordinates, to_coordinates, url,  foundRoute = True):
    from_coordinates = parseCoordinates(from_coordinates)
    to_coordinates = parseCoordinates(to_coordinates)

    geometry = {}
    geometry['type'] = 'LineString'
    geometry['coordinates'] = []
    geometry['coordinates'].append(from_coordinates)
    geometry['coordinates'].append(to_coordinates)

    properties = {}
    properties['stroke'] = '#019801' if foundRoute else '#f71818'
    properties['stroke-opacity'] = 0.8
    properties['stroke-width'] = 1
    properties['url'] = url



    newLine = {
        'type': 'Feature',
        'geometry': geometry,
        'properties': properties
    }
    return newLine


def main(input_blob=None):
    if (input_blob is None):
        return

    datasets = [dict([(response["id_tuple"], response) for response in input_blob['responses']]), ]

    id_tuples = datasets[0].keys()


    if len(id_tuples) == 0:
        print("Input does not contain any data")
        exit()

    data = {}
    data['type'] = 'FeatureCollection'
    data['features'] = []

    # data['features'].append(getNewLine(8.87012, 48.6035, 8.8881, 48.5907, False))

    for id_tuple in id_tuples:

        for i, dataset in enumerate(datasets):

            response = dataset[id_tuple]
            foundRoute = False

            # Filter out long walks (OTP has only soft walk limitin)
            if not 'itins' in response:
                foundRoute = False

            elif len(response['itins']) == 0:
                foundRoute = False

            elif all((itin['walk_limit_exceeded'] for itin in response['itins'])):
                foundRoute = False

            else:
                foundRoute = True

            data['features'].append(getNewLine(response['from'], response['to'], response['url'], foundRoute))

    print("Create geojson file successfully")
    file = open("herrenberg/geojson.json", "w")
    json.dump(data, file, indent=2)
    file.close()
