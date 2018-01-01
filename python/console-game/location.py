class _Location:
    def __init__(self, level, *loc):
        self.level = level
        self.loc = loc

    def __repr__(self):
        return self.level + ": " + repr(self.loc)


class Sector(_Location):
    def __init__(self, n):
        self.n = n % 16
        super().__init__('Sector', n)

    @staticmethod
    def from_string(string):
        return Sector(int(string) - 1)

    def __repr__(self):
        return str(self.n + 1)


class Major(_Location):
    def __init__(self, x, y):
        super().__init__('Major', x, y)
        self.x = x % 4
        self.y = y % 4

    @staticmethod
    def from_string(string):
        x = int(string[0]) - 1
        y = ord(string[1]) - ord('a')
        return Major(x, y)

    def __repr__(self):
        return str(self.x + 1) + chr(ord('a') + self.y)


class Minor(_Location):
    def __init__(self, x, y):
        super().__init__('Minor', x, y)
        self.x = x % 4
        self.y = y % 4

    @staticmethod
    def from_string(string):
        x = int(string[0]) - 1
        y = ord(string[1]) - ord('e')
        return Minor(x, y)

    def __repr__(self):
        return str(self.x + 1) + chr(ord('e') + self.y)


class Point(_Location):
    def __init__(self, x, y):
        super().__init__('Point', x, y)
        self.x = x % 3
        self.y = y % 3

    @staticmethod
    def from_string(string):
        x = int(string[0]) - 1
        y = ord(string[1]) - ord('x')
        return Point(x, y)

    def __repr__(self):
        return str(self.x + 1) + chr(ord('x') + self.y)


class Location:
    # YOU WERE DOING THISS LOOK AT ITTT
    def distance(self, other):
        passSAD,MGKLASD

    @staticmethod
    def from_string(string):
        data = string.split(', ')
        s = Sector.from_string(data[0])
        M = Major.from_string(data[1])
        m = Minor.from_string(data[2])
        p = Point.from_string(data[3])
        return Location(s, M, m, p)

    def __init__(self, s, M, m, p):
        self.s = s
        self.M = M
        self.m = m
        self.p = p

    def __repr__(self):
        s = repr(self.s)
        M = repr(self.M)
        m = repr(self.m)
        p = repr(self.p)
        return ', '.join([s, M, m, p])
