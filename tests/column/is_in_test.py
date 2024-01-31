from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any

import pytest

from tests.utils import compare_column_with_reference
from tests.utils import float_dataframe_1
from tests.utils import float_dataframe_2
from tests.utils import float_dataframe_3

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize(
    ("df_factory", "expected_values"),
    [
        (float_dataframe_1, [False, True]),
        (float_dataframe_2, [True, False]),
        (float_dataframe_3, [True, False]),
    ],
)
@pytest.mark.filterwarnings("ignore:np.find_common_type is deprecated")
def test_is_in(
    library: str,
    df_factory: Callable[[str], Any],
    expected_values: list[bool],
) -> None:
    df = df_factory(library).persist()
    pdx = df.__dataframe_namespace__()
    ser = pdx.col("a")
    other = ser + 1
    result = df.assign(ser.is_in(other).rename("result"))
    compare_column_with_reference(
        result.get_column("result"),
        expected_values,
        dtype=pdx.Bool,
    )


@pytest.mark.parametrize(
    ("df_factory", "expected_values"),
    [
        (float_dataframe_1, [False, True]),
        (float_dataframe_2, [True, False]),
        (float_dataframe_3, [True, False]),
    ],
)
@pytest.mark.filterwarnings("ignore:np.find_common_type is deprecated")
def test_expr_is_in(
    library: str,
    df_factory: Callable[[str], Any],
    expected_values: list[bool],
) -> None:
    df = df_factory(library)
    pdx = df.__dataframe_namespace__()
    col = pdx.col
    ser = col("a")
    other = ser + 1
    result = df.assign(ser.is_in(other).rename("result"))
    compare_column_with_reference(
        result.persist().get_column("result"),
        expected_values,
        dtype=pdx.Bool,
    )
