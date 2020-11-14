"""
Wrapper to get ROVA calendar from Rova's Mobile App or Website
See https://www.rova.nl/
"""

from datetime import datetime

import random
import requests

__title__ = "rova"
__version__ = "0.2.1"
__author__ = "Gido Hakvoort"
__license__ = "MIT"

ROVA_SOURCE_SITE = 'site'
ROVA_SOURCE_API = 'api'

class Rova:
    """
    ROVA class directing requests to provided datasource
    """

    def __init__(self, zip_code, house_number, house_addition='', source=ROVA_SOURCE_API):

        if source == ROVA_SOURCE_SITE:
            self.source = RovaSourceWebsite(zip_code, house_number, house_addition)
        else:
            self.source = RovaSourceAPI(zip_code, house_number, house_addition)

    def is_rova_area(self):
        """
        Check with data source if ROVA collects garbage at this address
        """
        return self.source.is_rova_area()

    def get_calendar_items(self):
        """
        Request ROVA calendar items from selected data source
        """
        return self.source.get_calendar_items()


class AbstractRovaSource:
    """
    Abstract class holding location data
    """

    def __init__(self, zip_code, house_number, house_addition):
        """
        To fetch the garbage calendar, you need to set a zip_code and house_number.
        """
        self.zip_code = zip_code.replace(' ', '')
        self.house_number = house_number.strip()
        self.house_addition = house_addition.strip()

    def is_rova_area(self):
        """
        Check if ROVA collects garbage at this address
        """

    def get_calendar_items(self):
        """
        Request ROVA calendar items
        """


class RovaSourceWebsite(AbstractRovaSource):
    """
    DataSource using ROVA's Website-method.
    See https://www.rova.nl/
    """

    def __init__(self, zip_code, house_number, house_addition):
        """
        A random id will automatically be generated
        """
        super().__init__(zip_code, house_number, house_addition)
        self.rova_id = random.randint(10000, 30000)

    def is_rova_area(self):
        """
        Check if ROVA collects garbage at this address
        """
        url = 'https://www.rova.nl/api/visitor'

        # request data from rova server and check if rova collects garbage at this address
        response = requests.post(url, data = {
            'HouseNumber': self.house_number,
            'ZipCode': self.zip_code,
            'Ip': 'b',
            'Portal': 'inwoners',
            'UserAgent': 'text'
            })

        response.raise_for_status()

        rova_response = response.json()

        return rova_response.get('IsRovaArea')

    def get_calendar_items(self):
        """
        Request ROVA calendar items
        """
        url = 'https://www.rova.nl/api/TrashCalendar/GetCalendarItems'

        # request data from rova server and return response in json
        response = requests.get(url, params={'portal': 'inwoners'}, cookies=self.get_cookies())

        response.raise_for_status()

        rova_response = response.json()

        items = []
        types = []

        # add next pickup date for each garbage type
        for item in rova_response:
            date = datetime.strptime(item["Date"], "%Y-%m-%dT%H:%M:%S")
            garbage_type = item["GarbageTypeCode"].upper()

            if garbage_type not in types:
                items.append({
                    'GarbageTypeCode': garbage_type,
                    'Date': date.strftime("%Y-%m-%dT%H:%M:%S")
                })
                types.append(garbage_type)

        return items

    def get_cookies(self):
        """Generate cookies for ROVA API request"""
        return {'RovaLc_inwoners': "{{'Id':{},'ZipCode':'{}', \
        'HouseNumber':'{}', 'HouseAddition':'{}','Municipality':'', \
        'Province':'', 'Firstname':'','Lastname':'','UserAgent':'', \
        'School':'', 'Street':'','Country':'','Portal':'', \
        'Lat':'','Lng':'', 'AreaLevel':'','City':'','Ip':''}}"
        .format(self.rova_id, self.zip_code, self.house_number, self.house_addition)}


class RovaSourceAPI(AbstractRovaSource):
    """
    Object using ROVA's app API-methods
    https://play.google.com/store/apps/details?id=nl.quintor.mip.android&hl=en
    https://www.rova.nl/inwoners/faq/600/detail/
    """

    API_KEY = '5ef443e778f41c4f75c69459eea6e6ae0c2d92de729aa0fc61653815fbd6a8ca'

    def __init__(self, zip_code, house_number, house_addition):
        """
        The current API_KEY from the ROVA app will be used
        """
        super().__init__(zip_code, house_number, house_addition)

        self.api_key = self.API_KEY

    def is_rova_area(self):
        """
        Check if ROVA collects garbage at this address
        """
        url = 'http://api.inzamelkalender.rova.nl/webservices/appsinput/'

        # request data from rova api and check if rova collects garbage at this address
        response = requests.get(url, params = {
            'apikey': self.api_key,
            'method': 'tinyPostcodeCheck',
            'postcode': self.zip_code,
            'huisnummer': self.house_number,
            'toevoeging':self.house_addition
            })

        response.raise_for_status()

        rova_response = response.text.strip()

        return rova_response == "OK"

    def get_calendar_items(self):
        """
        Get next pickup date for each garbage types
        """
        url = 'http://api.inzamelkalender.rova.nl/webservices/appsinput/'

        # request data from rova API and save response in year items
        response = requests.get(url, params = {
            'toevoeging' : self.house_addition,
            'huisnummer': self.house_number,
            'postcode': self.zip_code,
            'apikey': self.api_key,
            'method': 'postcodecheck',
            'platform': 'pc',
            'street': '',
            })

        response.raise_for_status()

        rova_response = response.json()

        today = datetime.now()

        items = []
        types = []

        # add next pickup date for each garbage type
        for item in rova_response['data']['ophaaldagen']['data']:
            date = datetime.strptime(item["date"], "%Y-%m-%d")
            garbage_type = item["type"].upper()

            # only add pickup dates in the future
            if date >= today and garbage_type not in types:
                items.append({
                    'GarbageTypeCode': garbage_type,
                    'Date': date.strftime("%Y-%m-%dT%H:%M:%S")
                })
                types.append(garbage_type)

        return items
