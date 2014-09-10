import numpy as np
try:
    __import__('odml')
except ImportError:
    warnings.warn("odml package not available. Install via pip (sudo pip install odml) or get it on Github (https://github.com/G-Node/python-odml)")


def gauss_kernel(sigma, sample_rate, duration):
    """
    Creates a Gaussian kernel centered in a vector of given duration.

    :param sigma: the standard deviation of the kernel in seconds
    :param sample_rate: the temporal resolution of the kernel in Hz
    :param duration: the desired duration of the kernel in seconds, (in general at least 4 * sigma)

    :return: the kernel as numpy array
    """
    l = duration * sample_rate
    x = np.arange(-np.floor(l / 2), np.floor(l / 2)) / sample_rate
    y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-(x ** 2 / (2 * sigma ** 2)));
    y /= np.sum(y)
    return y


def binary_spike_train_to_rate(binary, sample_rate, kernel_width, return_metadata=True):
    """
    Converts the binary representation of a spike train to a spike rate. Conversion is done by convolving the binary
    data with a Gaussian kernel of the specified width.

    :param binary: Binary representation of a spike train. 1 represents the occurrence of a spike, 0 its absence
    :param sample_rate: the rate in Hz in which the data has been sampled
    :param kernel_width: the standard deviation of the Gaussian kernel in seconds
    :param return_metadata: If true the analysis metadata are returned as odml section

    :return: the rate vector as numpy array
    """
    g = gauss_kernel(kernel_width, sample_rate, kernel_width * 8)
    rate = convolve(binary, g, mode='same') * sample_rate

    if not return_metadata or 'odml' not in globals():
        return rate
    metadata = odml.Section("PSTH", "analysis/psth")
    metadata.append(odml.Property("Description", "PSTH estimated by convolution with a Gaussian kernel."))
    value = odml.Value(kernel_width, unit='s')
    metadata.append(odml.Property("KernelWidth", value))
    metadata.append(odml.Property("KernelType", "Gaussian"))
    metadata.append(odml.Property("Date", dt.date.today().isoformat()))
    return rate, metadata


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
    :param return_metadata: If true the analysis metadata are returned as odml section

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
