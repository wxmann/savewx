import os
from unittest import mock

from nose.tools import assert_raises

from savewx import nasaghcc
from savewx.nasaghcc import GOES_16_BASE_URL, NASA_MSFC_BASE_URL


@mock.patch('savewx.nasaghcc.save_image')
@mock.patch('savewx.nasaghcc.requests')
@mock.patch('savewx.core.requests')
def test_goes_16_successful(dummy_request1, dummy_request2, dummy_save_img):
    dummy_raw_response = mock.MagicMock()
    dummy_raw_response.status_code = 200
    with open('ghcc_goes16_response.html', 'r') as f:
        response_text = f.read()
        dummy_raw_response.text = response_text
    dummy_request1.get.return_value = dummy_raw_response

    dummy_img_response = mock.MagicMock()
    dummy_img_response.status_code = 200
    dummy_request2.get.return_value = dummy_img_response

    saveloc = '/my/directory'

    sat = 'GOESEastconusband02'
    xy = (200, 55)
    goes16save = nasaghcc.goes16(sat, xy=xy)
    goes16save(saveloc)

    target = os.sep.join([saveloc, 'GHCC_20170617_0017.jpg'])
    assert_correct_goes16_api_call(dummy_request1, sat, xy)
    dummy_request2.get.assert_called_with(NASA_MSFC_BASE_URL + '/goes/abi/dynamic/GOES001720171689nSPoh.jpg',
                                          stream=True)
    dummy_save_img.assert_called_with(dummy_img_response, target)


def test_goes_16_missing_both_latlon_xy_args():
    sat = 'GOESEastconusband02'
    assert_raises(ValueError, nasaghcc.goes16, sat)


def assert_correct_goes16_api_call(req, sat, xy, **kwargs_to_explictly_check):
    call = req.get.call_args_list[0]
    args, kwargs = call[0:2]
    assert args[0] == GOES_16_BASE_URL

    queryparams = kwargs['params']
    for paramkey in ('satellite', 'map', 'zoom', 'past', 'colorbar',
                     'mapcolor', 'quality', 'width', 'height', 'type', 'x', 'y'):
        assert paramkey in queryparams

    assert queryparams['satellite'] == sat
    assert queryparams['x'] == xy[0]
    assert queryparams['y'] == xy[1]
    assert queryparams['type'] == 'Image'

    for k in kwargs_to_explictly_check:
        assert queryparams[k] == kwargs_to_explictly_check[k]

    assert kwargs['stream'] is True


if __name__ == '__main__':
    import nose
    nose.runmodule()
