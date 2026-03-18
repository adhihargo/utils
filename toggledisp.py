# Toggle primary monitor
import json
import os
import subprocess

CONF_NAME = "toggledisp.json"
script_dir = os.path.dirname(__file__)
config_path = os.path.join(script_dir, CONF_NAME)


def main():
    do_extend = read_config()

    do_extend = not do_extend
    exec_displayswitch(do_extend)
    write_config(do_extend)


def read_config() -> bool:
    if not os.path.exists(config_path):
        # Assume initial run, and already extends display
        do_extend = True
    else:
        with open(config_path, "rb") as json_cfg_file:
            json_cfg = json.load(json_cfg_file)
            display_mode = json_cfg["display"]
        do_extend = (display_mode == "extend")
    return do_extend


def write_config(do_extend: bool):
    display_mode = "extend" if do_extend else "external"
    with open(config_path, "w") as json_cfg_file:
        json.dump({"display": display_mode}, json_cfg_file)


def exec_displayswitch(do_extend: bool):
    display_mode = "extend" if do_extend else "external"
    subprocess.run(["displayswitch", "/{}".format(display_mode)])


if __name__ == '__main__':
    main()
