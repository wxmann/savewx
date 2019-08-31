import os
from datetime import datetime, timedelta

from savewx.tcinfo import satellite_position
from savewx.ghcc_params import with_defaults
from savewx.ghcc import ghcc_save
from savewx.tt import tt_save_for_hr

"""
example event JSON:
{
    "storm_id": "al052019",
    "params": {
        "satellite": "GOESEastconusband13",
        "zoom": 1,
        "width": 1200,
        "height": 900,
        "palette": "ir10.pal"
    },
    "folder": "blah"
}
"""
def ghcc_satellite(event, context):
    storm_id = event['storm_id']
    bucket = os.getenv('bucket')

    params = with_defaults(event['params'])
    lat, lon = satellite_position(storm_id)
    params['lat'] = lat
    params['lon'] = lon

    folder = event.get('folder', None)
    ghcc_save(params, to_bucket=bucket, folder=folder)


"""
example event JSON:
{
    "storm_id": "05L",
    "params": {
        "satellite": "goes16",
        "sattype": "ir",
        "datetime": "2010-08-03T10:00:00"
    },
    "folder": "blah"
}
"""
def tt_satellite(event, context):
    storm_id = event['storm_id']
    bucket = os.getenv('bucket')

    params = event['params']
    params['storm'] = storm_id
    datetime_ = params.get('datetime', None)

    if not datetime_:
        datetime_ = datetime.utcnow() - timedelta(hours=1)
    else:
        datetime_ = datetime.strptime(datetime_, '%Y-%m-%dT%H:%M:%S')

    folder = event.get('folder', None)
    tt_save_for_hr(params, datetime_=datetime_, to_bucket=bucket, folder=folder)


# if __name__ == '__main__':
#     os.environ['bucket'] = 'savewx-dump'
#     tt_satellite({
#         "storm_id": "05L",
#         "params": {
#             "satellite": "goes16",
#             "sattype": "ir",
#             "datetime": "2019-08-31T05:00:00"
#         },
#         "folder": "Dorian_TT_IR"
#     }, None)
