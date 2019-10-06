from datetime import datetime, timedelta

from savewx.request import http_stream, s3_put, RequestException


def himawari_tgt_save(sattype, s3_bucket, folder=None, go_back_hours=21, delta_min=10):
    url = f'https://weather-models.info/latest/images/himawari/target/{sattype}'
    current_time = datetime.utcnow()

    save_time = (current_time - timedelta(hours=go_back_hours)).replace(minute=0, second=0)
    appender = sattype if sattype == 'vis' else 'color'
    while save_time < current_time:
        save_url = url + f'/{save_time:%H}/{save_time:%H%M%S}-{appender}.png'
        try:
            response = http_stream(save_url, retries=None)
            filename = f'Himawari-target-{save_time:%Y%m%d%H%M%S}-{appender}.png'

            if folder:
                filename = f'{folder}/{filename}'

            s3_put(s3_bucket, filename, response.content)
        except RequestException:
            pass

        save_time += timedelta(minutes=delta_min)

# `if __name__ == '__main__':
#     himawari_tgt_save('ir', 'savewx-dump', 'Faxai-IR', go_back_hours=16)
#     himawari_tgt_save('vis', 'savewx-dump', 'Faxai-VIS', go_back_hours=16)