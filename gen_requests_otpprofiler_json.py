import csv
import json


def generateRequestsFromEndpoints(endpoints,TEST_ALL_MODES=True,random=False):
    json_out = {}
    json_out['name'] = "herrenberg.qa.stadtnavi.eu/reiseplan"
    json_out['eps'] = 100
    json_out['hits_percentile'] = 50
    json_out['idsite'] = "4"
    json_out['router'] = []
    json_out['min_samples'] = 2

    json_out['requests'] = {}



    # Initialize the otpprofiler DB 'requests' table with query parameters.
    # Note that on-street modes are not walk-limited, so we don't want to vary the max walk param there.
    # another way to do this would be to store the various values in tables, and construct this
    # view as a constrained product of all the other tables (probably eliminating the synthetic keys).

    # (time, arriveBy)
    times = [ ("08:50:00", False ),
              ("14:00:00", True ),
              ("18:00:00", False),
              ("23:45:00", True) ]

    if TEST_ALL_MODES:
        # (mode, walk, min)
        # OTP clamps walk distance to max 15km
        modes = [ ("WALK,TRANSIT", 10000, "QUICK"), ("WALK,TRANSIT", 10000, "SAFE") ] # More WALK, TRANSIT
        # modes.append( ("BICYCLE,TRANSIT", 15000, "QUICK") )
        # modes.append( ("CAR,WALK", 2000, "QUICK") )
        # modes.append( ("BICYCLE", 15000, "SAFE") )
        # modes.append( ("CARPOOL,WALK", 2000, "SAFE") )
        # modes.append( ("BICYCLE,WALK", 4000, "QUICK") )


    else:
        # (mode, walk, min)
        modes = [ ("WALK,TRANSIT", 2000, "QUICK") ]

    all_params = [(time, walk, mode, minimize, arriveBy)
        for (time, arriveBy) in times
        for (mode, walk, minimize) in modes]

    requests_json = []
    for i, params in enumerate( all_params ) :
        # NOTE the use of double quotes to force case-sensitivity for column names. These columns
        # represent query parameters that will be substituted directly into URLs, and URLs are defined
        # to be case-sensitive.

        time,maxWalkDist,mode,min,arriveBy = params
        typical = (time=="08:50:00" and maxWalkDist == 2 and "BICYCLE" not in mode)

        requests_json.append( dict(zip(('time','maxWalkDistance','mode','min','arriveBy','typical','id'),params+(typical,i))) )
    json_out['requests']['requests'] = requests_json

    # Initialize the otpprofiler DB with random endpoints and user-defined endpoints
    import csv
    endpoints_json = []

    for i, rec in enumerate( endpoints ):
        endpoint_rec = {'id':i, 'random':random, 'lon':float(rec['lon']), 'lat':float(rec['lat']), 'name':rec['name'], 'notes':None}
        endpoints_json.append( endpoint_rec )
    json_out['requests']['endpoints'] = endpoints_json

    return json_out


if __name__ == '__main__':
    endpoints = open("herrenberg/routes.csv")
    reader = csv.DictReader(endpoints,delimiter=";")

    endpoints = list(reader)
    json_out = {}
    json_out['herrenberg_routes_test_suite'] = []

    json_requests = generateRequestsFromEndpoints(endpoints)
    json_out['herrenberg_routes_test_suite'].append(json_requests)
    fpout = open("requests_routes.json","w")
    json.dump(json_out, fpout, indent=2 )
    fpout.close()
