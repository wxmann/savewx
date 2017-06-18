import shutil
from html.parser import HTMLParser


def save_image(response, saveloc):
    with open(saveloc, 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)


def get_image_srcs(html):
    parser = ImagesHTMLParser()
    parser.feed(html)
    return parser.results()


class ImagesHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.foundimages = []

    def handle_starttag(self, tag, attrs):
        self.foundimages += [attrval for attr, attrval in attrs if tag.lower() == 'img' and attr.lower() == 'src']

    def results(self):
        return self.foundimages