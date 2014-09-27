"""
Tidies up the data downloaded from wikipedia.
"""

import pandas
import re
import locale

# set the locale for converting numeric data from human readable interpretation
locale.setlocale(locale.LC_NUMERIC, "")

data = pandas.read_csv("data/raw/longestflights.csv")

# select only certain columns
data = data[[0, 1, 2, 3, 5, 6, 7]]
# rename them
data.columns = ["ranking",
                "from",
                "to",
                "airline",
                "distance",
                "duration",
                "aircraftType"]



# this function removes numbers that are in square brackets. Wikipedia likes to
# put a lot of these in tables
def replace_references(s):
    return re.sub("\[[0-9]*\]", "", s)

# apply this function to remove those references from the data
data = data.apply(lambda x: x.apply(replace_references), 
                  axis = 0)

# there are some columns that have two rows in them, for example they have a
# note about the aircraft type changing. take just the first item in cases like
# this
def first_row(cell):
    return cell.split("\n")[0]

data.duration = data.duration.apply(first_row)
data.aircraftType = data.aircraftType.apply(first_row)

# select just the range in kilometres
def distance_kilometres(cell):
    kilometres = cell.split(" ")[0]
    return locale.atoi(kilometres)
data.distance = data.distance.apply(distance_kilometres)

# convert the ranks to numbers
def convert_rank(cell):
    return int(cell.split(" ")[0])

data.ranking = data.ranking.apply(convert_rank)

# the final thing that I want to do is convert the duration to decimal
# representation
def decimal_hours(cell):
    matcher = re.match(r"([0-9]+).* ([0-9]+).*", cell)
    hour = float(matcher.group(1))
    minute = float(matcher.group(2))
    return hour + (minute / 60)
data.duration = data.duration.apply(decimal_hours)

# there is some inconsistency in the data, jo'burg airport has a few different
# names, so does dubai. remove these.
def remove_inconsistency(cell):
    if re.match("Dubai", cell):
        return "Dubai"
    if re.match("Johannesburg", cell):
        return "Johannesburg"
    else:
        return cell

data['from'] = data['from'].apply(remove_inconsistency)
data['to'] = data['to'].apply(remove_inconsistency)

# output to csv
data.to_csv("data/processed/clean_data.csv", index = False)
