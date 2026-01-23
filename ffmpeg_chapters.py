import argparse
import os
import re
import subprocess
import sys

from utils_lib import get_dstFileName

CHAPTER_FILENAME = "chapters.txt"
METADATA_FILENAME = "metadata.txt"


def append_metadataFile(inputChapterFilePath, outputMetadataFilePath):
    chapters = list()
    with open(inputChapterFilePath, 'r') as f:
        for line in f:
            line = line.strip()
            x = re.match(r"^(?:(\d{2}):)?(\d{1,2}):(\d{1,2}) (.*)", line)
            if not x:
                print("SKIPPED: ", line)
                continue
            hrs = int(x.group(1)) if x.group(1) else 0
            mins = int(x.group(2))
            secs = int(x.group(3))
            title = x.group(4)

            minutes = (hrs * 60) + mins
            seconds = secs + (minutes * 60)
            timestamp = (seconds * 1000)
            chap = {
                "title": title,
                "startTime": timestamp
            }
            chapters.append(chap)

    text = ""
    for i in range(len(chapters) - 1):
        chap = chapters[i]
        title = chap['title']
        start = chap['startTime']
        end = chapters[i + 1]['startTime'] - 1
        text += f"""
[CHAPTER]
TIMEBASE=1/1000
START={start}
END={end}
title={title}
"""

    with open(outputMetadataFilePath, 'a') as f:
        f.write(text)


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
    srcFilePath = sys.argv[1]
    metadataFilePath = os.path.abspath(METADATA_FILENAME)
    subprocess.call(["ffmpeg", "-y", "-i", srcFilePath, "-f", "ffmetadata", metadataFilePath])

    chapterFilePath = os.path.abspath(CHAPTER_FILENAME)
    if not os.path.exists(chapterFilePath):
        print("No chapters.txt file found")

    append_metadataFile(chapterFilePath, metadataFilePath)

    dstFilePath = get_dstFileName(srcFilePath)
    subprocess.call(["ffmpeg", "-y", "-i", srcFilePath, "-i", METADATA_FILENAME,
                     "-map_metadata", "1", "-codec", "copy", dstFilePath])


if __name__ == '__main__':
    main()
