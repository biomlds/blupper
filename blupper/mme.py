import pandas as pd
import numpy as np


def short_pedigree_to_long(df):
    """Reformat short table into long one

    Short:
    Calf  Sire      Dam
    0     4     1  Unknown
    1     5     3        2
    2     6     1        2
    3     7     4        5
    4     8     3        6

    Long:
    Calf    Sire      Dam
    0     1  Uknown   Uknown
    1     2  Uknown   Uknown
    2     3  Uknown   Uknown
    0     4       1  Unknown
    1     5       3        2
    2     6       1        2
    3     7       4        5
    4     8       3        6

    Arguments:
        df {pd.DataFrame} -- a table containing pedegree [and traits]
    """

    sire_not_in_calf = list(set(df['Sire']).difference(df.Calf))
    dam_not_in_calf = list(set(df['Dam']).difference(df.Calf))
    extra_calfs = sorted([i for i in (sire_not_in_calf + dam_not_in_calf)
                          if i != 'Unknown'])
    extra_calfs_dict = {'Calf': extra_calfs}

    for colname in df.columns.values[1:]:
        if colname == 'Sex':
            extra_calfs_sex = []
            for i in extra_calfs:
                check_sex = (df[['Dam', 'Sire']] == i).apply(sum)
                parent = check_sex.index[check_sex > 0][0]
                extra_calfs_sex.append(parent)
            extra_calfs_sex = ['Male' if i == 'Sire' else 'Female'
                               for i in extra_calfs_sex]
            extra_calfs_dict.update({'Sex': extra_calfs_sex})
        else:
            extra_calfs_dict.update({colname: ['Unknown']*len(extra_calfs)})

    top = pd.DataFrame(extra_calfs_dict)
    long_df = top.append(df).reset_index(drop=True)

    return(long_df)


def make_XyZ(df, response_var, fixed_factor=['Sex']):
    """Produce X, y, Z matrix as in Mrode RA, 2014 (p. 38)

    Arguments:
    df {pd.DataFrame} -- contains info about animals (pedigree, etc.)
    response_var {str} -- response variable

    Keyword Arguments:
        fixed_factor {list} -- list of fixed factors (default: {['Sex']})
    """

    df_long = short_pedigree_to_long(df)
    missing_records = sum(df_long[response_var] == 'Unknown')
    X = pd.get_dummies(df[fixed_factor]).to_numpy()
    X = np.fliplr(X)
    n_animals = df_long.shape[0]
    Z = np.identity(n_animals)[missing_records:, :]
    y = df[[response_var]].to_numpy()

    return(X, y, Z)


def A_matrix(pedigree_table):
    """Return a numerator relationship matrix

    Arguments:
        pedigree_table {pandas.DataFrame} -- pedigree written in following format:

        Calf     Sire      Dam
            3        1        2
            4        1  Unknown
            5        4        3
            6        5        2
    """

    n_rows = pedigree_table.shape[0]
    pedigree_table['n_missing_parent'] = (
        pedigree_table == "Unknown").apply(sum, axis=1)

    A = np.array([np.nan]*(n_rows**2)).reshape((n_rows, n_rows))

    for i in range(n_rows):
        if pedigree_table['n_missing_parent'][i] == 0:
            s = int(pedigree_table.Sire[i])-1
            d = int(pedigree_table.Dam[i])-1
            for j in range(i):
                A[i][j] = A[j][i] = np.round(0.5*(A[j][s]+A[j][d]), 3)
            A[i][i] = np.round(1 + 0.5*A[s][d], 3)

        if pedigree_table['n_missing_parent'][i] == 1:
            s = int(pedigree_table.Sire[i])-1
            for j in range(i):
                A[i][j] = A[j][i] = np.round(0.5*A[j][s], 3)
            A[i][i] = 1

        if pedigree_table['n_missing_parent'][i] == 2:
            for j in range(i):
                A[i][j] = A[j][i] = 0
            A[i][i] = 1
    return(A)


