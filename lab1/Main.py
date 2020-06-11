from Controller import Controller
from Problem import Problem
from UI import UI

filename2 = "sudoku20.txt"
filename3 = "sudoku3.txt"

root = Problem.readfile(filename2)

problem = Problem(root)
ctrl = Controller(problem)
ui = UI(ctrl)
ui.main_menu()




