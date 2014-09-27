# Longest flights in the world

Using data from [wikipedia](http://en.wikipedia.org/wiki/Non-stop_flight),
can we plot the routes using D3?

## Getting the data

You can easily scrape wiki tables using Google Spreadsheets.
I've loaded the data into [my spreadsheet](https://docs.google.com/spreadsheets/d/1jbcCzAhUqRFAtlN6T21bWQaP17RnSyWEROZCPRwaRO4/edit#gid=0) using this formula.

```
=IMPORTHTML("http://en.wikipedia.org/wiki/Non-stop_flight", "table", 2)
```

This is saved in `longestflights.csv`.

## Cleaning the data

The `clean_data.py` script tidies up the data and writes it out to `data/processed/clean_data.py`.
Should be nicer to work with.
