import os


def get_dstFileName(srcFileName, suffix="_", dstDir=None):
    if not suffix:
        raise Exception("Suffix must not be empty.")

    if dstDir is not None:
        if not os.path.exists(dstDir):
            os.makedirs(dstDir)
        srcFileName = os.path.join(dstDir, os.path.basename(srcFileName))

    baseFileName, baseFileExt = os.path.splitext(srcFileName)
    dstFileName = "{}{}{}".format(baseFileName, suffix, baseFileExt)
    return dstFileName
