from variable_correlations import get_correlations
import numpy as np
import pytest
import pandas as pd

def test_correlation():
    ids = np.zeros(10)
    feature_1 = np.ones(10)
    feature_2 = feature_1
    feature_3 = np.zeros(10)
    data = np.stack([ids, feature_1, feature_2, feature_3], axis=1)
    train_data = pd.DataFrame(data)
    train_data.columns = ['Employee ID', 'feature_1', 'feature_2', 'Mental Fatigue Score']
    dependent_variable="Mental Fatigue Score"
    method='pearson'
    assert get_correlations(train_data, dependent_variable, method) != 0

if __name__ == "__main__":
    test_correlation()