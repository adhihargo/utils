import logging
import os

from vlc import get_config, get_parser_base, vlc_send_cmd

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


def get_parser(config):
    parser = get_parser_base(config)
    parser.add_argument("commands", nargs="+")
    return parser


def main():
    config = get_config()
    parser = get_parser(config)
    args = parser.parse_args()
    for command in args.commands:
        vlc_address = ("localhost", args.port)
        vlc_send_cmd(vlc_address, command)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Execution error:")
