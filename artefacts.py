from lib.readers import ARTFReader
from lib.hdf5_reader_module import SignalClass
from lib.funcs import read_artf, read_hdf5

import argparse

WINDOW_SIZE_SEC = 10


def main(args):
    hdf5_filepath = args.fh
    artf_filename = args.fa

    # load hdf5
    icp, abp = read_hdf5(hdf5_filepath)

    if args.s == 'icp':
        # get sample rates
        sr = int(icp["sample_rate"])

        # get start times
        start_time_s = icp["start_time_s"]
    elif args.s == 'abp':
        # get sample rates
        sr = int(abp["sample_rate"])

        # get start times
        start_time_s = abp["start_time_s"]

    # load artefacts
    artefacts = read_artf(artf_filename)

    # get artefacts
    global_artefacts = artefacts["global_artefacts"]

    if args.s == 'icp':
        artefacts = artefacts["icp_artefacts"]
        artefacts = artefacts + global_artefacts

        artefact_count = len(artefacts)

        # get artefact start indices
        # [0] is start index, [1] is end index of the signal array
        artefacts_idx = [
                    (
                    artefact.to_index(sr, WINDOW_SIZE_SEC, start_time_s)[0],
                    artefact
                    ) for artefact in artefacts]
        # sort by index
        artefacts_idx = sorted(artefacts_idx, key=lambda x: x[0])

    elif args.s == 'abp':
        artefacts = artefacts["abp_artefacts"]
        artefacts = artefacts + global_artefacts

        artefact_count = len(artefacts)

        # get artefact start indices
        # [0] is start index, [1] is end index of the signal array
        artefacts_idx = [
                    (
                    artefact.to_index(sr, WINDOW_SIZE_SEC, start_time_s)[0],
                    artefact
                    ) for artefact in artefacts]
        # sort by index
        artefacts_idx = sorted(artefacts_idx, key=lambda x: x[0])

    for (idx, artefact) in artefacts_idx:
        print(f"Artefact ({args.s}) at signal index {idx} ({artefact.start_time})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""
            HDF5 Creathon artefacts tool.
            Use this tool to get information about artefacts present in HDF5 file.
            """)
    parser.add_argument('-fh', type=str, help='Path to HDF5 file', required=True)
    parser.add_argument('-fa', type=str, help='Path to ARTF file', required=True)
    parser.add_argument('-s', type=str, help='Signal to export, abp or icp', required=True)

    args = parser.parse_args()

    if args.s not in {'abp', 'icp'}:
        raise Exception("Unknown signal value")

    main(args)

