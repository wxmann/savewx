from datetime import datetime

from savewx.request import http_stream, s3_put, RequestException


def ssd_save(params, to_bucket, folder=None):
    sattype = params['sattype']
    storm = params['storm']

    dt = datetime.utcnow()
    relpath = f'{storm}_{sattype}_{dt:%Y%m%d%H%M%S}.gif'
    url = f'https://www.ssd.noaa.gov/PS/TROP/floaters/{storm}/imagery/{sattype}-animated.gif'

    dest = relpath
    if folder:
        dest = f'{folder}/{relpath}'

    try:
        ssd_response = http_stream(url)
        s3_put(to_bucket, key=dest, content=ssd_response.content)
    except RequestException:
        print(f'Cannot save SSD image for storm {storm} at {dt:%Y%m%d%H%M%S}Z')
