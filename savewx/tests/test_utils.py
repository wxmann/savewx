from savewx import utils
from savewx.tests._testcommon import open_resource


def test_get_img_srcs():
    with open_resource('ghcc_response.html', 'r') as f:
        text = f.read()
        imgsrcs = utils.get_image_srcs(text)
        assert imgsrcs == ['/goes/abi/dynamic/GOES001720171689nSPoh.jpg']


def test_get_img_srcs_with_filter():
    the_filter = lambda img: '.png' in img
    with open_resource('ghcc_response.html', 'r') as f:
        text = f.read()
        imgsrcs = utils.get_image_srcs(text, the_filter)
        assert imgsrcs == []


def test_get_links_with_filter():
    the_filter = lambda img: 'Z-avn' in img
    with open_resource('ssd_response.html', 'r') as f:
        text = f.read()
        links = utils.get_links(text, the_filter)
        assert links == ['20170618_0645Z-avn.gif', '20170618_0715Z-avn.gif', '20170618_0745Z-avn.gif']


if __name__ == '__main__':
    import nose
    nose.runmodule()