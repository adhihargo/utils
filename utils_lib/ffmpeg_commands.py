import logging
import re
import subprocess
from datetime import timedelta, datetime

TIME_RE_STR = "(?P<hour>\d+):(?P<min>\d+):(?P<sec>\d+)(\.(?P<msec>\d+))?"

logger = logging.getLogger(__name__)


def ffprobe_audio_bitrate(srcFilePath, optBitrate):
    # guess most optimal bitrate for output audiofile from input videofile's
    # audio channel bitrate, and use it even if already set in switch
    ffprobeCmdList = ["ffprobe", "-show_entries", "stream=codec_type,bit_rate",
                      "-of", "compact=p=0:nk=1",
                      "-v", "0", srcFilePath,
                      ]
    streamList = [line.split("|")
                  for line in subprocess.check_output(ffprobeCmdList).split("\n")
                  ]
    audioBitrateList = [streamTuple[1].strip()[:-3]
                        for streamTuple in streamList
                        if streamTuple[0] == "audio"
                        ]
    bitrate = audioBitrateList[0] + "k" if audioBitrateList else optBitrate
    return bitrate


def ffprobe_duration(filePath):
    """Converts ffprobe output into duration using timedelta object, so it can be used directly in time arithmetics."""
    ffprobeCmdList = ["ffprobe", "-hide_banner", filePath]
    ffprobeOutputStr = subprocess.check_output(ffprobeCmdList, stderr=subprocess.STDOUT).decode("utf-8")
    duration_re = re.compile(r"duration: " + TIME_RE_STR, re.IGNORECASE)
    duration = None
    for line in ffprobeOutputStr.split("\n"):
        match = duration_re.search(line)
        if match:
            duration = timedelta(hours=int(match.group("hour")), minutes=int(match.group("min")),
                                 seconds=int(match.group("sec")), milliseconds=int(match.group("msec")) * 10)
            break
    return duration


def ffmpeg_convert_audio(srcFilePath, dstFilePath, bitrate, fileFormat, suppressQuestion=False, verbose=False):
    ffmpegCmdList = \
        ["ffmpeg", "-y" if suppressQuestion else "-n",
         "-i", srcFilePath,
         "-ab", bitrate,
         "-v", "32" if verbose else "24",
         "-f", fileFormat,
         dstFilePath,
         ]
    logger.debug("EXE: %s", ffmpegCmdList)
    subprocess.call(ffmpegCmdList)


def ffmpeg_cut(srcFilePath, dstFilePath, timeStart=None, timeEnd=None, suppressQuestion=False, verbose=False):
    duration = None
    if (timeStart and timeStart.endswith("-")) or (timeEnd and timeEnd.endswith("-")):
        duration = ffprobe_duration(srcFilePath)

    timeList = []
    for timeStr in [timeStart, timeEnd]:
        if timeStr is not None and timeStr.endswith("-"):
            try:
                timeEndDict = {k: int(v) for k, v in
                               zip(["seconds", "minutes", "hours"], reversed(timeStr[:-1].split(":")))}
                timeEndObj = timedelta(**timeEndDict)
                timeEndRealObj = duration - timeEndObj
                logger.debug("{} = {} - {} = {}".format(timeStr, duration, timeEndObj, timeEndRealObj))
                timeStr = str((datetime.min + timeEndRealObj).time())
            except OverflowError:
                logger.exception("Time format error, ignored: {}".format(timeStr))
                timeStr = None
        timeList.append(timeStr)
    timeStart, timeEnd = timeList

    ffmpegCmdList = \
        ["ffmpeg", "-y" if suppressQuestion else "-n",
         "-i", srcFilePath, ] + \
        (["-ss", timeStart] if timeStart else []) + \
        (["-to", timeEnd, ] if timeEnd else []) + \
        ["-c", "copy",
         "-v", "32" if verbose else "24",
         dstFilePath,
         ]
    logger.debug("EXE: %s", ffmpegCmdList)
    subprocess.call(ffmpegCmdList)


def ffmpeg_amplify(srcFilePath, dstFilePath, ampVolume, codec=None, bitrate=None, suppressQuestion=False, verbose=False):
    amplifyCmdList = (["ffmpeg", "-y" if suppressQuestion else "-n", "-i", srcFilePath, "-v", "32" if verbose else "24",
                       "-vcodec", "copy", "-af", "volume={}dB".format(ampVolume)] +
                      (["-acodec", codec] if codec else []) +
                      (["-ab", bitrate] if bitrate else []) +
                      [dstFilePath])
    logger.debug("AMPLIFYING {}dB: {}".format(ampVolume, srcFilePath))
    subprocess.call(amplifyCmdList)
