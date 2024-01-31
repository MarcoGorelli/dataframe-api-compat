from __future__ import annotations

import pytest

from tests.utils import compare_column_with_reference
from tests.utils import integer_dataframe_1


@pytest.mark.parametrize(
    ("reduction", "expected", "expected_dtype"),
    [
        ("min", 1, "Int64"),
        ("max", 3, "Int64"),
        ("sum", 6, "Int64"),
        ("prod", 6, "Int64"),
        ("median", 2.0, "Float64"),
        ("mean", 2.0, "Float64"),
        ("std", 1.0, "Float64"),
        ("var", 1.0, "Float64"),
    ],
)
def test_expression_reductions(
    library: str,
    reduction: str,
    expected: float,
    expected_dtype: str,
) -> None:
    df = integer_dataframe_1(library)
    pdx = df.__dataframe_namespace__()
    pdx = df.__dataframe_namespace__()
    ser = pdx.col("a")
    ser = ser - getattr(ser, reduction)()
    result = df.assign(ser.rename("result"))
    reference = list((df.persist().get_column("a") - expected).to_array())
    expected_ns_dtype = getattr(pdx, expected_dtype)
    compare_column_with_reference(
        result.persist().get_column("result"),
        reference,
        expected_ns_dtype,
    )
