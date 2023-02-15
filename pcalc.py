import math
import numpy as np
import pandas as pd


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    @classmethod
    def create(cls, ax, ay, az):
        cls.x = int(ax)
        cls.y = ay
        cls.z = az
        return cls(cls.x, cls.y, cls.z)  
    
    def __str__(self):
        return f"X  = {self.x} y = {self.y} and z = {self.z}"

class Cabinet:
    def __init__(self, x, y, width, height, type_cab, side):
        if not width:
            raise ValueError("Empty Field!")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type_cab = type_cab
        self.side = side
    
    def __str__(self):
        return f"A cabinet, W = {self.width} and H = {self.height} mm, type {self.type_cab}, bottom corner = {self.bottom_corner()['x']}"
    
    def top_corner(self):
        top_corn = {"x": 0, "y": 0}
        top_corn["x"] = self.x + self.width
        top_corn["y"] = self.y + self.height
        return top_corn

    def bottom_corner(self):
        bot_corn = {"x": 0, "y": 0}
        bot_corn["x"] = self.x + self.width
        bot_corn["y"] = self.y
        return bot_corn       

    @classmethod
    def create(cls, i, wall_offset, door_thickness, plinth, height, cabinets, kitch_height, side):
        if i > 0:
            cls.x = cabinets[i - 1].bottom_corner()["x"]
        else:
            cls.x = wall_offset + 520 + door_thickness * 2
        
        cls.y = plinth
        cls.width = get_int("Cabinet width, mm: ")
        cls.type_cab = input("Type of cabinet[1,2,3,4,5,6 or 7]: ")
        if cls.type_cab == "1" or cls.type_cab == "2" or cls.type_cab == "3" or cls.type_cab == "7":
            cls.height = height
        else:
            cls.height = kitch_height - plinth
        cls.side = side

        return cls(cls.x, cls.y, cls.width, cls.height, cls.type_cab, cls.side)

    @classmethod
    def create_r_from_file(cls, i, wall_offset, door_thickness, plinth, height, cabinets, kitch_height, width, type, side):
        if i > 0:
            cls.x = cabinets[i - 1].bottom_corner()["x"]
        else:
            cls.x = wall_offset + 520 + door_thickness * 2
        
        cls.y = plinth
        cls.width = width
        cls.type_cab = type
        if cls.type_cab == "1" or cls.type_cab == "2" or cls.type_cab == "3" or cls.type_cab == "7":
            cls.height = height
        else:
            cls.height = kitch_height - plinth
        cls.side = side

        return cls(cls.x, cls.y, cls.width, cls.height, cls.type_cab, cls.side)

    @classmethod
    def create_l_from_file(cls, i, wall_offset, door_thickness, plinth, height, cabinets, kitch_height, width, type, side):
        cls.width = width
        if i > 0:
            cls.x = cabinets[i - 1].x - cls.width
        else:
            cls.x = 0 - wall_offset - 520 - door_thickness * 2 - cls.width
        cls.y = plinth
        cls.type_cab = type
        if cls.type_cab == "1" or cls.type_cab == "2" or cls.type_cab == "3" or cls.type_cab == "7":
            cls.height = height
        else:
            cls.height = kitch_height - plinth
        cls.side = side

        return cls(cls.x, cls.y, cls.width, cls.height, cls.type_cab, cls.side) 

    @classmethod
    def create_left(cls, i, wall_offset, door_thickness, plinth, height, cabinets, kitch_height, side):
        cls.width = get_int("Cabinet width, mm: ")
        if i > 0:
            cls.x = cabinets[i - 1].x - cls.width
        else:
            cls.x = 0 - wall_offset - 520 - door_thickness * 2 - cls.width
        cls.y = plinth
        cls.type_cab = input("Type of cabinet[1,2,3,4,5,6 or 7]: ")
        if cls.type_cab == "1" or cls.type_cab == "2" or cls.type_cab == "3" or cls.type_cab == "7":
            cls.height = height
        else:
            cls.height = kitch_height - plinth
        cls.side = side

        return cls(cls.x, cls.y, cls.width, cls.height, cls.type_cab, cls.side)

    @classmethod
    def create_top(cls, i, top_width, door_thickness, height, cabinets, kitch_height, r_length, door_w, door_qtn):
        cls.width = door_w
        if i > 0:
            cls.x = cabinets[i - 1].x + cls.width
        else:
            cls.x = top_width + door_thickness * 2 + r_length - door_qtn * door_w
        cls.y = height + 580
        cls.type_cab = "1"
        cls.height = kitch_height - cls.y
        cls.side = 'r'

        return cls(cls.x, cls.y, cls.width, cls.height, cls.type_cab, cls.side)

    @classmethod
    def create_top_left(cls, i, top_width, door_thickness, height, cabinets, kitch_height, l_length, door_w, door_qtn):
        cls.width = door_w
        if i > 0:
            cls.x = cabinets[i - 1].x - cls.width
        else:
            cls.x = 0 - top_width - door_thickness * 2 - (l_length - (door_qtn - 1) * door_w)
        cls.y = height + 580
        cls.type_cab = "1"
        cls.height = kitch_height - cls.y
        cls.side = 'l'

        return cls(cls.x, cls.y, cls.width, cls.height, cls.type_cab, cls.side)


