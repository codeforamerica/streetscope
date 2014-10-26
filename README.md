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

* plus Chattanooga fellow [Jeremia Kimelman](https://github.com/jeremiak).

### Setup

* [Install Elasticsearch](http://www.elasticsearch.org/guide/en/elasticsearch/guide/current/_installing_elasticsearch.html) or for osx homebrew users `brew install elasticsearch`
* [Install Python and Virtualenv](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md)

In your command line, run the following (the lines after $ are commands and the lines after # are comments):

```
$ git clone https://github.com/codeforamerica/streetscope.git
$ cd streetscope
$ mkdir venv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# make sure elasticsearch is running, then:

$ cp sample.env .env

# create elasticsearch index on local elasticsearch instance

$ curl -XPUT "localhost:9200/addresses/"
```

Note where the proccess OpenAddresses CSV lives on your computer. **KEEP IN MIND** that the OpenAddresses schema does not include city, county, or state names so the results for `123 main street` are implicitly within the indexed area.

```
$ python index_addresses.py path/to/open-addresses-csv.csv
$ ... takes a few minutes

# start the flask app

$ honcho start
```

Application should be running on localhost:5000.

### Test it out locally

* If you have access to the 'curl' command

`$ curl http://localhost:5000/geocode?query=449+w+4th` ... should return some json!

### Deploy to Heroku

Make sure to save your OpenAddresses CSV in the root of the project. Then, in your command line, run the following:

```
$ heroku create
$ git push heroku master
$ heroku addons:add bonsai
$ bonsai=`heroku config:get BONSAI_URL`
$ curl -XPUT "$bonsai/addresses/"
$ heroku run python index_addresses.py open-addresses-csv.csv
$ ... takes a few minutes
$ heroku open
```

### Enable request logging in PostgreSQL for geocoding quality analysis (optional)

This project includes a QA/QC element by enabling request logging for geocoding quality analysis. It requires setting up a PostgreSQL instance to keep track of the geocodes. This is **optional:** You do not need to do this for Streetscope to run successfully.

* [Install PostgreSQL](https://github.com/codeforamerica/howto/blob/master/PostgreSQL.md)
* Make sure PostgreSQL is running

In your command line, run the following:

```
$ psql -c 'CREATE DATABASE geocoder'
```

Set the following environment vars in your `.env` file

```
RECORD_REQUESTS=True
DATABASE_URL=postgres://postgres@localhost/geocoder
```

In the command line, run the following:

```
$ python setup_postgres.py
```

Now geocoding requests will get logged to your PostgreSQL database along with a quality score from Elasticsearch. In the future, we'll grab the lowest quality scores, compare them to another geocoder, and figure out how to tune the Elasticsearch query to improve results.
