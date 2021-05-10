import numpy as np


def lhs(dim, nsamples, centered=False,
        return_original=False, seed=None):
    """
    Compute latin hypercube samples.
    
    :param dim: Dimensionality of the samples
    :type dim: int
    :param nsamples: Number of samples
    :type nsamples: int
    :param centered: If 'True' returns samples
                     centered within intervals
    :type centered: bool
    :param return_original: If 'centered=False' return
                            the random, non-statefied
                            sample.
    :type return_original: bool
    :returns: Latin hypercube samples with dimension
              nsamples x dim and optionally the 
              original random sample before stratifying.
    :rtype: :class:`numpy.ndarray`
    """
    rs = np.random.default_rng(seed)
    # Make the random pairings
    H = np.zeros((nsamples, dim))
    if centered:
        # Generate the intervals
        cut = np.linspace(0, 1, nsamples + 1)
        # Fill points uniformly in each interval
        a = cut[:nsamples]
        b = cut[1:nsamples + 1]
        _center = (a + b)/2
        for j in range(dim):
            H[:, j] = rs.permutation(_center)
    else:
        u = rs.random((nsamples, dim))
        for j in range(dim):
            H[:, j] = rs.permutation(np.arange(nsamples))/nsamples + u[:,j]/nsamples
        if return_original:
            return u, H
    return H
