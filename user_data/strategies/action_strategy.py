# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Optional, Union

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,
    # Hyperopt Parameters
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    RealParameter,
    # timeframe helpers
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_prev_date,
    # Strategy helper functions
    merge_informative_pair,
    stoploss_from_absolute,
    stoploss_from_open,
)

#
# --------------------------------
# Add your lib to import here
import talib.abstract as taS
from technical import qtpylib


class ActionStrategy(IStrategy):
    """
    ActionStrategy - A simple time-based strategy that alternates between buying and selling BTC.
    
    Strategy logic:
    - Use 1-minute timeframe 
    - Buy on odd minutes (1, 3, 5...)
    - Sell on even minutes (0, 2, 4...)
    - Uses market orders for fast execution
    
    This is designed for dry-run testing only.
    """

    # Strategy interface version
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI - effectively disabled
    minimal_roi = {"0": 100}  

    # Stoploss - effectively disabled
    stoploss = -1.0 

    # Use 1-minute timeframe
    timeframe = "1m"

    # Process new candles only
    process_only_new_candles = True

    # Use market orders for fast execution
    order_types = {
        "entry": "market",
        "exit": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Order time in force
    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    # Position sizing (default to 95% of available balance)
    stake_amount = "95%"

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 1

    def informative_pairs(self):
        """
        No informative pairs needed for this strategy
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        No technical indicators needed for this time-based strategy
        """
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Buy on odd minutes (1, 3, 5...)
        """
        dataframe['enter_long'] = (dataframe['date'].dt.minute % 2 == 1).astype(int)
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Sell on even minutes (0, 2, 4...)
        """
        dataframe['exit_long'] = (dataframe['date'].dt.minute % 2 == 0).astype(int)
        return dataframe
