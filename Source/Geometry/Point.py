class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point((self.x + o.x), (self.y + o.y)) 

    def __sub__(self, o):
        return Point((self.x - o.x), (self.y - o.y))

    def __NEG__(self, o):
        return Point(-self.x, -self.y)

    def offset(self, pt):
        return self + pt

    def coords(self):
        return (self.x,self.y)


if __name__ == "__main__":
    pt = Point(0,0)

    print(f"Point : {pt}")