def main():
    offset_3d = 5000
    # take start params from txt file
    with open("data.txt", "r") as file:
        lines = file.readlines()
    # each needed number - second word in the string, after '=' sign
    height_top = int(lines[0].strip().rstrip().split('=')[1])
    gapBetweenBox = int(lines[1].strip().rstrip().split('=')[1])
    gola_min = int(lines[2].strip().rstrip().split('=')[1])
    kitch_height = int(lines[3].strip().rstrip().split('=')[1])
    wall_offset = int(lines[4].strip().rstrip().split('=')[1])
    top_width = int(lines[5].strip().rstrip().split('=')[1])
    tabletop  = int(lines[6].strip().rstrip().split('=')[1])
    plinth = int(lines[7].strip().rstrip().split('=')[1])
    door_thickness = int(lines[8].strip().rstrip().split('=')[1])
    cabinet_depth = int(lines[9].strip().rstrip().split('=')[1])

    cabinet_height = height_top - tabletop - plinth

    # cab height must be even number, if not - add 1 mm
    if cabinet_height % 2 != 0:
        print(f"Cabinet height is {cabinet_height}, it must be even, so will be increase in 1 mm")
        cabinet_height += 1
        height_top +=1
    
    gola_height = gola_finder(gola_min, gapBetweenBox, cabinet_height)
    big_drawer = (cabinet_height - gola_height * 2) / 2
    narrow_drawer = (big_drawer - gapBetweenBox) / 2
    print(f"Gola............{gola_height} mm")
    print(f"Big drawer......{big_drawer} mm")
    print(f"Narrow drawer...{narrow_drawer} mm")
    print(f"Solid door......{cabinet_height - gola_height} mm")
    print(f"Cabinet height..{cabinet_height} mm")


    coords = [
        [wall_offset, plinth, wall_offset + 520, cabinet_height + plinth],
        [0, height_top - tabletop, 600, height_top],
        #[600, height_top, 1600, height_top - tabletop],
        [wall_offset + 520, plinth, wall_offset + 520 + door_thickness, plinth + cabinet_height - gola_height],
        [wall_offset + 520 + door_thickness, plinth, wall_offset + 520 + door_thickness * 2, plinth + cabinet_height - gola_height],
        [0, height_top + 580, top_width - 20, height_top + 580 + 18],
        [16, height_top + 580 + 18, top_width, kitch_height],
        [top_width, kitch_height, top_width + door_thickness, height_top + 580],
        [top_width + door_thickness, kitch_height, top_width + door_thickness * 2, height_top + 580]
        ]

    initial_draw(coords)

    crosshairs_draw(coords[0])
    crosshairs_draw(coords[5])

    cabinets = []
    cabinets_right = []
    cabinets_left = []
    if input("Create cabinets from file, y/n? ") == 'y':
        data = pd.read_excel('param.xlsx')
        i = 0
        for row in data.iterrows():
            width = row[1]['width']
            type_ = str(row[1]['type'])
            index = int(row[0])
            print(f"index = {index}, side = {row[1]['side']}")

            if row[1]['side'] == 'r':                
                cabinets_right.append(Cabinet.create_r_from_file(index, wall_offset, door_thickness, plinth, cabinet_height, cabinets_right, kitch_height, width, type_, row[1]['side']))
                print("Branch R works")
            else:
                cabinets_left.append(Cabinet.create_l_from_file(i, wall_offset, door_thickness, plinth, cabinet_height, cabinets_left, kitch_height, width, type_, row[1]['side']))
                i += 1
            print(f"row = {row[1]['width'], row[1]['type']}")

        for obj in cabinets_right:
            print(obj)
            x1 = obj.top_corner()["x"]
            y1 = obj.top_corner()["y"]
            #x2 = obj.x
            y2 = - wall_offset - cabinet_depth
            #x3 = x1
            y3 = - wall_offset
            cabinet_draw(obj.x, obj.y, x1, y1)
            cabinet_draw(obj.x, y2, x1, y3)
            cabinet_draw(obj.x + gapBetweenBox / 2, y2, x1 - gapBetweenBox / 2, y2 - door_thickness)
            ls = create_fasad_list(obj, gapBetweenBox, gola_height, big_drawer, narrow_drawer)
            for row in ls:
                draw_rectangle(row)
        
        for obj in cabinets_left:
            x1 = obj.top_corner()["x"]
            y1 = obj.top_corner()["y"]
            x2 = wall_offset + cabinet_depth
            y2 = obj.x
            x3 = wall_offset
            y3 = x1
            cabinet_draw(obj.x, obj.y, x1, y1)
            cabinet_draw(x2, obj.x, x3, x1)
            cabinet_draw(x2, obj.x + gapBetweenBox / 2, x2 + door_thickness, x1 - gapBetweenBox / 2)
            ls = create_fasad_list(obj, gapBetweenBox, gola_height, big_drawer, narrow_drawer)
            for row in ls:
                draw_rectangle(row)
        
        #draw the left tabletop
        cabinet_draw(-600, height_top - tabletop, left_tabletop(cabinets_left), height_top)
        cabinet_draw(0, 0, 600, left_tabletop(cabinets_left))

        #draw the right tabletop
        print(right_tabletop(cabinets_right))
        cabinet_draw(600, height_top - tabletop, right_tabletop(cabinets_right), height_top)
        cabinet_draw(600, 0, right_tabletop(cabinets_right), -600)


    else:
        i = 0
        if input("Create right side, y/n? ") == 'y':
            side = 'r'
            cabinets.append(Cabinet.create(i, wall_offset, door_thickness, plinth, cabinet_height, cabinets, kitch_height, side))
            while input("Create one more bottom cabinet, y/n? ") == "y":
                i += 1
                cabinets.append(Cabinet.create(i, wall_offset, door_thickness, plinth, cabinet_height, cabinets, kitch_height, side))
        positiv_cab = i
        for obj in cabinets:
            x1 = obj.top_corner()["x"]
            y1 = obj.top_corner()["y"]
            #x2 = obj.x
            y2 = - wall_offset - cabinet_depth
            #x3 = x1
            y3 = - wall_offset
            cabinet_draw(obj.x, obj.y, x1, y1)
            cabinet_draw(obj.x, y2, x1, y3)
            cabinet_draw(obj.x + gapBetweenBox / 2, y2, x1 - gapBetweenBox / 2, y2 - door_thickness)
            ls = create_fasad_list(obj, gapBetweenBox, gola_height, big_drawer, narrow_drawer)
            for row in ls:
                draw_rectangle(row)
        
        points = []
        for obj in cabinets:
            x = wall_offset + cabinet_depth
            y = obj.x
            z = plinth
            points.append(Point.create(x, y, z))
            x = wall_offset
            points.append(Point.create(x, y, z))
            z = obj.top_corner()["y"]
            points.append(Point.create(x, y, z))
            x = wall_offset + cabinet_depth
            points.append(Point.create(x, y, z))
            y = y + obj.width
            z = plinth
            points.append(Point.create(x, y, z))
            x = wall_offset
            points.append(Point.create(x, y, z))
            z = obj.top_corner()["y"]
            points.append(Point.create(x, y, z))
            x = wall_offset + cabinet_depth
            points.append(Point.create(x, y, z))
            x = y = z =0

        turn_x = math.radians(-65)
        turn_y = math.radians(0)
        turn_z = -135 * 3.14159 / 180
        sin_x = math.sin(turn_x)
        cos_x = math.cos(turn_x)
        sin_y = math.sin(turn_y)
        cos_y = math.cos(turn_y)
        sin_z = math.sin(turn_z)
        cos_z = math.cos(turn_z)
        turn_matrix = np.array([[cos_y * cos_z, -1 * sin_z * cos_y, sin_y],
        [sin_x * sin_y * cos_z + sin_z * cos_x, -1 * sin_x * sin_y * sin_z + cos_x * cos_z, -1 * sin_x * cos_y],
        [sin_x * sin_z - sin_y * cos_x * cos_z, sin_x * cos_z + sin_y * sin_z * cos_x, cos_x * cos_y]])
        turned_points = []
        for ptn in points:
            vector = np.array([ptn.x, ptn.y, ptn.z])
            res_vector = turn_matrix.dot(vector)
            ptn.x = res_vector[0]
            ptn.y = res_vector[1] 
            ptn.z = res_vector[2]
            #draw_point(ptn)
        matrix = []
        #for i in range(8):
        #    matrix.append(points[i]) 
        
        #for j in range(0, int(len(points) / 8)):
        #    for i in range(j * 8, j * 8 + 8):
        #        matrix[i - j * 8] = points[i] 
            #draw_cab_3d(matrix)

        #print(points[3])


        if input("Create left side, y/n? ") == 'y':
            i += 1
            side = 'l'
            cabinets.append(Cabinet.create_left(0, wall_offset, door_thickness, plinth, cabinet_height, cabinets, kitch_height, side))
            while input("Create one more bottom cabinet, y/n? ") == "y":
                i += 1
                cabinets.append(Cabinet.create_left(i, wall_offset, door_thickness, plinth, cabinet_height, cabinets, kitch_height, side))
        
        for i in range(positiv_cab + 1, len(cabinets)):
            x1 = cabinets[i].top_corner()["x"]
            y1 = cabinets[i].top_corner()["y"]
            x2 = wall_offset + cabinet_depth
            y2 = cabinets[i].x
            x3 = wall_offset
            y3 = x1
            cabinet_draw(cabinets[i].x, cabinets[i].y, x1, y1)
            cabinet_draw(x2, cabinets[i].x, x3, x1)
            cabinet_draw(x2, cabinets[i].x + gapBetweenBox / 2, x2 + door_thickness, x1 - gapBetweenBox / 2)
            ls = create_fasad_list(cabinets[i], gapBetweenBox, gola_height, big_drawer, narrow_drawer)
            for row in ls:
                draw_rectangle(row)

            print(cabinets[i]) 

        #draw the left tabletop
        cabinet_draw(-600, height_top - tabletop, left_tabletop(cabinets), height_top)
        cabinet_draw(0, 0, 600, left_tabletop(cabinets))

        #draw the right tabletop
        print(right_tabletop(cabinets, positiv_cab))
        cabinet_draw(600, height_top - tabletop, right_tabletop(cabinets, positiv_cab), height_top)
        cabinet_draw(600, 0, right_tabletop(cabinets, positiv_cab), -600)

    #draw corner fasad elements
    cabinet_draw(wall_offset + cabinet_depth + door_thickness * 2, -wall_offset - cabinet_depth - door_thickness, wall_offset + cabinet_depth + door_thickness, -wall_offset - cabinet_depth + 180)
    cabinet_draw(wall_offset + cabinet_depth + door_thickness, -wall_offset - cabinet_depth - door_thickness * 2 + gapBetweenBox / 2, wall_offset + cabinet_depth, -wall_offset - cabinet_depth + 180)

    top_cabinets = []
    if input("Create top right side, y/n? ") == 'y':
        top_x1 = top_width + door_thickness * 2
        top_x2 = right_tabletop(cabinets_right)
        length_top = top_x2 - top_x1
        w = get_int(f"Wide of door (L/4 = {length_top / 4}, L/5 = {length_top / 5}, L/3 = {length_top/3}): ")
        qtn = math.floor(length_top / w)
        for i in range(0, qtn):
            top_cab = Cabinet.create_top(i, top_width, door_thickness, height_top, top_cabinets, kitch_height, length_top, w, qtn)
            top_cabinets.append(top_cab)
    
    for obj in top_cabinets:
        x1 = obj.top_corner()["x"]
        y1 = obj.top_corner()["y"]
        cabinet_draw(obj.x, obj.y, x1, y1)

    topleft_cabinets = []
    if input("Create top left side, y/n? ") == 'y':
        top_x1 = 0 - top_width - door_thickness * 2
        top_x2 = left_tabletop(cabinets_left)
        length_top = top_x1 - top_x2
        w = get_int(f"Wide of door (L/4 = {length_top / 4}, L/5 = {length_top / 5}, L/3 = {length_top/3}): ")
        qtn = math.floor(length_top / w)
        for i in range(0, qtn):
            top_cab = Cabinet.create_top_left(i, top_width, door_thickness, height_top, topleft_cabinets, kitch_height, length_top, w, qtn)
            topleft_cabinets.append(top_cab)

    for obj in topleft_cabinets:
        x1 = obj.top_corner()["x"]
        y1 = obj.top_corner()["y"]
        cabinet_draw(obj.x, obj.y, x1, y1)
    
        

