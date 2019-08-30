import requests

from savewx.logs import logger
from .utils import save_image, skip_save


class HTTPImageSave(object):
    def __init__(self, url, queryparams=None,
                 process_response=None, failure_callback=None,
                 on_file_exists='skip'):
        self.url = url
        self.queryparams = queryparams
        self.process_response = process_response or default_save
        self.failure_callback = failure_callback
        self.on_file_exists = on_file_exists

    def __call__(self, saveloc):
        # TODO: add retry policy
        try:
            response = requests.get(self.url, params=self.queryparams, stream=True)
            if response.status_code != 200:
                if self.failure_callback is not None:
                    self.failure_callback(response)
                else:
                    logger.info("Expected status 200, got {} for url: {}".format(response.status_code, response.url))
                    # raise SaveException("Expected status 200, got {}".format(response.status_code))
            else:
                self.process_response(response, saveloc, self.on_file_exists)
        except Exception as e:
            logger.error(e)


def default_save(response, saveloc, on_file_exists):
    if not skip_save(saveloc, on_file_exists):
        save_image(response, saveloc)


class SaveException(Exception):
    pass
