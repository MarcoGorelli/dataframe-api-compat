from __future__ import annotations

import pandas as pd

from tests.utils import integer_dataframe_1
from tests.utils import integer_series_1
from tests.utils import interchange_to_pandas


def test_column_divmod(library: str) -> None:
    df = integer_dataframe_1(library).collect()
    ser = integer_series_1(library)
    other = df.get_column("b")
    result_quotient, result_remainder = ser.__divmod__(other)
    # quotient
    result = df.insert_columns(result_quotient.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_quotient = pd.Series([0, 0, 0], name="result")
    pd.testing.assert_series_equal(result_pd, expected_quotient)
    # remainder
    result = df.insert_columns(result_remainder.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_remainder = pd.Series([1, 2, 3], name="result")
    pd.testing.assert_series_equal(result_pd, expected_remainder)


def test_column_divmod_with_scalar(library: str) -> None:
    df = integer_dataframe_1(library).collect()
    ser = df.get_column("a")
    df.get_column("b")
    result_quotient, result_remainder = ser.__divmod__(2)
    # quotient
    result = df.insert_columns(result_quotient.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_quotient = pd.Series([0, 1, 1], name="result")
    pd.testing.assert_series_equal(result_pd, expected_quotient)
    # remainder
    result = df.insert_columns(result_remainder.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_remainder = pd.Series([1, 0, 1], name="result")
    pd.testing.assert_series_equal(result_pd, expected_remainder)


def test_expression_divmod(library: str) -> None:
    df = integer_dataframe_1(library)
    namespace = df.__dataframe_namespace__()
    ser = namespace.col("a")
    other = namespace.col("b")
    result_quotient, result_remainder = ser.__divmod__(other)
    # quotient
    result = df.insert_columns(result_quotient.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_quotient = pd.Series([0, 0, 0], name="result")
    pd.testing.assert_series_equal(result_pd, expected_quotient)
    # remainder
    result = df.insert_columns(result_remainder.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_remainder = pd.Series([1, 2, 3], name="result")
    pd.testing.assert_series_equal(result_pd, expected_remainder)


def test_expression_divmod_with_scalar(library: str) -> None:
    df = integer_dataframe_1(library)
    namespace = df.__dataframe_namespace__()
    ser = namespace.col("a")
    result_quotient, result_remainder = ser.__divmod__(2)
    # quotient
    result = df.insert_columns(result_quotient.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_quotient = pd.Series([0, 1, 1], name="result")
    pd.testing.assert_series_equal(result_pd, expected_quotient)
    # remainder
    result = df.insert_columns(result_remainder.rename("result"))
    result_pd = interchange_to_pandas(result, library)["result"]
    expected_remainder = pd.Series([1, 0, 1], name="result")
    pd.testing.assert_series_equal(result_pd, expected_remainder)