def draw_point(point):
    with open("export.txt", "a") as file:
      file.write(f"_point\n{point.x},{point.y}\n")  

def draw_cab_3d(points):
    with open("export.txt", "a") as file:
      file.write(f"_line\n{points[0].x},{points[0].y}\n{points[3].x},{points[3].y}\n\n")
      file.write(f"_line\n{points[0].x},{points[0].y}\n{points[4].x},{points[4].y}\n\n")
      file.write(f"_line\n{points[3].x},{points[3].y}\n{points[2].x},{points[2].y}\n\n")
      file.write(f"_line\n{points[3].x},{points[3].y}\n{points[7].x},{points[7].y}\n\n")
      file.write(f"_line\n{points[2].x},{points[2].y}\n{points[6].x},{points[6].y}\n\n")
      file.write(f"_line\n{points[7].x},{points[7].y}\n{points[6].x},{points[6].y}\n\n")
      file.write(f"_line\n{points[4].x},{points[4].y}\n{points[7].x},{points[7].y}\n\n")
      file.write(f"_line\n{points[4].x},{points[4].y}\n{points[5].x},{points[5].y}\n\n")
      file.write(f"_line\n{points[5].x},{points[5].y}\n{points[6].x},{points[6].y}\n\n")



def left_tabletop(cabinets):
    tall = True
    i = len(cabinets) - 1
    while tall:
        cab = cabinets[i]
        if cab.type_cab == "4" or cab.type_cab == "5" or cab.type_cab == "6":
            x = cab.top_corner()["x"]
            i -= 1
        else:
            x = cab.x
            tall = False
    return x

