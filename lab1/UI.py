import time


class UI:

    def __init__(self, ctrl):
        self.__ctrl = ctrl


    @staticmethod
    def print_menu():
        print("1 - uninformed search (BFS)")
        print("2 - informed search (GBFS)")
        print("0 - exit")


    def main_menu(self):
        while(True):
            self.print_menu()
            cmd = input("choose: ")

            if cmd == "0":
                print("bye then..")
                break
            elif cmd == "1":
                self.ui_search("uninformed")
            elif cmd == "2":
                self.ui_search("informed")
            else:
                print("invalid command")


    def ui_search(self, type):
        try:
            start_time = time.time()

            if type == "uninformed":
                solved = self.__ctrl.BreadthFirstSearch()
            else:
                solved = self.__ctrl.BestFirstSearch()

            print("--- %s seconds ---" % (time.time() - start_time))
            print(str(solved))

        except ValueError as ve:
            print(ve)