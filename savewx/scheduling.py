import threading
from datetime import datetime

from savewx.logs import logger


def schedule(saver, saveloc, interval, start=None, stop=None):
    executor = SaveExecutor(saver, saveloc, interval)

    if start is not None and isinstance(start, datetime) and start > datetime.now():
        dt = start - datetime.now()
        timer = threading.Timer(dt.seconds, executor.start)
        timer.start()
    else:
        if stop is not None and isinstance(stop, datetime) and stop > datetime.now():
            dt = stop - datetime.now()
            timer = threading.Thread(dt.seconds, executor.stop)
            timer.start()

        executor.start()


class SaveExecutor(threading.Thread):
    def __init__(self, saver, saveloc, interval):
        threading.Thread.__init__(self)
        self._saver = saver
        self._saveloc = saveloc
        self._stopper = threading.Event()
        self._interval = interval

    def run(self):
        logger.info("Start saving to: {} with interval: {}".format(self._saveloc, self._interval))
        while not self._stopper.is_set():
            self._saver(self._saveloc)
            self._stopper.wait(self._interval.seconds)

    def stop(self):
        logger.info("Stopping saving to: " + str(self._saveloc))
        self._stopper.set()
