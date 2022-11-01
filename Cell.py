from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
import constants


class Cell:
    def __init__(self, row, col, driver):
        self.number = "blank"
        self.row = row
        self.col = col
        self.neighbors = set()
        self.bomb = False
        self.blank = True
        self.actions = ActionChains(driver)
        self.element = driver.find_element(By.ID, f'{row}_{col}')

    def set_neighbors(self, size_row, size_col, board):
        for i in range(-1,2):
            neighborRow = int(self.row) + i
            #checks if selected row is within dimension
            if neighborRow <= size_row and neighborRow > 0:
                for j in range(-1,2):
                    #passes current cell so itself is not a neighbor of itself
                    if i == 0 and j == 0:
                        continue
                    neighborCol = int(self.col) + j
                    #checks if selected col is within dimension
                    if neighborCol <= size_col and neighborCol > 0:
                        id = f'{neighborRow}_{neighborCol}'
                        self.neighbors.add(board.dict[id])

    def set_blanks(self):
        return set(filter(lambda neighbor: neighbor.blank, self.neighbors))

                        
    def set_bombs(self):
        return set(filter(lambda neighbor: neighbor.bomb, self.neighbors))

    def click(self):
        self.element.click()
        self.set_number()
        while self.number == "blank":
            self.element.click()
            self.set_number()


    def to_reveal(self):
        return self.neighbors.difference(self.neighbor_bombs)

    def set_number(self):
        self.blank = False
        if self.number == "blank":
            elementClass = self.element.get_attribute('class')
            self.number = constants.CELL_CLASS[elementClass]

    def clear_cells(self, board):
            try:
                if str(self.number).isdigit() == True:
                    if int(self.bombs()) == int(self.number):
                        for cell in self.to_reveal():
                            cellSplit = cell.split("_")
                            board.add_cell(cellSplit[0], cellSplit[1])
                            if board.dict[cell].number == "blank":
                                print("click",cell)
                                board.dict[cell].click()

                                if board.dict[cell].number == "death":
                                    board.completed = "LOSER"
                                    return
                                else:
                                    board.dict[cell].clear_cells(board)
            except UnexpectedAlertPresentException:
                board.completed = "WIN"
            print("CLEARCELL FINISH")

    def auto_clear_cells(self):
        bombs = len(self.set_bombs())
        if bombs == int(self.number) and bombs > 0:
            for cell in self.set_blanks():
                print(f"{cell.row}_{cell.col} click")
                cell.click()

    
    def set_cell(self, row, col, board):
        self.set_number()
        self.set_neighbors(row, col, board)

    def flag(self):
        self.bomb = True
        self.blank = False
        self.actions.context_click(self.element)
        self.actions.perform()

