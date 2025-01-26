import pandas as pd
from sklearn.model_selection import train_test_split

from utils.constants import TRAIN_TEST_SPLIT_RATIO


def perform_train_test_split(
    dataframe: pd.DataFrame,
    test_size: float = TRAIN_TEST_SPLIT_RATIO,
) -> pd.DataFrame:
        train_set, test_set = train_test_split(
            dataframe,
            test_size=test_size
        )
        
        return train_set,test_set