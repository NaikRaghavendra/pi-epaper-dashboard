
import Geometry.Point as PT

class Rectangle():
    def __init__(self, tl:PT.Point, br:PT.Point):
        self.tl = tl
        self.br = br

    def offset(self, pt):
        return Rectangle(self.tl + pt, self.br + pt)

    def coords(self):
        return self.tl.coords() + self.br.coords()

    def width(self):
        return (self.br-self.tl).x

    def height(self):
        return (self.br-self.tl).y

    def size(self):
        return self.br - self.tl

    def shrink(self, stl:PT.Point, sbr:PT.Point):
        return Rectangle(self.tl.offset(stl), self.br.offset(PT.Point(-sbr.x, -sbr.y,)))

    def center(self):
        return PT.Point(int(self.tl.x + self.width()/2), int(self.tl.y + self.height()/2))

    def getMinDimension(self):
        return self.width() if self.width() < self.height() else self.height()

    def partition_x(self, factor):
        partitionpoint1 = self.tl + PT.Point(int(self.width()*factor), 0)
        partitionpoint2 = self.tl + PT.Point(int(self.width()*factor), self.height())
        return [Rectangle(self.tl, partitionpoint2), Rectangle(partitionpoint1, self.br)]

    def partition_y(self, factor):
        partitionpoint1 = self.tl + PT.Point(0,int(self.height()*factor))
        partitionpoint2 = self.tl + PT.Point(self.width(), int(self.height()*factor))
        return [Rectangle(self.tl, partitionpoint2), Rectangle(partitionpoint1, self.br)]

    def alignCenter(self, other):
        centeroffset = self.center() - other.center()
        return other.offset(centeroffset)

    def pointinrect(self, pt:PT.Point):
        return self.tl.x <= pt.x and self.br.x >= pt.x and self.tl.y <= pt.y and self.br.y >= pt.y

    def includes(self, other):
        return self.pointinrect(other.tl) and self.pointinrect(other.br)


if __name__ == "__main__":
    pt = Rectangle(PT.Point(0,0), PT.Point(200,100))
    print(f"Width : {pt.width()}")

    
