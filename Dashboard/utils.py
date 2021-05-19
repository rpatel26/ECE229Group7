import pandas as pd
def load_data():
    '''loads the data from the data subdirectory'''
    train = pd.read_csv('../data/train.csv')
    #remove missing values form last three coloms
    train = train.dropna(subset=['Resource Allocation','Mental Fatigue Score',
                             'Burn Rate']).reset_index(drop=True)
    return train 