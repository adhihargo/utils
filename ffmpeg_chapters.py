import argparse
import datetime
import os
import re
import subprocess
import sys
import tempfile

from utils_lib import get_dstFileName
from utils_lib.ffmpeg_commands import ffprobe_duration

CHAPTER_FILENAME = "chapters.txt"


def append_metadataFile(inputChapterFilePath, outputMetadataFilePath, duration: datetime.timedelta = None):
    chapters = list()
    with open(inputChapterFilePath, 'r') as f:
        for line in f:
            line = line.strip()
            x = re.match(r"^(?:(\d{,2}):)?(\d{1,2}):(\d{1,2})[\s-]+(.*)$", line)
            if not x:
                raise Exception("SKIPPED: ", line)
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
        if duration is not None:
            chapters.append({
                "startTime": (duration.total_seconds()) * 1000
            })

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
    metadataFile = tempfile.NamedTemporaryFile(delete=False)
    metadataFile.close()

    doEmbedChapters = False
    doEmbedSubtitle = False

    subFilePath = os.path.splitext(srcFilePath)[0] + ".srt"
    if os.path.exists(subFilePath):
        doEmbedSubtitle = True

    chapterFileDir = os.path.dirname(srcFilePath)
    chapterFilePath = os.path.join(chapterFileDir, CHAPTER_FILENAME)
    if os.path.exists(chapterFilePath):
        # get original metadata
        cmdList = ["ffmpeg", "-hide_banner", "-y", "-i", srcFilePath, "-f", "ffmetadata", metadataFile.name]
        subprocess.check_output(cmdList)

        duration = ffprobe_duration(srcFilePath)
        append_metadataFile(chapterFilePath, metadataFile.name, duration)
        doEmbedChapters = True
    else:
        print("No chapters.txt file found")

    dstFilePath = get_dstFileName(srcFilePath)
    cmdList = ["ffmpeg", "-hide_banner", "-y", "-i", srcFilePath]
    if doEmbedChapters:
        cmdList.extend(["-i", metadataFile.name, "-map_metadata", "1"])
    if doEmbedSubtitle:
        cmdList.extend(["-i", subFilePath, "-c:s", "mov_text"])
    cmdList.extend(["-c:v", "copy", "-c:a", "copy", dstFilePath])
    if doEmbedChapters or doEmbedSubtitle:
        retval = subprocess.call(cmdList)
        if retval == 0:
            os.remove(srcFilePath)
            os.rename(dstFilePath, srcFilePath)


if __name__ == '__main__':
    main()
