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

GUIDE_ORIENT = {
        'vert': '1,0',
        'horz': '0,1'
}


def createGuide(x, y, orientation, parent):
    """ Create a sodipodi:guide node on the given parent
    """
    inkex.etree.SubElement(
            parent,
            '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}guide',
            {'position': str(x) + "," + str(y), 'orientation': orientation})


def deleteAllGuides(document):
        # getting the parent's tag of the guides
        nv = document.xpath(
                '/svg:svg/sodipodi:namedview', namespaces=inkex.NSS)[0]

        # getting all the guides
        children = document.xpath('/svg:svg/sodipodi:namedview/sodipodi:guide',
                                  namespaces=inkex.NSS)

        # removing each guides
        for element in children:
                nv.remove(element)


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
                dest='shapes', default='none',
                help='Label shapes to draw')

            self.OptionParser.add_option(
                '--delete_existing_guides',
                action='store', type='inkbool',
                dest='delete_existing_guides', default=False,
                help='Delete existing guides from document')
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

            return custom_opts

        def _construct_preset_opts(self, preset):
            """Construct an options object for a preset label template
            """

            return {}

        def _draw_label_guides(self, document, label_opts):
            """Draws label guides onto the SVG document
            """

            # Get parent tag of the guides
            nv = document.find(inkex.addNS('namedview', 'sodipodi'))

            # Draw vertical guides, left to right
            x = label_opts['margin']['l']

            for x_idx in range(label_opts['count']['x']):

                orient = GUIDE_ORIENT['vert']

                l_pos = x
                r_pos = x + label_opts['size']['x']

                # Draw guide on label left and right
                createGuide(l_pos, 0, orient, nv)
                createGuide(r_pos, 0, orient, nv)

                # Step over to next label
                x += label_opts['pitch']['x']

            # Draw horizontal guides, top to bottom
            height = self.unittouu(self.getDocumentHeight())

            y = height - label_opts['margin']['t']

            for y_idx in range(label_opts['count']['y']):

                orient = GUIDE_ORIENT['horz']

                t_pos = y
                b_pos = y - label_opts['size']['y']

                createGuide(0, t_pos, orient, nv)
                createGuide(0, b_pos, orient, nv)

                # Step over to next label
                y -= label_opts['pitch']['y']

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
                deleteAllGuides(self.document)

            self._draw_label_guides(self.document, label_opts)


if __name__ == '__main__':
    # Create effect instance and apply it.
    effect = LabelGuides()
    effect.affect()
