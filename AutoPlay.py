from Board import Board
from Cell import Cell
from time import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class AutoPlay(Board):
    def __init__(self, rows, cols, path):
        super().__init__(rows, cols, path)
        self.actions = ActionChains(self)

    def initialize_board(self):
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                self.add_cell(i,j)
        print("INITIALIZATION FINISHED")

    def play(self):
        start = time()
        self.initialize_board()
        print(time() - start)
        middle = self.find_element(By.ID, f"{int(self.rows/2)}_{int(self.cols/2)}")
        middle.click()
        while True:
            revealedElem = self.find_elements(By.CSS_SELECTOR, "div[class*='open']:not([class*='checked'])")
            if len(revealedElem) == 0:
                break
            for i in revealedElem:
                id = i.get_attribute('id')
                self.dict[id].set_number()
                self.dict[id].set_blanks(self.rows, self.cols, self)
                if self.dict[id].number == len(self.dict[id].blanks) + len(self.dict[id].neighbor_bombs):
                    for blankCell in self.dict[id].blanks:
                        print("FLAG", blankCell)
                        self.flag(blankCell)
                if len(self.dict[id].blanks) == 0:
                    elemClass = i.get_attribute("class")
                    self.execute_script("arguments[0].setAttribute('class','" +elemClass+" checked')", i)


    def flag(self, id):
        element = self.dict[id].element
        self.actions.context_click(element)
        self.actions.perform()
        for cell in self.dict[id].neighbors:
            self.dict[cell].add_neighbor_bomb(id)
            self.dict[cell].auto_clear_cells(self)

