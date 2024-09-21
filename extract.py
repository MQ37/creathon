from lib.readers import ARTFReader
from lib.hdf5_reader_module import SignalClass
from lib.funcs import read_artf, read_hdf5

import numpy as np
import argparse
import os

WINDOW_SIZE_SEC = 10


def main(args):
    hdf5_filepath = args.fh
    artf_filename = args.fa
    output_dir = args.o
    include_artefacts = artf_filename is not None

    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # load hdf5
    icp, abp = read_hdf5(hdf5_filepath)

    if args.s == 'icp':
        # get sample rates
        sr = int(icp["sample_rate"])

        # get start times
        start_time_s = icp["start_time_s"]

        # get signals
        signal = icp["signal"]

        # trim signals to be divisible by window size
        remainder = int(len(signal) % (sr * WINDOW_SIZE_SEC))
        signal = signal[:-remainder]
    elif args.s == 'abp':
        # get sample rates
        sr = int(abp["sample_rate"])

        # get start times
        start_time_s = abp["start_time_s"]

        # get signals
        signal = abp["signal"]

        # trim signals to be divisible by window size
        remainder = int(len(signal) % (sr * WINDOW_SIZE_SEC))
        signal = signal[:-remainder]

    if include_artefacts:
        # load artefacts
        artefacts = read_artf(artf_filename)

        # get artefacts
        global_artefacts = artefacts["global_artefacts"]

        if args.s == 'icp':
            artefacts = artefacts["icp_artefacts"]
            artefacts = artefacts + global_artefacts

            # get artefact start indices
            # [0] is start index, [1] is end index of the signal array
            artefacts_idx = [artefact.to_index(sr, WINDOW_SIZE_SEC, start_time_s)[0] for artefact in artefacts]
            artefacts_idx = set(artefacts_idx)

            artefact_count = len(artefacts_idx)
        elif args.s == 'abp':
            artefacts = artefacts["abp_artefacts"]
            artefacts = artefacts + global_artefacts

            # get artefact start indices
            # [0] is start index, [1] is end index of the signal array
            artefacts_idx = [artefact.to_index(sr, WINDOW_SIZE_SEC, start_time_s)[0] for artefact in artefacts]
            artefacts_idx = set(artefacts_idx)

            artefact_count = len(artefacts_idx)
    else:
        artefacts_idx = set()
        artefact_count = None

    # save segments
    check_normal_count = args.sn and include_artefacts
    normal_count = 0
    for i in range(0, len(signal), sr * WINDOW_SIZE_SEC):
        is_artefact = i in artefacts_idx

        # skip normals if same amount reached as artefacts
        if (check_normal_count
            and not is_artefact
            and normal_count >= artefact_count):
            continue

        # get segments
        segment = signal[i:i + sr * WINDOW_SIZE_SEC]
        assert len(segment.flatten()) == sr * WINDOW_SIZE_SEC

        np.savetxt(
                os.path.join(output_dir,
                             (
                             f"{args.s}_{i}_{1 if is_artefact else 0}.txt"
                             if is_artefact is not None else
                             f"{args.s}_{i}.txt")
                             ),
                segment)

        if check_normal_count and not is_artefact:
            normal_count += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""
            HDF5 Creathon extract tool.
            Use this tool to extract signal segments from HDF5 file and their annotations from ARTF file.
            Outputs signal segments as numpy text files in the output directory.
            Files are named as {signal}_{start_idx}_{is_artefact}.txt if artefacts are provided, otherwise {signal}_{start_idx}.txt where 0 is not an artefact and 1 is an artefact.
            """)
    parser.add_argument('-fh', type=str, help='Path to HDF5 file', required=True)
    parser.add_argument('-fa', type=str, help='Path to ARTF file')
    parser.add_argument('-s', type=str, help='Signal to export, abp or icp', required=True)
    parser.add_argument('-o', type=str, help='Output directory', required=True)
    parser.add_argument('-sn', action='store_true', help='Export same number of normal and artefact segments')

    args = parser.parse_args()

    if args.s not in {'abp', 'icp'}:
        raise Exception("Unknown signal value")

    main(args)

