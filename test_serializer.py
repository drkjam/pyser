# -*- coding: utf-8 -*-
#
#

import sys
import tempfile
import textwrap
import subprocess
import numpy
import pandas
from datetime import datetime

import py
import serializer


simple_tests = [
#   type: expected before/after repr
    4,
    3.25,
    [1,2,3],
    ["123", "hello"],
    (1,2,3),
    {(1,2,3): 32},
    datetime(2014,1,1),
    numpy.array([datetime(2014,1,1)]),
    pandas.date_range(datetime(2014,1,1), periods=12),
    pandas.DataFrame({"col1": pandas.TimeSeries(datetime(2014,1,1))})
]

@py.test.mark.parametrize("obj", simple_tests)
def test_simple(obj):
    j = serializer.data_to_json(obj)
    back = serializer.json_to_data(j)
    try:
        assert back == obj
    except ValueError:
        assert all(back == obj)
