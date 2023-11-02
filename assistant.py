import os
import sys
import time

import json
import pandas
from io import StringIO
from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright, expect

import logging
import traceback
from rich.console import Console
console = Console()

def logging_setup():
    path = os.path.dirname(sys.argv[0])
    if not os.path.exists(f'{path}/logs'): os.makedirs(f'{path}/logs')
    logging.basicConfig(filename = f'{path}/logs/logs.log', 
                        filemode = 'w', 
                        format = '[%(levelname)s] [%(asctime)s] %(message)s', 
                        level = logging.DEBUG, 
                        encoding = 'UTF-8')
logging_setup()

div_phrases = ".b-word-statistics__column.b-word-statistics__including-phrases"
div_similar = ".b-word-statistics__column.b-word-statistics__phrases-associations"
div_wrapper = ".b-word-statistics__table-wrapper"
info_selector = ".b-word-statistics__info-wrapper .b-word-statistics__info"
table_selector = ".b-word-statistics__table"

COLUMNS = ["Слова", "Показы в месяц"]


