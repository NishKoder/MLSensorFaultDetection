from operator import is_
import pandas as pd
from scipy.stats import ks_2samp

from AIUtiils.constants import DATA_DRIFT_THRESHOLD
from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.types import SimpleJson


_exception_handler = AdvancedExceptionHandler()


def validate_number_of_columns(
    data: pd.DataFrame,
    expected_columns: int,
    raise_on_mismatch: bool = False
) -> bool:
    """
    Validates the number of columns in the DataFrame.
    If `raise_on_mismatch` is True, raise an Exception when mismatch occurs.

    Args:
        data (pd.DataFrame): DataFrame to validate.
        expected_columns (int): Expected number of columns.
        raise_on_mismatch (bool): Whether to raise an exception on mismatch.

    Returns:
        bool: True if the number of columns matches the expected number, 
            False otherwise.

    Raises:
        Exception: If validation fails, it's handled by _exception_handler.
    """
    try:
        if data.shape[1] != expected_columns and raise_on_mismatch:
            raise ValueError("Unexpected number of columns.")
        return data.shape[1] == expected_columns
    except Exception as exc:
        _exception_handler.logger.error("Error validating number of columns.")
        _exception_handler.handle_exception(exc)

def is_numeric_column_exist(
    data: pd.DataFrame,
    columns: list[str] = None,
    dtype: str = "float64",
    exact_match: bool = True
) -> bool:
    """
    Checks if a numeric column (of the specified dtype) exists in the DataFrame.
    If columns are provided, only checks those columns.
    If `exact_match` is False, checks if dtype is contained in the column dtypes.
    """
    try:
        relevant_dtypes = data[columns].dtypes if columns else data.dtypes
        if exact_match:
            return any(relevant_dtypes == dtype)
        else:
            return any(relevant_dtypes.astype(str).str.contains(dtype))
    except Exception as exc:
        _exception_handler.logger.error("Error checking if numeric column exists.")
        _exception_handler.handle_exception(exc)


def select_columns(
    data: pd.DataFrame,
    columns: list[str],
    copy: bool = True
) -> pd.DataFrame:
    """
    Selects columns from a DataFrame.
    If `copy` is True, returns a copy; otherwise returns a view if possible.

    Args:
        data (pd.DataFrame): DataFrame to select columns from.
        columns (list): List of columns to select.
        copy (bool): Whether to return a copy of the selected columns.

    Returns:
        pd.DataFrame: DataFrame with only the selected columns.

    Raises:
        Exception: If selection fails, it's handled by _exception_handler.
    """
    try:
        selected = data[columns]
        return selected.copy() if copy else selected
    except Exception as exc:
        _exception_handler.logger.error("Error selecting columns.")
        _exception_handler.handle_exception(exc)


def drop_columns(
    data: pd.DataFrame,
    columns: list[str],
    inplace: bool = False,
    errors: str = "raise"
) -> pd.DataFrame:
    """
    Drops columns from a DataFrame.
    Pass `inplace=True` to modify the data directly.
    `errors` can be 'ignore' or 'raise'.

    Args:
        data (pd.DataFrame): DataFrame to drop columns from.
        columns (list): List of columns to drop.
        inplace (bool): Whether to modify the data directly.
        errors (str): Whether to raise or ignore errors.

    Returns:
        pd.DataFrame: DataFrame with the columns dropped.

    Raises:
        Exception: If dropping fails, it's handled by _exception_handler.
    """
    try:
        return (
            data.drop(columns, axis=1, inplace=inplace, errors=errors)
            if inplace
            else data.drop(columns, axis=1, errors=errors)
        )
    except Exception as exc:
        _exception_handler.logger.error("Error dropping columns.")
        _exception_handler.handle_exception(exc)

def drop_duplicates(
    data: pd.DataFrame,
    subset: list[str] = None,
    keep: str = "first",
    inplace: bool = False,
    ignore_index: bool = False
) -> pd.DataFrame:
    """
    Drops duplicate rows from a DataFrame.
    Pass `subset` columns to consider duplicates.
    `keep` can be 'first', 'last', or False.
    `inplace` modifies the data directly.

    Args:
        data (pd.DataFrame): DataFrame to drop duplicates from.
        subset (list): List of columns to consider duplicates.
        keep (str): Whether to keep the first, last, or no duplicates.
        inplace (bool): Whether to modify the data directly.
        ignore_index (bool): Whether to ignore the index.

    Returns:
        pd.DataFrame: DataFrame with duplicates dropped.

    Raises:
        Exception: If dropping duplicates fails, it's handled by _exception_handler.
    """
    try:
        return data.drop_duplicates(
            subset=subset,
            keep=keep,
            inplace=inplace,
            ignore_index=ignore_index
        )
    except Exception as exc:
        _exception_handler.logger.error("Error dropping duplicates.")
        _exception_handler.handle_exception(exc)

def drop_zero_std_columns(
    data: pd.DataFrame,
    threshold: float = 0.0,
    inplace: bool = False
) -> pd.DataFrame:
    """
    Drops columns with standard deviation <= threshold (default 0.0).
    Pass `inplace=True` to modify the data directly.

    Args:
        data (pd.DataFrame): DataFrame to drop columns from.
        threshold (float): Threshold for standard deviation.
        inplace (bool): Whether to modify the data directly.

    Returns:
        pd.DataFrame: DataFrame with columns with zero standard deviation dropped.

    Raises:
        Exception: If dropping fails, it's handled by _exception_handler.
    """
    try:
        cols_to_drop = data.loc[:, data.std() <= threshold].columns
        if inplace:
            data.drop(cols_to_drop, axis=1, inplace=True)
            return data
        return data.drop(cols_to_drop, axis=1)
    except Exception as exc:
        _exception_handler.logger.error(
            "Error dropping columns with zero standard deviation."
        )
        _exception_handler.handle_exception(exc)


def detect_data_drift(
    base_df: pd.DataFrame,
    current_df: pd.DataFrame,
    threshold: float = DATA_DRIFT_THRESHOLD,
) -> SimpleJson:
    try:
        status = True
        drift_report = {}
        for column in base_df.columns:
            base_column = base_df[column]
            current_column = current_df[column]
            drift = ks_2samp(base_column, current_column)
            if threshold <= drift.pvalue:
                is_drifted = False
            else:
                is_drifted = True
                status =  False
            drift_report[column] = {
                "pvalue": float(drift.pvalue),
                "is_drifted": is_drifted
            }
        return status, drift_report
    except Exception as exc:
        _exception_handler.logger.error("Error detecting data drift.")
        _exception_handler.handle_exception(exc)