#!/usr/bin/env python2
'''
Label Guides Creator

Copyright (C) 2018 John Beard - john.j.beard **guesswhat** gmail.com

## Simple Extension to draw guides and outlines for common paper labels

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import inkex
import simplestyle

GUIDE_ORIENT = {
        'vert': '1,0',
        'horz': '0,1'
}

# Preset list
# Regular grids defined as:
#       'reg', unit, page_szie, l marg, t marg, X size, Y size,
#       X pitch, Y pitch, Number across, Number down, shapes
PRESETS = {
    # Rounded rectangular labels in grid layout
    'L7167':        ['reg', 'mm', 'a4', 5.2, 3.95, 199.6, 289.1, 289.1, 199.6, 1, 1, 'rrect']
    'L7168':        ['reg', 'mm', 'a4', 5.2, 5, 199.6, 143.5, 143.5, 199.6, 1, 1, 'rrect']
    'L7169':        ['reg', 'mm', 'a4', 4.65, 9.5, 99.1, 139, 139, 101.6, 2, 2, 'rrect']
    'L7701':        ['reg', 'mm', 'a4', 9, 24.5, 192, 62, 62, 192, 1, 1, 'rrect']
    'L7171':        ['reg', 'mm', 'a4', 5, 28.5, 200, 60, 60, 200, 1, 1, 'rrect']
    'L7166':        ['reg', 'mm', 'a4', 4.65, 8.85, 99.1, 93.1, 93.1, 101.6, 2, 2, 'rrect']
    'L4760':        ['reg', 'mm', 'a4', 9, 12, 192, 39, 39, 192, 1, 1, 'rrect']
    'L7165':        ['reg', 'mm', 'a4', 4.65, 13.1, 99.1, 67.7, 67.7, 101.6, 2, 2, 'rrect']
    'L7664':        ['reg', 'mm', 'a4', 18, 4.9, 70, 71.8, 71.8, 104, 2, 2, 'rrect']
    'L7667':        ['reg', 'mm', 'a4', 38.5, 15.3, 133, 29.6, 29.6, 133, 1, 1, 'rrect']
    'L7173':        ['reg', 'mm', 'a4', 4.65, 6, 99.1, 57, 57, 101.6, 2, 2, 'rrect']
    'J5103':        ['reg', 'mm', 'a4', 4.75, 13.5, 38.1, 135, 135, 40.6, 5, 5, 'rrect']
    'L7666':        ['reg', 'mm', 'a4', 23, 18.5, 70, 52, 52, 94, 2, 2, 'rrect']
    'L7783':        ['reg', 'mm', 'a4', 7.85, 21.75, 95.8, 50.7, 50.7, 98.5, 2, 2, 'rrect']
    'L7164':        ['reg', 'mm', 'a4', 7.25, 4.5, 63.5, 72, 72, 66, 3, 3, 'rrect']
    'L7671':        ['reg', 'mm', 'a4', 27.55, 9.3, 76.2, 46.4, 46.4, 78.7, 2, 2, 'rrect']
    'L7177':        ['reg', 'mm', 'a4', 4.65, 21.6, 99.1, 42.3, 42.3, 101.6, 2, 2, 'rrect']
    'L7163':        ['reg', 'mm', 'a4', 4.65, 15.15, 99.1, 38.1, 38.1, 101.6, 2, 2, 'rrect']
    'L7668':        ['reg', 'mm', 'a4', 13.5, 21.25, 59, 50.9, 50.9, 62, 3, 3, 'rrect']
    'L7162':        ['reg', 'mm', 'a4', 4.65, 12.9, 99.1, 33.9, 33.9, 101.6, 2, 2, 'rrect']
    'L7674':        ['reg', 'mm', 'a4', 32.5, 12.5, 145, 17, 17, 145, 1, 1, 'rrect']
    'L7161':        ['reg', 'mm', 'a4', 7.25, 8.7, 63.5, 46.6, 46.6, 66, 3, 3, 'rrect']
    'L7172':        ['reg', 'mm', 'a4', 3.75, 13.5, 100, 30, 30, 102.5, 2, 2, 'rrect']
    'J5101':        ['reg', 'mm', 'a4', 4.75, 10.5, 38.1, 69, 69, 40.6, 5, 5, 'rrect']
    'L7160':        ['reg', 'mm', 'a4', 7.25, 15.15, 63.5, 38.1, 38.1, 66, 3, 3, 'rrect']
    'L7159':        ['reg', 'mm', 'a4', 7.25, 12.9, 63.5, 33.9, 33.9, 66, 3, 3, 'rrect']
    'L7665':        ['reg', 'mm', 'a4', 22, 21.6, 72, 21.15, 21.15, 94, 2, 2, 'rrect']
    'L7170':        ['reg', 'mm', 'a4', 38, 16.5, 134, 11, 11, 134, 1, 1, 'rrect']
    'L6011':        ['reg', 'mm', 'a4', 7.25, 15.3, 63.5, 29.6, 29.6, 66, 3, 3, 'rrect']
    'LP33_53':      ['reg', 'mm', 'a4', 21, 17.5, 54, 22, 24, 57, 3, 3, 'rrect']
    'LP36_49':      ['reg', 'mm', 'a4', 4.8, 15.3, 48.9, 29.6, 29.6, 50.5, 4, 4, 'rrect']
    'L7654':        ['reg', 'mm', 'a4', 9.7, 21.5, 45.7, 25.4, 25.4, 48.3, 4, 4, 'rrect']
    'L7636':        ['reg', 'mm', 'a4', 9.85, 21.3, 45.7, 21.2, 21.2, 48.2, 4, 4, 'rrect']
    'LP56_89':      ['reg', 'mm', 'a4', 8, 8.5, 89, 10, 10, 105, 2, 2, 'rrect']
    'L7651':        ['reg', 'mm', 'a4', 4.75, 10.7, 38.1, 21.2, 21.2, 40.6, 5, 5, 'rrect']
    'L7656':        ['reg', 'mm', 'a4', 5.95, 15.95, 46, 11.1, 12.7, 50.7, 4, 4, 'rrect']
    'L7658':        ['reg', 'mm', 'a4', 8.6, 13.5, 25.4, 10, 10, 27.9, 7, 7, 'rrect']
    'L7657':        ['reg', 'mm', 'a4', 4.75, 13.5, 17.8, 10, 10, 20.3, 10, 10, 'rrect']

    # Round labels
    "LP35_37R":     ['reg', 'mm', 'a4', 8.5, 13, 37, 37, 39, 39, 5, 7, 'circle'],

    # Square labels
    "LP35_37SQ":    ['reg', 'mm', 'a4', 8.5, 13, 37, 37, 39, 39, 5, 7, 'rrect'],
}


def add_SVG_guide(x, y, orientation, colour, parent):
    """ Create a sodipodi:guide node on the given parent
    """

    attribs = {
            'position': str(x) + "," + str(y),
            'orientation': orientation
    }

    if colour is not None:
        attribs[inkex.addNS('color', 'inkscape')] = colour

    inkex.etree.SubElement(
            parent,
            inkex.addNS('guide', 'sodipodi'),
            attribs)


def delete_all_guides(document):
    # getting the parent's tag of the guides
    nv = document.xpath(
            '/svg:svg/sodipodi:namedview', namespaces=inkex.NSS)[0]

    # getting all the guides
    children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',
                              namespaces=inkex.NSS)

    # removing each guides
    for element in children:
        nv.remove(element)


def draw_SVG_ellipse(rx, ry, cx, cy, style, parent):

    attribs = {
        'style': simplestyle.formatStyle(style),
        inkex.addNS('cx', 'sodipodi'):   str(cx),
        inkex.addNS('cy', 'sodipodi'):   str(cy),
        inkex.addNS('rx', 'sodipodi'):   str(rx),
        inkex.addNS('ry', 'sodipodi'):   str(ry),
        inkex.addNS('type', 'sodipodi'): 'arc',
    }

    inkex.etree.SubElement(parent, inkex.addNS('path', 'svg'), attribs)


def draw_SVG_rect(x, y, w, h, round, style, parent):

    attribs = {
        'style':    simplestyle.formatStyle(style),
        'height':   str(h),
        'width':    str(w),
        'x':        str(x),
        'y':        str(y)
    }

    if round:
        attribs['ry'] = str(round)

    inkex.etree.SubElement(parent, inkex.addNS('rect', 'svg'), attribs)


def add_SVG_layer(parent, gid, label):

    layer = inkex.etree.SubElement(parent, 'g', {
        'id': gid,
        inkex.addNS('groupmode', 'inkscape'): 'layer',
        inkex.addNS('label', 'inkscape'): label
    })

    return layer


class LabelGuides(inkex.Effect):

    def __init__(self):

        inkex.Effect.__init__(self)

        self.OptionParser.add_option(
            '--label_preset',
            action='store', type='string',
            dest='label_preset', default='custom',
            help='Use the given preset, overriding all other parameters')

        self.OptionParser.add_option(
            '--units',
            action='store', type='string',
            dest='units', default="mm",
            help='The units to use for custom label sizing')

        self.OptionParser.add_option(
            '--margin_l',
            action='store', type='float',
            dest='margin_l', default=8.5,
            help='Left page margin (mm)')

        self.OptionParser.add_option(
            '--margin_t',
            action='store', type='float',
            dest='margin_t', default=13,
            help='Top page margin (mm)')

        self.OptionParser.add_option(
            '--size_x',
            action='store', type='float',
            dest='size_x', default=37,
            help='Label X size (mm)')

        self.OptionParser.add_option(
            '--size_y',
            action='store', type='float',
            dest='size_y', default=37,
            help='Label Y size (mm)')

        self.OptionParser.add_option(
            '--pitch_x',
            action='store', type='float',
            dest='pitch_x', default=39,
            help='Label X pitch (mm)')

        self.OptionParser.add_option(
            '--pitch_y',
            action='store', type='float',
            dest='pitch_y', default=39,
            help='Label Y pitch (mm)')

        self.OptionParser.add_option(
            '--count_x',
            action='store', type='int',
            dest='count_x', default=5,
            help='Number of labels across')

        self.OptionParser.add_option(
            '--count_y',
            action='store', type='int',
            dest='count_y', default=7,
            help='Number of labels down')

        self.OptionParser.add_option(
            '--shapes',
            action='store', type='string',
            dest='shapes', default='rect',
            help='Label shapes to draw')

        self.OptionParser.add_option(
            '--delete_existing_guides',
            action='store', type='inkbool',
            dest='delete_existing_guides', default=False,
            help='Delete existing guides from document')

        self.OptionParser.add_option(
            '--draw_edge_guides',
            action='store', type='inkbool',
            dest='draw_edge_guides', default=True,
            help='Draw guides at label edges')

        self.OptionParser.add_option(
            '--inset',
            action='store', type='float',
            dest='inset', default=5,
            help='Inset to use for inset guides')

        self.OptionParser.add_option(
            '--draw_inset_guides',
            action='store', type='inkbool',
            dest='draw_inset_guides', default=True,
            help='Draw guides inset to label edges')

        self.OptionParser.add_option(
            '--draw_shapes',
            action='store', type='inkbool',
            dest='draw_shapes', default=True,
            help='Draw label outline shapes')

        self.OptionParser.add_option(
            '--set_page_size',
            action='store', type='inkbool',
            dest='set_page_size', default=True,
            help='Set page size (presets only)')

        # TODO: Option Parsing

    def _to_uu(self, val, unit):
        return self.unittouu(str(val) + unit)

    def set_SVG_page_size(self, document, x, y, unit):

        svg = document.getroot()

        # Re-calculate viewbox in terms of User Units
        new_uu_w = self._to_uu(x, unit)
        new_uu_h = self._to_uu(y, unit)

        # set SVG page size
        svg.attrib['width'] = str(x) + unit
        svg.attrib['height'] = str(y) + unit

        svg.attrib['viewBox'] = "0 0 %f %f" % (new_uu_w, new_uu_h)

    def _read_custom_options(self):
        """Read custom label geometry options and produce
        a dictionary of parameters for ingestion
        """
        unit = self.options.units

        custom_opts = {
                'units': self.options.units,
                'page_size': None,
                'margin': {
                    'l': self._to_uu(self.options.margin_l, unit),
                    't': self._to_uu(self.options.margin_t, unit)
                },
                'size': {
                    'x': self._to_uu(self.options.size_x, unit),
                    'y': self._to_uu(self.options.size_y, unit)
                },
                'pitch': {
                    'x': self._to_uu(self.options.pitch_x, unit),
                    'y': self._to_uu(self.options.pitch_y, unit)
                },
                'count': {
                    'x': self.options.count_x,
                    'y': self.options.count_y
                },
                'shapes': self.options.shapes
        }

        return custom_opts

    def _get_page_size(self, size):

        if isinstance(size, (list,)):
            # Explicit size
            return size
        elif size == "a4":
            return [210, 297]

        # Failed to find a useful size, None will inhibit setting the size
        return None

    def _construct_preset_opts(self, preset_id):
        """Construct an options object for a preset label template
        """
        preset = PRESETS[preset_id]

        unit = preset[1]

        opts = {
                'units': unit,
                'page_size': self._get_page_size(preset[2]),
                'margin': {
                    'l': self._to_uu(preset[3], unit),
                    't': self._to_uu(preset[4], unit)
                 },
                'size': {
                    'x': self._to_uu(preset[5], unit),
                    'y': self._to_uu(preset[6], unit)
                },
                'pitch': {
                    'x': self._to_uu(preset[7], unit),
                    'y': self._to_uu(preset[8], unit)
                },
                'count': {
                    'x': preset[9],
                    'y': preset[10]
                },
                'shapes': preset[11]
        }

        return opts

    def _get_regular_guides(self, label_opts, inset):
        """Get the guides for a set of labels defined by a regular grid

        This is done so that irregular-grid presets can be defined if
        needed
        """

        guides = {'v': [], 'h': []}

        x = label_opts['margin']['l']

        for x_idx in range(label_opts['count']['x']):

            l_pos = x + inset
            r_pos = x + label_opts['size']['x'] - inset

            guides['v'].extend([l_pos, r_pos])

            # Step over to next label
            x += label_opts['pitch']['x']

        # Horizontal guides, top to bottom
        height = self.unittouu(self.getDocumentHeight())

        y = height - label_opts['margin']['t']

        for y_idx in range(label_opts['count']['y']):

            t_pos = y - inset
            b_pos = y - label_opts['size']['y'] + inset

            guides['h'].extend([t_pos, b_pos])

            # Step over to next label
            y -= label_opts['pitch']['y']

        return guides

    def _draw_label_guides(self, document, label_opts, inset, colour):
        """Draws label guides from a regular guide description object
        """
        guides = self._get_regular_guides(label_opts, inset)

        self._draw_guides(document, guides, colour)

    def _draw_guides(self, document, guides, colour):
        """
        Draw guides from a generic list of h/v guides
        """
        # Get parent tag of the guides
        nv = self.getNamedView()

        # Draw vertical guides
        for g in guides['v']:
            add_SVG_guide(g, 0, GUIDE_ORIENT['vert'], colour, nv)

        for g in guides['h']:
            add_SVG_guide(0, g, GUIDE_ORIENT['horz'], colour, nv)

    def _draw_shapes(self, document, label_opts):
        """
        Draw label shapes from a regular grid
        """

        style = {
                'stroke': '#000000',
                'stroke-width': self._to_uu(1, "px"),
                'fill': "none"
        }

        guides = self._get_regular_guides(label_opts, 0)
        shape = label_opts['shapes']

        shapeLayer = add_SVG_layer(
                self.document.getroot(),
                self.uniqueId("outlineLayer"),
                "Label outlines")

        # guides start from the bottom, SVG items from the top
        height = self.unittouu(self.getDocumentHeight())

        # draw shapes between every set of two guides
        for xi in range(0, len(guides['v']), 2):

            for yi in range(0, len(guides['h']), 2):

                if shape == 'circle':
                    cx = (guides['v'][xi] + guides['v'][xi + 1]) / 2
                    cy = (guides['h'][yi] + guides['h'][yi + 1]) / 2

                    rx = cx - guides['v'][xi]
                    ry = guides['h'][yi] - cy

                    draw_SVG_ellipse(rx, ry, cx, height - cy, style,
                                     shapeLayer)

                elif shape in ["rect", "rrect"]:

                    x = guides['v'][xi]
                    w = guides['v'][xi + 1] - x

                    y = guides['h'][yi]
                    h = y - guides['h'][yi + 1]

                    rnd = self._to_uu(1, "mm") if (shape == "rrect") else None

                    draw_SVG_rect(x, height - y, w, h, rnd, style, shapeLayer)

    def _set_page_size(self, document, label_opts):

        size = label_opts['page_size']
        unit = label_opts['units']

        inkex.errormsg(str(size))

        if size is not None:
            self.set_SVG_page_size(document, size[0], size[1], unit)

    def effect(self):

        # Read in custom options
        label_preset = self.options.label_preset

        if label_preset == "custom":
            # construct from parameters
            label_opts = self._read_custom_options()
        else:
            # construct from a preset
            label_opts = self._construct_preset_opts(label_preset)

        if self.options.delete_existing_guides:
            delete_all_guides(self.document)

        # Resize page first, otherwise guides won't be in the right places
        if self.options.set_page_size:
            self._set_page_size(self.document, label_opts)

        if self.options.draw_edge_guides:
            self._draw_label_guides(self.document, label_opts, 0, "#00A000")

        if self.options.draw_inset_guides and self.options.inset > 0.0:
            self._draw_label_guides(self.document, label_opts,
                                    self.options.inset, None)

        if self.options.draw_shapes:
            self._draw_shapes(self.document, label_opts)


if __name__ == '__main__':
    # Create effect instance and apply it.
    effect = LabelGuides()
    effect.affect()
