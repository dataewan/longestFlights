"""
Finds locations for the airports
"""

from geopy.geocoders import Nominatim
import pandas
import time

geocoder = Nominatim()

data = pandas.read_csv("data/processed/clean_data.csv")


def geocode(cell):
    # output messages
    print "geocoding %s" % cell
    # don't hit the api too often, wait for a bit to be polite
    time.sleep(1)
    # stick airport on the end, so we get the airport where possible. probably
    # spurious level of accuracy
    geocoded = geocoder.geocode("%s airport" % cell)
    # if the geocoding doesn't work, it returns a None, check for that first
    # and return just the aiport name
    if geocoded is not None:
        return pandas.Series({
            "%s_latitude" % column_name : geocoded.latitude,
            "%s_longitude" % column_name : geocoded.longitude
        })
    else:
        return pandas.Series({
            "%s_latitude" % column_name : cell,
            "%s_longitude" % column_name : cell
        })

# you can't pass variables to the apply function, so this column_name variable
# is defined here at a global context
column_name = "from"
# apply the geocoding function
x = data['from'].apply(geocode)
# stick this onto the data
data = data.join(x)

# and do the same for the `to` data
column_name = "to"
x = data['to'].apply(geocode)
data = data.join(x)

# write out to csv
data.to_csv("data/processed/geocoded.csv")
