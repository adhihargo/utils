#!/usr/bin/env python

import argparse
import configparser
import datetime
import logging
import os
import subprocess
import sys
import time

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
sys.path.append(os.path.dirname(__file__))
from utils_lib import ffmpeg_commands, get_dstFileName


def get_parser():
    parser = argparse.ArgumentParser(description="Cut an audio/video file.")
    parser.add_argument("file_name", metavar="FILE")
    parser.add_argument("-s", dest="start",
                        help="Timestamp of starting point to cut from.")
    parser.add_argument("-e", dest="end",
                        help="Timestamp of end point to cut to.")
    parser.add_argument("--suffix", dest="suffix", default="_",
                        help="Suffix to be appended to resulting filename.")
    parser.add_argument("-c", "--conf", action="store_true",
                        help="Mark input FILE as config file. See README for format. "
                             "If set, other switches but -y and -V are ignored.")
    parser.add_argument("-y", dest="suppressQuestion", action="store_true",
                        help="Suppress question if file exists.")
    parser.add_argument("-V", dest="verbose", action="store_true",
                        help="Verbosity")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.conf:
        confFilePath = args.file_name
        config = configparser.ConfigParser(interpolation=None)
        config.read(confFilePath)
        if not {"main", "sections"} <= set(config.sections()):
            parser.error("config file does not contain the required sections.")
        if not "src" in config["main"]:
            parser.error("config file does not state source file.")

        srcFilePath = config["main"]["src"]
        if not os.path.isfile(srcFilePath):
            parser.error("source file does not exist.")

        # whitespace-separated sequence of section names to process
        sectionStr = config["main"].get("sections", "")
        sectionList = sectionStr.split(" ") if sectionStr else []

        sectionDict = {}
        for sectionName in sectionList:
            sectionTest = sectionName.endswith("*")
            sectionData = {"test": sectionTest}
            sectionDict[sectionName[:-1] if sectionTest else sectionName] = sectionData

        sectionPairs = config.items("sections")
        for index, (section, value) in enumerate(sectionPairs):
            timeStart = datetime.datetime.now()

            # skip sections not listed in config["main"]["sections"]
            sectionData = sectionDict.get(section)
            if not sectionData:
                continue

            sectionStart = value or None
            if sectionData["test"]:
                startStr = sectionStart if sectionStart else "0:0:0"
                dotPos = startStr.find(".")  # exclude milliseconds if present
                startTime = time.strptime(startStr[:dotPos if dotPos > -1 else len(startStr)], "%H:%M:%S")

                # sections suffixed with '*' will be processed only the first 5 seconds, intended for test cuts
                start = datetime.timedelta(hours=startTime.tm_hour, minutes=startTime.tm_min, seconds=startTime.tm_sec)
                end = start + datetime.timedelta(seconds=5)
                sectionEnd = str(end)
            else:
                sectionEnd = sectionPairs[index + 1][1] if (index < len(sectionPairs) - 1) else None
            sectionSuffix = "_{:>02}".format(section)
            dstFilePath = get_dstFileName(srcFilePath, sectionSuffix)

            logger.info("Processing section {}: {} - {}".format(section, sectionStart, sectionEnd))
            ffmpeg_commands.ffmpeg_cut(srcFilePath, dstFilePath, sectionStart, sectionEnd,
                                       suppressQuestion=args.suppressQuestion, verbose=args.verbose)

            timeEnd = datetime.datetime.now()
            timeDuration = timeEnd - timeStart
            logger.info("Section {} processing duration: {}".format(section, timeDuration))

    else:
        srcFilePath = args.file_name
        dstFilePath = get_dstFileName(srcFilePath, args.suffix)
        timeStart = args.start
        timeEnd = args.end
        suppressQuestion = args.suppressQuestion
        verbose = args.verbose
        ffmpeg_commands.ffmpeg_cut(srcFilePath, dstFilePath, timeStart, timeEnd,
                                   suppressQuestion=suppressQuestion, verbose=verbose)

    subprocess.call("echo /|choice /N 2> nul | echo dummy > nul", shell=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
