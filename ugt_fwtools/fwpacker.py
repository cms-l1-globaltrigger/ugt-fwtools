import argparse
import configparser
import os
import shutil
import tempfile
import tarfile

from . import utils

logger = utils.get_colored_logger(__name__)

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="build configuration file to read")
    parser.add_argument("--outdir", metavar="<path>", type=os.path.abspath, help="set location to write tarball")
    return parser.parse_args()


def main():
    """Main routine."""

    # Parse command line arguments.
    args = parse_args()

    # with tarfile

    config = configparser.RawConfigParser()
    config.read(args.config)

    for section in config.sections():
        print(section)
        for option in config.options(section):
            print(" ", option, "=", config.get(section, option))

    menu = config.get("menu", "name")
    location = config.get("menu", "location")
    build = utils.build_t(config.get("menu", "build"))  # format "ffff"
    board = config.get("device", "alias")
    buildarea = os.path.dirname(args.config)  # relative to build config
    menu_modules = int(config.get("menu", "modules"))
    timestamp = utils.timestamp()

    # Definitions for name of IPBB "proj" directory
    fw_type = config.get("firmware", "type")
    device_name = config.get("device", "name")

    basename = f"{menu}_v{build}_{board}"
    basepath = os.path.dirname(args.config)

    # Custom output directory?
    if args.outdir:
        basepath = args.outdir
    filename = os.path.join(basepath, f"{basename}-{timestamp}.tar.gz")

    tmpdir = tempfile.mkdtemp()
    logger.info("Created temporary dircetory %s", tmpdir)

    # Check modules
    for i in range(menu_modules):
        logger.info("collecting data from module %s", i)
        module_dir = f"module_{i}"

        proj_dir = os.path.join("proj", module_dir)
        build_dir = os.path.join(tmpdir, module_dir, "build")
        log_dir = os.path.join(tmpdir, module_dir, "log")

        # for IPBB v0.5.2 directory structure
        proj_runs = os.path.join(module_dir, f"{module_dir}.runs")
        bit_file = f"module_{i}.bit"

        os.makedirs(build_dir)
        os.makedirs(log_dir)
        shutil.copy(
            os.path.join(buildarea, proj_dir, "products", bit_file),
            os.path.join(build_dir, f"gt_mp7_{board}_v{build}_module_{i}.bit")
        )
        shutil.copy(
            os.path.join(buildarea, proj_dir, proj_runs, "synth_1", "runme.log"),
            os.path.join(log_dir, "runme_synth_1.log")
        )
        shutil.copy(
            os.path.join(buildarea, proj_dir, proj_runs, "impl_1", "runme.log"),
            os.path.join(log_dir, "runme_impl_1.log")
        )

    logger.info("adding build configuration: %s", args.config)
    shutil.copy(args.config, tmpdir)

    xml_file = os.path.join(buildarea, "src", f"{menu}.xml")
    logger.info("adding XML menu: %s", xml_file)
    shutil.copy(xml_file, tmpdir)

    logger.info("creating tarball: %s", filename)
    with tarfile.open(filename, "w:gz") as tar:
        logger.info("adding to tarball: %s", tmpdir)
        tar.add(tmpdir, arcname=basename, recursive=True)
    logger.info("closed tarball: %s", filename)

    logger.info("removing temporary directory %s.", tmpdir)
    shutil.rmtree(tmpdir)

    logger.info("done.")


if __name__ == "__main__":
    main()

