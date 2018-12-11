#!/usr/bin/python3
import argparse
import re
import subprocess

XWININFO_BIN = "xwininfo"
XRANDR_BIN = "xrandr"
XDOTOOL_BIN = "xdotool"
WMCTRL_EXEC_INIT = ["wmctrl", "-r", ":ACTIVE:"]


def get_window_id():
    """Get ID of active window, to be accessed by other tools.
    :return: ID int
    """
    return subprocess.getoutput("{} getactivewindow".format(XDOTOOL_BIN))


def get_display_geometry_list():
    """Get size of all displays.
    :return: List of screen size dictionary
    """
    connected_line_re = re.compile(r'''
        \bconnected\b[\sa-z]+
        (?P<W>\d+)x
        (?P<H>\d+)\+
        (?P<X>\d+)\+
        (?P<Y>\d+).+''', re.VERBOSE)
    xrandr_output: str = subprocess.getoutput(XRANDR_BIN)
    size_tuple = [line_match.groupdict() for line in xrandr_output.splitlines()
                  for line_match in [connected_line_re.search(line)]
                  if line_match != None]
    return size_tuple


def get_window_geometry():
    absolute_line_re = re.compile(r"Absolute upper-left (\w):\s+(\d+)")
    window_id = get_window_id()
    output: str = subprocess.getoutput("{} -id {}".format(XWININFO_BIN, window_id))
    output_lines = dict([line_match.groups() for line in output.splitlines()
                         for line_match in [absolute_line_re.search(line)]
                         if line_match != None])
    return output_lines


def move_window(display_index: int, pos):
    """The main function. It receives index of display to move window to, and position within the display.
    :param display_index: Which display to move to.
    :param pos: What position within the display to resize to.
    :return:
    """
    display_geometry_list = get_display_geometry_list()
    if display_index is None or display_index < 0 or display_index > len(display_geometry_list):
        return

    # first, remove maximized states
    subprocess.call(WMCTRL_EXEC_INIT + ["-b", "remove,maximized_vert,maximized_horz"])

    # then move to desired monitor and display
    move_to_display(display_geometry_list, display_index, pos)

    # return vertical maximized state
    pos_shortcut = "super+Left" if pos == 'l' else "super+Right"
    subprocess.call([XDOTOOL_BIN, "key", pos_shortcut])


def move_to_display(display_geometry_list, display_index: int, pos):
    display_geometry = display_geometry_list[display_index]

    x, y = int(display_geometry['X']), display_geometry['Y']
    width = int(int(display_geometry['W']) / 2.0)
    height = display_geometry['H']
    if pos == 'r':
        x += width

    command_list = WMCTRL_EXEC_INIT + ["-e", "0,{},{},{},{}".format(x, y, width, height)]
    subprocess.call(command_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Poor man's GridMove.")
    parser.add_argument("-d", help="Move to display DISPLAY_ID", type=int, metavar="DISPLAY_ID", dest="display_index")
    parser.add_argument("pos", help="Move to screen position indicated", choices=["l", "r"])
    args = parser.parse_args()
    move_window(args.display_index, args.pos)
