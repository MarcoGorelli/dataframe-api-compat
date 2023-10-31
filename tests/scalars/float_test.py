import pytest

from tests.utils import integer_dataframe_1
from tests.utils import integer_dataframe_2


@pytest.mark.parametrize(
    "attr",
    [
        "__lt__",
        "__le__",
        "__eq__",
        "__ne__",
        "__gt__",
        "__ge__",
        "__add__",
        "__radd__",
        "__sub__",
        "__rsub__",
        "__mul__",
        "__rmul__",
        "__mod__",
        "__rmod__",
        "__pow__",
        "__rpow__",
        "__floordiv__",
        "__rfloordiv__",
        "__truediv__",
        "__rtruediv__",
    ],
)
def test_float_binary(library: str, attr: str) -> None:
    other = 0.5
    df = integer_dataframe_2(library).collect()
    scalar = df.col("a").mean()
    float_scalar = float(scalar)
    assert getattr(scalar, attr)(other).force_materialise() == getattr(
        float_scalar,
        attr,
    )(other)


def test_float_binary_invalid(library: str) -> None:
    lhs = integer_dataframe_2(library).collect().col("a").mean()
    rhs = integer_dataframe_1(library).collect().col("b").mean()
    with pytest.raises(ValueError):
        _ = lhs > rhs


def test_float_binary_lazy_valid(library: str) -> None:
    df = integer_dataframe_2(library)
    lhs = df.col("a").mean()
    rhs = df.col("b").mean()
    _ = lhs > rhs  # should not raise


@pytest.mark.parametrize(
    "attr",
    [
        "__pos__",
        "__abs__",
        "__int__",
        "__float__",
        "__bool__",
        "__neg__",
        "__pos__",
    ],
)
def test_float_unary(library: str, attr: str) -> None:
    df = integer_dataframe_2(library).collect()
    scalar = df.col("a").mean()
    float_scalar = float(scalar)
    assert getattr(scalar, attr)() == getattr(float_scalar, attr)()
