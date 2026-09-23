# Make manually-added doc sites recognized as HTTrack mirror sites
import argparse
import configparser
import io
import itertools
import logging
import os.path

logger = logging.getLogger(os.path.basename(__file__))


class HeaderlessConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.optionxform = str  # preserve key case

    def read_file(self, fp, source=None):
        prepended_f = itertools.chain(("[main]",), fp)
        super().read_file(prepended_f)

    def write(self, fp, space_around_delimiters=False):
        # We temporarily redirect the default write output to a string list
        buf = io.StringIO()
        super().write(buf, space_around_delimiters=space_around_delimiters)

        # Filter out lines that start with '[' and end with ']'
        buf.seek(0)
        for line in buf:
            if not (line.strip().startswith('[') and line.strip().endswith(']')):
                fp.write(line)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Make manually-added doc sites recognized as HTTrack mirror sites.")
    parser.add_argument("rootpathlist", metavar="PATH", nargs="*", default=[],
                        help="Directory containing files to add prefix to.")
    parser.add_argument("-s", "--site", action="store_true",
                        help="Interpret arguments as site paths")
    parser.add_argument("-c", "--category", help="Site category")

    return parser


def process_site(site_path, category="apps", force=False):
    if not os.path.isdir(site_path):
        return

    logger.debug("Processing site: {}".format(site_path))
    cache_path = os.path.join(site_path, "hts-cache")
    os.makedirs(cache_path, exist_ok=True)

    config_path = os.path.join(cache_path, "winprofile.ini")
    if not os.path.exists(config_path):
        logger.info("Writing config file: {}".format(config_path))
        with open(config_path, "w") as f:
            f.write("Category={}\n".format(category))
    elif force:
        logger.info("Modifying config file: {}".format(config_path))
        cfg = HeaderlessConfigParser()
        with open(config_path, "r") as f:
            cfg.read_file(f, source=config_path)
            cfg["main"]["Category"] = category
        with open(config_path, "w") as f:
            cfg.write(f)


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.site:
        for site_path in args.rootpathlist:
            process_site(site_path, category=args.category, force=True)
    else:
        for root_path in args.rootpathlist:
            if not os.path.isdir(root_path):
                logger.warning("Not a directory: {}".format(root_path))
                continue

            is_httrack_root_site = False
            site_path_list = []
            for site_name in os.listdir(root_path):
                site_path = os.path.join(root_path, site_name)
                if os.path.isfile(site_path) and site_name.endswith(".whtt") and not is_httrack_root_site:
                    is_httrack_root_site = True
                elif os.path.isdir(site_path):
                    site_path_list.append(site_path)

            if is_httrack_root_site:
                logger.error("Possibly not a WinHTTrack base path, skipping.")
                continue

            for site_path in site_path_list:
                process_site(site_path, category=args.category)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
