from datetime import timedelta

from savewx.nasaghcc import goes16
from savewx.scheduling import schedule
from savewx.ssd import ssd_animated


def goes_16_vis(posxy, saveloc, past=0):
    saver = goes16('GOESEastconusband02', posxy, uselatlon=False, zoom=2, past=past, width=1200, height=900)
    saver(saveloc)


def goes_16_ir(posxy, saveloc, past=0):
    saver = goes16('GOESEastfullDiskband14', posxy, uselatlon=False, palette='ir2.pal',
                   past=past)
    saver(saveloc)


def goes_16_saver(sattype, posxy, past=0, width=1200, height=900, zoom=None, palette=None, **kwargs):
    if sattype.lower() == 'ir':
        sat = 'GOESEastfullDiskband14'
        zoom = zoom or 1
        palette = palette or 'ir2.pal'
    elif sattype.lower() == 'vis':
        sat = 'GOESEastfullDiskband02'
        zoom = zoom or 2
        palette = None
    else:
        raise ValueError("Incorrect sat type: {}".format(sattype))

    saver = goes16(sat, posxy, uselatlon=False, width=width, height=height, zoom=zoom, past=past,
                   palette=palette, **kwargs)
    return saver


def save_ssd_animated(saveloc):
    for enh in 'avn', 'rgb':
        schedule(ssd_animated('06E', enh), saveloc, interval=timedelta(seconds=5))


if __name__ == '__main__':
    for past in reversed(range(0, 21)):
        goes_16_vis((250, 175), '/Users/jitang/Dropbox/2019_WX', past)
    # for i in reversed(range(70)):
    #     goes_16_vis((332, 189), saveloc='/Users/jitang/Dropbox/Hurricane_Michael/VIS_181010', past=i)
    # locs = {
    #     'kingvale': 'http://www1.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy80atkingvalewb/hwy80atkingvalewb.jpg',
    #     'donner': 'http://www1.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy80atdonnersummit/hwy80atdonnersummit.jpg',
    #     'echo': 'http://www1.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy50atechosummit/hwy50atechosummit.jpg',
    #     'soda_springs': 'http://www.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy80atsodaspringseb/hwy80atsodaspringseb.jpg',
    #     'castle_peak': 'http://www.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy80atcastlepeak/hwy80atcastlepeak.jpg',
    #     'twin_bridges': 'http://www1.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy50attwinbridges/hwy50attwinbridges.jpg'
    # }
    # # locs = {
    # #     'castle_peak': 'http://www.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy80atcastlepeak/hwy80atcastlepeak.jpg'
    # # }
    # # locs = {
    # #     'twin_bridges': 'http://www1.dot.ca.gov/cwwp2/data/d3/cctv/image/hwy50attwinbridges/hwy50attwinbridges.jpg'
    # # }
    #
    # for loc in locs:
    #     saveloc = '/Users/jitang/Dropbox/2018_MarchStorm/{}'.format(loc)
    #     saver = HTTPImageSave(
    #         url=locs[loc],
    #         process_response=append_timestamp(loc, 'jpg')
    #     )

        # schedule(saver, saveloc, interval=timedelta(minutes=2))

    # xy = (436, 151)
    # for past in reversed(range(20, 51)):
    #     goes_16_saver('vis', xy, past=past)(saveloc)