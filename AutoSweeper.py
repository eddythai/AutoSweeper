from turtle import clear
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import collections

class Cell:
    def __init__(self,bombs,number):
        self.bombs = bombs
        #-2 = unchecked
        #-1 = flagged
        # 0 >= square number
        self.number = number

board = collections.defaultdict(Cell) #holds data of cells (bombs and number) in the board

def main():
    s = Service('C:/SeleniumDrivers/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.get("https://minesweeperonline.com/")

    while True:
        try:
            #waits until user flags as a starting point
            flaggedElement = WebDriverWait(driver,60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='square bombflagged']"))
            )
        finally:
            #when checked for flag, change class attribute so we dont repeat checks.
            driver.execute_script("arguments[0].setAttribute('class','square bombflagged checked')", flaggedElement)

            #gets id of specific cell #_#
            flaggedID = flaggedElement.get_attribute('id').split("_")

            #sets flagged cell into the board dictionary
            board[flaggedElement.get_attribute('id')] = Cell(0,-1)

            #goes through all adjacent cells and adds a bomb to each one in the board
            for row in range(-1,2):
                for col in range(-1,2):
                    checkString = str(int(flaggedID[0])+row)+"_"+str(int(flaggedID[1])+col)
                    checkElement = driver.find_element(By.ID, checkString)
                    if board.get(checkElement.get_attribute('id'), None) == None:
                        board[checkElement.get_attribute('id')] = Cell(1,-2)
                    else:
                        board.get(checkElement.get_attribute('id')).bombs += 1
                        #if bomb is equal to square number, then clear all the squares adjacent to that
                        if int(board.get(checkElement.get_attribute('id')).bombs) == int(board.get(checkElement.get_attribute('id')).number):
                            clearSquares(checkElement,driver)

                    elemAttribute = checkElement.get_attribute('class').split()
                    if "open" in elemAttribute[1]:
                        board.get(checkElement.get_attribute('id')).number = elemAttribute[1][-1]
                        if int(board.get(checkElement.get_attribute('id')).bombs) == int(board.get(checkElement.get_attribute('id')).number):
                            print("equals")
                            clearSquares(checkElement,driver)
            for key,value in board.items():
                print(key, value.bombs, value.number)

def clearSquares(checkElement,driver):
    checkID = checkElement.get_attribute('id').split("_")
    for row2 in range(-1,2):
        for col2 in range(-1,2):
            boardKey = str(int(checkID[0])+row2)+"_"+str(int(checkID[1])+col2)
            if board.get(boardKey,None) == None:
                keyElement = driver.find_element(By.ID, boardKey)
                keyAttribute = keyElement.get_attribute('class').split()
                if "open" in keyAttribute[1]:
                    board[boardKey] = Cell(0,keyAttribute[1][-1])
                elif "flag" in keyAttribute[1]:
                    driver.execute_script("arguments[0].setAttribute('class','square bombflagged checked')", keyElement)
                    board[boardKey] = Cell(0,-1)
                else:
                    board[boardKey] = Cell(0,-2)
                    
            if board.get(boardKey).number == -2:
                clearElement = driver.find_element(By.ID, boardKey)
                clearElement.click()

                clearID = clearElement.get_attribute('id')
                board.get(clearID).number = clearElement.get_attribute('class').split()[1][-1]
                if int(board.get(clearID).bombs) == int(board.get(clearID).number):
                    clearSquares(checkElement,driver)

                

main()

