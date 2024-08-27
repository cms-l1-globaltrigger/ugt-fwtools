import argparse
import os
import shutil
import tempfile
import logging

from . import utils

logger = utils.get_colored_logger(__name__)

DefaultQuestaSimPath = "/opt/mentor/questasim"
DefaultQuestaSimLibsPath = "questasimlibs"


def run_compile_simlib(questasim_base: str, questasimlib_path: str) -> None:
    pwd = os.getcwd()

    # Temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Installation path of questasim (tcl syntax)
        questasim_path = os.path.join(questasim_base, "bin")
        # Path and compile_simlib command of tcl file used in Vivado
        tcl_compile_cmd = f"compile_simlib -no_systemc_compile -simulator questa -simulator_exec_path {{{questasim_path}}} -family virtex7 -language vhdl -library all -dir {{{questasimlib_path}}}"
        tcl_file = os.path.join(temp_dir, "compile_simlib.tcl")

        # Writing commands to tcl file
        with open(tcl_file, "wt") as fp:
            fp.write("#!/usr/bin/tcls\n")
            fp.write(f"{tcl_compile_cmd}\n")
            fp.write("exit\n")

        # Checking if questasimlib_path exists
        if not os.path.isdir(questasimlib_path):
            logger.info("===========================================================================")
            # Remove modelsim.ini before creating sim libs to get correct modelsim.ini in $HOME/questasimlibs_<version>
            utils.remove(os.path.join(pwd, "modelsim.ini"))
            logger.info("Creating Questa simlibs in %r (running %r)", questasimlib_path, tcl_file)
            utils.vivado_batch(tcl_file)
            utils.remove(os.path.join(pwd, "modelsim.ini"))
            logger.info("Done!")
            logger.info("===========================================================================")
        else:
            logger.info("===========================================================================")
            logger.info("Questa sim libs in %s already exists", questasimlib_path)
            logger.info("Nothing to do!")
            logger.info("===========================================================================")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--questasim", default=DefaultQuestaSimPath, help="Questasim installation path")
    parser.add_argument("-o", "--output", default=DefaultQuestaSimLibsPath, help="Questasim Vivado libraries output path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_compile_simlib(args.questasim, args.output)


if __name__ == "__main__":
    main()
