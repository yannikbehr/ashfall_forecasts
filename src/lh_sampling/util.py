import numpy as np
import pandas as pd

from lh_sampling import get_data


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


def read_db(remove_calculated=True):
    """
    Read the eruption database into a dataframe
   
    :param remove_calculated: If 'True' remove all values that
                              are based on calculations.
    :type remove_calculated: bool
    :returns: Eruption database
    :rtype: :class:`pandas.DataFrame`
    """
    def str2float(val):
        if val == '':
            return np.nan
        else:
            return float(val)

    def str2cat(val):
        if val.find('CAL') != -1:
            return 1
        return 0
    
    def str2str(val):
        if val.find('Magmatic small to moderate*') !=-1:
            return 'Magmatic small to moderate'
        else:
            return val
            
    df = pd.read_csv(get_data('/data/SR2021-12 Spreadsheet_IVESPA.csv'),
                     usecols=[1,4,5,6,7,8,9,11,12,13],
                     converters={5: str2str, 6:str2float, 7:str2cat, 8:str2float,
                                 9:str2float, 11:str2cat, 12:str2float,
                                 13:str2cat})
    df.rename(columns={'MER_kg/s':'MER', 'Vent_elevation_km':'Vent_elevation',
                       'Column_height_km':'Column_height',
                       'Duration_hr':'Duration',
                       'Magma_type':'Magma type'},
              inplace=True)

    if remove_calculated:
        df['Column_height'] = np.where(df.Column_height_note==1, np.nan, df['Column_height'])
        df['MER'] = np.where(df.MER_note==1, np.nan, df['MER'])
        df['Duration'] = np.where(df.Duration_note==1, np.nan, df['Duration'])

    # Add log columns
    df['Volume'] = df['MER'] * df['Duration']
    df['log Volume'] = np.log(df['Volume'])
    df['log MER [kg/s]'] = np.log(df['MER'])
    df['log Column height [km]'] = np.log(df['Column_height'])
    df['log Duration [h]'] = np.log(df['Duration'])
    
    return df
