from unittest import mock

from nose.tools import assert_raises

from savewx.core import HTTPImageSave, SaveException


@mock.patch('savewx.core.requests')
def test_call_save_successful_with_process_response_func(dummy_requests):
    dummy_response = mock.MagicMock()
    dummy_response.status_code = 200
    dummy_process_response = mock.MagicMock()
    dummy_requests.get.return_value = dummy_response

    url = 'http://example.com'
    saveloc= '/my/directory'

    imgsave = HTTPImageSave(url, process_response=dummy_process_response)
    imgsave(saveloc)

    dummy_process_response.assert_called_with(dummy_response, saveloc, 'skip')


@mock.patch('savewx.core.requests')
def test_call_save_failure_with_callback(dummy_requests):
    dummy_response = mock.MagicMock()
    dummy_response.status_code = 404
    dummy_process_response = mock.MagicMock()
    dummy_requests.get.return_value = dummy_response
    dummy_failure_callback = mock.MagicMock()

    url = 'http://example.com'
    saveloc= '/my/directory'

    imgsave = HTTPImageSave(url, process_response=dummy_process_response,
                            failure_callback=dummy_failure_callback)
    imgsave(saveloc)

    dummy_failure_callback.assert_called_with(dummy_response)
    dummy_process_response.assert_not_called()


@mock.patch('savewx.core.requests')
def test_call_save_failure_without_callback(dummy_requests):
    dummy_response = mock.MagicMock()
    dummy_response.status_code = 404
    dummy_process_response = mock.MagicMock()
    dummy_requests.get.return_value = dummy_response

    url = 'http://example.com'
    saveloc= '/my/directory'

    imgsave = HTTPImageSave(url, process_response=dummy_process_response)

    assert_raises(SaveException, imgsave, saveloc)


if __name__ == '__main__':
    import nose
    nose.runmodule()
