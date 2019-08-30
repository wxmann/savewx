import os

from savewx.tcinfo import satellite_position
from savewx.ghcc_params import with_defaults
from savewx.ghcc import ghcc_save

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

    folder = None
    if 'folder' in event:
        folder = event['folder']

    ghcc_save(params, to_bucket=bucket, folder=folder)


# if __name__ == '__main__':
#     os.environ['bucket'] = 'hurricane-dorian'
#     ghcc_satellite({
#         "storm_id": "al052019",
#         "params": {
#             "satellite": "GOESEastconusband13",
#             "zoom": 1,
#             "width": 1200,
#             "height": 900,
#             "palette": "ir10.pal"
#         },
#         "folder": "hurricane"
#     }, None)
