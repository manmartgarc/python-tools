# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:34:47 2018

@author:    Manuel Martinez
@email:     manmartgarc@gmail.com
@purpose:   Define a function that assign treatments over an arbitrary
            number of strata.
"""

def randomizer(df, idx_var, cluster_var, treats, seed):
    """
    Takes a dataframe and assigns treatments on equally sized treatment groups,
    while randomly assigning misfits (left overs from groups not divisible
    by the number of treatments).

    The function returns a pandas DataFrame object, which can be merged back
    to the original dataframe.

    >>> treatments = randomizer(df, 'myid', 'clusters', 3, 100)
    >>> for cluster in df['cluster'].unique():
        df.loc[df['cluster'] == cluster, 'treat'] = (
            treatments.loc[treatments['cluster'] == cluster, 'treat'])
    """
    np.random.seed(seed)
    slizes = []
    for cluster in sorted(df[cluster_var].unique(), reverse=False):
        treats = int(treats)

        # slize df by cluster
        slize = df.loc[df[cluster_var] == cluster][[cluster_var]].copy()

        # attempt to divide cluster into three equal groups
        if len(slize) % treats == 0:  # if group is divisible by 3
            # divide cluster into three groups
            treat_block = int(len(slize) / treats)

            # assign random numbers to each household
            slize['rand'] = np.random.uniform(size=len(slize))

            # order by random numbers
            slize = slize.sort_values(by='rand', ascending=False).reset_index()

            # assign treatments based on treat blocks
            slize.loc[:treat_block, 'treat'] = 0
            slize.loc[treat_block:treat_block * 2, 'treat'] = 1
            slize.loc[treat_block * 2:treat_block * 3, 'treat'] = 2

        elif (len(slize) % treats != 0):  # if group is not divisible by treats
            # remove extra and classify as misfits
            new_len = len(slize) - (len(slize) % treats)
            new_slize = slize.iloc[:new_len].copy()
            misfits = slize.iloc[new_len:].copy().reset_index()

            treat_block = int(len(new_slize) / treats)

            # assign random numbers to each household
            new_slize['rand'] = np.random.uniform(size=len(new_slize))

            # order by random numbers
            new_slize = new_slize.sort_values(by='rand', ascending=False)
            new_slize = new_slize.reset_index()

            # assign treatments based on treat blocks
            new_slize.loc[:treat_block, 'treat'] = 0
            new_slize.loc[treat_block:treat_block * 2, 'treat'] = 1
            new_slize.loc[treat_block * 2:treat_block * 3, 'treat'] = 2

            # deal with misfits depending on the misfit N
            # if only one misfit
            if len(misfits) == 1:
                misfits['rand'] = np.random.uniform(size=len(misfits))
                misfits['treat'] = (
                    np.where(misfits['rand'] <= 1/3, 0,
                             np.where((misfits['rand'] > 1/3) &
                                      (misfits['rand'] < 2/3), 1, 2)))
            # if two misfits
            elif len(misfits) == 2:
                misfits['rand'] = np.random.uniform()
                rand = misfits['rand'].iloc[0]
                if rand <= 1/6:
                    misfits.loc[0, 'treat'] = 1
                    misfits.loc[1, 'treat'] = 2
                elif (rand > 1/6) & (rand <= 2/6):
                    misfits.loc[0, 'treat'] = 1
                    misfits.loc[1, 'treat'] = 0
                elif (rand > 2/6) & (rand <= 3/6):
                    misfits.loc[0, 'treat'] = 2
                    misfits.loc[1, 'treat'] = 1
                elif (rand > 3/6) & (rand <= 4/6):
                    misfits.loc[0, 'treat'] = 2
                    misfits.loc[1, 'treat'] = 0
                elif (rand > 4/6) & (rand <= 5/6):
                    misfits.loc[0, 'treat'] = 0
                    misfits.loc[1, 'treat'] = 1
                elif (rand > 5/6):
                    misfits.loc[0, 'treat'] = 0
                    misfits.loc[1, 'treat'] = 2

            # un-marginalize misfits :skull:
            slize = pd.concat([new_slize, misfits], sort=False)

        slize = slize.set_index('building_id')
        slizes.append(slize)

    return pd.concat(slizes)