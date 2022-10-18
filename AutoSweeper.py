from Board import Board
from time import sleep
from FlagPlay import FlagPlay
from AutoPlay import AutoPlay

def main():
    path='C:/SeleniumDrivers/chromedriver.exe'
    board = AutoPlay(16, 30, path)
    board.get("https://minesweeperonline.com/")
    board.play()
    sleep(100)
                

main()

