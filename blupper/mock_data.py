import pandas as pd


def ex_pedigree_six_animals():
    """
    Create an example DataFrame containing pedegree for 6 animals
    Table 2.1., p. 23
    """

    data_dict = {'Calf': [3, 4, 5, 6],
                 'Sire': [1, 1, 4, 5],
                 'Dam': [2, 'Unknown', 3, 2]}

    df = pd.DataFrame(data_dict)

    return(df)


def ex_pedigree_eight_animals():
    """
    Create an example DataFrame containing pedegree for 8 animals
    Table 3.1., p. 37
    """
    data_dict = {'Calf': [4, 5, 6, 7, 8],
                 'Sire': [1, 3, 1, 4, 3],
                 'Dam': ['Unknown', 2, 2, 5, 6]}

    A = pd.DataFrame(data_dict)
    return(A)


def ex_eight_animals_data_table():
    """
    Create an example DataFrame containing pedegree for 8 animals
    Table 3.1., p. 37
    """
    data_dict = {'Calf': [4, 5, 6, 7, 8],
                 'Sire': [1, 3, 1, 4, 3],
                 'Dam': ['Unknown', 2, 2, 5, 6],
                 'Sex': ['Male', 'Female', 'Female', 'Male', 'Male'],
                 'WWG': [4.5, 2.9, 3.9, 3.5, 5.0]}

    df = pd.DataFrame(data_dict)

    return(df)


def ex_sire_model_data_table():
    """
    Returns Pandas DataFrame containing pedegree
    """
    data_dict = {'Calf': [1, 3, 1, 4, 3],
                 'Sire': ['Unknown', 'Unknown', 'Unknown', 1, 'Unknown'],
                 'Dam': ['Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown'],
                 'Sex': ['Male', 'Female', 'Female', 'Male', 'Male'],
                 'WWG': [4.5, 2.9, 3.9, 3.5, 5.0]}

    df = pd.DataFrame(data_dict)

    return(df)
