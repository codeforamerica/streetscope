# Streetscope (Flask version)

Streetscope is a service to allow people, but especially computer programs, to submit an address like '123 Main St.' and find its lat/lon coordinates and canonical parcel_id in the Lexington, KY Property Value Administrator's set of addresses.

### Why are we doing this?

City agencies in Lexington sometimes disagree on the correct way to reference a single address or taxlot. (And sometimes someone entering data just makes a typo. Oops!) That makes it really hard to get a complete picture of a single property.

Streetscope allows different databases to know they're talking about the same address, even if it's not spelled exactly the same. It returns a geographic location and a parcel ID for matching addresses across databases to enable connections between these datasets and get a true picture of the city.

### What will this do in the future?

* Accept files to geocode as a batch
* Emit performance metrics to indicate when this geocoder varies from other geocoders in geographic distance or ability to match an address
* Generalize for any city that has a reliable address dataset

### Who is this made by?

Lexingteam!

* [Erik Schwartz](https://github.com/eeeschwartz)
* [Lyzi Diamond](https://github.com/lyzidiamond)
* [Livien Yin](https://github.com/livienyin)

With completely indispensable help from Jonathan Hollinger and Shaye Rabold at [Lexington-Fayette Urban County Government](http://lexingtonky.gov/) and David O'Neill, the [Property Valuation Administrator](http://www.fayette-pva.com/)
