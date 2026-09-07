import argparse
import os
import re
import sys
import traceback
from pathlib import Path

PREFIX_RE = re.compile(r"^(\d+)\.\s")


def get_parser():
    parser = argparse.ArgumentParser(
        description="Add index prefix to filenames in a directory based on file modification date.")
    parser.add_argument("pathlist", metavar="PATH", nargs="*", default=[os.getcwd()],
                        help="Directory containing files to add prefix to.")
    parser.add_argument("-e", dest="ext", default="mp4",
                        help="Filename extension of files to rename.")
    parser.add_argument("-a", dest="ascii", action="store_true",
                        help="Force-convert filename to ASCII format.")

    return parser


def get_mdate(fn):
    f_stat = os.lstat(fn)
    return f_stat.st_mtime


def list_latest_files(args, root_path: Path):
    ren_file_list = []
    last_index = None
    unindexed_found = False
    glob_str = "*.{}".format(args.ext)
    for f_path in sorted(root_path.glob(glob_str), key=get_mdate):
        f_name = f_path.name
        name_match = PREFIX_RE.match(f_name)
        if not unindexed_found:
            if name_match:
                last_index = name_match.group(1)
            else:
                unindexed_found = True
                ren_file_list.append(f_path)
        else:
            ren_file_list.append(f_path)
    print("Last index: {}".format(last_index))

    if last_index is None:
        last_index = 0
    else:
        last_index = int(last_index)
    for f_index, f_path in enumerate(ren_file_list, start=last_index + 1):
        f_name = f_path.name
        if args.ascii:
            f_name = f_name.encode("ascii", "ignore").decode("ascii")  # remove problematic chars
        f_name = PREFIX_RE.sub("", f_name)
        f_path_new = Path(f_path.parent, "{:02}. ".format(f_index) + f_name)
        print("Renaming: ", f_path_new)
        f_path.rename(f_path_new)


def main():
    parser = get_parser()
    args = parser.parse_args()

    path_list = args.pathlist
    try:
        for root_dir in path_list:
            if not os.path.isdir(root_dir):
                print("Skipped: {}".format(root_dir))
                continue

            list_latest_files(args, Path(root_dir))
    except Exception:
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
