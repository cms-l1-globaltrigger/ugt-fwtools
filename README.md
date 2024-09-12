# ugt-fwtools

Firmware build tools for Phase-1 uGT

## Prerequisites

**Note:** this section will be subject to changes.

The tools require following environment variables to be set, eg. by sourcing a bash script.

```bash
export UGT_QUESTASIM_SIM_PATH=/opt/mentor/questa/2021.1_2
export UGT_QUESTASIM_LIBS_PATH=$HOME/.questasimlibs
export UGT_VIVADO_BASE_DIR=/opt/Xilinx/Vivado
export UGT_VIVADO_VERSION=2021.2
source ${UGT_VIVADO_BASE_DIR}/${UGT_VIVADO_VERSION}/settings64.sh
```

## Install

```bash
pip install git+https://github.com/cms-l1-globaltrigger/ugt-fwtools.git@0.8.1
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
