# Creathon HDF5 Utils

This repository contains a set of utilities for working with HDF5 files.

Raw signals are stored in HDF5 files. These can be loaded using the functions provided in the `lib/funcs.py` module. When a signal is annotated, it is split into segments of 10 seconds. Each segment is given a label based on whether an artefact is present in the segment. The artefact information is stored in a separate XML file with the same name as the HDF5 file, but with an `.artf` extension. See the provided tools for more information on how to work with the data at a low level.

## Installation (Linux/MacOS)
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

## Installation (Windows)
**Python 3.9+ is required**

1. Clone and enter the repository:
```
git clone https://github.com/MQ37/creathon.git
cd creathon
```

2. Create and activate Python virtual environment:
```
python -m venv venv
venv\Scripts\activate
```

3. Install the requirements:
```
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

To export ABP/ICP 10s segments from an HDF5 file, use the provided extract.py script. The segments will be exported as NumPy text files named as `{signal}_{start_idx}_{is_artefact}.txt` if artefacts are provided, otherwise `{signal}_{start_idx}.txt` where `0` indicates normal and `1` indicates an artefact segment.
```
# ABP signal with annotation
python3 extract.py -fh ./data/TBI_003.hdf5 -fa ./data/TBI_003.artf -o ./export/ -s abp
# ICP signal with annotation
python3 extract.py -fh ./data/TBI_003.hdf5 -fa ./data/TBI_003.artf -o ./export/ -s icp

# ABP signal without annotation
python3 extract.py -fh ./data/TBI_003.hdf5 -o ./export/ -s abp
```
To export the same number of normal segments (not marked as artefacts) as artefact segments, use the `-sn` switch. For example, if there are 704 marked artefacts in the ABP signal of this file, then only the first 704 normal segments will be exported along with the artefact segments (without this switch, all normal segments are exported).
```
# ABP signal without annotation
python3 extract.py -fh ./data/TBI_003.hdf5 -fa ./data/TBI_003.artf -o ./export/ -s abp -sn
```
To print all artifacts present in the HDF5 file with their signal index and datetime, use the `artefacts.py` tool. 
```
# ABP
python3 artefacts.py -fh ./data/TBI_003.hdf5 -fa ./data/TBI_003.artf -s abp
# ICP
python3 artefacts.py -fh ./data/TBI_003.hdf5 -fa ./data/TBI_003.artf -s icp
```

## Tools

- `info.py`: Displays information about the HDF5 file.
- `extract.py`: Extracts data from the HDF5 file and saves it as a NumPy TXT file.
- `artefacts.py`: Displays information about artefacts present in the HDF5 file. 

## ARTF File Format

The ARTF file, stored in XML format, contains information about artefacts present in the corresponding HDF5 file. It has the following structure:

* **`<ICMArtefacts>`**: The root element encompassing all artefact information.
* **`<Global>`**: Contains artefacts that apply to all signals in the HDF5 file.
    * **`<Artefact>`**:  Defines an artefact with `StartTime` and `EndTime` attributes specifying its duration.
* **`<SignalGroup>`**:  Contains artefacts specific to a particular signal, identified by the `Name` attribute.
    * **`<Artefact>`**: Similar to the global artefact, defines an artefact with `StartTime` and `EndTime` attributes.
* **`<Info>`**:  Provides metadata about the ARTF file.
    * **`HDF5Filename`**:  The name of the associated HDF5 file
    * **`UserID`**: (Optional) Identifier of the user who annotated the artefacts

**Example**

```xml
<?xml version="1.0" ?>
<ICMArtefacts>

    <Global>
        <Artefact StartTime="01/01/1970 00:00:05.000"
                  EndTime="01/01/1970 00:00:15.000"/>
    </Global>

    <SignalGroup Name="icp">
        <Artefact StartTime="01/01/1970 00:00:15.000"
                  EndTime="01/01/1970 00:00:25.000"/>
    </SignalGroup>

    <SignalGroup Name="abp">
        <Artefact StartTime="01/01/1970 00:00:25.000"
                  EndTime="01/01/1970 00:00:35.000"/>
        <Artefact StartTime="01/01/1970 00:00:35.000"
                  EndTime="01/01/1970 00:00:45.000"/>
    </SignalGroup>

    <Info HDF5Filename="soubor.hdf5" UserID="uzivatel1"/>

</ICMArtefacts>
``` 

## Notes
**Be sure to read this**

Note that the ABP wave signal is sometimes stored in HDF5 files as `waves.art` instead of `waves.abp`. 


