from Board import Board
from Cell import Cell
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FlagPlay(Board):
    def __init__(self, rows, cols, path):
        super().__init__(rows, cols, path)

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
                                    self.add_cell(neighborCellRow, neighborCellCol)

                                    boardKey = f'{neighborCellRow}_{neighborCellCol}'
                                    self.dict[boardKey].add_neighbor_bomb(flaggedID)
                                    self.dict[boardKey].clear_cells(self)