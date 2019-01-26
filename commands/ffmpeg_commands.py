import logging
import subprocess

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
    audioBitrateList = [streamTuple[1][:-3]
                        for streamTuple in streamList
                        if streamTuple[0] == "audio"
                        ]
    bitrate = audioBitrateList[0] + "k" if audioBitrateList else optBitrate
    return bitrate


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

