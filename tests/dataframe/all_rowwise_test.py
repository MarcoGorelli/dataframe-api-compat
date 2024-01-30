from __future__ import annotations

import pandas as pd
import pytest

from tests.utils import bool_dataframe_1
from tests.utils import interchange_to_pandas


def test_all_horizontal(library: str) -> None:
    df = bool_dataframe_1(library)
    pdx = df.__dataframe_namespace__()
    mask = pdx.all_horizontal(*[pdx.col(col_name) for col_name in df.column_names])
    result = df.filter(mask)
    result_pd = interchange_to_pandas(result)
    expected = pd.DataFrame({"a": [True, True], "b": [True, True]})
    pd.testing.assert_frame_equal(result_pd, expected)


@pytest.mark.xfail(strict=False)
def test_all_horizontal_invalid(library: str) -> None:
    df = bool_dataframe_1(library)
    pdx = df.__dataframe_namespace__()
    with pytest.raises(ValueError):
        _ = pdx.all_horizontal(pdx.col("a"), (df + 1).col("b"))
