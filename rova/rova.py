import random
import json
import requests

__title__ = "rova"
__version__ = "0.0.2"
__author__ = "Gido Hakvoort"
__license__ = "MIT"


class Rova(object):
    """
    Object using ROVA's API-method.
    See https://www.rova.nl/
    """

    def __init__(self, zip_code, house_number):
        """
        To fetch the garbage calendar, you need to set a zip_code and house_number.
        A random id will automatically be generated
        """
        self.zip_code = zip_code
        self.house_number = house_number
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
        return json.loads(response.text)

    def get_cookies(self):
        """Generate cookies for ROVA API request"""
        return {'RovaLc_inwoners': "{{'Id':{},'ZipCode':'{}', \
        'HouseNumber':'{}', 'HouseAddition':'','Municipality':'', \
        'Province':'', 'Firstname':'','Lastname':'','UserAgent':'', \
        'School':'', 'Street':'','Country':'','Portal':'', \
        'Lat':'','Lng':'', 'AreaLevel':'','City':'','Ip':''}}"
        .format(self.rova_id, self.zip_code, self.house_number)}



