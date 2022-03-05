# ROVA
Wrapper to get ROVA calendar from Rova's API
Acces to ROVA API has been simplified since version 0.2.1 of this wrapper
Just use https://www.rova.nl/api/waste-calendar/upcoming?postalcode=1000AA&houseNumber=1&addition=&take=5
with a existing combination of postalcode, housenumber, [housenumber addition]

take=5 means that five upcoming dates are returned, min is 1 max unknown

Be aware that ROVA API has not been officially published by ROVA.

## Create a new connection by supplying your zip code and house number

```
r = rova.Rova(YOUR_ZIP_CODE, YOUR_HOUSE_NUMBER, [YOUR_HOUSE_NUMBER_ADDITION])
```

## API Request
Check wether ROVA collects garbage at the given zip code and house number and addition
```
def is_rova_area():
```

This method return the parsed JSON response as a list.
```
def get_calendar_items([TAKE]):
```