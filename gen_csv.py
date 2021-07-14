#!/usr/bin/python
from __future__ import print_function
import json

from future.standard_library import install_aliases

install_aliases()

def run(requests_json=None):
    f = open("herrenberg/routes.csv", "w")
    f.write("name;lat;lon;notes\n")

    for request in endpoints:
        coordinates = "%s;%s" % (request['lat'], request['lon'])

        name = request['name']
        notes = request['notes']
        notes = notes if notes!=None else ""

        f.write(name + ";" + coordinates + ";" + notes + "\n")

    f.close()



f = open('otpqa_router_requests_feedback_different_modes.json')
router_sites = json.load(f)
f.close()

test_routers = list(router_sites.keys())

endpoints = router_sites[test_routers[0]][0]['requests']['endpoints']


run(requests_json=endpoints)
print("Created routes csv")



