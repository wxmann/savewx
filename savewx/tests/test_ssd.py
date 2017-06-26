import os
from unittest import mock

from nose.tools import assert_raises

from savewx import ssd
from savewx.core import SaveException
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

    dummy_img_response = mock.MagicMock()
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


@mock.patch('savewx.ssd.save_image')
@mock.patch('savewx.ssd.requests')
@mock.patch('savewx.core.requests')
def test_ssd_successful_lastn_less_than_amt_of_images(dummy_request1, dummy_request2, dummy_save_img):
    ssd_url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/92L/imagery/'
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    dummy_raw_response.url = ssd_url
    with open_resource('ssd_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get = mock.MagicMock()
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'
    types = ['avn', 'rgb']
    ssdsave = ssd.ssd('92L', types, last=2)
    ssdsave(saveloc)

    dummy_request1.get.assert_called_with(ssd_url, params=None, stream=True)
    for type in types:
        for img_template in ('20170618_0715Z-{}.gif', '20170618_0745Z-{}.gif'):
            img = img_template.format(type)
            target = os.path.join(saveloc, 'SSD_{}'.format(img))
            dummy_request2.get.assert_any_call(ssd_url + img, stream=True)
            dummy_save_img.assert_any_call(dummy_img_response, target)


@mock.patch('savewx.ssd.save_image')
@mock.patch('savewx.ssd.requests')
@mock.patch('savewx.core.requests')
def test_ssd_successful_lastn_greater_than_amt_of_images(dummy_request1, dummy_request2, dummy_save_img):
    ssd_url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/92L/imagery/'
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    dummy_raw_response.url = ssd_url
    with open_resource('ssd_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get = mock.MagicMock()
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'
    types = ['avn', 'rgb']
    ssdsave = ssd.ssd('92L', types, last=50)
    ssdsave(saveloc)

    dummy_request1.get.assert_called_with(ssd_url, params=None, stream=True)
    for type in types:
        for img_template in ('20170618_0645Z-{}.gif', '20170618_0715Z-{}.gif', '20170618_0745Z-{}.gif'):
            img = img_template.format(type)
            target = os.path.join(saveloc, 'SSD_{}'.format(img))
            dummy_request2.get.assert_any_call(ssd_url + img, stream=True)
            dummy_save_img.assert_any_call(dummy_img_response, target)


@mock.patch('savewx.ssd.save_image')
@mock.patch('savewx.ssd.requests')
@mock.patch('savewx.core.requests')
def test_ssd_successful_lastn_negative(dummy_request1, dummy_request2, dummy_save_img):
    ssd_url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/92L/imagery/'
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    dummy_raw_response.url = ssd_url
    with open_resource('ssd_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get = mock.MagicMock()
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'
    types = ['avn', 'rgb']
    ssdsave = ssd.ssd('92L', types, last=-2)
    ssdsave(saveloc)

    dummy_request1.get.assert_called_with(ssd_url, params=None, stream=True)
    for type in types:
        for img_template in ('20170618_0715Z-{}.gif', '20170618_0745Z-{}.gif'):
            img = img_template.format(type)
            target = os.path.join(saveloc, 'SSD_{}'.format(img))
            dummy_request2.get.assert_any_call(ssd_url + img, stream=True)
            dummy_save_img.assert_any_call(dummy_img_response, target)


@mock.patch('savewx.ssd.requests')
@mock.patch('savewx.core.requests')
def test_ssd_not_valid_sat_enhancement(dummy_request1, dummy_request2):
    ssd_url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/92L/imagery/'
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    dummy_raw_response.url = ssd_url
    with open_resource('ssd_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get = mock.MagicMock()

    saveloc = '/my/directory'
    types = ['not-valid-type']
    ssdsave = ssd.ssd('92L', types)
    ssdsave(saveloc)

    dummy_request1.get.assert_called_with(ssd_url, params=None, stream=True)
    dummy_request2.get.assert_not_called()


@mock.patch('savewx.ssd.requests')
@mock.patch('savewx.core.requests')
def test_ssd_not_valid_stormid(dummy_request1, dummy_request2):
    ssd_url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/not_valid_storm/imagery/'
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 404
    dummy_raw_response.url = ssd_url
    dummy_request1.get.return_value = dummy_raw_response

    saveloc = '/my/directory'
    types = ['avn']
    ssdsave = ssd.ssd('not_valid_storm', types)
    assert_raises(SaveException, ssdsave, saveloc)

    dummy_request1.get.assert_called_with(ssd_url, params=None, stream=True)
    dummy_request2.get.assert_not_called()


@mock.patch('os.path.isfile', return_value=True)
@mock.patch('savewx.ssd.save_image')
@mock.patch('savewx.ssd.requests')
@mock.patch('savewx.core.requests')
def test_skip_if_file_already_exists(dummy_request1, dummy_request2, dummy_save_img, isfile_func):
    ssd_url = 'http://www.ssd.noaa.gov/PS/TROP/floaters/92L/imagery/'
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    dummy_raw_response.url = ssd_url
    with open_resource('ssd_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get = mock.MagicMock()
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'
    types = ['avn', 'rgb']
    ssdsave = ssd.ssd('92L', types)
    ssdsave(saveloc)

    dummy_request1.get.assert_called_with(ssd_url, params=None, stream=True)
    dummy_request2.get.assert_not_called()
    dummy_save_img.assert_not_called()