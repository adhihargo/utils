import argparse
import configparser
import logging
import os
import socket

CONFIG_FILENAME = "vlc.cfg"

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


def get_config():
    if os.path.exists(CONFIG_FILENAME):
        config = configparser.ConfigParser(interpolation=None)
        config.read(CONFIG_FILENAME, encoding="utf-8")
    else:
        config = None
    return config


def get_parser(config):
    parser = get_parser_base(config)
    parser.add_argument("files", nargs="+")
    return parser


def get_parser_base(config):
    parser = argparse.ArgumentParser()
    env_port = int(os.getenv("VLC_TARGET_PORT", 4212))
    if config and not {"main"} <= set(config.sections()):
        parser.error("config file does not contain the required sections.")
    if config:
        config_port = int(config["main"].get("port", env_port))
    else:
        config_port = env_port
    parser.add_argument("-p", "--port", type=int, default=config_port)
    return parser


def vlc_send_cmd(address, cmd_str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as vlcSocket:
        vlcSocket.settimeout(1)
        try:
            vlcSocket.connect(address)
            vlcSocket.sendall(cmd_str.encode())
        except (ConnectionRefusedError, socket.timeout) as exc:
            logger.warning("Unable to connect to VLC: {}".format(exc))


def main():
    config = get_config()
    parser = get_parser(config)
    args = parser.parse_args()
    for filepath in args.files:
        vlc_cmd_str = "enqueue {}\r\n".format(filepath)
        vlc_address = ("localhost", args.port)
        vlc_send_cmd(vlc_address, vlc_cmd_str)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Execution error:")
