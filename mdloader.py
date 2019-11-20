import re
import os
import cairosvg
import mistletoe

from collections import namedtuple
from html.parser import HTMLParser
from syntaxer import syntax_dict

HTML_TABS = "&nbsp;&nbsp;&nbsp;&nbsp;"

HTMLTag = namedtuple('HTMLTag', ('tag', 'children', 'attrs'))


def handle_img_tag(attrs, path):
    new_attrs = []
    for attr in attrs:
        if attr[0] == 'src':
            src = attr[1].replace('?invert_in_darkmode', '')
            if 'http' not in src:
                src = os.path.join(path, src)
                if 'svg' in src:
                    filename = src + '.png'
                    cairosvg.svg2png(url=src, write_to=filename, dpi=300)
                    src = filename
            new_attrs.append((attr[0], src))
        elif attr[0] == 'width' or attr[0] == 'height':
            new_attrs.append((attr[0], re.match(r'\d*.?\d*', attr[1])[0]))
        else:
            new_attrs.append(attr)
    return new_attrs


class MyHTMLParser(HTMLParser):
    def __init__(self, path, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.path = path
        self.openTags = []
        self.tagList = []

    def handle_starttag(self, tag, attrs):
        self.openTags.append(HTMLTag(tag, [], attrs))

    def handle_endtag(self, tag):
        last_opened = self.openTags.pop()

        if last_opened.tag == 'code':
            if self.openTags[-1].tag == 'p':
                last_opened = HTMLTag(
                    'font',
                    last_opened.children,
                    last_opened.attrs + [('name', 'Courier-Bold'),
                                         ('fontsize', '11'),
                                         ('textcolor', 'red')]
                )
            elif self.openTags[-1].tag == 'pre':

                which = last_opened.attrs[0][1] if last_opened.attrs else 'default'
                last_opened = HTMLTag(
                    last_opened.tag,
                    [syntax_dict[which](''.join(last_opened.children))],
                    last_opened.attrs
                )

        if len(self.openTags) > 0:
            self.openTags[-1].children.append(last_opened)
        else:
            self.tagList.append(last_opened)

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            attrs = handle_img_tag(attrs, self.path)
        if len(self.openTags) > 0:
            self.openTags[-1].children.append(HTMLTag(tag, [], attrs))
        else:
            self.tagList.append(HTMLTag(tag, [], attrs))

    def handle_data(self, data):
        if data == '\n':
            return
        data = data.replace('\\$', '$').replace('\t', HTML_TABS).replace('    ', HTML_TABS)
        if len(self.openTags) > 0:
            self.openTags[-1].children.append(data)


class MDLoader:
    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.dirname(os.path.realpath(filename))

    def read(self):
        with open(self.filename) as f:
            data = mistletoe.markdown(f)
            data = data.replace('/>', ' />').replace("<br>", "<br/>")

        parser = MyHTMLParser(self.path)
        parser.feed(data)

        return parser.tagList


if __name__ == '__main__':
    import sys
    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    filename = sys.argv[1]
    data = MDLoader(filename).read()
    pp.pprint(data)
