# Files

### otpqa_router_requests.json:

This file contains the requests to be ran against the api when we run otpprofiler_json.py

The format of the file should be in a json format

```json
{
  "finland": [
    {
      "name": "herrenberg.qa.stadtnavi.eu/reiseplan", // name to be used as the Digitransit host
      "eps": 100,
      "hits_percentile": 50,
      "idsite": "4",
      "router": [],
      "requests": {
        "requests": [
          {
            "min": "QUICK",
            "arriveBy": false,
            "maxWalkDistance": 2000,
            "mode": "WALK,TRANSIT",
            "time": "08:50:00",
            "id": 0,
            "typical": true
          }
        ],
        //origin
        "endpoints": [
          {
            "name": "First Address",
            "notes": null,
            "random": false,
            "lon": 24.671347151586097,
            "lat": 60.149728735355815,
            "id": 0
          },
          //destination
          {
            "name": "Second Address",
            "notes": null,
            "random": false,
            "lon": 24.65683695113468,
            "lat": 60.14848405134595,
            "id": 1
          }
        ]
      },

      "min_samples": 2
    }
  ]
}
```

- If otpqa_router_requests.json is empty or not found then the tool will check requests.json with the same format
- Change line 46 to the count of routes in the file (Addresses count / 2). If the count is more than double the actaul count, the tool will randomize the origin and destination pairs.
- Change line 51 to the number of iteneraries you wish to be returned from otp


```json
{
  "requests": [
    {
      "min": "QUICK",
      "arriveBy": false,
      "maxWalkDistance": 2000,
      "mode": "WALK,TRANSIT",
      "time": "08:50:00",
      "id": 0,
      "typical": true
    }
  ],
  "endpoints": [
    {
      "name": "Mattilan p\u00e4iv\u00e4koti, Tuusula",
      "notes": null,
      "random": false,
      "lon": 25.071417,
      "lat": 60.412161,
      "id": 0
    },
    {
      "name": "Karakalliontie 14, Espoo",
      "notes": null,
      "random": false,
      "lon": 24.765385,
      "lat": 60.230409,
      "id": 1
    }
  ]
}
```

Each request must have 2 endpoints corresponding to it (origin, destination)

Run otpprofiler_json.py with param https://api.staging.stadtnavi.eu/routing/v1/router/ which returns xml by default.

Change 
```python
if (not "/otp/routers" in host) and (not "/routing/v1/routers" in host):
```
to 
```python
if (not "/otp/routers" in host) and (not "/routing/v1/router" in host): 
```
in line 466 in file otpprofiler.py so the url in not altered


I'm still investigating how to use https://api.dev.stadtnavi.eu/otp/routers/default/
as it return json by default

A new otpqa_report_key-in-requests.html will be generated with the results.

### otpprofiler.py:

This uses the requests.json in the same directory which should have requests and origin, destination pairs

Run otpprofiler.py -o, 2 new summary files are generated. run_summary.json has the response details from otp. full_itins.json has each leg's details for all the itineraries

### Optional params
-o to output those 2 files

-m 'MODE1, MODE2, MODE3'  to use those modes in requests

-i 5 to fetch 5 itineraries instead of 1 -> itinerary means a different route

run_summary.json file can then be used to compare results with a pre-written benchmark.json

## Comparing files
```bash
python compare.py benchmark_profile.json new_profile.json
```

* -t to change threshold time difference
If the difference in route < 1 minute - Passed

* -i to compare number of returned itineraries
* -it to add threshold for diff in number of iterneraries count to be compared
Note: we can add itineraries in json files by adding -i 5 and running otpprofiler.py

* -m to compare number of modes in request (count only walk, bicycle, car if they are the only modes in request)
* -mt to add max modes count to be compared

* -legs to compare number of legs in first itinerary (legs are the parts the trip is divided into)
* -legt to add max itineraries to be compared

* -trips to compare number of trips in first itinerary
* -tript to add max itineraries to be compared

* -s to compare cycling or walking speeds
* -st to change the threshold, default (0.2)

* -p to compare query execution time

* -tt to get totaltime threshold difference
* -at to get add averagetime threshold difference

### benchmark.json

Format:
```json
{
      "id_tuple": "4-1-3",
      "mode": "BICYCLE,TRANSIT",
      "itins": [
        {
          "start_time": "Mon May 31 11:19:29 2021 GMT",
          "duration": "8680 sec",
          "n_legs": 5,
          "n_vehicles": 1,
          "walk_distance": 971.0000623577392,
          "walk_limit_exceeded": false,
          "wait_time_sec": 0,
          "ride_time_sec": 600,
          "routes": [
            "790"
          ],
          "trips": [
            "hbg:56.T0.31-790-j21-1.2.H"
          ],
          "waits": [
            0.0
          ],
          "leg_modes": [
            "BICYCLE",
            "WALK",
            "BICYCLE",
            "BUS",
            "BICYCLE"
          ],
          "leg_times": [
            7.0,
            9.0,
            195.0,
            600.0,
            57.0
          ],
          "itinerary_number": 1
        }
```

To be compared with the other file same using `id_tuple` for each request


## Steps to run 
1) Generate random points from the address generator tool with the following params

    ```bash
    java - jar jarName.jar 100 otp addDistrict
    ```
    This will create a csv file with random points in herrenberg
2) Add this csv file in the OTPQA directory
3) Change the name of the csv file in gen_requests.py line 59 to match the file generated
4) Run gen_requests.py
5) A new requests.json file will be created that contains the correct format of (origin, destination) pairs
6) Run otpprofiler.py -o to generate run_summary.json and full_itins.json, you can add -i 5 to fetch up to 5 iteneraries
7) Set modes, time and min you want to be added to requests in gen_requests.py line 22
8) Copy the requests.json array to otpqa_router_requests.json to run in otpprofiler_json.py
9) Run otpprofiler_json.py to generate otpqa_report.html, you can change line 51 to change num_iteneraries (This file does what the otpprofiler.py does plus generates a report)
10) Investigate otpqa_report.html
11) Run compare.py benchmark.json against run_summary.json
12) You can run gen_geojson.py to generate geojson.json file to visualize the requests on geojson.io 

Note the otpprofiler.py adds mode TRANSIT to the request if the request's mode is BICYCLE or WALK and the distance is too long













