import os
import shutil
from datetime import datetime
from html.parser import HTMLParser

from savewx.logs import logger


def save_image(response, saveloc):
    with open(saveloc, 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)


def get_image_srcs(html, filter_results=None):
    parser = ImagesHTMLParser()
    parser.feed(html)
    return parser.results(filter_results)


class ImagesHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundimages = []

    def handle_starttag(self, tag, attrs):
        self.foundimages += [attrval for attr, attrval in attrs if tag.lower() == 'img' and attr.lower() == 'src']

    def results(self, filter_results=None):
        if filter_results is None:
            return self.foundimages
        else:
            return [img for img in self.foundimages if filter_results(img)]


def get_links(html, filter_results=None):
    parser = LinksHTMLParser()
    parser.feed(html)
    return parser.results(filter_results)


class LinksHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundlinks = []

    def handle_starttag(self, tag, attrs):
        self.foundlinks += [attrval for attr, attrval in attrs if tag.lower() == 'a' and attr.lower() == 'href']

    def results(self, filter_results=None):
        if filter_results is None:
            return self.foundlinks
        else:
            return [link for link in self.foundlinks if filter_results(link)]


def skip_save(saveloc, on_file_exists):
    if on_file_exists.lower() == 'skip' and os.path.isfile(saveloc):
        logger.warn("File: {} already exists, skipping".format(saveloc))
        return True
    return False


def append_timestamp(prefix, ext):
    def saveit(response, savedir, on_file_exists):
        now = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename = '{}_{}.{}'.format(prefix, now, ext)
        saveloc = os.path.join(savedir, filename)

        if not skip_save(saveloc, on_file_exists):
            save_image(response, saveloc)

    return saveit
