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
        print(f'add cell: {cell_row}_{cell_col}')
        key = f'{cell_row}_{cell_col}'
        if self.dict.get(key, None) == None:
                self.dict[key] = Cell(cell_row, cell_col, self)
                self.dict[key].set_cell(self.rows, self.cols, self)
        print("add finished")

    def play(self):
            print("PLAY")
            while True:
                print("PLAY WHILE LOOP")
                try:
                    #waits until user flags as a starting point
                    element = WebDriverWait(self,60).until(
                        EC.any_of(EC.presence_of_element_located((By.XPATH, "//div[@class='square bombflagged']")), EC.presence_of_element_located((By.XPATH, "//div[@class='square bombdeath']")))
                    )
                finally:
                    #when checked for flag, change class attribute so we dont repeat checks.
                    elementClass = element.get_attribute('class')
                    if 'death' in elementClass and "checked" not in elementClass:
                        print("BOMBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
                        self.execute_script("arguments[0].setAttribute('class','square bombdeath checked')", element)
                        return
                    else:
                        self.execute_script("arguments[0].setAttribute('class','square bombflagged checked')", element)

                        #gets id of specific cell #_#
                        flaggedID = element.get_attribute('id')
                        flaggedIDSplit = element.get_attribute('id').split("_")
                        print(flaggedID)

                        #sets flagged cell into the board dictionary
                        self.dict[flaggedID] = Cell(flaggedIDSplit[0], flaggedIDSplit[1], self)

                        #goes through all adjacent cells and adds a bomb to each one in the board
                        for row in range(-1,2):
                            for col in range(-1,2):
                                if self.completed != "NOT COMPLETED":
                                    if self.completed == "LOSE":
                                        print("completed BOMB loser")
                                        bomb = self.find_element(By.CLASS_NAME, "bombdeath")
                                        self.execute_script("arguments[0].setAttribute('class','square bombdeath checked')", bomb)
                                    return
                                else:
                                    neighborCellRow = int(flaggedIDSplit[0])+row
                                    neighborCellCol = int(flaggedIDSplit[1])+col
                                    boardKey = f'{neighborCellRow}_{neighborCellCol}'
                                    self.add_cell(neighborCellRow, neighborCellCol)
                                    self.dict[boardKey].add_neighbor_bomb(flaggedID)
                                    self.dict[boardKey].clear_cells(self)
