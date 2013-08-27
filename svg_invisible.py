#  License  : MIT
#  Author   : Jarno Leppänen
#  Date     : 2013-08-26

import os
import re
from freestyle import *
from Functions0D import *
from PredicatesB1D import *
from PredicatesU0D import *
from PredicatesU1D import *
from logical_operators import *
from shaders import *
from parameter_editor import *
from ChainingIterators import *

# select
preds = [
    pyNatureUP1D(Nature.SILHOUETTE),
    pyNatureUP1D(Nature.CREASE),
    ContourUP1D()
]
upred = join_unary_predicates(preds, OrUP1D)
upred = AndUP1D(NotUP1D(QuantitativeInvisibilityUP1D(0)), upred)
Operators.select(upred)

# chain
Operators.bidirectional_chain(ChainSilhouetteIterator())

# sort
Operators.sort(pyZBP1D())

# shade and write svg
path = re.sub(r'\.blend$|$', '.svg', bpy.data.filepath)
f = open(path, "a")

scene = getCurrentScene()
w = scene.render.resolution_x * scene.render.resolution_percentage / 100
h = scene.render.resolution_y * scene.render.resolution_percentage / 100

class SVGPathShader(StrokeShader):
    def shade(self, stroke):
        f.write('<path fill="none" stroke="black" stroke-width="1" stroke-dasharray="2,2" d="\nM ')
        for v in stroke:
            x, y = v.point
            f.write('%.3f,%.3f ' % (x, h - y))
        f.write('"\n />')

shaders_list = [
    SamplingShader(50),
    SVGPathShader(),
    ConstantColorShader(1, 0, 0),
    ConstantThicknessShader(10)
    ]

f.write('<g id="invisible">\n')
Operators.create(TrueUP1D(), shaders_list)
f.write('</g>\n')

f.close()
