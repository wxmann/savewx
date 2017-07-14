import os
import re
import warnings
from datetime import datetime
from functools import partial

import requests

try:
    # PYTHON 2
    import urlparse
except ImportError:
    # PYTHON 3
    import urllib.parse as urlparse

from .utils import get_links, save_image, skip_save
from .core import HTTPImageSave


def ssd(stormid, enhancements, last=1):
    url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/{}/imagery/'.format(stormid)
    process_response = partial(extract_img_from_response, enhancements=enhancements, last=last)
    return HTTPImageSave(url, process_response=process_response)


def ssd_animated(stormid, enhancement):
    url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/{}/imagery/{}-animated.gif'.format(stormid, enhancement.lower())
    return HTTPImageSave(url, process_response=direct_save_timed_img(enhancement))


SSD_TIME_REGEX = r'\d{8}_\d{4}Z'


def extract_img_from_response(response, saveloc, on_file_exists,
                              enhancements, last):
    def filter_imgs(link):
        if re.search(SSD_TIME_REGEX, link) is None:
            return False
        else:
            for enh in enhancements:
                if enh.lower() in link:
                    return True
        return False

    found_imgs = get_links(response.text, filter_imgs)

    if not found_imgs:
        warnings.warn("Cannot find image links under: {} with "
                      "one of enhancements: {}".format(response.url, enhancements))
        return

    for enh in enhancements:
        imgs_for_enh = [img for img in found_imgs if enh in img]
        go_back = min(abs(last), len(imgs_for_enh))

        for img_link in imgs_for_enh[-go_back:]:
            filename = 'SSD_{}'.format(img_link)
            save_to = os.path.join([saveloc, filename])
            if not skip_save(save_to, on_file_exists):
                direct_img_response = requests.get(urlparse.urljoin(response.url, img_link), stream=True)
                save_image(direct_img_response, save_to)


def direct_save_timed_img(enhancement):

    def saveit(response, savedir, on_file_exists):
        now = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = 'SSD_{}-{}.gif'.format(enhancement.upper(), now)
        saveloc = os.sep.join([savedir, filename])

        if not skip_save(saveloc, on_file_exists):
            save_image(response, saveloc)

    return saveit