def A_inverse_no_inbreeding(df):
    """Return a numerator relationship matrix as in Mrode RA, 2014 (p. 26)

    Arguments:
        df {pandas.DataFrame} -- pedigree written in following format:

        Calf     Sire      Dam
            3        1        2
            4        1  Unknown
            5        4        3
            6        5        2
    """

    pedigree_table = short_pedigree_to_long(df)[['Calf', 'Sire', 'Dam']]
    n_rows = pedigree_table.shape[0]
    pedigree_table['n_missing_parent'] = (
        pedigree_table == "Unknown").apply(sum, axis=1)

    A_inverse = np.zeros((n_rows, n_rows))

    for i in range(n_rows):
        if pedigree_table['n_missing_parent'][i] == 0:
            alpha = 2
            s = int(pedigree_table.Sire[i])-1   # 1
            d = int(pedigree_table.Dam[i])-1    # 2
            A_inverse[i][i] = A_inverse[i][i] + alpha

            A_inverse[s][i] = A_inverse[s][i] - alpha/2
            A_inverse[i][s] = A_inverse[i][s] - alpha/2
            A_inverse[d][i] = A_inverse[d][i] - alpha/2
            A_inverse[i][d] = A_inverse[i][d] - alpha/2

            A_inverse[s][s] = A_inverse[s][s] + alpha/4
            A_inverse[s][d] = A_inverse[s][d] + alpha/4
            A_inverse[d][s] = A_inverse[d][s] + alpha/4
            A_inverse[d][d] = A_inverse[d][d] + alpha/4

        if pedigree_table['n_missing_parent'][i] == 1:
            alpha = 4/3
            s = int(pedigree_table.Sire[i])-1
            A_inverse[i][i] = A_inverse[i][i] + alpha
            A_inverse[s][i] = A_inverse[s][i] - alpha/2
            A_inverse[i][s] = A_inverse[i][s] - alpha/2
            A_inverse[s][s] = A_inverse[s][s] + alpha/4

        if pedigree_table['n_missing_parent'][i] == 2:
            alpha = 1
            A_inverse[i][i] = A_inverse[i][i] + alpha

    return(A_inverse)


def mme_solution(df, sigma_sq_a, sigma_sq_e, response_var, fixed_factor=['Sex']):
    """Solve mixed model equations as in Mrode RA, 2014 (p. 36-39)

    Arguments:
        df {pandas.DataFrame} -- pedigree written in following format:
        sigma_sq_a {numeric} -- variance(a)
        sigma_sq_e {numeric} -- variance(e)
        response_var {str} -- response variable

    Keyword Arguments:
        fixed_factor {list} -- fixed factors (default: {['Sex']})
    """

    alpha = sigma_sq_e/sigma_sq_a
    X, y, Z = make_XyZ(df, response_var, fixed_factor)
    long_table = short_pedigree_to_long(df)
    A_inverse = A_inverse_no_inbreeding(df)

    part_X = np.concatenate((np.dot(X.T, X),
                             np.dot(Z.T, X)),
                            axis=0)
    part_Z = np.concatenate((np.dot(X.T, Z),
                             np.dot(Z.T, Z) + A_inverse*alpha),
                            axis=0)

    LSE_left = np.concatenate((part_X, part_Z), axis=1)
    LSE_right = np.concatenate((np.dot(X.T, y), np.dot(Z.T, y)), axis=0)

    coefficients = np.dot(np.linalg.pinv(LSE_left), LSE_right).reshape(1, -1)
    blup = coefficients[0, -Z.shape[1]:]  # .reshape(1, -1)
    animals = long_table.Calf.to_numpy()
    LSE_left_diag = np.linalg.inv(LSE_left).diagonal()[-Z.T.shape[0]:]
    r_squared = 1 - LSE_left_diag*alpha
    r = np.sqrt(r_squared)
    sep = np.sqrt((1 - r_squared)*sigma_sq_a)

    df_out_tmp = pd.DataFrame({'Animal': animals, 'BLUP': blup,
                               'r_squared': r_squared, 'r': r, 'SEP': sep})

    return(df_out_tmp)
