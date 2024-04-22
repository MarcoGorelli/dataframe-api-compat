from __future__ import annotations

import pytest
from packaging.version import Version

from tests.utils import BaseHandler
from tests.utils import mixed_dataframe_1
from tests.utils import pandas_version


@pytest.mark.parametrize(
    ("dtype", "expected"),
    [
        ("integral", ["a", "b", "c", "d", "e", "f", "g", "h"]),
        ("signed integer", ["a", "b", "c", "d"]),
        ("unsigned integer", ["e", "f", "g", "h"]),
        ("floating", ["i", "j"]),
        ("bool", ["k"]),
        ("string", ["l"]),
        (("string", "integral"), ["a", "b", "c", "d", "e", "f", "g", "h", "l"]),
        (("string", "unsigned integer"), ["e", "f", "g", "h", "l"]),
    ],
)
@pytest.mark.skipif(
    Version("2.0.0") > pandas_version(),
    reason="before pandas got non-nano support",
)
def test_is_dtype(library: BaseHandler, dtype: str, expected: list[str]) -> None:
    df = mixed_dataframe_1(library).persist()
    namespace = df.__dataframe_namespace__()
    result = [i for i in df.column_names if namespace.is_dtype(df.schema[i], dtype)]
    assert result == expected
