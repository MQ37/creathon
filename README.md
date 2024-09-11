# Creathon HDF5 Utils

This repository contains a set of utilities for working with HDF5 files.

Raw signals are stored in HDF5 files. These can be loaded using the functions provided in the `lib/funcs.py` module. When a signal is annotated, it is split into segments of 10 seconds. Each segment is given a label based on whether an artefact is present in the segment. The artefact information is stored in a separate XML file with the same name as the HDF5 file, but with an `.artf` extension. See the provided tools for more information on how to work with the data at a low level.

## Installation
**Python 3.9+ is required**

1. Clone and enter the repository:
```
git clone https://github.com/MQ37/creathon.git
cd creathon
```
2. Create and activate Python virtualenv:
```
python3 -m venv venv
source venv/bin/activate
```
3. Install the requirements:
```bash
pip install -r requirements.txt
```

## Usage
**Python virtualenv must be activated**

Run the desired tool/script with the required arguments (these can be found in the help message using the `-h` flag). For example, to use the `info` tool, run:
```bash
python3 info.py -fh <path_to_hdf5_file> [-fa <path_to_artf_file>]
# example
python3 info.py -fh ./data/TBI_003.hdf5 -fa ./data/TBI_003.artf
```

## Tools

- `info.py`: Displays information about the HDF5 file.
- `extract.py`: Extracts data from the HDF5 file and saves it as a NumPy TXT file.
