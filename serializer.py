"""
transparent serialization of numpy/pandas data via the standard lib json module.

loosely based on ideas from
http://robotfantastic.org/serializing-python-data-to-json-some-edge-cases.html

compatible to python2.7 and python3.3 and allows to serialize 
between the two interpreters.

Note that the serialization/deserialization is not space-efficient
due to the nature of json and not very fast either.  You could
certainly save space by compressing/decompressing the 
resulting json output if you need to.

"""

import numpy as np
import pandas as pd
from datetime import datetime
import json

def serialize(data):
    if data is None or isinstance(data, (bool, int, float, str)):
        return data
    if isinstance(data, datetime):
        return {"py/datetime": {"ordinal": data.toordinal()}}
    if isinstance(data, list):
        return [serialize(val) for val in data]
    if isinstance(data, dict):
        if all(isinstance(k, str) for k in data):
            return {k: serialize(v) for k, v in data.items()}
        return {"py/dict": [[serialize(k), serialize(v)] for k, v in data.items()]}
    if isinstance(data, tuple):
        return {"py/tuple": [serialize(val) for val in data]}
    if isinstance(data, set):
        return {"py/set": [serialize(val) for val in data]}
    if isinstance(data, pd.tseries.index.DatetimeIndex):
        return {"py/pandas.tseries.index.DatetimeIndex": {
            "values": serialize(data.tolist()),
            "dtype":  str(data.dtype)}}
    if isinstance(data, np.ndarray):
        return {"py/numpy.ndarray": {
            "values": serialize(data.tolist()),
            "dtype":  str(data.dtype)}}
    if isinstance(data, pd.DataFrame):
        return {"py/pandas.DataFrame": {
            "data": serialize(data.to_dict()),
            "dtypes":  [str(x) for x in data.dtypes.tolist()],
        }}
    raise TypeError("Type %s not data-serializable" % type(data))

def restore(dct):
    if "py/dict" in dct:
        return dict(dct["py/dict"])
    if "py/tuple" in dct:
        return tuple(dct["py/tuple"])
    if "py/set" in dct:
        return set(dct["py/set"])
    if "py/pandas.tseries.index.DatetimeIndex" in dct:
        data = dct["py/pandas.tseries.index.DatetimeIndex"]
        return pd.tseries.index.DatetimeIndex(data["values"], 
               dtype=data["dtype"])
    if "py/pandas.DataFrame" in dct:
        data = dct["py/pandas.DataFrame"]
        return pd.DataFrame(data["data"])
    if "py/numpy.ndarray" in dct:
        data = dct["py/numpy.ndarray"]
        return np.array(data["values"],  dtype=data["dtype"])
    if "py/datetime" in dct:
        data = dct["py/datetime"]
        return datetime.fromordinal(data["ordinal"])
    return dct

def data_to_json(data):
    return json.dumps(serialize(data))

def json_to_data(s):
    return json.loads(s, object_hook=restore)


