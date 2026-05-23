import ctypes
import os
import subprocess
import sys
from collections import namedtuple

__route_tuple__ = namedtuple("RouteTuple", ["dest", "netmask", "gateway", "interface", "metric"])


class RouteTuple(__route_tuple__):
    def __repr__(self):
        return "IF: {}, GATEWAY: {}, NETMASK: {}, DEST: {}, METRIC: {}".format(
            self.interface, self.gateway, self.netmask, self.dest, self.metric)


def uac_elevate():
    try:
        uac_is_elevated = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        uac_is_elevated = False

    if not uac_is_elevated:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def get_metric(gateway):
    cmdlist = ["route", "print", "0.0.0.0", "mask", "0.0.0.0"]
    output_str = subprocess.check_output(cmdlist, text=True)

    in_active_route = False
    route_metric = None
    for line in output_str.split("\n"):
        if line.lower().find("active routes") == 0:
            in_active_route = True
        if in_active_route:
            columns = line.split()
            route_info = RouteTuple(*columns) if len(columns) == 5 else None
            if route_info is None:
                continue
            else:
                print("Route: ", route_info)
                if route_info.gateway != gateway:
                    continue
            route_metric = route_info.metric

    return route_metric


def toggle_metric(gateway, metric_new, interface):
    cmdlist = ["route", "change", "0.0.0.0", "mask", "0.0.0.0", gateway, "metric", metric_new]
    if interface:
        cmdlist.extend(["IF", interface])
    subprocess.check_output(cmdlist)


def main(gateway=None, interface=None, metric_new=None):
    # Network interface to switch metric of must be defined in
    # environment variable TOGGLEROUTE_GATEWAY.
    if gateway is None:
        gateway = os.getenv("TOGGLEROUTE_GATEWAY", None)
    if not gateway:
        print("Gateway not specified in TOGGLEROUTE_GATEWAY environment variable.")
        return

    # Get interface index from Interface List printed by "route print"
    # command. Without this, each calls to "route change" seemingly will
    # try to create a new route.
    if interface is None:
        interface = os.getenv("TOGGLEROUTE_INTERFACE", None)

    if metric_new is None:
        metric = get_metric(gateway)
        if not metric:
            print("Route info not found.")
            return

        is_prioritized = int(metric) < 400
        metric_new = "500" if is_prioritized else "100"
        print("Deprioritize" if is_prioritized else "Prioritize", gateway,
              ": {} > {}".format(metric, metric_new))
    else:
        print("Set new metric for {}: {}".format(gateway, metric_new))
    toggle_metric(gateway, metric_new, interface)


if __name__ == '__main__':
    uac_elevate()
    main()
