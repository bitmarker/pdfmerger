"""
@author: Leonid Lezner
"""

import copy
import math
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import argparse
import os
import glob


def merge_pdfs(source_folder, output_file, rotate_deg):
    """
    Function for merging multiple pdf files into one with
    optional page rotation.

    :param source_folder: Folder containing separate pdf files
    :param output_file: Merged file
    :param rotate_deg: rotation of page (CW in degree)
    :return: None
    """

    output = PdfFileWriter()

    filenames = glob.glob(os.path.join(source_folder, '*.pdf'))

    for filename in filenames:
        pdf_reader = PdfFileReader(open(filename, 'rb'))

        for pagenum in range(pdf_reader.numPages):
            page = pdf_reader.getPage(pagenum)

            if rotate_deg is not None:
                page.rotateClockwise(int(rotate_deg))

            output.addPage(page)

    outputStream = open(output_file, "wb")
    output.write(outputStream)
    outputStream.close()


def main(arguments):
    merge_pdfs(arguments.src, arguments.output, arguments.r)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help='Source folder path')
    parser.add_argument('output', help='Destination file path')
    parser.add_argument('-r', help='Rotate clockwise (deg)', type=int)
    main(parser.parse_args())

