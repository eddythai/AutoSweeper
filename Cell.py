from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import UnexpectedAlertPresentException
import constants


class Cell:
    def __init__(self, row, col, driver):
        self.number = "blank"
        self.row = row
        self.col = col
        self.neighbors = set()
        self.neighbor_bombs = set()
        self.element = driver.find_element(By.ID, f'{row}_{col}')

    def set_neighbors(self, size_row, size_col, board):
        for i in range(-1,2):
            neighborRow = int(self.row) + i
            #checks if selected row is within dimension
            if neighborRow <= size_row and neighborRow > 0:
                for j in range(-1,2):
                    #passes current cell so itself is not a neighbor of itself
                    if i == 0 and j == 0:
                        pass
                    neighborCol = int(self.col) + j
                    #checks if selected col is within dimension
                    if neighborCol <= size_col and neighborCol > 0:
                        id = f'{neighborRow}_{neighborCol}'
                        self.neighbors |= {id}

                        
    def add_neighbor_bomb(self, bomb):
        self.neighbor_bombs |= {bomb}

    def click(self):
        self.element.click()
        self.set_number()
        while self.number == "blank":
            self.element.click()
            self.set_number()


    def to_reveal(self):
        return self.neighbors.difference(self.neighbor_bombs)

    def set_number(self):
        if self.number == "blank":
            elementClass = self.element.get_attribute('class')
            self.number = constants.CELL_CLASS[elementClass]
                
    def bombs(self) -> int:
        return len(self.neighbor_bombs)

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
    
    def set_cell(self, row, col, board):
        self.set_number()
        self.set_neighbors(row, col, board)