def right_tabletop(cabinets):
    tall = True
    i = len(cabinets) - 1
    while tall:
        cab = cabinets[i]
        if cab.type_cab == "4" or cab.type_cab == "5" or cab.type_cab == "6":
            x = cab.x
            i -= 1
        else:
            x = cab.top_corner()["x"]
            tall = False
    return x

def create_right_bottom(i, cabinets, wall_offset, door_thickness, plinth, cabinet_height, kitch_height):
    cabinets.append(Cabinet.create(i, wall_offset, door_thickness, plinth, cabinet_height, cabinets, kitch_height))

#try to find golaHeight
def gola_finder(gola_height, gap, height_box):
    big_draw_height = (height_box - gola_height * 2) / 2
    while (big_draw_height - gap) % 2 != 0:
        gola_height += 1
        if gola_height > 40:
            print("Cannot find solution, try change height")
            break
        big_draw_height = (height_box - gola_height * 2) / 2
    return gola_height

def initial_draw(c):
    clear_export()
    for line in c:
        draw_rectangle(line)
        draw_negative(line)

def crosshairs_draw(c):
    with open("export.txt", "a") as file:
        file.write(f"clayer hidden\n")

        file.write(f"_line\n{c[0]},{c[1]}\n{c[2]},{c[3]}\n\n")
        file.write(f"_line\n{c[0]},{c[3]}\n{c[2]},{c[1]}\n\n")

        file.write(f"_line\n{c[0] * (- 1)},{c[1]}\n{c[2] * (- 1)},{c[3]}\n\n")
        file.write(f"_line\n{c[0] * (- 1)},{c[3]}\n{c[2] * (- 1)},{c[1]}\n\n")

        file.write(f"clayer 0\n")

