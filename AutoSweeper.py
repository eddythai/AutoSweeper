from Board import Board
from time import sleep

def main():
    path='C:/SeleniumDrivers/chromedriver.exe'
    board = Board(16, 30, path)
    board.get("https://minesweeperonline.com/")
    board.play()
                

main()

