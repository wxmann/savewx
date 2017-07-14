from datetime import timedelta

from savewx.nasaghcc import goes16
from savewx.scheduling import schedule
from savewx.ssd import ssd_animated


def goes_16_vis(posxy, saveloc, past=0):
    saver = goes16('GOESEastfullDiskband02', posxy, uselatlon=False, zoom=4, past=past)
    saver(saveloc)


def goes_16_ir(posxy, saveloc, past=0):
    saver = goes16('GOESEastfullDiskband14', posxy, uselatlon=False, palette='ir10.pal',
                   past=past)
    saver(saveloc)


def save_ssd_animated(saveloc):
    for enh in 'avn', 'rgb':
        schedule(ssd_animated('06E', enh), saveloc, interval=timedelta(seconds=5))


if __name__ == '__main__':
    saveloc = '/your/location/here'
    save_ssd_animated(saveloc)