import re
import argparse
import configparser
import logging
import os
import subprocess

DefaultVivadoVersion = os.getenv("UGT_VIVADO_VERSION", "")
if not DefaultVivadoVersion:
    raise RuntimeError("UGT_VIVADO_VERSION is not defined.")

VivadoBaseDir = os.getenv("UGT_VIVADO_BASE_DIR", "")
if not VivadoBaseDir:
    raise RuntimeError("UGT_VIVADO_BASE_DIR is not defined.")

vivadoPath = os.path.abspath(os.path.join(VivadoBaseDir, DefaultVivadoVersion))
if not os.path.isdir(vivadoPath):
    raise RuntimeError("No installation of Vivado in %r" % vivadoPath)

def build_str_t(version: str) -> str:
    """Validates build number."""
    if not re.match(r'^0x[A-Fa-f0-9]{4}$', version):
        raise ValueError("not a valid build version: '{version}'".format(**locals()))
    return version

def vivado_t(version: str) -> str:
    """Validates Xilinx Vivado version number."""
    if not re.match(r'^\d{4}\.\d{1}$', version):
        raise ValueError("not a xilinx vivado version: '{version}'".format(**locals()))
    return version

def show_screen_sessions() -> None:
    subprocess.run(["screen", "-ls"])

def start_screen_session(session: str, commands: str) -> None:
    subprocess.run(["screen", "-dmS", session, "bash", "-c", commands]).check_returncode()

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--vivado", metavar="<version>", default=DefaultVivadoVersion, type=vivado_t, help=f"Vivado version to run (default is {DefaultVivadoVersion!r})")
    parser.add_argument("--build", type=build_str_t, required=True, metavar="<version>", help="menu build version (eg. 0x1001) [required]")
    parser.add_argument("--mod_id", required=True, help="module number (eg. 1) [required]")
    parser.add_argument("--path", metavar="<path>", required=True, type=os.path.abspath, help=f"fw build path [required] (eg. ../work_synth/production")
    return parser.parse_args()

def main() -> None:
    """Main routine."""

    # Parse command line arguments.
    args = parse_args()
    
    ipbb_dir = args.path
    project_type = "mp7_ugt_legacy"
    module_id = args.mod_id
    module_name = f"module_{module_id}"

    # Check for UGT_VIVADO_BASE_DIR
    vivado_base_dir = os.getenv("UGT_VIVADO_BASE_DIR")
    if not vivado_base_dir:
        raise RuntimeError("Environment variable 'UGT_VIVADO_BASE_DIR' not set. Set with: 'export UGT_VIVADO_BASE_DIR=...'")

    # Vivado settings
    settings64 = os.path.join(vivado_base_dir, args.vivado, "settings64.sh")
    if not os.path.isfile(settings64):
        raise RuntimeError(
            f"no such Xilinx Vivado settings file {settings64!r}\n"
            f"  check if Xilinx Vivado {args.vivado} is installed on this machine."
	)

        
    logging.info("===========================================================================")
    logging.info("running IPBB project, synthesis and implementation, creating bitfile for module %s ...", module_id)

    # IPBB commands: running IPBB project, synthesis and implementation, creating bitfile
    cmd_ipbb_project = "ipbb vivado generate-project --single"  # workaround to prevent "hang-up" in make-project with IPBB v0.5.2
    cmd_ipbb_synth = "ipbb vivado synth impl package"

    # Set variable "module_id" for tcl script (l1menu_files.tcl in uGT_algo.dep)
    command = f'cd; source {settings64}; cd {ipbb_dir}/{args.build}/proj/{module_name}; module_id={module_id} {cmd_ipbb_project} && {cmd_ipbb_synth}'

    session = f"build_{project_type}_{args.build}_{module_id}"
    logging.info("starting screen session %r for module %s ...", session, module_id)

#    run_command(command)
    start_screen_session(session, command)

    # list running screen sessions
    logging.info("===========================================================================")
    show_screen_sessions()

    os.chdir(ipbb_dir)
    
if __name__ == "__main__":
    main()

