from request import s3_retrieve
import re
from datetime import datetime


def himawari_sattime_gt(min_dt_str):
    def pred(file):
        regex = re.compile(r'\d{14}')
        match = regex.search(file)
        dt = datetime.strptime(match.group(0), '%Y%m%d%H%M%S')
        min_dt = datetime.strptime(min_dt_str, '%Y%m%d%H%M')
        return dt > min_dt

    return pred


if __name__ == '__main__':
    s3_retrieve('savewx-dump', 'Goni-IR-closeup',
                dest='/Users/jitang/Downloads/savewx-dump',
                key_pred=himawari_sattime_gt('202010311200'))
