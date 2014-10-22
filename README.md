# Streetscope (OpenAddresses version)

Streetscope is a service to allow people, but especially computer programs, to submit an address like '123 Main St.' and find its lat/lon coordinates. This version is meant to take an [OpenAddresses](http://github.com/openaddresses) CSV and use it to create a geocoder. This idea came from [@daguar](http://github.com/daguar) and [@lyzidiamond](http://github.com/lyzidiamond) while hiking. Go on more hikes.

The original version was created for the City of Lexington, KY using parcel data from the Fayette County Property Valuation Administrator. You can see it live [here](http://streetscope.net).

### Why are we doing this?

Part of the value of the OpenAddresses project is the ability to create a geocoder with the addresses collected. Streetscope makes geocoders from given datasets. Together, everybody wins!

### What will this do in the future?

* Accept files to geocode as a batch
* Emit performance metrics to indicate when this geocoder varies from other geocoders in geographic distance or ability to match an address
* Generalize for any city that has a reliable address dataset

### Who is this made by?

Lexingteam!

* [Erik Schwartz](https://github.com/eeeschwartz)
* [Lyzi Diamond](https://github.com/lyzidiamond)
* [Livien Yin](https://github.com/livienyin)

with Chattanooga fellow [Jeremia Kimelman](https://github.com/jeremiak).

### How to use it?

When programming, make an HTTP GET request to `http://lexington-geocoder-flask.herokuapp.com/geocode?query=449+w+4th`

The geoJSON response:

```
{
"type": "FeatureCollection",
   "features": [
       {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [
              -84.4949386945456,
              38.055285154852555
            ]
          },
          "properties": {
              "formatted_address": "449 W FOURTH ST",
              "parcel_id": "15602150"
          }
       },
       ... { more features }
   ]
},
```

The json result can be previewed through the [HTML UI](http://streetscope.net/). ![HTML UI](https://raw.githubusercontent.com/codeforamerica/lexington-geocoder/master/screenshots/streetscope.png)

### Setup

* [Install Elasticsearch](http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/_installing_elasticsearch.html) or for osx homebrew users `brew install elasticsearch`
* [Install Python and Virtualenv](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md)

In your command line, run the following:

```
$ git clone https://github.com/codeforamerica/lexington-geocoder-flask.git
$ cd lexington-geocoder-flask
$ git checkout openaddresses
$ mkdir venv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# make sure elasticsearch is running, then:

$ mv sample.env .env
```

Note where your OpenAddresses CSVs live on your computer. You can load more than one CSV into the geocoder at a time. **KEEP IN MIND** that the OpenAddresses schema does not include city, county, or state names, so there may end up being duplicates in your dataset if you use more than one CSV.

```
$ python index_addresses.py path/to/csv.csv path/to/another_csv.csv
$ ... takes a few minutes
$ honcho start
```

Application should be running on localhost:5000.

### Test it out locally

* If you have access to the 'curl' command

`$ curl http://localhost:5000/geocode?query=449+w+4th` ... should return some json!

### Deploy to Heroku

Make sure to save your CSVs in the root of the project. Then, in your command line, run the following:

```
$ heroku create
$ git push heroku master
$ heroku addons:add bonsai
$ bonsai=`heroku config:get BONSAI_URL`
$ curl -XPUT "$bonsai/addresses/"
$ heroku run python index_addresses.py filename1.csv filename2.csv
$ ... takes a few minutes
$ heroku open
```

### Enable request logging in Postgres for geocoding quality analysis

```
$ psql -c 'CREATE DATABASE geocoder'
```

Set the following environment vars in your `.env` file

```
RECORD_REQUESTS=True
DATABASE_URL=postgres://postgres@localhost/geocoder
```

run

```
$ python setup_postgres.py
```

Now geocoding requests will get logged to postgres along with a quality score from elasticsearch. In the future we'll grab the lowest quality scores, compare them to another geocoder and figure out how to tune the elasticsearch query to improve results.
