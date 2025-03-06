# ugt-fwtools

Firmware build tools for Phase-1 uGT

## Prerequisites

**Note:** this section will be subject to changes.

The tools require following environment variables to be set
for simulation and synthesis:

```bash
export MODELSIM_ROOT=/opt/mentor/questa/2021.1_2
export MODELSIM_PATH=${MODELSIM_ROOT}/questasim/bin
export PATH=${MODELSIM_PATH}:${PATH}
export MTI_VCO_MODE=64
export MGLS_LICENSE_FILE=<license>
export UGT_GITLAB_USER_NAME=<user name>
export UGT_QUESTASIMLIBS_DIR=<home dir>
export UGT_QUESTASIM_SIM_PATH=${MODELSIM_ROOT}
export UGT_QUESTASIM_LIBS_PATH=<home dir>/questasimlibs
export UGT_BLK_MEM_GEN_VERSION_SIM=blk_mem_gen_v8_4_5
export UGT_VIVADO_BASE_DIR=/opt/Xilinx/Vivado
export UGT_VIVADO_VERSION=2021.2
source ${UGT_VIVADO_BASE_DIR}/${UGT_VIVADO_VERSION}/settings64.sh
```

## Install

Install ugt-fwtools in a python environment version 3.9, 3.10, 3.11 or 3.12 (if available).
For example:

```bash
python3.9 -m venv env
. env/bin/activate
```

Installation of ugt-fwtools (current version 0.9.1) with:

```bash
pip install --upgrade pip
pip install git+https://github.com/cms-l1-globaltrigger/ugt-fwtools.git@0.9.1
```

## Preface

In the following examples `L1Menu_sample-d1.xml` refers to an XML file located within
a menu distribution of the following layout.

```
L1Menu_sample-d1/
├── testvectors
├── vhdl
└── xml
    └── L1Menu_sample-d1.xml
```

Official menu distributions can be found at https://github.com/cms-l1-globaltrigger/cms-l1-menu/

All scripts support both local files and public remote http[s] resources as input
for XML files and test vectors.

## Simulation

First compile questasimlibs (if not exist) with:

```bash
ugt-compile-simlib --questasim /opt/mentor/questa/2021.1_2/questasim --output <home dir>/questasimlibs
```

and run simulation with:

```bash
ugt-simulate L1Menu_sample-d1.xml --tv sample_ttbar.txt
```

Use command line option `--ugttag <tag>` to run with a different ugt tag or branch.

To persist the simulation results use option `--output <dir>`.

## Synthesis (all modules)

```bash
ugt-synthesize L1Menu_sample-d1.xml --build 0x1190
```

Use command line option `--ugttag <tag>` to run with a different ugt tag or branch.

## Synthesis (subset of modules)

```bash
ugt-synthesize L1Menu_sample-d1.xml --build 0x1190 --modules 1,4-5
```

Use command line option `-m|--modules <list>` to synthesize only a subset of modules by supplying a comma separted list,
e.g. `1`, `2,4,5`, `0-2`, or `0,2-4`.

## Resynthesis of an existing module

```bash
ugt-implement-module 2 build_0x1190.cfg   # resynthesize module number 2
```

## Check results

```bash
ugt-checksynth build_0x1190.cfg
```

Use command line option `-o <file>` to write output to a file, e.g. `-o result.log`.

## Build report

Print Markdown or Textile formatted information to be inserted into issues and wiki.

```bash
ugt-buildreport build_0x1190.cfg
```

Use command line option `--format <type>` to select the output format, e.g. `--format textile` (default is `markdown`).

## Bundle firmware

```bash
ugt-fwpacker build_0x1190.cfg
```

## Vivado archives

Create Vivado archives of all modules.

```bash
ugt-archive build_0x1190.cfg
```

Create Vivado archive of individual module.

```bash
ugt-archive build_0x1190.cfg -m 1  # module_1
```
