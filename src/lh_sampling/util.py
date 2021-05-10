import numpy as np


def inv_cdf(x, usamples):
    """
    Draw samples from any cdf by computing the
    empirical inverse CDF.
    
    :param x: Random samples from the target
              distribution
    :type x: :class:`numpy.ndarray`
    :param usamples: Uniformly distributed samples
                     to resample the target distribution.
    :type usamples: :class:`numpy.ndarray`
    :returns: New samples from the target distribution.
    :rtype: :class:`numpy.ndarray`
    """
    x_sorted, cdf = ecdf(x)
    idx = np.digitize(usamples, cdf)
    return x[idx]


def ecdf(x):
    data = np.sort(x)
    n = data.size
    cdf = np.arange(1, n+1)/n
    return (data, cdf)
