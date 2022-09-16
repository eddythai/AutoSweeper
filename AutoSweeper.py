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

def main():
    board = collections.defaultdict(Cell)
    s = Service('C:/SeleniumDrivers/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    driver.get("https://minesweeperonline.com/")

    while True:
        try:
            flaggedElement = WebDriverWait(driver,60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='square bombflagged']"))
            )
        finally:
            driver.execute_script("arguments[0].setAttribute('class','square bombflagged checked')", flaggedElement)
            flaggedID = flaggedElement.get_attribute('id').split("_")
            board[flaggedElement.get_attribute('id')] = Cell(0,-1)
            for row in range(-1,2):
                for col in range(-1,2):
                    checkString = str(int(flaggedID[0])+row)+"_"+str(int(flaggedID[1])+col)
                    checkElement = driver.find_element(By.ID, checkString)
                    if board.get(checkElement.get_attribute('id'), None) == None:
                        board[checkElement.get_attribute('id')] = Cell(1,-2)
                    else:
                        board.get(checkElement.get_attribute('id')).bombs += 1

                    elemAttribute = checkElement.get_attribute('class').split()
                    if "open" in elemAttribute[1]:
                        board.get(checkElement.get_attribute('id')).number = elemAttribute[1][-1]
            for key,value in board.items():
                print(key, value.bombs, value.number)

# def clearSquares(checkElement,driver):
#     elemAttribute = checkElement.get_attribute('class').split()
#     if "open" in elemAttribute[1]:
#         board.get(checkElement.get_attribute('id')).number = elemAttribute[1][-1]
#         checkID = checkElement.get_attribute('id').split("_")

#         bombs = 0
#         for row2 in range(-1,2):
#             for col2 in range(-1,2):
#                 clearString = str(int(checkID[0])+row2)+"_"+str(int(checkID[1])+col2)
#                 clearElement = driver.find_element(By.ID, clearString)
#                 if "bombflagged" in clearElement.get_attribute('class'):
#                     bombs+=1

#         if int(elemAttribute[1][-1]) == bombs:
#             for row2 in range(-1,2):
#                 for col2 in range(-1,2):
#                     clearString = str(int(checkID[0])+row2)+"_"+str(int(checkID[1])+col2)
#                     clearElement = driver.find_element(By.ID, clearString)
#                     if clearElement.get_attribute('class') == "square blank":
#                         clearElement.click()

main()

