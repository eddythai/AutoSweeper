import collections
from Cell import Cell
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Board(webdriver.Chrome):
    def __init__(self, rows, cols, path):
        self.start_t = time.time()
        super().__init__(path)
        self.dict = collections.defaultdict()
        self.rows = rows
        self.cols = cols
        self.completed = "NOT COMPLETED"
    
    def board_clear(self):
        self.dict.clear()
        self.completed = "NOT COMPLETED"

    def add_cell(self, cell_row, cell_col):
        key = f'{cell_row}_{cell_col}'
        if self.dict.get(key, None) == None:
                self.dict[key] = Cell(cell_row, cell_col, self)

    def set_neighbors(self, cell_row, cell_col):
        key = f'{cell_row}_{cell_col}'
        self.dict[key].set_neighbors(self.rows, self.cols, self)