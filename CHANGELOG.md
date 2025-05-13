# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.4] - 2025-05-13

### Changes
- default ugttag v1.31.2 (for simulation and sythesis)

## [0.9.3] - 2025-04-11

### Changes
- added infos to output in simulation.py

## [0.9.2] - 2025-04-08

### Changes
- in simulation.py and sythesis.py (DefaultUgtTag = "v1.30.0")

## [0.9.1] - 2024-09-25

### Added
- IGNORED_ALGOS (in simulation.py)

## [0.9.0] - 2024-09-11

### Added
- tcl script to fix cells in vivado (in synthesis.py)

## [0.8.1] - 2024-09-10

### Fixed
- checksynth output to file

## [0.8.0] - 2024-08-30

### Changes
- using src-layout

## [0.7.0] - 2024-08-23

### Added
- option `-m|--modules` to synthesize only a subset of modules
- option `--manual` to run without screen sessions
- select markdown/textile format for build report

### Changed
- renamed script synth_1_module.py to resynthesize_one_module.py

### Fixed
- detecting tmEventSetup and tm-vhdlproducer version in new and old VHDL files

## [0.6.0] - 2024-03-15

### Changed
- script simulation.py for axol1tl
- script build_report.py (to get tmEventSetup version correctly)

## [0.5.0] - 2024-01-02

### Changed
- added topological trigger

## [0.4.0] - 2023-10-16

### Changed
- used utils.get_colored_logger in other python files

## [0.3.0] - 2023-10-13

### Added
- fwtools version to build configuration file (synthesis.py)
- used utils.get_colored_logger (in synthesis.py and fwpacker.py)

## [0.2.0] - 2023-10-10

### Added
- script synth_1_module.py (re-synthesis of only one module)

## [0.1.2] - 2023-09-12

### Changed
- added option `-lic_noqueue` to vsim command to prevent waiting for license in a queue.

## [0.1.1] - 2023-06-15

### Changed
- default mp7 repository to `https://gitlab.cern.ch/cms-l1-globaltrigger/mp7.git`

### Fixed
- bugs in modules `fwpacker` and `synthesis`

## [0.1.0] - 2023-05-12

### Added
- migrated scripts from `ugt_mp7_legacy/scripts` repo.

[Unreleased]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.9.4...HEAD
[0.9.4]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.9.3...0.9.4
[0.9.3]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.9.2...0.9.3
[0.9.2]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.9.1...0.9.2
[0.9.1]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.9.0...0.9.1
[0.9.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.8.1...0.9.0
[0.8.1]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.8.0...0.8.1
[0.8.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.7.0...0.8.0
[0.7.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.6.0...0.7.0
[0.6.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.5.0...0.6.0
[0.5.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.1.2...0.2.0
[0.1.2]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.1.1...0.1.2
[0.1.1]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/compare/0.1.0...0.1.1
[0.1.0]: https://github.com/cms-l1-globaltrigger/ugt-fwtools/releases/tag/0.1.0
