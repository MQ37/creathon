from lib.readers import ARTFReader
from lib.hdf5_reader_module import SignalClass
from lib.funcs import read_artf, read_hdf5_with_signals

import h5py
import numpy as np
import argparse


def main(args):
    hdf5_filepath = args.fh
    artf_filename = args.fa

    # load hdf5
    icp_signal, abp_signal, signals = read_hdf5_with_signals(hdf5_filepath)

    # get start times and end times
    icp_start_time_s = icp_signal["start_time_s"]
    icp_end_time_s = icp_signal["end_time_s"]
    abp_start_time_s = abp_signal["start_time_s"]
    abp_end_time_s = abp_signal["end_time_s"]

    # get signal lengths
    icp_length_s = icp_end_time_s - icp_start_time_s
    icp_length_h = icp_length_s / 3600
    abp_length_s = abp_end_time_s - abp_start_time_s
    abp_length_h = abp_length_s / 3600

    # get number of segments
    icp_n_segments = int(icp_length_s // 10)
    abp_n_segments = int(abp_length_s // 10)

    print(f"Signals: {','.join(signals)}")
    print(f"ICP length: {icp_length_h:.2f} h")
    print(f"ABP length: {abp_length_h:.2f} h")
    print(f"ICP segments (10 s): {icp_n_segments}")
    print(f"ABP segments (10 s): {abp_n_segments}")

    # get sample rates
    icp_sr = icp_signal["sample_rate"]
    abp_sr = abp_signal["sample_rate"]
    assert icp_sr == abp_sr

    print(f"ICP sample rate: {icp_sr:.2f} Hz")
    print(f"ABP sample rate: {abp_sr:.2f} Hz")


    if artf_filename is not None:
        # load artefacts
        artefacts = read_artf(artf_filename)

        # get artefacts
        global_artefacts = artefacts["global_artefacts"]
        icp_artefacts = artefacts["icp_artefacts"]
        abp_artefacts = artefacts["abp_artefacts"]

        icp_artefacts = icp_artefacts + global_artefacts
        abp_artefacts = abp_artefacts + global_artefacts

        print("ICP artefact segments: ", len(icp_artefacts))
        print("ABP artefacts segments: ", len(abp_artefacts))
        total_artefacts = len(global_artefacts) + len(icp_artefacts) + len(abp_artefacts)
        print("Total artefacts: ", total_artefacts)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""
            HDF5 Creathon info tool.
            Use this tool to get information about the HDF5 file and the artefacts.
            """)
    parser.add_argument('-fh', type=str, help='Path to HDF5 file', required=True)
    parser.add_argument('-fa', type=str, help='Path to ARTF file')

    args = parser.parse_args()

    main(args)

