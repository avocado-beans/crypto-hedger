from binance_historical_data import BinanceDataDumper
import datetime

data_dumper = BinanceDataDumper(
    path_dir_where_to_dump=".",
    data_type="klines",  # aggTrades, klines, trades
    data_frequency="1m",  # argument for data_type="klines"
)

data_dumper.dump_data(
    tickers=['SANDBUSD'],
    date_start=datetime.date(year=2021, month=12, day=1),
    date_end=datetime.date(year=2022, month=1, day=1),
    is_to_update_existing=False,
)

