import argparse
import os.path
import re
import subprocess
import tempfile
from collections import namedtuple

TOCLineInfo = namedtuple("TOCLineInfo", ["level", "title", "page"])
LINE_RE = re.compile(r"(?P<LEVEL>\s*)(?P<TITLE>.+)\s+(?P<PAGE>\d+)\s*$")


def get_toc_list(file_path):
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


def toc_to_pdfdata(toc_list):
    line_list = []
    for toc in toc_list:
        line_list.extend([
            "BookmarkBegin",
            "BookmarkTitle: {}".format(toc.title),
            "BookmarkLevel: {}".format(toc.level),
            "BookmarkPageNumber: {}".format(toc.page)
        ])
    return line_list


def get_toc_tempfile(file_path):
    toc_list = get_toc_list(file_path)
    line_list = toc_to_pdfdata(toc_list)
    tf = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    for l in line_list:
        tf.write(l)
        tf.flush()
        tf.write("\n")
    tf.seek(0)
    return tf


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

        with get_toc_tempfile(args.toc) as toc_file:
            toc_file_path = toc_file.name
            subprocess.run(["pdftk", input_path, "update_info", toc_file_path, "output", output_path])
        if os.path.isfile(toc_file_path):
            os.remove(toc_file_path)


if __name__ == '__main__':
    main()
