from savewx import utils


def test_get_img_srcs():
    with open('ghcc_goes16_response.html', 'r') as f:
        text = f.read()
        imgsrcs = utils.get_image_srcs(text)
        assert imgsrcs == ['/goes/abi/dynamic/GOES001720171689nSPoh.jpg']


if __name__ == '__main__':
    import nose
    nose.runmodule()