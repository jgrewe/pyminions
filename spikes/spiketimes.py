import numpy as np
import warnings

try:
    __import__('odml')
except ImportError:
    warnings.warn("odml package not available. Install via ")


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


def serial_correlation(spike_times, max_lags=50, return_metadata=True):
    """
        Calculate the serial correlation for the the spike train provided by spike_times.

    :param spike_times: the spike times of a single trial. This should be a 1D array.
    :param max_lags: The number of lags to take into account
    :param return_metadata: If true the analysis metadata are returned
    :return: the serial correlation as a function of the lag, and, if wanted, the metadata.

    """
    if len(spike_times.shape) > 1:
        raise ValueError("spike times must not be more than 1D.")

    isis = np.diff(spike_times)
    unbiased = isis - np.mean(isis, 0)
    norm = np.sum(unbiased**2)
    a_corr = np.correlate(unbiased, unbiased, "same")/norm
    a_corr = a_corr[len(a_corr)/2:]

    if not return_metadata or 'odml' not in globals():
        return a_corr[:max_lags]

    metadata = odml.Section("Serial correlation", "analysis/serial_correlation")
    metadata.append(odml.Property("Description", "The serial correlation of inter-spike-intervals."))
    metadata.append(odml.Property("NoOfLags", max_lags))
    metadata.append(odml.Property("FirstLagCorrelation", a_corr[1]))
    metadata.append(odml.Property("Date", dt.date.today().isoformat()))
    return a_corr[:max_lags], metadata
