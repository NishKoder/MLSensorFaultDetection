import os
from typing import Optional
import pandas as pd
import yaml

from AIUtiils.exceptions import AdvancedExceptionHandler
from AIUtiils.types import SimpleJson, UnionDT


_exception_handler = AdvancedExceptionHandler()


def read_pd_data_to_csv(
    file_path: str,
    sep: str = ",",
    header: UnionDT = "infer",
    names: Optional[list[str]] = None,
    index_col: Optional[UnionDT] = None,
    usecols: Optional[list[str]] = None,
    dtype: Optional[SimpleJson] = None,
    nrows: Optional[int] = None,
    encoding: Optional[str] = None,
    skiprows: Optional[UnionDT] = None
) -> pd.DataFrame:
    """
    Reads a CSV file with optional parameters.

    Args:
        file_path (str): Path to the CSV file.
        sep (str, optional): Delimiter. Defaults to ",".
        header (int|None, optional): Row to use as header. Defaults to "infer".
        names (list, optional): List of column names. Defaults to None.
        index_col (int|str, optional): Column to set as index. Defaults to None.
        usecols (list, optional): Columns to read. Defaults to None.
        dtype (dict, optional): Data types. Defaults to None.
        nrows (int, optional): Number of rows to read. Defaults to None.
        encoding (str, optional): Encoding. Defaults to None.
        skiprows (int|list, optional): Rows to skip. Defaults to None.

    Raises:
        Exception: If reading fails, it's handled by _exception_handler.
    """
    try:
        data = pd.read_csv(
            file_path,
            sep=sep,
            header=header,
            names=names,
            index_col=index_col,
            usecols=usecols,
            dtype=dtype,
            nrows=nrows,
            encoding=encoding,
            skiprows=skiprows,
            low_memory=False,
        )
        return data
    except Exception as exc:
        _exception_handler.handle_exception(exc)


def write_pd_data_to_csv(
    data: pd.DataFrame,
    file_path: str,
    sep: str = ",",
    index: bool = False,
    header: bool = True,
    encoding: str = "utf-8",
    mode: str = "w",
    columns: Optional[list[str]] = None,
    quoting: Optional[int] = None
) -> None:
    """
    Writes a pandas DataFrame to a CSV file with optional parameters.

    Args:
        data (pd.DataFrame): DataFrame to be written.
        file_path (str): Path to the output CSV file.
        sep (str, optional): Field delimiter. Defaults to ",".
        index (bool, optional): Write row names. Defaults to False.
        header (bool, optional): Write column names. Defaults to True.
        encoding (str, optional): Encoding of the output file. Defaults to "utf-8".
        mode (str, optional): File mode (e.g. 'w', 'a'). Defaults to "w".
        columns (list, optional): Columns to write. Defaults to None.
        quoting (int, optional): Controls quote style. Defaults to None.

    Raises:
        Exception: If any I/O error occurs, it's handled by _exception_handler.
    """
    try:
        data.to_csv(
            file_path,
            sep=sep,
            index=index,
            header=header,
            encoding=encoding,
            mode=mode,
            columns=columns,
            quoting=quoting
        )
    except Exception as exc:
        _exception_handler.handle_exception(exc)


def read_pd_data_from_excel(
    file_path: str,
    sheet_name: UnionDT = 0,
    header: UnionDT = 0,
    names: Optional[list[str]] = None,
    index_col: Optional[UnionDT] = None,
    usecols: Optional[UnionDT] = None,
    dtype: Optional[SimpleJson] = None,
    nrows: Optional[int] = None,
    skiprows: Optional[UnionDT] = None
) -> pd.DataFrame:
    """
    Reads an Excel file with optional parameters.

    Args:
        file_path (str): Path to the Excel file.
        sheet_name (str|int|None, optional): Sheet name or index. Defaults to 0.
        header (int|None, optional): Row to use as header. Defaults to 0.
        names (list, optional): List of column names. Defaults to None.
        index_col (int|str, optional): Column to set as index. Defaults to None.
        usecols (str|list, optional): Columns to read. Defaults to None.
        dtype (dict, optional): Data types. Defaults to None.
        nrows (int, optional): Number of rows to read. Defaults to None.
        skiprows (int|list, optional): Rows to skip. Defaults to None.

    Raises:
        Exception: If reading fails, it's handled by _exception_handler.
    """
    try:
        data = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=header,
            names=names,
            index_col=index_col,
            usecols=usecols,
            dtype=dtype,
            nrows=nrows,
            skiprows=skiprows
        )
        return data
    except Exception as exc:
        _exception_handler.handle_exception(exc)


def read_pd_data_from_json(
    file_path: str,
    orient: Optional[str] = None,
    typ: str = "frame",
    dtype: Optional[SimpleJson] = None,
    convert_axes: bool = None,
    convert_dates: bool = True,
    keep_default_dates: bool = True,
    numpy: bool = False,
    precise_float: bool = False,
    date_unit: Optional[str] = None,
    encoding: Optional[str] = None,
    lines: bool = False,
    chunksize: Optional[int] = None,
    compression: Optional[str] = "infer"
) -> pd.DataFrame:
    """
    Reads a JSON file with optional parameters.

    Args:
        file_path (str): Path to the JSON file.
        orient (str, optional): Indication of expected JSON string format.
            Defaults to None.
        typ (str, optional): Type of object to recover. Defaults to "frame".
        dtype (dict, optional): Data types. Defaults to None.
        convert_axes (bool, optional): Convert axes to the proper types.
            Defaults to None.
        convert_dates (bool, optional): Convert dates. Defaults to True.
        keep_default_dates (bool, optional): Keep default date parsing. 
            Defaults to True.
        numpy (bool, optional): Direct decoding to numpy arrays. Defaults to False.
        precise_float (bool, optional): Use precise floating point converter. 
            Defaults to False.
        date_unit (str, optional): Date unit. Defaults to None.
        encoding (str, optional): Encoding. Defaults to None.
        lines (bool, optional): Read the file as a JSON object per line. 
            Defaults to False.
        chunksize (int, optional): Return JsonReader object for iteration. 
            Defaults to None.
        compression (str, optional): Compression type. Defaults to "infer".

    Raises:
        Exception: If reading fails, it's handled by _exception_handler.
    """
    try:
        data = pd.read_json(
            file_path,
            orient=orient,
            typ=typ,
            dtype=dtype,
            convert_axes=convert_axes,
            convert_dates=convert_dates,
            keep_default_dates=keep_default_dates,
            numpy=numpy,
            precise_float=precise_float,
            date_unit=date_unit,
            encoding=encoding,
            lines=lines,
            chunksize=chunksize,
            compression=compression
        )
        return data
    except Exception as exc:
        _exception_handler.handle_exception(exc)


def read_yaml_to_dict(file_path: str) -> dict:
    """
    Reads a YAML file and returns a dictionary.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: The YAML file content as a dictionary.

    Raises:
        Exception: If reading fails, it's handled by _exception_handler.
    """
    try:
        with open(file_path, "rb") as file:
            data = yaml.safe_load(file)
        return data
    except Exception as exc:
        _exception_handler.handle_exception(exc)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file.

    Args:
        file_path (str): Path to the output YAML file.
        content (object): Content to write to the file.
        replace (bool, optional): Replace the file if it already exists.
            Defaults to False.

    Raises:
        Exception: If any I/O error occurs, it's handled by _exception_handler.
    """
    try:
        if os.path.isdir(file_path):
            raise IsADirectoryError(f"Specified file path is a directory: {file_path}")
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as exc:
        _exception_handler.handle_exception(exc)
