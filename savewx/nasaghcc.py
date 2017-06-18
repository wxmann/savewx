import os
import re
import warnings
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

GOES_16_BASE_URL = urlparse.urljoin(NASA_MSFC_BASE_URL, '/cgi-bin/get-abi')

GOES_LEGACY_BASE_URL = urlparse.urljoin(NASA_MSFC_BASE_URL, '/cgi-bin/get-goes')


def goes16(sat, position, uselatlon=True, **kwargs):
    params = _assemble_params(sat, position, uselatlon, **kwargs)
    return HTTPImageSave(GOES_16_BASE_URL, params, process_response=ghcc_dynamic_imgsave)


def goeslegacy(sat, info, position, uselatlon=True, **kwargs):
    params = _assemble_params(sat, position, uselatlon, info=info, **kwargs)
    return HTTPImageSave(GOES_LEGACY_BASE_URL, params, process_response=ghcc_dynamic_imgsave)


default_params = {
    'map': 'standard',
    'zoom': 1,
    'past': 0,
    'colorbar': 0,
    'mapcolor': 'black',
    'quality': 90,
    'width': 1000,
    'height': 800,
    'type': 'Image'
}


def _assemble_params(sat, position, uselatlon, info=None, **kwargs):
    if len(position) != 2:
        raise ValueError("Position must be an x,y or lat,lon pair")

    params = kwargs.copy()
    for k in default_params:
        if k not in params:
            params[k] = default_params[k]

    params['satellite'] = sat

    if uselatlon:
        params['lat'], params['lon'] = position[0], position[1]
    else:
        params['x'], params['y'] = position[0], position[1]
    if info is not None:
        params['info'] = info

    if params['type'] != 'Image':
        warnings.warn('Only Image type supported at this time. Default to Image type')
        params['type'] = 'Image'

    return params


def ghcc_dynamic_imgsave(response, saveloc):
    goes_jpg_filter = lambda img: 'GOES' in img and '.jpg' in img
    img_urls = get_image_srcs(response.text, goes_jpg_filter)

    if not img_urls:
        raise SaveException(
            "Cannot parse an image URL for response. Text of response: \n\n{}".format(response.text))

    img_url_to_save = urlparse.urljoin(NASA_MSFC_BASE_URL, img_urls[0])

    img_ts = ghcc_extract_time(img_url_to_save)
    img_file = 'GHCC_{}.jpg'.format(img_ts.strftime('%Y%m%d_%H%M'))
    saveloc_file = os.sep.join([saveloc, img_file])

    response = requests.get(img_url_to_save, stream=True)
    return save_image(response, saveloc_file)


def ghcc_extract_time(url):
    regex = 'GOES(\d{2})(\d{2})(\d{4})(\d{1,3})(.{6})\.jpg'
    found = re.search(regex, url)
    if not found:
        raise SaveException("Cannot find date-time for file: {0}".format(url))

    found_hour = int(found.group(1))
    found_min = int(found.group(2))
    found_year = int(found.group(3))
    found_dayofyr = int(found.group(4))

    day_before_year = datetime(year=found_year - 1, month=12, day=31)
    current_day = day_before_year + timedelta(days=found_dayofyr)

    return datetime(year=found_year, month=current_day.month, day=current_day.day,
                    hour=found_hour, minute=found_min)
