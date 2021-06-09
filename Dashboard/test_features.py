import pytest
import numpy as np
import pandas as pd
from feature_analysis import * 
from utils import * 


def test_get_corr():
    data = load_data()
    corr = get_corr(data)
    assert(isinstance(corr, pd.DataFrame))
    corr = np.array(corr)
    assert((corr.all() >= -1) & (corr.all() <= 1))
