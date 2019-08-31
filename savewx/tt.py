from datetime import timedelta
from .request import http_stream, s3_put


def tt_save_for_hr(params, datetime_, to_bucket, folder=None):
    sat = params.get('satellite', 'goes16')
    sattype = params.get('sattype', 'ir')
    storm = params['storm']

    dt = datetime_.replace(minute=2)
    while dt.hour == datetime_.hour:
        relpath = f'{sat}_{sattype}_{storm}_{dt:%Y%m%d%H%M}.jpg'
        url = f'https://www.tropicaltidbits.com/sat/images/{relpath}'

        dest = relpath
        if folder:
            dest = f'{folder}/{relpath}'

        tt_response = http_stream(url)
        s3_put(to_bucket, key=dest, content=tt_response.content)

        dt += timedelta(minutes=5)
