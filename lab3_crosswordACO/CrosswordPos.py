
class CrosswordPos:
    def __init__(self, nr, x, y, horizontal, length):
        self.nr = nr
        self.x = x
        self.y = y
        if horizontal == 0:
            self.horizontal = True
        else:
            self.horizontal = False
        self.length = length

    def printself(self):
        string = "#" + str(self.nr) + ", coords: (" + str(self.x) + ";" + str(self.y) + "), length: " + str(self.length) + ", orientation: "
        if self.horizontal:
             string += "horizontal"
        else:
            string += "vertical"
        print(string)
