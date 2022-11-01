from Board import Board
from Cell import Cell
from time import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class AutoPlay(Board):
    def __init__(self, rows, cols, path, seed = None):
        super().__init__(rows, cols, path)
        self.start = time()
        self.seed = seed if seed is not None else None 

    def set_seed(self):
        if self.seed != None:
            print("setting seed")
            self.find_element(By.ID, "import-link").click()
            element = WebDriverWait(self,60).until(
                        EC.presence_of_element_located((By.XPATH, "//form[@id='import-form']//textarea"))
            )
            element.send_keys(self.seed)
            self.find_element(By.XPATH, "//input[@value='Load Game']").click()
            print("seed set")

    def initialize_board(self):
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                self.add_cell(i,j)
        for i in range(1, self.rows + 1):
            for j in range(1, self.cols + 1):
                self.set_neighbors(i,j)
        print("INITIALIZATION FINISHED, time taken: "+ str(time() - self.start))

    def play(self):
        self.set_seed()
        print("Initializing Board...")
        self.initialize_board()
        self.dict[f"{int(self.rows/2)}_{int(self.cols/2)}"].element.click()
        while True:
            revealedElem = self.find_elements(By.CSS_SELECTOR, "div[class*='open']:not([class*='checked'])")
            print("WHILE STEP", len(revealedElem))
            if len(revealedElem) == 0:
                break
            print(self.dict[f"{int(self.rows/2)}_{int(self.cols/2)}"].blank)
            if self.dict[f"{int(self.rows/2)}_{int(self.cols/2)}"].blank == True:
                print("HELLO TESTING")
                for i in revealedElem:
                    id = i.get_attribute('id')
                    self.dict[id].set_number()
            self.find_flag(revealedElem)
            self.find_reveal(revealedElem)

    def find_flag(self, revealedElem):
            for i in revealedElem:
                id = i.get_attribute('id')
                self.dict[id].set_number()
                if self.dict[id].number == len(self.dict[id].set_blanks()) + len(self.dict[id].set_bombs()) and self.dict[id].number > 0:
                    for blankCell in self.dict[id].set_blanks():
                        blankCell.flag()
                elemClass = i.get_attribute("class")
                self.execute_script("arguments[0].setAttribute('class','square open0 checked')", i)

    
    def find_reveal(self, revealedElem):
            for i in revealedElem:
                id = i.get_attribute('id')
                self.dict[id].auto_clear_cells()

                        


