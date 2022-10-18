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
        self.blanks = set()
        self.element = driver.find_element(By.ID, f'{row}_{col}')

    #auto = false means flag only, else auto.
    def set_neighbors(self, size_row, size_col, auto = True):
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
                        if auto == True:
                            self.blanks |= {id}

                        
    def add_neighbor_bomb(self, bomb):
        self.neighbor_bombs |= {bomb}

    def clear_blanks(self, board):
        id = f"{self.row}_{self.col}"
        for neighbor in self.neighbors:
            board.dict[neighbor].blanks.discard(id)

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

    def auto_clear_cells(self, board):
        try:
            if str(self.number).isdigit() == True:
                if int(self.bombs()) == int(self.number):
                    for cell in self.blanks.copy():
                        print("click",cell)
                        initElem = board.find_elements(By.CSS_SELECTOR, "div[class*='open']:not([class*='checked'])")
                        board.dict[cell].click()
                        revealedElem = set(board.find_elements(By.CSS_SELECTOR, "div[class*='open']:not([class*='checked'])")).difference(set(initElem))
                        
                        for i in revealedElem:
                            id = i.get_attribute('id')
                            board.dict[id].set_number()
                            board.dict[id].clear_blanks(board)

                        if board.dict[cell].number == "death":
                            board.completed = "LOSER"
                            return
                        else:
                            board.dict[cell].auto_clear_cells(board)
        except UnexpectedAlertPresentException:
            board.completed = "WIN"
    
    def set_cell(self, row, col):
        self.set_number()
        self.set_neighbors(row, col)