def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            pass

def clear_export():
    with open("export.txt", "w") as file:
        file.write(f"clayer 0\n")
        file.write(f"_point\n0,0\n")

def draw_rectangle(c):
    with open("export.txt", "a") as file:
        if c[1] == "0":
            return
        file.write(f"_rectangle\n{c[0]},{c[1]}\n{c[2]},{c[3]}\n")

def draw_negative(c):
    with open("export.txt", "a") as file:
        file.write(f"_rectangle\n{c[0] * (-1)},{c[1]}\n{c[2] * (-1)},{c[3]}\n")

def cabinet_draw(x, y, x1, y1):
    with open("export.txt", "a") as file:
         file.write(f"_rectangle\n{x},{y}\n{x1},{y1}\n")

def create_fasad_list(cab: Cabinet, gap, gola, big_dr, small_dr):
    fasad_coords = [["x", "y", "x1", "y1"],
    ["x", "y", "x1", "y1"],
    ["x", "y", "x1", "y1"],
    ["x", "y", "x1", "y1"]
    ]

    if cab.type_cab =="1":       
        x = str(cab.x + gap / 2) 
        y = str(cab.y)
        x1 = str(cab.top_corner()["x"] - gap / 2)
        y1 = str(cab.top_corner()["y"] - gola)
        fasad_coords = [[x, y, x1, y1],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"]]

    elif cab.type_cab == "2":
        x = x2 = cab.x + gap / 2 
        y = cab.y
        x1 = x21 = cab.top_corner()["x"] - gap / 2
        y1 = cab.bottom_corner()["y"] + big_dr
        y2 = y1 + gola
        y21 = y2 + big_dr
        fasad_coords = [[str(x), str(y), str(x1), str(y1)],
        [str(x2), str(y2), str(x21), str(y21)],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"]]
    elif cab.type_cab == "3":
        x = cab.x + gap / 2 
        y = cab.y
        x1 = cab.top_corner()["x"] - gap / 2
        y1 = cab.bottom_corner()["y"] + big_dr
        x2 = x
        y2 = y1 + gola
        x21 = x1
        y21 = y2 + small_dr
        x3 = x
        y3 = y21 + gap
        x31 = x1
        y31 = y3 + small_dr
        fasad_coords = [[str(x), str(y), str(x1), str(y1)],
        [str(x2), str(y2), str(x21), str(y21)],
        [str(x3), str(y3), str(x31), str(y31)],
        ["0", "0", "0", "0"]]
    elif cab.type_cab == "4":
        x = cab.x + gap / 2 
        y = cab.y
        x1 = cab.top_corner()["x"] - gap / 2
        y1 = cab.bottom_corner()["y"] + big_dr
        x2 = x
        y2 = y1 + gola
        x21 = x1
        y21 = y2 + 600
        x3 = x
        y3 = y21 + gap
        x31 = x1
        y31 = y3 + 380
        x4 = x
        y4 = y31 + gap
        x41 = x1
        y41 = cab.height + cab.y
        fasad_coords = [[str(x), str(y), str(x1), str(y1)],
        [str(x2), str(y2), str(x21), str(y21)],
        [str(x3), str(y3), str(x31), str(y31)],
        [str(x4), str(y4), str(x41), str(y41)]]
    elif cab.type_cab == "5":
        x = cab.x + gap / 2 
        y = cab.y
        x1 = cab.top_corner()["x"] - gap / 2
        y1 = cab.bottom_corner()["y"] + 770
        x2 = x
        y2 = y1 + gap
        x21 = x1
        y21 = cab.top_corner()["y"] - 400
        x3 = x
        y3 = y21 + gap
        x31 = x1
        y31 = cab.top_corner()["y"]
        fasad_coords = [[str(x), str(y), str(x1), str(y1)],
        [str(x2), str(y2), str(x21), str(y21)],
        [str(x3), str(y3), str(x31), str(y31)],
        ["0", "0", "0", "0"]]
    elif cab.type_cab =="6":
        fasad_coords = [["0", "0", "0", "0"],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"]]
    elif cab.type_cab == "7":
        x = x2 = cab.x + gap / 2 
        y = cab.y
        x1 = x21 = cab.top_corner()["x"] - gap / 2
        y1 = cab.top_corner()["y"] - 600 - gola - 10
        y2 = y1 + 10
        y21 = y2 + 600
        fasad_coords = [[str(x), str(y), str(x1), str(y1)],
        [str(x2), str(y2), str(x21), str(y21)],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"]]

    return fasad_coords  


if __name__ == "__main__":
    main()
