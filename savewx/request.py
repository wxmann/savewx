import requests
import boto3
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def retry_session(retries, session=None, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def http_stream(url, queryparams=None, retries=5, expected_response=200):
    print(f'Making request to URL: {url} with query parameters: {queryparams}')
    try:
        if not retries:
            response = requests.get(url, params=queryparams, stream=True)
        else :
            session = retry_session(retries)
            response = session.get(url, params=queryparams, stream=True)

        if response is None:
            raise RequestException(f'Expected response to exist for url {url}')
        elif response.status_code != expected_response:
            raise RequestException(
                f'Expected status {expected_response}, got {response.status_code} for url: {response.url}')
        return response

    except Exception as e:
        print(e)
        raise


def s3_put(bucket_name, key, content):
    print(f'Saving file: {key} to S3 bucket: {bucket_name}')
    s3_object = boto3.resource('s3').Object(bucket_name, key)
    s3_object.put(Body=content)



class RequestException(Exception):
    pass