# ROVA
Wrapper to get ROVA calendar from Rova's Mobile App or Website
See https://www.rova.nl/

## Create a new connection by supplying your zip code and house number

```
r = rova.Rova(YOUR_ZIP_CODE, YOUR_HOUSE_NUMBER, [YOUR_HOUSE_NUMBER_ADDITION], [ROVA_DATA_SOURCE])
```

ROVA_DATA_SOURCE can be set to indicate which data source should be used. Possible options are ```site``` and ```api```.
- ```site``` will get the data using Rova's Website-method. See https://www.rova.nl/
- ```api``` will get the data using Rova's Mobile App-method. See https://www.rova.nl/inwoners/faq/600/detail/

## API Request
Check wether ROVA collects garbage at the given zip code and house number 
```
def is_rova_area():
```

This method return the parsed JSON response as a list.
```
def get_calendar_items():
```

## TODO
* Add API documentation
