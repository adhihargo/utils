#!/usr/bin/env python

import getopt
import glob
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
sys.path.append(os.path.dirname(__file__))
from utils_lib import ffmpeg_commands


def main():
    fileNameList, optDict = parser_read_args(sys.argv[1:])
    curDirPath = os.getcwd()

    # extend original source file list with the content of textfiles containing
    # another list
    srcListFilePath = optDict.get("--file")
    if srcListFilePath:
        with open(srcListFilePath, "rb") as srcListFile:
            fileNameList.extend([fn.strip() for fn in srcListFile.readlines()])

    optFormat = optDict.get("-f", "mp3")
    for srcFileName in fileNameList:
        # check if filename spec is a glob. if it is, skip and add glob result to
        # filelist.
        if srcFileName.find("*") > -1:
            fileNameList.extend(glob.glob(srcFileName))
            continue

        # construct output filename
        dstFileName = get_dstFileName(srcFileName, optFormat)
        if srcFileName == dstFileName:
            continue

        srcFilePath = os.path.join(curDirPath, srcFileName)
        dstFilePath = os.path.join(curDirPath, dstFileName)
        logger.debug("SRC: %s", srcFileName)
        logger.debug("DST: %s", dstFileName)

        optBitrate = ffmpeg_commands.ffprobe_audio_bitrate(srcFilePath, optDict.get("-b", "128k"))
        logger.debug("BR: %s", optBitrate)

        # no actual conversion if only testing
        optTest = optDict.has_key("--test")
        if optTest:
            logger.debug("Test. Skipping.")
            continue

        # execute conversion
        optVerbose = optDict.has_key("-v")
        optSuppressQuestion = optDict.has_key("-y")
        ffmpeg_commands.ffmpeg_convert_audio(srcFilePath, dstFilePath, optBitrate, optFormat, optSuppressQuestion,
                                             optVerbose)


def get_dstFileName(srcFileName, fileFormat):
    baseFileName = os.path.splitext(srcFileName)[0]
    dstFileName = "%s.%s" % (baseFileName, fileFormat)
    return dstFileName


def parser_read_args(args):
    # -b: bitrate
    # -f: format
    # -y: suppress question
    # -v: verbose
    # --test: skip actual encoding process
    # --file: textfile containing list of inputfiles
    optList, fileNameList = getopt.getopt(args, "b:f:yv", ["test", "file="])
    optDict = dict(optList)
    return fileNameList, optDict


if __name__ == '__main__':
    main()
