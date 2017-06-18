import os
from datetime import datetime
from unittest import mock

from nose.tools import assert_raises

from savewx import nasaghcc
from savewx.core import SaveException
from savewx.nasaghcc import GOES_16_BASE_URL, NASA_MSFC_BASE_URL, GOES_LEGACY_BASE_URL
from savewx.tests._testcommon import open_resource


@mock.patch('savewx.nasaghcc.save_image')
@mock.patch('savewx.nasaghcc.requests')
@mock.patch('savewx.core.requests')
def test_goes_16_successful(dummy_request1, dummy_request2, dummy_save_img):
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    with open_resource('ghcc_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'

    sat = 'GOESEastconusband02'
    xy = (200, 55)
    goes16save = nasaghcc.goes16(sat, xy, uselatlon=False)
    goes16save(saveloc)

    target = os.sep.join([saveloc, 'GHCC_20170617_0017.jpg'])
    assert_correct_goes16_api_call(dummy_request1, sat, xy, uselatlon=False)
    dummy_request2.get.assert_called_with(NASA_MSFC_BASE_URL + '/goes/abi/dynamic/GOES001720171689nSPoh.jpg',
                                          stream=True)
    dummy_save_img.assert_called_with(dummy_img_response, target)


@mock.patch('savewx.nasaghcc.save_image')
@mock.patch('savewx.nasaghcc.requests')
@mock.patch('savewx.core.requests')
def test_goes_legacy_successful(dummy_request1, dummy_request2, dummy_save_img):
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    with open_resource('ghcc_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'

    sat = 'GOES-E CONUS'
    info = 'ir'
    xy = (200, 55)
    goeslegacysave = nasaghcc.goeslegacy(sat, info, xy, uselatlon=False)
    goeslegacysave(saveloc)

    target = os.sep.join([saveloc, 'GHCC_20170617_0017.jpg'])
    assert_correct_goeslegacy_api_call(dummy_request1, sat, info, xy, uselatlon=False)
    dummy_request2.get.assert_called_with(NASA_MSFC_BASE_URL + '/goes/abi/dynamic/GOES001720171689nSPoh.jpg',
                                          stream=True)
    dummy_save_img.assert_called_with(dummy_img_response, target)


@mock.patch('savewx.nasaghcc.ghcc_dynamic_imgsave')
@mock.patch('savewx.core.requests')
def test_goes_save_with_kwargs(dummy_request1, dummy_save_img):
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    with open_resource('ghcc_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    saveloc = '/my/directory'

    sat = 'GOES-E CONUS'
    info = 'ir'
    xy = (200, 55)
    goeslegacysave = nasaghcc.goeslegacy(sat, info, xy, uselatlon=False, past=5, palette='ir2.pal')
    goeslegacysave(saveloc)

    assert_correct_goeslegacy_api_call(dummy_request1, sat, info, xy, uselatlon=False,
                                       past=5, palette='ir2.pal')
    dummy_save_img.assert_called_with(dummy_raw_response, saveloc)


@mock.patch('savewx.nasaghcc.ghcc_dynamic_imgsave')
@mock.patch('savewx.core.requests')
def test_goes_save_handle_animation_kwarg(dummy_request1, dummy_save_img):
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    with open_resource('ghcc_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    saveloc = '/my/directory'

    sat = 'GOES-E CONUS'
    info = 'ir'
    xy = (200, 55)
    goeslegacysave = nasaghcc.goeslegacy(sat, info, xy, uselatlon=False, type='animation')
    goeslegacysave(saveloc)

    assert_correct_goeslegacy_api_call(dummy_request1, sat, info, xy, uselatlon=False)
    dummy_save_img.assert_called_with(dummy_raw_response, saveloc)


@mock.patch('savewx.nasaghcc.ghcc_dynamic_imgsave')
@mock.patch('savewx.core.requests')
def test_goes_save_use_latlon(dummy_request1, dummy_save_img):
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    with open_resource('ghcc_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    saveloc = '/my/directory'

    sat = 'GOES-E CONUS'
    info = 'ir'
    xy = (200, 55)
    goeslegacysave = nasaghcc.goeslegacy(sat, info, xy, uselatlon=True)
    goeslegacysave(saveloc)

    assert_correct_goeslegacy_api_call(dummy_request1, sat, info, xy, uselatlon=True)
    dummy_save_img.assert_called_with(dummy_raw_response, saveloc)


@mock.patch('savewx.nasaghcc.save_image')
@mock.patch('savewx.nasaghcc.requests')
@mock.patch('savewx.core.requests')
def test_goes_legacy_failure(dummy_request1, dummy_request2, dummy_save_img):
    fail_response = mock.MagicMock()
    fail_response.status_code = 200
    with open_resource('ghcc_fail_response.html', 'r') as f:
        response_text = f.read()
        fail_response.text = response_text
    dummy_request1.get.return_value = fail_response

    saveloc = '/my/directory'

    sat = 'GOES-E CONUS'
    info = 'ir'
    xy = (200, 55)
    goeslegacysave = nasaghcc.goeslegacy(sat, info, xy, uselatlon=False)
    assert_raises(SaveException, goeslegacysave, saveloc)

    assert_correct_goeslegacy_api_call(dummy_request1, sat, info, xy, uselatlon=False)
    dummy_request2.get.assert_not_called()


def assert_correct_goes16_api_call(req, sat, position, uselatlon=True, **kwargs_to_explictly_check):
    call = req.get.call_args_list[0]
    args, kwargs = call[0:2]
    assert args[0] == GOES_16_BASE_URL

    queryparams = kwargs['params']
    for paramkey in ('satellite', 'map', 'zoom', 'past', 'colorbar',
                     'mapcolor', 'quality', 'width', 'height', 'type'):
        assert paramkey in queryparams

    assert queryparams['satellite'] == sat
    if uselatlon:
        assert 'lat' in queryparams
        assert 'lon' in queryparams
        assert queryparams['lat'] == position[0]
        assert queryparams['lon'] == position[1]
    else:
        assert 'x' in queryparams
        assert 'y' in queryparams
        assert queryparams['x'] == position[0]
        assert queryparams['y'] == position[1]
    assert queryparams['type'] == 'Image'

    for k in kwargs_to_explictly_check:
        assert queryparams[k] == kwargs_to_explictly_check[k]

    assert kwargs['stream'] is True


def assert_correct_goeslegacy_api_call(req, sat, info, position, uselatlon=True,
                                       **kwargs_to_explictly_check):
    call = req.get.call_args_list[0]
    args, kwargs = call[0:2]
    assert args[0] == GOES_LEGACY_BASE_URL

    queryparams = kwargs['params']
    for paramkey in ('satellite', 'info', 'map', 'zoom', 'past', 'colorbar',
                     'mapcolor', 'quality', 'width', 'height', 'type'):
        assert paramkey in queryparams

    assert queryparams['satellite'] == sat
    assert queryparams['info'] == info
    if uselatlon:
        assert 'lat' in queryparams
        assert 'lon' in queryparams
        assert queryparams['lat'] == position[0]
        assert queryparams['lon'] == position[1]
    else:
        assert 'x' in queryparams
        assert 'y' in queryparams
        assert queryparams['x'] == position[0]
        assert queryparams['y'] == position[1]
    assert queryparams['type'] == 'Image'

    for k in kwargs_to_explictly_check:
        assert queryparams[k] == kwargs_to_explictly_check[k]

    assert kwargs['stream'] is True


def test_extract_time():
    url1 = 'https://weather.msfc.nasa.gov/goes/abi/dynamic/GOES001720171689nSPoh.jpg'
    extracted_time1 = nasaghcc.ghcc_extract_time(url1)
    assert extracted_time1 == datetime(year=2017, month=6, day=17, hour=0, minute=17)

    url2 = 'https://weather.msfc.nasa.gov/goes/abi/dynamic/GOES001720171knSPoh.jpg'
    extracted_time2 = nasaghcc.ghcc_extract_time(url2)
    assert extracted_time2 == datetime(year=2017, month=1, day=1, hour=0, minute=17)

    url3 = 'https://weather.msfc.nasa.gov/goes/abi/dynamic/GOES00172017168knSPoh.jpg'
    extracted_time3 = nasaghcc.ghcc_extract_time(url3)
    assert extracted_time3 == datetime(year=2017, month=6, day=17, hour=0, minute=17)

    url4 = 'https://weather.msfc.nasa.gov/goes/abi/dynamic/GOES0017201719nSPoh.jpg'
    extracted_time4 = nasaghcc.ghcc_extract_time(url4)
    assert extracted_time4 == datetime(year=2017, month=1, day=1, hour=0, minute=17)


if __name__ == '__main__':
    import nose
    nose.runmodule()
