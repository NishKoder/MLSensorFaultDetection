import os
from tkinter import E
import dill
import numpy as np
import pandas as pd
from AIUtiils.exceptions import AdvancedExceptionHandler


_exception_handler = AdvancedExceptionHandler()


def save_numpy_to_csv(data: np.ndarray, file_path: str) -> None:
    """
    Saves a NumPy array to a CSV file.

    Args:
        data (np.ndarray): NumPy array to save.
        file_path (str): Path to save the CSV file.
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
    except Exception as exc:
        _exception_handler.logger.error("Error saving NumPy array to CSV.")
        _exception_handler.handle_exception(exc)


def save_numpy_array_data_to_file(data: np.ndarray, file_path: str) -> None:
    """
    Saves a NumPy array to a file.

    Args:
        data (np.ndarray): NumPy array to save.
        file_path (str): Path to save the file.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, data)
    except Exception as exc:
        _exception_handler.logger.error("Error saving NumPy array to file.")
        _exception_handler.handle_exception(exc)


def load_numpy_array_data_from_file(file_path: str) -> np.ndarray:
    """
    Loads a NumPy array from a file.

    Args:
        file_path (str): Path to load the file.

    Returns:
        np.ndarray: NumPy array loaded from the file.
    """
    try:
        with open(file_path, "rb") as file:
            data = np.load(file)
        return data
    except Exception as exc:
        _exception_handler.logger.error(f"Error loading NumPy array from file: {file_path}")
        _exception_handler.handle_exception(exc)


def load_csv_to_numpy(file_path: str) -> np.ndarray:
    """
    Loads a CSV file to a NumPy array.

    Args:
        file_path (str): Path to load the CSV file.

    Returns:
        np.ndarray: NumPy array loaded from the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        data = df.to_numpy()
        return data
    except Exception as exc:
        _exception_handler.logger.error("Error loading CSV to NumPy array.")
        _exception_handler.handle_exception(exc)


def save_object_to_file(obj: object, file_path: str) -> None:
    """
    Saves an object to a file.

    Args:
        obj (object): Object to save.
        file_path (str): Path to save the file.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            dill.dump(obj, file)
    except Exception as exc:
        _exception_handler.logger.error("Error saving object to file.")
        _exception_handler.handle_exception(exc)


def load_object_from_file(file_path: str) -> object:
    """
    Loads an object from a file.

    Args:
        file_path (str): Path to load the file.

    Returns:
        object: Object loaded from the file.
    """
    try:
        if not os.path.exists(file_path):
            return Exception("File does not exist.")
        with open(file_path, "rb") as file:
            obj = dill.load(file)
        return obj
    except Exception as exc:
        _exception_handler.logger.error("Error loading object from file.")
        _exception_handler.handle_exception(exc)