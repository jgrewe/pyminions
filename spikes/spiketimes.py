import numpy as np

def spike_times_to_binary(spike_times, sample_rate, duration):
    """
    Converts a spike train from the spike time representation to a binary representation
    i.e. a vector of zeros in which spike occurence is marked with a 1

    :param spike_times: The times at which a spike occurred, times should be given in seconds.
    :param sample_rate: The rate, in Hz, in which the binary representation should be given.
    :param duration: The duration of the binary vector in seconds

    :return: binary representation of the data :numpy.ndarray

    """
    if len(spike_times.shape) > 1:
        raise ValueError("spike_times must not have more than one dimension")
    binary = np.zeros(int(duration * sample_rate))
    indices = np.asarray(spike_times  * sample_rate, dtype=int)
    binary[indices] = 1
    return binary
