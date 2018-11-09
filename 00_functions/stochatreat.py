# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 14:34:47 2018

@author:    Manuel Martinez
@email:     manmartgarc@gmail.com
@purpose:   Define a function that assign treatments over an arbitrary
            number of strata.
"""

import pandas as pd
import numpy as np

# %% Main


def stochatreat(df, block_cols, treats,
                seed=0, idx_col=None, size=None, weights=None):
    """
    Takes a dataframe and an arbitrary number of treatments over an
    arbitrary number of clusters or strata.

    Attempts to return equally sized treatment groups, while randomly
    assigning misfits (left overs from groups not divisible by the number
    of treatments).

    Parameters
    ----------
    df: string
        DataFrame of your data.
    block_cols: string or list of strings
        Columns of your DataFrame over wich you wish to stratify over.
    treats:
        Number of treatment cells you wish to use (including control).
    size:
        Target sample size.
    seed:
        Seed for the randomization process, default is 0.
    idx_col: string
        DataFrame column with unique identifiers. If empty, uses the
        DataFrame's index as a unique identifier.
    weights: list of floats
        Fractions for each block that will be drawn. Make sure you
        take a look at your data and count the unique treatment blocks.
        The program expects that the number of weights is equal to the number
        of blocks.

        If your blocks are a combination of two or more columns, i.e.
        gender and smoker status, these will be calculated based on the
        order that you imputed them on block_cols.

        Therefore if the block_cols parameter looks
        like ['gender', 'smoker'], you should declare the
        weights parameter as nested list
        [[gender_w1, gender_w2], [smoker_w1, smoker_w3]]
        where w1, and w2 refered to weight 1 and weight 2 specifically.

        An example is as follows:
            >>>     Gender  |   Smoker
                    ------------------
                       0           0
                       0           1
                       1           0
                       1           1


    Returns
    -------

    The function returns a pandas DataFrame object, which can be merged back
    to the original dataframe.

    Usage
    -----
    Single cluster:

    >>> treatments = randomizer(df, 'clusters', 2, seed=1337, idx_col='myid')
    >>> df = df.merge(treatments, on='myid')

    Multiple clusters:

    >>> treatments = randomizer(df, ['cluster1', 'cluster2'],
                                2, seed=1337, idx_col='myid')
    >>> df = df.merge(treatments, on='myid')
    """
    np.random.seed(seed)

    # if idx_col parameter was not defined.
    if idx_col is None:
        df = df.reset_index()
        idx_col = 'index'
    elif type(idx_col) is not str:
        raise TypeError('idx_col has to be a string.')

    # check for unique identifiers
    if df[idx_col].duplicated(keep=False).sum() > 0:
        raise ValueError('Values in idx_col are not unique.')

    # deal with multiple clusters
    if type(block_cols) is str:
        block_cols = [block_cols]

    # combine cluster cells
    df = df[[idx_col] + block_cols].copy()
    df['blocks'] = df[block_cols].astype(str).sum(axis=1)

    # apply weights to each block
    # calculate weights if none were given
    if weights is None and size is not None:
        weights = (df.groupby('blocks')['blocks'].count() / len(df)).values

    # calculate weights if weights were given
    elif weights is not None and size is not None:
        blocks = df['blocks'].nunique()
        if len(weights) != blocks:
            raise ValueError('Length of weights ({}) is not the same as the '
                             'number of blocks ({}).'
                             .format(len(weights), blocks))
        else:
            for block in block_cols:
                continue
        
            

    # keep only ids and concatenated clusters
    df = df[df.columns[~df.columns.isin(block_cols)]]

    # set sample size
    if size is not None:
        size = int(size)

    # TODO:
    # make sure to assign before dropping people to select a desired
    # sample size.

    slizes = []
    for cluster in sorted(df['blocks'].unique()):
        treats = int(treats)

        # slize df by cluster
        slize = df.loc[df['blocks'] == cluster].copy()
        slize = slize[[idx_col]]
        slize = slize.set_index(idx_col)

        # attempt to divide cluster into equal groups depending on treatments
        if len(slize) % treats == 0:  # cluster fits into treatments nicely
            treat_block = int(len(slize) / treats)

            # assign random numbers to each household
            slize['rand'] = np.random.uniform(size=len(slize))

            # order by random numbers
            slize = slize.sort_values(by='rand', ascending=False)
            slize = slize.reset_index()

            # assign treatments based on treatment blocks
            for i in range(treats):
                # if first treatment cell
                if i == range(treats)[0]:
                    slize.loc[:treat_block, 'treat'] = i
                # if not the first treatment cell
                else:
                    slize.loc[treat_block * i:treat_block * (i + 1),
                              'treat'] = i

        elif (len(slize) % treats != 0):  # cluster doesn't fit into treats
            # remove extra and classify as misfits
            new_len = len(slize) - (len(slize) % treats)
            new_slize = slize.iloc[:new_len].copy()

            misfits = slize.iloc[new_len:].copy()
            misfits = misfits.reset_index()

            treat_block = int(len(new_slize) / treats)

            # assign random numbers to each household
            new_slize['rand'] = np.random.uniform(size=len(new_slize))

            # order by random numbers
            new_slize = new_slize.sort_values(by='rand', ascending=False)
            new_slize = new_slize.reset_index()

            # assign treatments based on treatment blocks
            for i in range(treats):
                # if first treatment cell
                if i == range(treats)[0]:
                    new_slize.loc[:treat_block, 'treat'] = i
                # if not the first treatment cell
                else:
                    new_slize.loc[treat_block * i:treat_block * (i + 1),
                                  'treat'] = i

            # deal with misfits
            misfits['treat'] = np.random.randint(0, treats,
                                                 size=len(misfits))

            # un-marginalize misfits :skull:
            slize = pd.concat([new_slize, misfits], sort=False)

        slize = slize.drop(columns='rand')
        
        # apply weights to slize.
        
        
        slizes.append(slize)
        ids_treats = pd.concat(slizes)

    return ids_treats
