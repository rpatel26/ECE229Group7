import pytest
import pandas as pd
from utils import *


def test_data_format():
    data = load_data()
    assert check_data_format(data)


def test_data_gender():
    data = load_data()
    assert set(data['Gender']) == {'Female', 'Male'}


def test_data_company():
    data = load_data()
    assert set(data['Company Type']) == {'Product', 'Service'}


def test_data_WFH():
    data = load_data()
    assert set(data['WFH Setup Available']) == {'Yes', 'No'}


def test_data_design():
    data = load_data()
    assert all(data['Designation'] >= 0) and all(data['Designation'] <= 5)


def test_data_resource():
    data = load_data()
    assert all(data['Resource Allocation'] >= 0) and all(data['Resource Allocation'] <= 10)


def test_data_mental():
    data = load_data()
    assert all(data['Mental Fatigue Score'] >= 0) and all(data['Mental Fatigue Score'] <= 10)
