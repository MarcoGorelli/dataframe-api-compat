import pandas as pd
import numpy as np
import collections
import re

class PandasColumn:
    def __init__(self, column):
        self._value = column
    
    def __dlpack__(self):
        return self._value.__dlpack__()
    
    def isnull(self):
        return PandasColumn(self.value.isna())

    def notnull(self):
        return PandasColumn(self.value.notna())
    
    def any(self):
        return self.value.any()

    def all(self):
        return self.value.all()
    
    def __len__(self):
        return len(self.value)

class PandasGroupBy:
    def __init__(self, df, keys):
        self.df = df
        self.keys = keys

    def _validate_result(self, result):
        failed_columns = self.df.columns.difference(result.columns)
        if len(failed_columns) > 0:
            raise RuntimeError(
                "Groupby operation could not be performed on columns "
                f"{failed_columns}. Please drop them before calling groupby."
            )

    def any(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).any()
        if not (self.df.drop(columns=self.keys).dtypes == 'bool').all():
            raise ValueError('Expected boolean types')
        self._validate_result(result)
        return PandasDataFrame(result)

    def all(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).all()
        if not (self.df.drop(columns=self.keys).dtypes == 'bool').all():
            raise ValueError('Expected boolean types')
        self._validate_result(result)
        return PandasDataFrame(result)

    def min(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).min()
        self._validate_result(result)
        return PandasDataFrame(result)

    def max(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).max()
        self._validate_result(result)
        return PandasDataFrame(result)

    def sum(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).sum()
        self._validate_result(result)
        return PandasDataFrame(result)

    def prod(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).prod()
        self._validate_result(result)
        return PandasDataFrame(result)

    def median(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).median()
        self._validate_result(result)
        return PandasDataFrame(result)

    def mean(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).mean()
        self._validate_result(result)
        return PandasDataFrame(result)

    def std(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).std()
        self._validate_result(result)
        return PandasDataFrame(result)

    def var(self, skipna: bool = True):
        result = self.df.groupby(self.keys, as_index=False).var()
        self._validate_result(result)
        return PandasDataFrame(result)

class PandasDataFrame:

    # Not technicall part of the standard

    def __init__(self, dataframe):
        self._validate_columns(dataframe.columns) 
        self.dataframe = dataframe

    def _validate_columns(self, columns):
        counter = collections.Counter(columns)
        for col, count in counter.items():
            if count > 1:
                raise ValueError(f'Expected unique column names, got {col} {count} time(s)')
        for col in columns:
            if not isinstance(col, str):
                raise TypeError(f'Expected column names to be of type str, got {col} of type {type(col)}')
    
    def _validate_comparand(self, other):
        if (
            isinstance(other, PandasDataFrame)
            and not (
                self.dataframe.index.equals(other.dataframe.index)
                and self.dataframe.shape == other.dataframe.shape
                and self.dataframe.columns.equals(other.dataframe.columns)
            )
        ):
            raise ValueError(
                'Expected DataFrame with same length, matching columns, '
                'and matching index.'
            )
    
    def _validate_booleanness(self):
        if not (self.dataframe.dtypes == 'bool').all():
            raise NotImplementedError(
                "'any' can only be called on DataFrame "
                "where all dtypes are 'bool'"
            )
    
    # In the standard
    
    def groupby(self, keys):
        if not isinstance(keys, collections.abc.Sequence):
            raise TypeError(f'Expected sequence of strings, got: {type(keys)}')
        for key in keys:
            if key not in self.get_column_names():
                raise KeyError(f'key {key} not present in DataFrame\'s columns')
        return PandasGroupBy(self.dataframe, keys)

    def get_column_by_name(self, name):
        return PandasColumn(self.dataframe.loc[:, name])
    
    def get_columns_by_name(self, names):
        return PandasDataFrame(self.dataframe.loc[:, names])

    def get_rows(self, indices):
        if not isinstance(indices, collections.Sequence):
            raise TypeError(f'Expected Sequence of int, got {type(indices)}')
        return PandasDataFrame(self.dataframe.iloc[indices, :])
    
    def slice_rows(self, start, stop, step):
        return PandasDataFrame(self.dataframe.iloc[start:stop:step])

    def get_rows_by_mask(self, mask):
        mask_array = np.asarray(mask)
        if not mask_array.dtype == 'bool':
            raise TypeError(f'Expected boolean array, got {type(mask_array)}')
        return PandasDataFrame(self.dataframe.loc[mask_array, :])

    def insert(self, loc, label, value):
        value_array = np.asarray(value)
        before = self.dataframe.iloc[:, :loc]
        after = self.dataframe.iloc[:, loc+1:]
        to_insert = pd.Series(value_array, index=self.dataframe.index)
        return pd.concat([before, to_insert, after], axis=1)

    def drop_column(self, label):
        if not isinstance(label, str):
            raise TypeError(f'Expected str, got: {type(label)}')
        return PandasDataFrame(self.dataframe.drop(label, axis=1))

    def set_column(self, label, value):
        columns = self.get_column_names()
        if label in columns:
            idx = columns.index(idx)
            return self.drop_column(label).insert(idx, label, value)
        return self.insert(len(columns), label, value)

    def rename_columns(self, mapping):
        if not isinstance(mapping, collections.abc.Mapping):
            raise TypeError(f'Expected Mapping, got: {type(mapping)}')
        return PandasDataFrame(self.dataframe.rename(columns=mapping))

    def get_column_names(self):
        return self.dataframe.columns

    def __iter__(self):
        raise NotImplementedError()
    
    def __eq__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame(self.dataframe.__eq__(other.dataframe))

    def __ne__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__ne__(other.dataframe)))

    def __ge__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__ge__(other.dataframe)))

    def __gt__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__gt__(other.dataframe)))

    def __le__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__le__(other.dataframe)))

    def __lt__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__lt__(other.dataframe)))

    def __add__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__add__(other.dataframe)))

    def __sub__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__sub__(other.dataframe)))

    def __mul__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__mul__(other.dataframe)))

    def __truediv__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__truediv__(other.dataframe)))

    def __floordiv__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__floordiv__(other.dataframe)))

    def __pow__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__pow__(other.dataframe)))

    def __mod__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__mod__(other.dataframe)))

    def __divmod__(self, other):
        self._validate_comparand(other)
        return PandasDataFrame((self.dataframe.__divmod__(other.dataframe)))
        
    def any(self):
        self._validate_booleanness()
        return PandasDataFrame(self.dataframe.any().to_frame().T)

    def all(self):
        self._validate_booleanness()
        return PandasDataFrame(self.dataframe.all().to_frame().T)
    