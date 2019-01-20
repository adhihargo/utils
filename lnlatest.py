#!/usr/bin/python3

import argparse
import ctypes
import glob
import logging
import os
import subprocess
import sys

TEST_LINK_NAME = "blender"
TEST_ROOT_DIR_PATH = r"D:/site-doc/"
TEST_SUB_DIR_PATTERN = "blender_*"

logger = logging.getLogger(__name__)


def is_admin():
    logger.debug("Checking for privilege...")
    if sys.platform != "win32":
        return True
    return ctypes.windll.shell32.IsUserAnAdmin() != 0


def get_dir_list(dir_path, pattern):
    logger.debug("Listing directories...")
    dir_path = os.path.normpath(dir_path)
    length_dir_path = len(dir_path)

    is_abs_path = os.path.isabs(pattern)

    path_pattern = pattern if is_abs_path \
        else os.path.join(dir_path, pattern)
    logger.debug("Path pattern: %s", path_pattern)

    file_stat_pair_list = []
    for fp in glob.iglob(path_pattern):
        if os.path.islink(fp) or not os.path.isdir(fp):
            # only list directories
            continue

        logger.debug("Directory: %s", fp)
        fp_mtime = os.stat(fp).st_mtime
        fp_processed = fp if is_abs_path \
            else fp[length_dir_path + 1:]
        file_stat_pair_list.append((fp_processed, fp_mtime))

    return [v[0] for v in sorted(file_stat_pair_list, key=lambda v: v[1])]


def get_dir_latest(dir_path, pattern):
    dir_list = get_dir_list(dir_path, pattern)
    return dir_list[-1] if dir_list else None


def get_create_link_command_list(dir_path, pattern, link_name):
    subdir_latest = get_dir_latest(dir_path, pattern)
    logger.info("Found latest dir: %s", subdir_latest)
    if subdir_latest is None:
        return []

    if sys.platform == "win32":
        return ["mklink", "/D", link_name, subdir_latest]
    else:
        return ["ln", "-s", subdir_latest, link_name]


def create_link(dir_path, pattern, link_name):
    """Execute command to create link.

    :param dir_path: Root directory of both symlink to be created and directories to match pattern with.
    :param pattern: Glob pattern to find matching directories.
    :param link_name: Symlink to be created.
    """
    # symlink will be created relative to target directory's parent. So set the parent as current directory.
    os.chdir(dir_path)

    command_list = get_create_link_command_list(dir_path, pattern, link_name)
    if not command_list:
        logger.error("No matching directory found.")
        return

    try:
        if is_admin():
            logger.debug("Executing link command.")
            subprocess.check_call(command_list, shell=(sys.platform == "win32"))
        else:
            logger.debug("Not at elevated permission, try to run as admin.")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except subprocess.CalledProcessError:
        logger.error("Error on called process")


def verify_safe_link_path(link_path, erase_old_link=False):
    """Verify if link path is safe to use. `mklink` and `ln` can fail if there's already a link there.

    :rtype: boolean
    :param link_path: Path to check
    :param erase_old_link: Remove LINK_PATH if exists.
    :return: True if link doesn't exist or, if DELETE_OLD_LINK is True, removal succeeds.
    """
    if os.path.exists(link_path):

        # only heed delete_old_link flag if it's a link
        if os.path.islink(link_path):
            if erase_old_link:
                os.remove(link_path)
                return True

        return False
    return True


TEST_ARGS_STRING = "blender -e"


def get_arg_parser():
    parser = argparse.ArgumentParser(
        description="Create symbolic link to latest directory matching a pattern.")
    parser.add_argument("link_name", metavar="LINK")
    parser.add_argument("pattern", metavar="PATTERN")
    parser.add_argument("-d", dest="dir_path")
    parser.add_argument("-e", dest="erase_old_link", action="store_true")
    parser.add_argument("-V", dest="verbose", action="store_true")

    return parser


def get_args():
    """Get program invocation arguments, filling in default values.

    :return: Argument list
    """
    parser = get_arg_parser()
    args = parser.parse_args(sys.argv[1:])
    if args.dir_path is None:
        args.dir_path = os.getcwd()
    return args


def start():
    args = get_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if verify_safe_link_path(args.link_name, args.erase_old_link):
        create_link(args.dir_path, args.pattern, args.link_name)
    else:
        logger.error("Link exists, can't continue. Use -e to remove existing link.")


if __name__ == '__main__':
    start()
