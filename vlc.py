import argparse
import configparser
import logging
import os
import socket
import tkinter as tk
from configparser import ConfigParser
from functools import partial

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "vlc.cfg")
CONFIG_DEFAULTS = {"main": {"port": 4212}}

logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])


class ConfigWindow(tk.Tk):
    def __init__(self, port, geometry=None):
        super().__init__()
        self.resizable(True, False)
        if geometry is not None:
            self.geometry(geometry)
        self.attributes("-topmost", True)
        self.title("VLC Control")

        self.default_port = port
        self.accepted = False
        self.location_str = None

        self.v_port = tk.IntVar(value=port)
        self.spb_port = tk.Spinbox(
            master=self, from_=1024, to=65535, width=20, justify=tk.CENTER, textvariable=self.v_port,
            validate="key", validatecommand=(self.register(lambda s: s == "" or s.isdigit()), "%P"))
        self.spb_port.pack(fill=tk.X, expand=True)
        self.spb_port.focus_set()

    def set_callback(self, callback_dict):
        for k, val in callback_dict.items():
            kseq = k.split(".", maxsplit=1)
            if len(kseq) < 2 or not (getattr(self, kseq[0], None) and kseq[1]):
                logger.warning("CALLBACK SKIPPED: {} -> {}".format(k, val))
                continue
            getattr(self, kseq[0]).bind(kseq[1], val)


class ConfigWriter(object):
    config: ConfigParser

    def __init__(self, config):
        self.config = config

    def __del__(self):
        self.save()

    def __setitem__(self, key, value):
        self.config.set("main", key, str(value))

    def save(self):
        with open(CONFIG_PATH, "w") as config_file:
            self.config.write(config_file)


def get_config():
    config = configparser.ConfigParser(interpolation=None)
    config.read_dict(CONFIG_DEFAULTS)
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH, encoding="utf-8")
    return config


def get_parser(config):
    parser = get_parser_base(config)
    parser.add_argument("-c", dest="command", action="store_true",
                        help="Interpret arguments as commands")
    parser.add_argument("-C", dest="config", action="store_true",
                        help="Open GUI to edit config")
    parser.add_argument("files", metavar="FILE", nargs="*",
                        help="Files to enqueue in VLC playlist")
    return parser


def get_parser_base(config):
    parser = argparse.ArgumentParser()
    env_port = int(os.getenv("VLC_TARGET_PORT", 4212))
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


def handle_spb_port_keys(window: ConfigWindow, event: tk.Event):
    if event.keysym == "r" and event.state & 0x4:
        window.v_port.set(window.default_port)
    elif event.keysym == "Escape":
        window.quit()
    elif event.keysym == "Return":
        window.location_str = "+{}+{}".format(window.winfo_x(), window.winfo_y())
        window.accepted = True
        window.quit()


def main():
    config = get_config()
    parser = get_parser(config)
    args = parser.parse_args()
    vlc_port = args.port
    if args.config:
        config_writer = ConfigWriter(config)
        location_str = config["main"].get("geometry")

        window = ConfigWindow(port=args.port, geometry=location_str)
        window.set_callback({"spb_port.<Key>": partial(handle_spb_port_keys, window)})
        window.mainloop()

        vlc_port = window.v_port.get()
        if window.accepted and vlc_port != args.port:
            logger.info("Setting new VLC port: {}".format(vlc_port))
            config_writer["port"] = vlc_port
        if window.location_str and window.location_str != config["main"].get("geometry"):
            logger.info("Saving window location: {}".format(window.location_str))
            config_writer["geometry"] = window.location_str

    vlc_address = ("localhost", vlc_port)
    vlc_cmd_pattern = "{}\r\n" if args.command else "enqueue {}\r\n"
    for filepath in args.files:
        vlc_cmd_str = vlc_cmd_pattern.format(filepath)
        vlc_send_cmd(vlc_address, vlc_cmd_str)
    if args.files:
        vlc_send_cmd(vlc_address, "play")


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception("Execution error:")
