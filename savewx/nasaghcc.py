import os
import re
from datetime import datetime, timedelta

import requests
try:
    # PYTHON 2
    import urlparse
except ImportError:
    # PYTHON 3
    import urllib.parse as urlparse

from .core import HTTPImageSave, SaveException
from .utils import save_image, get_image_srcs

NASA_MSFC_BASE_URL = 'https://weather.msfc.nasa.gov'

GOES_16_BASE_URL = '{}/cgi-bin/get-abi?'.format(NASA_MSFC_BASE_URL)


def goes16(sat, latlon=None, xy=None,
           bgmap='standard', zoom=1, past=0,
           palette=None, colorbar=0, mapcolor='black',
           quality=90, width=1000, height=800):

    if not latlon and not xy:
        raise ValueError("Must provide either one of latlon or xy")

    params = {
        'satellite': sat,
        'map': bgmap,
        'zoom': zoom,
        'past': past,
        'colorbar': colorbar,
        'mapcolor': mapcolor,
        'quality': quality,
        'width': width,
        'height': height,
        'type': 'Image'
    }

    if latlon:
        params['lat'], params['lon'] = latlon
    elif xy:
        params['x'], params['y'] = xy

    if palette is not None:
        params['palette'] = palette

    return HTTPImageSave(GOES_16_BASE_URL, params, process_response=ghcc_dynamic_imgsave)


def ghcc_dynamic_imgsave(response, saveloc):
    img_urls = get_image_srcs(response.text)

    if not img_urls:
        raise SaveException("Cannot parse an image URL for response: {}".format(response))

    img_url_to_save = urlparse.urljoin(NASA_MSFC_BASE_URL, img_urls[0])

    img_ts = ghcc_extract_time(img_url_to_save)
    img_file = 'GHCC_{}.jpg'.format(img_ts.strftime('%Y%m%d_%H%M'))
    saveloc_file = os.sep.join([saveloc, img_file])

    response = requests.get(img_url_to_save, stream=True)
    return save_image(response, saveloc_file)


def ghcc_extract_time(url):
    regex = 'GOES(\d{2})(\d{2})(\d{4})(\d{1,3})'
    found = re.search(regex, url)
    if not found:
        raise url.InvalidResourceError("Cannot find date-time for file: {0}".format(url))

    found_hour = int(found.group(1))
    found_min = int(found.group(2))
    found_year = int(found.group(3))
    found_dayofyr = int(found.group(4))

    day_before_year = datetime(year=found_year - 1, month=12, day=31)
    current_day = day_before_year + timedelta(days=found_dayofyr)

    return datetime(year=found_year, month=current_day.month, day=current_day.day,
                    hour=found_hour, minute=found_min)
