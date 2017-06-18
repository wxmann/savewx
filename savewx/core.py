import requests

from .utils import save_image


class HTTPImageSave(object):
    def __init__(self, url, queryparams=None,
                 process_response=None, failure_callback=None):
        self.url = url
        self.queryparams = queryparams
        self.process_response = process_response or save_image
        self.failure_callback = failure_callback

    def __call__(self, saveloc):
        # TODO: add retry policy
        response = requests.get(self.url, params=self.queryparams, stream=True)
        if response.status_code != 200:
            if self.failure_callback is not None:
                self.failure_callback(response)
            else:
                raise SaveException("Expected status 200, got {}".format(response.status_code))
        else:
            self.process_response(response, saveloc)


class SaveException(Exception):
    pass
