#!/usr/bin/env python

import getopt
import glob
import os
import subprocess
import sys
from pprint import pprint

import logging
logging.basicConfig()
logger = logging.getLogger("mp4_mp3")
# logger.setLevel(logging.DEBUG)

# -b: bitrate
# -f: format
# -y: suppress question
# -v: verbose
# --test: skip actual encoding process
# --file: textfile containing list of inputfiles
optList, fileNameList = getopt.getopt(sys.argv[1:], "b:f:yv", ["test", "file="])
optDict = dict(optList)
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
    if srcFileName.find("*")>-1:
        fileNameList.extend(glob.glob(srcFileName))
        continue
    
    # construct output filename
    baseFileName = os.path.splitext(srcFileName)[0]
    dstFileName = "%s.%s" % (baseFileName, optFormat)
    if srcFileName==dstFileName:
        continue

    srcFilePath = os.path.join(curDirPath, srcFileName)
    dstFilePath = os.path.join(curDirPath, dstFileName)
    logger.debug("SRC: %s", srcFileName)
    logger.debug("DST: %s", dstFileName)

    # guess most optimal bitrate for output audiofile from input videofile's
    # audio channel bitrate, and use it even if already set in switch
    ffprobeCmdList = [ "ffprobe", "-show_entries", "stream=codec_type,bit_rate",
                       "-of", "compact=p=0:nk=1",
                       "-v", "0", srcFilePath,
                       ]
    streamList = [ line.split("|")
                   for line in subprocess.check_output(ffprobeCmdList).split("\n")
                   ]
    audioBitrateList = [ streamTuple[1][:-3]
                  for streamTuple in streamList
                  if streamTuple[0]=="audio"
                  ]
    optBitrate = audioBitrateList[0] + "k" if audioBitrateList else optDict.get("-b", "128k")

    # no actual conversion if only testing
    if optDict.has_key("--test"):
        logger.debug("Test. Skipping.")
        continue

    # execute conversion
    ffmpegCmdList = [
        "ffmpeg", "-y" if optDict.has_key("-y") else "n",
        "-i", srcFilePath,
        "-ab", optBitrate,
        "-v", "32" if optDict.has_key("-v") else "24",
        "-f", optFormat,
        dstFilePath,
        ]
    logger.debug("EXE: %s", ffmpegCmdList)
    subprocess.call(ffmpegCmdList)
