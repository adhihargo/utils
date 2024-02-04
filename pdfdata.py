import argparse
import os.path
import subprocess


def get_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-d", "--dump", nargs="?", help="Dump PDF data to file.")
    parser.add_argument("-s", "--set", nargs="?", help="Set PDF data from file.")
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
            input_path_split = os.path.splitext(input_path)
            output_path = "{}~{}".format(input_path_split[0], input_path_split[1])
        subprocess.run(["pdftk", input_path, "update_info", args.set, "output", output_path])


if __name__ == '__main__':
    main()
