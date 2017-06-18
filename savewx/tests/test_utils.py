from savewx import utils


def test_get_img_srcs():
    with open('ghcc_response.html', 'r') as f:
        text = f.read()
        imgsrcs = utils.get_image_srcs(text)
        assert imgsrcs == ['/goes/abi/dynamic/GOES001720171689nSPoh.jpg']


def test_get_img_srcs_with_filter():
    the_filter = lambda img: '.png' in img
    with open('ghcc_response.html', 'r') as f:
        text = f.read()
        imgsrcs = utils.get_image_srcs(text, the_filter)
        assert imgsrcs == []


if __name__ == '__main__':
    import nose
    nose.runmodule()