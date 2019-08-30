import pandas as pd


def atcf(storm_id, convert_cols=True):
    link = f'https://ftp.nhc.noaa.gov/atcf/btk/b{storm_id}.dat'
    cols = [
        'basin', 'cy', 'yyyymmddhh', 'technum', 'tech', 'tau', 'lat', 'lon',
        'vmax', 'mslp', 'ty', 'rad', 'windcode', 'rad1', 'rad2', 'rad3', 'rad4',
        'pouter', 'router', 'rmw', 'gusts', 'eye', 'subregion', 'maxseas', 'initials',
        'dir', 'speed', 'stormname', 'depth', 'seas', 'seascode', 'seas1', 'seas2',
        'seas3', 'seas4', 'userdefine1', 'userdata1', 'userdefine2', 'userdata2',
        'userdefine3', 'userdata3', 'userdefine4', 'userdata4', 'userdefine5', 'userdata5'
    ]

    ret = pd.read_csv(link, header=None, names=cols, dtype={'yyyymmddhh': str})

    if convert_cols:
        ret['lat'] = pd.to_numeric(ret.lat.str[:-1]) * ret.lat.apply(lambda r: 1 if r[-1] == 'N' else -1) / 10
        ret['lon'] = pd.to_numeric(ret.lon.str[:-1]) * ret.lon.apply(lambda r: 1 if r[-1] == 'E' else -1) / 10
        ret['ts'] = pd.to_datetime(ret.yyyymmddhh.str.strip(), format='%Y%m%d%H')

    return ret


def satellite_position(storm_id):
    records = atcf(storm_id)
    return calc_center(records)


def calc_center(records):
    maxtime = records.ts.max()
    prevtime = records.ts.max() - pd.Timedelta('6 hr')

    maxtimelatlon = records[records.ts == maxtime].head(1)[['lat', 'lon']].values
    prevtimelatlon = records[records.ts == prevtime].head(1)[['lat', 'lon']].values

    current_time = pd.Timestamp.utcnow()
    ret = maxtimelatlon

    if current_time - maxtime.tz_localize('UTC') > pd.Timedelta('3 hr'):
        ret = maxtimelatlon + (maxtimelatlon - prevtimelatlon) / 2

    return ret[0]