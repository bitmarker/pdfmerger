# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 08:49:39 2015

@author: Matt Gumbley  (stackoverflow)
changed by Hanspeter Schmid to deal with already cropped pages
"""

import copy
import math
from PyPDF2 import PdfFileReader, PdfFileWriter
import argparse
import os


def split_pages2(src, dst):
    src_f = open(src, 'r+b')
    dst_f = open(dst, 'w+b')

    input = PdfFileReader(src_f)
    output = PdfFileWriter()

    for i in range(input.getNumPages()):
        # make two copies of the input page
        pp = input.getPage(i)
        p = copy.copy(pp)
        q = copy.copy(pp)

        # the new media boxes are the previous crop boxes
        p.mediaBox = copy.copy(p.cropBox)
        q.mediaBox = copy.copy(p.cropBox)

        x1, x2 = p.mediaBox.lowerLeft
        x3, x4 = p.mediaBox.upperRight

        x1, x2 = math.floor(x1), math.floor(x2)
        x3, x4 = math.floor(x3), math.floor(x4)
        x5, x6 = x1+math.floor((x3-x1)/2), x2+math.floor((x4-x2)/2)

        if (x3-x1) > (x4-x2):
            # horizontal
            q.mediaBox.upperRight = (x5, x4)
            q.mediaBox.lowerLeft = (x1, x2)

            p.mediaBox.upperRight = (x3, x4)
            p.mediaBox.lowerLeft = (x5, x2)
        else:
            # vertical
            p.mediaBox.upperRight = (x3, x4)
            p.mediaBox.lowerLeft = (x1, x6)

            q.mediaBox.upperRight = (x3, x6)
            q.mediaBox.lowerLeft = (x1, x2)


        p.artBox = p.mediaBox
        p.bleedBox = p.mediaBox
        p.cropBox = p.mediaBox

        q.artBox = q.mediaBox
        q.bleedBox = q.mediaBox
        q.cropBox = q.mediaBox

        output.addPage(q)
        output.addPage(p)

    output.write(dst_f)
    src_f.close()
    dst_f.close()


def main(arguments):
    dist = os.path.join(arguments.dist, os.path.basename(arguments.src))
    split_pages2(arguments.src, dist)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='Source file path')
    parser.add_argument('dist', help='Destination folder path')
    main(parser.parse_args())

