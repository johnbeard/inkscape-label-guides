#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple download tool for scraping LabelPlanet.co.uk pages for label
template specifications. Can output the descriptions for use in an INX file
enum, as well as the definitions for use in the label_guides.py enxtension's
database.

Licenced under the GNU General Public License v2.0
"""

from lxml.html import fromstring
import requests
import requests_cache
import re

import logging
from pprint import pformat
import argparse


class FormatFinder(object):
    """
    Gets a list of known formats from a template list page
    """

    def _nth_cell_text(self, row, nth):

        selector = "td:nth-child({})".format(nth)
        return row.cssselect(selector)[0].text_content()

    def _get_xy_size_from_celltext(self, txt):

        parts = re.findall(r"[\d.,]+", txt)

        return parts

    def _get_codes_from_celltext(self, txt):

        lpcode = re.search("LP[^\s]+", txt)

        avery = re.search("(?<=Avery )[A-Z\d]+", txt)

        return (lpcode.group(), avery.group() if avery else None)

    def _get_link_from_row(self, row):

        link = row.cssselect("a")[0].attrib['href']

        return link

    def _get_item_from_row(self, row):

        num_per_sheet = int(self._nth_cell_text(row, 1))

        lab_size = self._nth_cell_text(row, 2)

        # some lable sizes aren't supported
        if any(s in lab_size for s in ['/']):
            return None

        lab_size = self._get_xy_size_from_celltext(lab_size)

        codes = self._get_codes_from_celltext(self._nth_cell_text(row, 3))

        link = self._get_link_from_row(row)

        item = {
                'size': lab_size,
                'avery': codes[1],
                'lpcode': codes[0],
                'persheet': num_per_sheet,
                'prodlink': link
        }

        return item

    def get_list(self, list_page):

        url = ("https://www.labelplanet.co.uk/label-templates/" +
               list_page + ".php")

        shape = {
                "rectangular-rounded-corners": "rrect",
                "rectangular-square-corners": "rect",
                "square": "rrect",
                "round": "circle",
                "oval": "circle"
                }[list_page]

        r = requests.get(url)

        doc = fromstring(r.text)

        items = []

        for prod_row in doc.cssselect(".templatetable tbody tr"):

            # product rows have 3 cells
            if (len(prod_row.getchildren()) == 3):
                item = self._get_item_from_row(prod_row)

                if (item):
                    item['shape'] = shape
                    items.append(item)

        return items


class SpecRipper(object):
    """
    Gets the full spec for a label from the template page

    Updates the given item with description and label spec
    """

    def __init__(self, item):
        self.item = item

    def _get_desc_text(self, doc):

        e = doc.xpath('.//td'
                      '/strong[starts-with(text(), "Notes")]'
                      '/../..'
                      '/following-sibling::tr[1]/td'
                      '//li[1]')

        parts = e[0].text_content().split("–")

        if len(parts) > 1:
            return parts[0].strip()

        return None

    def _get_cell_by_xy(self, table, x, y):

        nxt = table.xpath(".//tr[2]/following-sibling::*[1]")[0]

        # handle broken table formatting
        # (missing <tr> on third row)
        if nxt.tag == "td" and y > 3:
            y += 3

        selector = "tr:nth-child({y}) > td:nth-child({x})".format(x=x, y=y)
        return table.cssselect(selector)[0]

    def _get_dim_from_text(self, txt):

        return txt.replace("mm", "").replace("(diameter)", "").strip()

    def _get_xy_template_spec(self, doc):

        table = doc.cssselect('.templatetable')[0]

        # cell x, cell y, data
        data_cells = [
                (2, 3, 'size_x', 'dim'),
                (3, 3, 'size_y', 'dim'),
                (4, 3, 'count_x', 'int'),
                (5, 3, 'count_y', 'int'),
                (1, 5, 'margin_t', 'dim'),
                (3, 5, 'margin_l', 'dim'),
                (2, 7, 'pitch_x', 'dim'),
                (1, 7, 'pitch_y', 'dim'),
        ]

        spec = {}

        for c in data_cells:

            txt = self._get_cell_by_xy(table, c[0], c[1]).text_content()

            if c[3] == 'dim':
                txt = self._get_dim_from_text(txt)

            spec[c[2]] = txt

        return spec

    def scrape(self):

        logging.debug("Scraping template: %s", self.item['lpcode'])

        url = self.item['prodlink']

        r = requests.get(url)

        doc = fromstring(r.text)

        self.item['desc'] = self._get_desc_text(doc)

        spec = self._get_xy_template_spec(doc)

        logging.debug(pformat(spec))

        self.item['layout'] = spec


class InxFormatter(object):

    def format_inx(self, item):

        idcode = item['avery'] if item['avery'] else item['lpcode'].replace("/", "_")

        size = " x ".join(item['size'])

        sheet = "A4"

        codes = []

        if item['avery']:
            codes.append(item['avery'])

        codes.append(item['lpcode'])

        codes = ", ".join(codes)

        desc = "Labels" if not item['desc'] else item['desc']

        s = "<_item value=\"{code}\">{size}mm {desc} ({per}/sheet, {sheet}) [{allcodes}]</_item>".format(
            code=idcode,
            size=size,
            per=item['persheet'],
            sheet=sheet,
            allcodes=codes,
            desc=desc
        )

        return s


class SpecFormatter(object):

    def format_spec(self, item):

        idcode = item['avery'] if item['avery'] else item['lpcode'].replace("/", "_")

        sheet = 'a4'

        layout = item['layout']

        s = "{indent}{idcode:16}['reg', 'mm', '{sheet}', {ml}, {mt}, {sx}, {sy}, {px}, {py}, {nx}, {ny}, '{shape}'],".format(
                indent=" " * 4,
                idcode="'{}':".format(idcode),
                sheet=sheet,
                ml=layout['margin_l'],
                mt=layout['margin_t'],
                sx=layout['size_x'],
                sy=layout['size_y'],
                px=layout['pitch_x'],
                py=layout['pitch_y'],
                nx=layout['count_x'],
                ny=layout['count_y'],
                shape=item['shape'],
            )

        return s


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description='Download label template specifications from '
                        'LabelPlanet.co.uk')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='verbose mode')
    parser.add_argument('-t', '--type', action='store', required=True,
                        choices=['rrect', 'rect', 'circ', 'oval', 'square'],
                        help='label type')
    parser.add_argument('--inx', action='store_true',
                        help='print INX items')
    parser.add_argument('--spec', action='store_true',
                        help='print specification items')

    args = parser.parse_args()

    # avoid re-downloading pages
    requests_cache.install_cache('demo_cache')

    # convert type
    label_type = {
            'rrect': 'rectangular-rounded-corners',
            'rect': 'rectangular-square-corners',
            'circ': 'round',
            'oval': 'oval',
            'square': 'square'
    }[args.type]

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    ff = FormatFinder()
    spec_list = ff.get_list(label_type)

    logging.debug("Got list of specs: ")
    logging.debug(pformat(spec_list))

    # get spec layouts + descs etc
    for spec in spec_list:

        spec_ripper = SpecRipper(spec)

        spec_ripper.scrape()

    if args.inx:
        inx_f = InxFormatter()

        for s in spec_list:

            inx = inx_f.format_inx(s)
            print(inx)

    if args.spec:

        spec_f = SpecFormatter()

        for s in spec_list:

            spec = spec_f.format_spec(s)
            print(spec)
