import os
from unittest import mock

from savewx import ssd
from savewx.tests._testcommon import open_resource


@mock.patch('savewx.ssd.save_image')
@mock.patch('savewx.ssd.requests')
@mock.patch('savewx.core.requests')
def test_ssd_successful(dummy_request1, dummy_request2, dummy_save_img):
    ssd_url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/92L/imagery/'
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    dummy_raw_response.url = ssd_url
    with open_resource('ssd_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock(name='img')
    dummy_img_response.status_code = 200
    dummy_request2.get = mock.MagicMock()
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'
    types = ['avn', 'rgb']
    ssdsave = ssd.ssd('92L', types)
    ssdsave(saveloc)

    dummy_request1.get.assert_called_with(ssd_url, params=None, stream=True)
    for type in types:
        img = '20170618_0745Z-{}.gif'.format(type)
        target = os.path.join(saveloc, 'SSD_{}'.format(img))
        dummy_request2.get.assert_any_call(ssd_url + img, stream=True)
        dummy_save_img.assert_any_call(dummy_img_response, target)


def mock_get_call(url, params=None, **kwargs):
    return url