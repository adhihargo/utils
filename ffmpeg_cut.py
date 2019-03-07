#!/usr/bin/env python

import argparse
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
sys.path.append(os.path.dirname(__file__))
from utils_lib import ffmpeg_commands


def get_arg_parser():
    parser = argparse.ArgumentParser(description="Cut an audio / video file.")
    parser.add_argument("file_name", metavar="FILE")
    parser.add_argument("-s", dest="start")
    parser.add_argument("-e", dest="end")
    parser.add_argument("-y", dest="suppressQuestion", action="store_true")
    parser.add_argument("-V", dest="verbose", action="store_true")
    parser.add_argument("--suffix", dest="suffix", default="_")

    return parser


def main():
    parser = get_arg_parser()
    args = parser.parse_args()

    suffix = args.suffix
    srcFilePath = args.file_name
    dstFilePath = get_dstFileName(srcFilePath, suffix)
    timeStart = args.start
    timeEnd = args.end
    suppressQuestion = args.suppressQuestion
    verbose = args.verbose
    ffmpeg_commands.ffmpeg_cut(srcFilePath, dstFilePath, timeStart, timeEnd,
                               suppressQuestion=suppressQuestion, verbose=verbose)


def get_dstFileName(srcFileName, suffix="_"):
    if not suffix:
        raise Exception("Suffix must not be empty.")

    baseFileName, baseFileExt = os.path.splitext(srcFileName)
    dstFileName = "{}{}{}".format(baseFileName, suffix, baseFileExt)
    return dstFileName


if __name__ == '__main__':
    main()
