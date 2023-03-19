import board
import digitalio
import time

from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException
from adafruit_display_text import LabelBase

STATION_CODE = config['metro_station_code']
REFRESH_INTERVAL = config['refresh_interval']

def refresh_trains(train_group: str) -> [dict]:
    try:
        return MetroApi.fetch_train_predictions(STATION_CODE, train_group)
    except MetroApiOnFireException:
        print('WMATA Api is currently on fire. Trying again later ...')
        return None

train_group = config['train_group_1']

train_board = TrainBoard(lambda: refresh_trains(train_group))

while True:
    train_board.refresh()
    time.sleep(REFRESH_INTERVAL)
    train_group = config['train_group_1'] if train_group == config['train_group_2'] else config['train_group_2']
