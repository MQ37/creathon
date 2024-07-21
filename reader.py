from lib.readers import ARTFReader
from lib.hdf5_reader_module import SignalClass

import h5py
import numpy as np
import matplotlib.pyplot as plt


WINDOW_SIZE_SEC = 10

def read_artf(filename):
    """
    Read artefacts from file

    Returns:
        global_artefacts: list of global artefacts
        icp_artefacts: list of ICP artefacts
        abp_artefacts: list of ABP artefacts
        metadata: metadata object
    """
    reader = ARTFReader(filename)
    try:
        global_artefacts, icp_artefacts, abp_artefacts, metadata = reader.read(abp_name="abp")
    except Exception:
        global_artefacts, icp_artefacts, abp_artefacts, metadata = reader.read(abp_name="art")

    return {
        "global_artefacts": global_artefacts,
        "icp_artefacts": icp_artefacts,
        "abp_artefacts": abp_artefacts,
        "metadata": metadata
    }

def read_hdf5_signal(hdf5_file, signal="icp"):
    """
    Read HDF5 file

    Returns:
        data: numpy array of data
        sample_rate: sample rate of data
        start_time_s: start time of data in seconds
        end_time_s: end time of data in seconds
    """
    wave_data = SignalClass(hdf5_file, signal)

    start_time = wave_data.get_all_data_start_time()
    start_time_s = start_time / 1e6
    end_time = wave_data.get_all_data_end_time()
    end_time_s = end_time / 1e6
    stream_duration_microsec = end_time - start_time

    stream = wave_data.get_data_stream(start_time, stream_duration_microsec)
    data = np.array(stream.values)

    sample_rate = stream.sampling_frq

    #return data, sample_rate, start_time_s, end_time_s
    return {
        "data": data,
        "sample_rate": sample_rate,
        "start_time_s": start_time_s,
        "end_time_s": end_time_s
    }

def read_hdf5(filename):
    hdf5_file = h5py.File(filename, 'r') 

    try:
        icp_signal = read_hdf5_signal(hdf5_file, signal="icp")
        try:
            abp_signal = read_hdf5_signal(hdf5_file, signal="abp")
        except KeyError:
            abp_signal = read_hdf5_signal(hdf5_file, signal="art")

        return icp_signal, abp_signal
    finally:
        hdf5_file.close()




# example usage of low level functions
def main():
    # TODO: change
    hdf5_filepath = ""
    artf_filename = ""

    icp_signal, abp_signal = read_hdf5(hdf5_filepath)
    artefacts = read_artf(artf_filename)

    print(icp_signal.keys())
    print(abp_signal.keys())
    print(artefacts.keys())

    # count all artefacts in the hdf5 file
    global_artefacts = artefacts["global_artefacts"]
    icp_artefacts = artefacts["icp_artefacts"]
    abp_artefacts = artefacts["abp_artefacts"]

    print("Global artefacts: ", len(global_artefacts))
    print("ICP artefacts: ", len(icp_artefacts))
    print("ABP artefacts: ", len(abp_artefacts))
    total_artefacts = len(global_artefacts) + len(icp_artefacts) + len(abp_artefacts)
    print("Total artefacts: ", total_artefacts)


    # get second 10s segment of icp
    icp_sr = icp_signal["sample_rate"]
    icp_data = icp_signal["data"]
    segment = icp_data[int(icp_sr * 10):int(icp_sr * 20)]
    plt.plot(segment)
    plt.show()


if __name__ == "__main__":
    main()

