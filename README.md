# ROVA
API wrapper for ROVA calendar

See https://www.rova.nl/

## Create a new connection by supplying your zip code and house number

```
r = rova.Rova(YOUR_ZIP_CODE, YOUR_HOUSE_NUMBER, [YOUR_HOUSE_NUMBER_ADDITION])
```

## API Request
Check wether ROVA collects garbage at the given zip code and house number 
```
def is_rova_area():
```

These methods return the parsed JSON response as a dict.
```
def get_calendar_items():
```

## TODO
* Parse ROVA response
* Add API documentation
