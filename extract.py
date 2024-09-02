from lib.readers import ARTFReader
from lib.hdf5_reader_module import SignalClass
from lib.funcs import read_artf, read_hdf5

import h5py
import numpy as np
import argparse
import os
import matplotlib.pyplot as plt


def main(args):
    hdf5_filepath = args.fh
    artf_filename = args.fa
    output_dir = args.o
    include_artefacts = artf_filename is not None

    if not os.path.exists(output_dir):
        raise FileNotFoundError(f"Output directory {output_dir} does not exist")

    # load hdf5
    icp, abp = read_hdf5(hdf5_filepath)

    # get sample rates
    icp_sr = int(icp["sample_rate"])
    abp_sr = int(abp["sample_rate"])
    assert icp_sr == abp_sr

    # get start times
    icp_start_time_s = icp["start_time_s"]
    abp_start_time_s = abp["start_time_s"]

    # get signals
    icp_signal = icp["signal"]
    abp_signal = abp["signal"]

    # trim signals to be divisible by window size
    WINDOW_SIZE_SEC = 10
    icp_remainder = int(len(icp) % (icp_sr * WINDOW_SIZE_SEC))
    abp_remainder = int(len(abp) % (abp_sr * WINDOW_SIZE_SEC))
    icp_signal = icp_signal[:-icp_remainder]
    abp_signal = abp_signal[:-abp_remainder]

    if include_artefacts:
        # load artefacts
        artefacts = read_artf(artf_filename)

        # get artefacts
        global_artefacts = artefacts["global_artefacts"]
        icp_artefacts = artefacts["icp_artefacts"]
        abp_artefacts = artefacts["abp_artefacts"]

        icp_artefacts = icp_artefacts + global_artefacts
        abp_artefacts = abp_artefacts + global_artefacts

        # get artefact start indices
        # [0] is start index, [1] is end index of the signal array
        icp_artefacts_idx = [artefact.to_index(icp_sr, WINDOW_SIZE_SEC, icp_start_time_s)[0] for artefact in icp_artefacts]
        abp_artefacts_idx = [artefact.to_index(abp_sr, WINDOW_SIZE_SEC, abp_start_time_s)[0] for artefact in abp_artefacts]
        icp_artefacts_idx = set(icp_artefacts_idx)
        abp_artefacts_idx = set(abp_artefacts_idx)

    # save segments
    for i in range(0, len(icp_signal), icp_sr * WINDOW_SIZE_SEC):
        # get segments
        icp_segment = icp_signal[i:i + icp_sr * WINDOW_SIZE_SEC]
        abp_segment = abp_signal[i:i + abp_sr * WINDOW_SIZE_SEC]

        if include_artefacts:
            icp_is_artefact = i in icp_artefacts_idx
            abp_is_artefact = i in abp_artefacts_idx

            np.savetxt(
                    os.path.join(output_dir,
                                 f"icp_{i}_{1 if icp_is_artefact else 0}.txt"),
                    icp_segment)
            np.savetxt(
                    os.path.join(output_dir,
                                 f"abp_{i}_{1 if abp_is_artefact else 0}.txt"),
                    abp_segment)
        else:
            np.savetxt(
                    os.path.join(output_dir, f"icp_{i}.txt"),
                    icp_segment)
            np.savetxt(
                    os.path.join(output_dir, f"abp_{i}.txt"),
                    abp_segment)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""
            HDF5 Creathon extract tool.
            Use this tool to extract signal segments from HDF5 file and their annotations from ARTF file.
            Outputs signal segments as text files in the output directory.
            Files are named as {signal}_{start_idx}_{is_artefact}.txt if artefacts are provided, otherwise {signal}_{start_idx}.txt where 0 is not an artefact and 1 is an artefact.
            """)
    parser.add_argument('-fh', type=str, help='Path to HDF5 file', required=True)
    parser.add_argument('-fa', type=str, help='Path to ARTF file')
    parser.add_argument('-o', type=str, help='Output directory', required=True)

    args = parser.parse_args()

    main(args)

