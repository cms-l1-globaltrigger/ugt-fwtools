import argparse
import configparser
import os
import tempfile

from . import utils


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("-m", type=int)
    return parser.parse_args()


def main():
    args = parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)
    menu_build = config["menu"]["build"]
    menu_modules = int(config["menu"]["modules"])
    buildarea = os.path.dirname(args.config)

    if args.m is not None:
        module_ids = [f"module_{args.m}"]
    else:
        module_ids = [f"module_{m}" for m in range(menu_modules)]

    for module_id in module_ids:
        project_file = os.path.realpath(os.path.join(buildarea, "proj", module_id, module_id, f"{module_id}.xpr"))
        archive_file = os.path.realpath(os.path.join(os.getcwd(), f"0x{menu_build}_{module_id}.zip"))
        with tempfile.NamedTemporaryFile(delete=True) as source:
            source.write(f"open_project {project_file}\n".encode())
            source.write(f"archive_project {archive_file}\n".encode())
            source.flush()
            with open(source.name) as x: print(x.read())
            utils.vivado_batch(source.name)


if __name__ == "__main__":
    main()
