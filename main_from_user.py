from plotter import Plotter


class Geometry:
    def __init__(self, name):
        self.__name = name

    def get_name(self):
        return self.__name


class Point(Geometry):
    def __init__(self, name, x, y):
        super().__init__(name)
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y


class Line(Geometry):
    def __init__(self, name, point_1, point_2):
        super().__init__(name)
        self.__point_1 = point_1
        self.__point_2 = point_2

    def get_point_1(self):
        return self.__point_1

    def get_point_2(self):
        return self.__point_2


class Polygon(Geometry):
    def __init__(self, name, points):
        super().__init__(name)
        self.__points = points

    def get_points(self):
        return self.__points

    def lines(self):
        res = []
        points = self.get_points()
        point_a = points[0]
        for point_b in points[1:]:
            res.append(Line(point_a.get_name() + '-' + point_b.get_name(), point_a, point_b))
            point_a = point_b
            # res.append(Line(point_a.get_name() + '-' + points[0].get_name(), point_a, points[0]))
        return res


class RCA:
    def __init__(self, polygen):
        self.polygon = polygen

    def find_category(self, point):
        lines = self.polygon.lines()
        # Store the number of intersections
        intersec_points_num = 0

        for line in lines:
            # Check whether the point is on the line of the polygen
            if self.is_point_on_line(point, line):
                return 'boundary'
            # Check whether the corresponding ray intersect with the line
            if self.is_ray_intersect_line(point, line):
                    intersec_points_num += 1

        return 'inside' if intersec_points_num % 2 == 1 else 'outside'

    @staticmethod
    def is_point_on_line(point, line):
        px = point.get_x()
        py = point.get_y()
        p_1_x = line.get_point_1().get_x()
        p_1_y = line.get_point_1().get_y()
        p_2_x = line.get_point_2().get_x()
        p_2_y = line.get_point_2().get_y()
        if (px - p_1_x) * (p_2_y - p_1_y) == (p_2_x - p_1_x) * (py - p_1_y) and min(p_1_x, p_2_x) <= px <= max(p_1_x,
                                                                                                               p_2_x) \
                and min(p_1_y, p_2_y) <= py <= max(p_1_y, p_2_y) and (p_1_x != p_2_x or p_1_y != p_2_y):
            return True
        else:
            return False

    @staticmethod
    def is_ray_intersect_line(point, line):
        px = point.get_x()
        py = point.get_y()
        p_1_x = line.get_point_1().get_x()
        p_1_y = line.get_point_1().get_y()
        p_2_x = line.get_point_2().get_x()
        p_2_y = line.get_point_2().get_y()
        if p_1_y == p_2_y:
            return False
        if p_1_y > py and p_2_y > py:
            return False
        if p_1_y < py and p_2_y < py:
            return False
        if p_1_y == py and p_2_y > py:
            return False
        if p_2_y == py and p_1_y > py:
            return False
        if p_1_x < px and p_2_y < py:
            return False

        xseg = p_2_x - (p_2_x - p_1_x) * (p_2_y - py) / (p_2_y - p_1_y)
        if xseg < px:
            return False
        return True


class MBR:
    def __init__(self, polygen):
        self.polygen = polygen

    def find_category(self, point):
        points = self.polygen.get_points()
        # Find the points which has minimum or maximum coordinates
        xs = [point.get_x() for point in points]
        ys = [point.get_y() for point in points]
        x_min = min(xs)
        x_max = max(xs)
        y_min = min(ys)
        y_max = max(ys)
        point_x = point.get_x()
        point_y = point.get_y()
        # If the point is in the minimum bounding rectangle, the point is outside of the polygen.
        if point_x > x_max or point_x < x_min or point_y > y_max or point_y < y_min:
            return 'outside'
        else:
            return None


def find_category(polygen, point):
    # First use MBR to check the point, if not work, use the RCA algorithm
    mbr = MBR(polygen)
    mbr_category = mbr.find_category(point)
    if mbr_category is not None:
        return mbr_category
    else:
        rca = RCA(polygen)
        rca_category = rca.find_category(point)
        return rca_category


def main():
    plotter = Plotter()

    print("read polygon.csv")
    # Init polygen_points to store points in the polygen
    polygen_points = []

    # Read polygon.csv
    with open('polygon.csv', 'r') as f:
        for line in f:
            if not line.startswith('id'):
                id = line.split(',')[0].strip()
                x = float(line.split(',')[1].strip())
                y = float(line.split(',')[2].strip())
                # Init a Point object
                point = Point(id, x, y)
                # Add the Point object to the list of points
                polygen_points.append(point)

    # Init a Polygon object
    polygen = Polygon('polygen', polygen_points)

    print("Insert point information")
    '''
        Give user 6 times to input a correct coordinate, if still the program can not get the correct input after 6 
        times, the program will be finished.
    '''
    input_time = 0
    while True:
        if input_time < 5:
            try:
                x = float(input("x coordinate: "))
                y = float(input("y coordinate: "))
                break
            except:
                print(f'The input is not a number！ please try again, you still have {5-input_time} chances left')
        else:
            try:
                x = float(input("x coordinate: "))
                y = float(input("y coordinate: "))
                break
            except:
                print('Can\'t get a correct ordinate, the program will finish!')
                return
        input_time += 1

    print("categorize point")
    test_point = Point('1', x, y)
    category = find_category(polygen, test_point)
    print(category)

    print("plot polygon and point")
    polygen_points = polygen.get_points()
    xs = []
    ys = []
    for polygen_point in polygen_points:
        xs.append(polygen_point.get_x())
        ys.append(polygen_point.get_y())
    plotter.add_polygon(xs, ys)
    plotter.add_point(test_point.get_x(), test_point.get_y(), category)
    plotter.show()


if __name__ == "__main__":
    main()
