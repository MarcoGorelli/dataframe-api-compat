from typing import Any


# Technically, it would be possible to correctly type hint this function
# with a tonne of overloads, but for now, it' not worth it, just use Any
def validate_comparand(left: Any, right: Any) -> Any:
    """Validate comparand, raising if it can't be compared with `left`.

    If `left` and `right` are derived from the same dataframe, then return
    the underlying object of `right`.

    If the comparison isn't supported, return `NotImplemented` so that the
    "right-hand-side" operation (e.g. `__radd__`) can be tried.
    """
    if hasattr(right, "__expression_namespace__") and hasattr(
        left,
        "__dataframe_namespace__",
    ):
        result = right.call(left)
        if hasattr(result, "__column_namespace__"):
            return result.column
        return result.scalar
    if hasattr(left, "__dataframe_namespace__") and hasattr(
        right,
        "__dataframe_namespace__",
    ):  # pragma: no cover
        # Technically, currently unreachable - but, keeping this in case it
        # becomes reachable in the future.
        msg = "Cannot compare different dataframe objects - please join them first"
        raise ValueError(msg)
    if hasattr(left, "__dataframe_namespace__") and hasattr(
        right,
        "__column_namespace__",
    ):
        if (
            hasattr(left.dataframe, "index")
            and hasattr(right.column, "index")
            and left.dataframe.index is not right.column.index
        ):
            msg = "Cannot compare Column with DataFrame it was not derived from."
            raise ValueError(msg)
        return right.column
    if hasattr(left, "__dataframe_namespace__") and hasattr(
        right,
        "__scalar_namespace__",
    ):
        return right.scalar

    if hasattr(left, "__column_namespace__") and hasattr(
        right,
        "__dataframe_namespace__",
    ):
        return NotImplemented
    if hasattr(left, "__column_namespace__") and hasattr(right, "__column_namespace__"):
        if (
            hasattr(left.column, "index")
            and hasattr(right.column, "index")
            and left.column.index is not right.column.index
        ):
            msg = "Cannot compare Columns from different dataframes"
            raise ValueError(msg)
        return right.column
    if hasattr(left, "__column_namespace__") and hasattr(right, "__scalar_namespace__"):
        return right.scalar
    if hasattr(left, "__scalar_namespace__") and hasattr(
        right,
        "__dataframe_namespace__",
    ):
        return NotImplemented
    if hasattr(left, "__scalar_namespace__") and hasattr(right, "__column_namespace__"):
        return NotImplemented
    if hasattr(left, "__scalar_namespace__") and hasattr(right, "__scalar_namespace__"):
        return right.scalar

    return right
