"""
Wrapper to get ROVA calendar from Rova's API
Acces to this ROVA API has been simplified since version 0.2.1 of this wrapper
Just use https://www.rova.nl/api/waste-calendar/upcoming?postalcode=1000AA&houseNumber=1&addition=&take=5
with a existing combination of postalcode, housenumber, housenumber addition

Be aware that this API has not been officially published by ROVA.
"""

from datetime import datetime

import random
import requests

__title__ = "rova"
__version__ = "0.3.0"
__author__ = "Gido Hakvoort and synoniem <synoniem@hotmail.com>"
__license__ = "MIT"


class Rova:
    """
    ROVA class
    """

    def __init__(self, zip_code, house_number, house_addition=""):
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
        url = 'https://www.rova.nl/api/waste-calendar/upcoming'

        # request data from rova API and check if garbage is collected at this address
        # requesting with a non-existing postalcode will result in a error message

        response = requests.get(url, params={
            'postalcode': self.zip_code,
            'houseNumber': self.house_number,
            'addition': self.house_addition,
            'take': '1',
            })

        response.raise_for_status()

        rova_response = response.text.strip()
        if rova_response != '[]':
            rova_response = "OK"
        return rova_response == "OK"

    def get_calendar_items(self, take=5):
        """
        Get next pickup date for each garbage types
        """
        url = 'https://www.rova.nl/api/waste-calendar/upcoming'
        # request data from rova API and save response first 5 items (default)
        response = requests.get(url, params={
            'postalcode': self.zip_code,
            'houseNumber': self.house_number,
            'addition': self.house_addition,
            'take': take,
            })

        response.raise_for_status()

        rova_response = response.json()

        items = []
        types = []
        # add next pickup date for each garbage type
        for item in rova_response:
            date = datetime.strptime(item["date"], "%Y-%m-%dT%H:%M:%SZ")
            date = date.strftime("%Y-%m-%dT%H:%M:%S")
            garbage_type = item["garbageTypeCode"].upper()

            items.append({
                'GarbageTypeCode': garbage_type,
                'Date': date
                })
            types.append(garbage_type)
        return items
