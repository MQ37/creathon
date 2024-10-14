from lib.loader import SingleFileExtractor
import datetime
import argparse

WINDOW_SIZE_SEC = 10


def main(args):
    hdf5_filepath = args.f
    mode = args.s

    extractor = SingleFileExtractor(hdf5_filepath,
                                    mode=mode,
                                    matching=True)
    anomaly_segments = extractor.get_anomalies()

    for segment in anomaly_segments:
        # micro to sec
        dt = datetime.datetime.utcfromtimestamp(segment.start_time / 1e6)
        print(f"Artefact ({mode}) at {segment.start_time} ({dt})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="""
            HDF5 Creathon artefacts tool.
            Use this tool to get information about artefacts present in HDF5 file.
            """)
    parser.add_argument('-f', type=str, help='Path to HDF5 file (with corresponding .artf file)', required=True)
    parser.add_argument('-s', type=str, help='Signal to export, abp or icp', required=True)

    args = parser.parse_args()

    if args.s not in {'abp', 'icp'}:
        raise Exception("Unknown signal value")

    main(args)

