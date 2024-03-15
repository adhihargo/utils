import argparse
import contextlib
import os.path
import re
import subprocess
import tempfile
from collections import namedtuple

TOCLineInfo = namedtuple("TOCLineInfo", ["level", "title", "page"])
LINE_RE = re.compile(r"(?P<LEVEL>\s*)(?P<TITLE>.+)\s+(?P<PAGE>\d+)\s*$")


def read_tocfile(file_path):
    toc_list = []
    with open(file_path, 'r') as f:
        for line_index, line in enumerate(f, start=1):
            match = LINE_RE.match(line)
            if not match:
                if line.strip():
                    print("SKIPPED({}): {}".format(line_index, line.strip()))
                continue

            line_info = match.groupdict()
            line_info["LEVEL"] = len(line_info["LEVEL"]) + 1  # replace with char count = numeric level
            toc_list.append(TOCLineInfo(line_info["LEVEL"], line_info["TITLE"], line_info["PAGE"]))
    return toc_list


def toclist_to_datalist(toc_list):
    line_list = []
    for toc in toc_list:
        line_list.append(
            "BookmarkBegin\n" +
            "BookmarkTitle: {}\n".format(toc.title) +
            "BookmarkLevel: {}\n".format(toc.level) +
            "BookmarkPageNumber: {}\n".format(toc.page)
        )
    return line_list


def write_datafile(data_file, data_list):
    for l in data_list:
        data_file.write(l)
    data_file.seek(0)


@contextlib.contextmanager
def temp_file():
    tf = tempfile.NamedTemporaryFile("w+", delete=False)
    yield tf
    tf.close()
    os.remove(tf.name)


def generate_output_path(input_path):
    input_path_split = os.path.splitext(input_path)
    output_path = "{}~{}".format(input_path_split[0], input_path_split[1])
    return output_path


def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-d", "--dump", nargs="?", help="Dump PDF data to file.")
    parser.add_argument("-s", "--set", nargs="?", help="Set PDF data from file.")
    parser.add_argument("-t", "--toc", nargs="?", help="Set PDF bookmark data from TOC file.")
    parser.add_argument("-o", "--output", nargs="?", help="Output PDF file if setting PDF data.")
    parser.add_argument('file')
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    input_path = args.file
    if isinstance(args.dump, str):
        subprocess.run(["pdftk", input_path, "dump_data", "output", args.dump])
    elif isinstance(args.set, str):
        output_path = args.output
        if output_path is None:
            output_path = generate_output_path(input_path)
        subprocess.run(["pdftk", input_path, "update_info", args.set, "output", output_path])
    elif isinstance(args.toc, str):
        output_path = args.output
        if output_path is None:
            output_path = generate_output_path(input_path)

        with temp_file() as tf:
            toc_list = read_tocfile(args.toc)
            data_list = toclist_to_datalist(toc_list)
            write_datafile(tf, data_list)
            subprocess.run(["pdftk", input_path, "update_info", tf.name, "output", output_path])


if __name__ == '__main__':
    main()
