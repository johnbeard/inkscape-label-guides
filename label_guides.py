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
#       'reg', unit, l marg, t marg, X size, Y size, X pitch, Y pitch,
#       Number across, Number down, shapes
PRESETS = {
        "LP35_37R": ['reg', 'mm', 8.5, 13, 37, 37, 39, 39, 5, 7, 'circle']
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

        # TODO: Option Parsing

    def _to_uu(self, val, unit):
        return self.unittouu(str(val) + unit)

    def _read_custom_options(self):
        """Read custom label geometry options and produce
        a dictionary of parameters for ingestion
        """
        unit = self.options.units

        custom_opts = {}

        custom_opts['margin'] = {}
        custom_opts['margin']['l'] = self._to_uu(self.options.margin_l, unit)
        custom_opts['margin']['t'] = self._to_uu(self.options.margin_t, unit)

        custom_opts['size'] = {}
        custom_opts['size']['x'] = self._to_uu(self.options.size_x, unit)
        custom_opts['size']['y'] = self._to_uu(self.options.size_y, unit)

        custom_opts['pitch'] = {}
        custom_opts['pitch']['x'] = self._to_uu(self.options.pitch_x, unit)
        custom_opts['pitch']['y'] = self._to_uu(self.options.pitch_y, unit)

        custom_opts['count'] = {}
        custom_opts['count']['x'] = self.options.count_x
        custom_opts['count']['y'] = self.options.count_y

        custom_opts['shapes'] = self.options.shapes

        return custom_opts

    def _construct_preset_opts(self, preset_id):
        """Construct an options object for a preset label template
        """
        preset = PRESETS[preset_id]

        unit = preset[1]

        opts = {
                'margin': {
                    'l': self._to_uu(preset[2], unit),
                    't': self._to_uu(preset[3], unit)
                 },
                'size': {
                    'x': self._to_uu(preset[4], unit),
                    'y': self._to_uu(preset[5], unit)
                },
                'pitch': {
                    'x': self._to_uu(preset[6], unit),
                    'y': self._to_uu(preset[7], unit)
                },
                'count': {
                    'x': preset[8],
                    'y': preset[9]
                },
                'shapes': preset[10]
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

                    draw_SVG_ellipse(rx, ry, cx, height - cy, style, shapeLayer)

                elif shape == "rect":

                    x = guides['v'][xi]
                    w = guides['v'][xi + 1] - x

                    y = guides['h'][yi]
                    h = y - guides['h'][yi + 1]

                    rnd = self._to_uu(1, "mm")

                    draw_SVG_rect(x, height - y, w, h, rnd, style, shapeLayer)

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
