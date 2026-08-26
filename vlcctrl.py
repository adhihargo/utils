import logging
import os
from configparser import ConfigParser

from vlc import get_config, get_parser_base, vlc_send_cmd, CONFIG_PATH

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


def get_parser(config):
    parser = get_parser_base(config)
    parser.add_argument(
        '-C', "--control", type=int, metavar="PORT",
        help="Sets default port to control. Also sets current port if --port not set.")
    parser.add_argument("commands", nargs="*")
    return parser


def set_config_port(config: ConfigParser, port: int):
    config.set("main", "port", str(port))
    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)


def main():
    config = get_config()
    parser = get_parser(config)
    args = parser.parse_args()
    if args.control is not None:
        set_config_port(config, args.control)
        current_port = args.control
    else:
        current_port = args.port

    for command in args.commands:
        vlc_address = ("localhost", current_port)
        vlc_send_cmd(vlc_address, command)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Execution error:")
