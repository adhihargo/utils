import argparse
import logging
import re
import subprocess

from utils_lib import get_dstFileName
from utils_lib.ffmpeg_commands import ffmpeg_amplify

logger = logging.getLogger('ffmpeg_amplify')


def get_max_volume(filePath):
    checkVolumeCmdList = ["ffmpeg", "-hide_banner", "-i", filePath, "-af", "volumedetect", "-vn", "-sn", "-dn",
                          "-f", "null", "NUL"]
    try:
        ffmpegOutputStr = subprocess.check_output(checkVolumeCmdList, stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError:
        # no audio stream found
        ffmpegOutputStr = ""
    maxVolumeRe = re.compile(r"max_volume:\s*(?P<vol>-?\d+\.\d+)\s*dB", re.IGNORECASE)
    maxVolume = 0.0
    for line in ffmpegOutputStr.split("\n"):
        match = maxVolumeRe.search(line)
        if not match: continue
        maxVolume = float(match.group("vol"))
        break
    return maxVolume


def get_parser():
    parser = argparse.ArgumentParser(description="Amplify audio/video file")
    parser.add_argument("file_name", metavar="FILE")
    parser.add_argument("-v", "--volume", type=float, help="Manually set volume amplification level")
    parser.add_argument("-s", "--show_only", action="store_true", help="Show file's current volume level, then exit")
    parser.add_argument("-m", "--min_threshold", type=float, default=-1.0)
    parser.add_argument("-M", "--max_threshold", type=float, default=-30.0)
    parser.add_argument("-y", dest="suppressQuestion", action="store_true")
    parser.add_argument("-V", dest="verbose", action="store_true")
    parser.add_argument("--suffix", dest="suffix", default="_amp")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    srcFilePath = args.file_name
    dstFilePath = get_dstFileName(srcFilePath, args.suffix)
    maxVolume = get_max_volume(srcFilePath)
    if args.show_only:
        logger.info("MAX VOLUME: {}".format(maxVolume))
        return

    ampVolume = args.volume if args.volume else abs(maxVolume)
    min_threshold = abs(args.min_threshold) * -1
    max_threshold = abs(args.max_threshold) * -1
    if not args.volume and (maxVolume >= min_threshold or maxVolume <= max_threshold):
        logger.info("Skipping file: {}".format(srcFilePath))
        return

    ffmpeg_amplify(srcFilePath, dstFilePath, ampVolume,
                   suppressQuestion=args.suppressQuestion, verbose=args.verbose)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
