import os


def get_dstFileName(srcFileName, suffix="_"):
    if not suffix:
        raise Exception("Suffix must not be empty.")

    baseFileName, baseFileExt = os.path.splitext(srcFileName)
    dstFileName = "{}{}{}".format(baseFileName, suffix, baseFileExt)
    return dstFileName
