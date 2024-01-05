from __future__ import annotations

from tests.utils import compare_dataframe_with_reference
from tests.utils import integer_dataframe_6


def test_expression_sorted_indices_ascending(library: str) -> None:
    df = integer_dataframe_6(library)
    pdx = df.__dataframe_namespace__()
    col = df.col
    sorted_indices = col("b").sorted_indices()
    result = df.take(sorted_indices)
    compare_dataframe_with_reference(
        result,
        {"a": [2, 2, 1, 1, 1], "b": [1, 2, 3, 4, 4]},
        dtype=pdx.Int64,
    )


def test_expression_sorted_indices_descending(library: str) -> None:
    df = integer_dataframe_6(library)
    pdx = df.__dataframe_namespace__()
    col = df.col
    sorted_indices = col("b").sorted_indices(ascending=False)
    result = df.take(sorted_indices)
    compare_dataframe_with_reference(
        result,
        {"a": [1, 1, 1, 2, 2], "b": [4, 4, 3, 2, 1]},
        dtype=pdx.Int64,
    )


def test_column_sorted_indices_ascending(library: str) -> None:
    df = integer_dataframe_6(library)
    pdx = df.__dataframe_namespace__()
    sorted_indices = df.col("b").sorted_indices()
    result = df.take(sorted_indices)
    compare_dataframe_with_reference(
        result,
        {"a": [2, 2, 1, 1, 1], "b": [1, 2, 3, 4, 4]},
        dtype=pdx.Int64,
    )


def test_column_sorted_indices_descending(library: str) -> None:
    df = integer_dataframe_6(library)
    pdx = df.__dataframe_namespace__()
    sorted_indices = df.col("b").sorted_indices(ascending=False)
    result = df.take(sorted_indices)
    compare_dataframe_with_reference(
        result,
        {"a": [1, 1, 1, 2, 2], "b": [4, 4, 3, 2, 1]},
        dtype=pdx.Int64,
    )
