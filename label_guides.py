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

# Preset list
# Regular grids defined as:
#       'reg', unit, l marg, t marg, X size, Y size, X pitch, Y pitch,
#       Number across, Number down, shapes
PRESETS = {
        "LP35_37R": ['reg', 'mm', 8.5, 13, 37, 37, 39, 39, 5, 7, 'round']
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
                    }
            }

            return opts

        def _get_regular_guides(self, label_opts):
            """Get the guides for a set of labels defined by a regular grid

            This is done so that irregular-grid presets can be defined if
            needed
            """

            guides = {'v': [], 'h': []}

            x = label_opts['margin']['l']

            for x_idx in range(label_opts['count']['x']):

                l_pos = x
                r_pos = x + label_opts['size']['x']

                guides['v'].extend([l_pos, r_pos])

                # Step over to next label
                x += label_opts['pitch']['x']

            # Horizontal guides, top to bottom
            height = self.unittouu(self.getDocumentHeight())

            y = height - label_opts['margin']['t']

            for y_idx in range(label_opts['count']['y']):

                t_pos = y
                b_pos = y - label_opts['size']['y']

                guides['h'].extend([t_pos, b_pos])

                # Step over to next label
                y -= label_opts['pitch']['y']

            return guides

        def _draw_label_guides(self, document, label_opts):
            """Draws label guides from a regular guide description object
            """
            guides = self._get_regular_guides(label_opts)

            self._draw_guides(document, guides)

        def _draw_guides(self, document, guides):
            """
            Draw guides from a generic list of h/v guides
            """
            # Get parent tag of the guides
            nv = document.find(inkex.addNS('namedview', 'sodipodi'))

            # Draw vertical guides
            for g in guides['v']:
                createGuide(g, 0, GUIDE_ORIENT['vert'], nv)

            for g in guides['h']:
                createGuide(0, g, GUIDE_ORIENT['horz'], nv)

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
