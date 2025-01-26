from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split

from utils.constants import TRAIN_TEST_SPLIT_RATIO


def perform_train_test_split(
    dataframe: pd.DataFrame,
    test_size: float = TRAIN_TEST_SPLIT_RATIO,
) -> tuple[Any, Any]:
    """
    Splits the given DataFrame into training and testing sets.

    Parameters:
    dataframe (pd.DataFrame): The DataFrame to split.
    test_size (float): The proportion of the dataset to include in the test split.
                       Defaults to TRAIN_TEST_SPLIT_RATIO.

    Returns:
    tuple: A tuple containing the training set and the testing set.
    """
    train_set, test_set = train_test_split(
        dataframe,
        test_size=test_size
    )

    return train_set, test_set