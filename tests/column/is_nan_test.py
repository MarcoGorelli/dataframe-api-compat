from __future__ import annotations

from tests.utils import compare_column_with_reference
from tests.utils import nan_dataframe_1


def test_column_is_nan(library: str) -> None:
    df = nan_dataframe_1(library).persist()
    pdx = df.__dataframe_namespace__()
    ser = pdx.col("a")
    result = df.assign(ser.is_nan().rename("result"))
    expected = [False, False, True]
    compare_column_with_reference(result.get_column("result"), expected, dtype=pdx.Bool)
