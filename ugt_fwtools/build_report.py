"""Creates textile formatted snippets for build issues
and bitfile table in redmine.
"""

import configparser
import argparse
import re
import os
from datetime import datetime


def textile_strong(s):
    return f"*{s}*"


def textile_pre_inline(s):
    return f"@{s}@"


def detect_tm_reporter_version(filename):
    """Try to detect tm-reporter version from L1Menu-HTML file.

    Required format:
    <meta name="generator" content="tm-reporter 2.7.2">
    """
    regex = re.compile(r'^.*tm-reporter\s+(\d+\.\d+\.\d+)')
    with open(filename, "rt") as fp:
        for line in fp:
            m = regex.match(line)
            if m:
                return m.group(1)
    return None


def detect_versions_vx_y_z(filename, needle):
    """Try to detect versions of VHDL producer, tmEventSetup, etc. from comments of generated output
    VHDL files. Returns version string or None if no information was found.
    """
    with open(filename, "r") as fp:
        line = fp.readline()
        while(line):
            if line.strip().startswith(needle):
                line2=fp.readline()
                return line2.split(" ")[2].strip()
            else:
                line=fp.readline()
    return None

def detect_gt_versions(filename):
    """Try to detect uGT, FDL and GTL versions from VHDL statements. Returns a
    dictionary containing version strings with keys used in VHDL constants.
    >>> detect_gt_versions("/path/to/gt_mp7_core_pkg.vhd")
    {'GT': '1.22.3', 'FRAME': '1.2.3', 'FDL_FW': '1.2.2', 'GTL_FW': '1.5.0'}
    """
    versions = {}
    regex = re.compile(r'^\s*\w+\s+(\w+)_(\w+)_VERSION.*\:\=\s*(\d+)')
    with open(filename, "rt") as fp:
        for line in fp:
            m = regex.match(line)
            if m:
                key = m.group(1)
                if key not in versions:
                    versions[key] = {}
                versions[key][m.group(2)] = m.group(3)
    for k, v in versions.items():
        versions[k] = "{MAJOR}.{MINOR}.{REV}".format(**v)
    return versions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="build config file (*.cfg)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    config = configparser.ConfigParser()
    config.read(args.filename)

    menu_location = config.get("menu", "location")
    buildarea = os.path.dirname(args.filename)  # relative to build config

    menu_name = config.get("menu", "name")

    build_id = "0x{0}".format(config.get("menu", "build"))
    n_modules = config.get("menu", "modules")
    username = config.get("environment", "username")
    hostname = config.get("environment", "hostname")
    timestamp = config.get("environment", "timestamp")
    mp7fw_tag = config.get("firmware", "mp7tag")
    ugt_tag = config.get("firmware", "ugttag")
    l1menu_html = f"{menu_name}.html"

    versions = {}
    ugt_constants_path = os.path.join(buildarea, "src", "module_0", "vhdl_snippets", "ugt_constants.vhd")
    needle = "-- tmEventSetup"
    versions["tm-eventsetup"] = detect_versions_vx_y_z(ugt_constants_path, needle)
    needle = "-- VHDL producer"
    versions["tm-vhdlproducer"] = detect_versions_vx_y_z(ugt_constants_path, needle)
    #exit(0)
    versions["tm-reporter"] = detect_tm_reporter_version(os.path.join(buildarea, "src", l1menu_html))
    versions.update(detect_gt_versions(os.path.join(buildarea, "src", "mp7_ugt_legacy", "firmware", "hdl", "packages", "gt_mp7_core_pkg.vhd")))
    vivado_version = config.get("vivado", "version")

    table = [
        ("Menu", menu_name),
        ("Build", build_id),
        ("Modules", n_modules),
        ("Created", timestamp),
        ("Username", username),
        ("Hostname", hostname),
        ("Vivado", vivado_version),
        ("Build area", buildarea),
        ("Menu url", menu_location),
        ("MP7 tag", mp7fw_tag),
        ("uGT tag", ugt_tag),
        ("uGT", versions["GT"]),
        ("FRAME", versions["FRAME"]),
        ("FDL", versions["FDL_FW"]),
        ("GTL", versions["GTL_FW"]),
        ("tm-eventsetup", versions["tm-eventsetup"]),
        ("tm-vhdlproducer", versions["tm-vhdlproducer"]),
        ("tm-reporter", versions["tm-reporter"]),
    ]

    print("Insert into ISSUE description:\n")

    for row in table:
        print(("|_<.{0} |{1} |".format(*row)))

    items = [
        menu_name,
        textile_pre_inline(build_id),
        username,
        vivado_version,
        mp7fw_tag,
        ugt_tag,
        versions["GT"],
        versions["FRAME"],
        versions["GTL_FW"],
        versions["FDL_FW"],
        "#",
        f"created on *{hostname}*",
        datetime.now().strftime("%Y-%m-%d"),
    ]
    print("\nPrepend BITFILES table:\n")
    print("|_.Menu tag |_.Build |_.Creator |_.Vivado |_.MP7 tag |_.uGT tag |_.uGT |_.Frame |_.GTL |_.FDL |_.Issue |_.Remarks |_.Date |")
    print(("|{0} |".format(" |".join(items))))


if __name__ == "__main__":
    main()
