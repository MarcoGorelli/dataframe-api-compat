from __future__ import annotations

import pandas as pd
import polars as pl
from polars.testing import assert_series_equal


def test_scale_column_pandas() -> None:
    s = pd.Series([1, 2, 3], name="a")
    ser = s.__column_consortium_standard__()
    ser = ser - ser.mean()
    result = ser.column
    pd.testing.assert_series_equal(result, pd.Series([-1, 0, 1.0], name="a"))


def test_scale_column_polars() -> None:
    s = pl.Series("a", [1, 2, 3])
    ser = s.__column_consortium_standard__()
    ser = ser - ser.mean()
    result = ser.df.select(ser.column).dataframe["a"]
    assert_series_equal(result, pl.Series("a", [-1, 0, 1.0]))
