import pygame
import math
pygame.init()

running = True
drawing = False

shapes = {"vline":False,
          "hline":False,
          "dline":False,
          "triangle":False,
          "rectangle":False,
          "circle":False}

#storing location values --> tuples in list
mouse_loc = []

#setting the screen size to the user screen size
screen_size = pygame.display.get_desktop_sizes()
screen = pygame.display.set_mode(screen_size[0],pygame.FULLSCREEN )
pygame.display.set_caption("Mouse Draw")


def drawing_line(screen,start_pos,current_pos):
    dx=current_pos[0]-start_pos[0]
    dy=current_pos[1]-start_pos[1]
    #number of circles bw the line , increase if drawing big / more circles needed
    num_circles = 20
    width = 25
    colour = (143,38,14)
    for i in range(num_circles):
        # location of centre of circle to draw circles bw the lines
        x = start_pos[0] + dx *i / num_circles
        y = start_pos[1] + dy *i / num_circles
        pygame.draw.circle(screen,colour,(x,y),width) 

vertical_tolerance = 40
hor_ver_threshold = 15
corner = 0
cor_list = []

def checkcorner():
    global corner
    cor_list.clear()
    corner_threshold = 40
    angle_threshold = 30
    corner = 0
    for i in range(5, len(mouse_loc)-5): #to get the points before and after with step 5
        p1 = mouse_loc[i-5]
        p2 = mouse_loc[i]
        p3 = mouse_loc[i+5]

        vec1 = pygame.math.Vector2(p2[0] - p1[0],p2[1] - p1[1])
        vec2 = pygame.math.Vector2(p3[0] - p2[0],p3[1] - p2[1])
        
        if vec1.length() != 0:
            vec1 = vec1.normalize()
        if vec2.length() != 0:
            vec2 = vec2.normalize()
        dot = vec1.dot(vec2)

        #clamp for some err regarding cos being above 1 or below -1 which shouldnt be possible
        if dot > 1:
            dot = 1
        if dot <-1:
            dot = -1

        #angle b/w the points
        angle = math.degrees(math.acos(dot))
        #if the angle is smaller it isnt a corner
        if angle > angle_threshold:
            cor_list.append((p2,angle))
        
    last_corner= None
    for i in range(0,len(cor_list)):
        current_pos =cor_list[i][0]
        if last_corner is None:
            corner +=1
            last_corner = current_pos
        else:
            dist = math.dist(current_pos,last_corner)
            #detects corner only after the threshold
            if dist>corner_threshold:
                corner += 1
                last_corner = current_pos
    checkcircle()

def checkcircle():
    global shapes
    shapes["circle"] = False
    start = mouse_loc[0]
    end = mouse_loc[-1]
    end_dist = math.dist(start,end)
    #if there are more then 5 corners and the distance b/w the ending of the line and the starting is less 50
    if corner > 5 and end_dist < 50:
        shapes["circle"] = True


def detection():
    global corner,shapes

    #line is too small to detect
    if len(mouse_loc) < 5:
        return
    
    #seperating x and y values in the tuple
    xs = []
    ys = []
    for point in mouse_loc:
        xs.append(point[0])
        ys.append(point[1])

    #total movement
    hor_tot = max(xs) - min(xs)
    ver_tot = max(ys) - min(ys)
     #check if the line is too small
    if hor_tot < 50 and ver_tot < 50:
        print("The line is too small")
        return
    
    checkcorner()

    #reset the screen
    screen.fill((0,0,0))
    if shapes["circle"] == False:
        if corner <= 1:
            if hor_tot > hor_ver_threshold and ver_tot < vertical_tolerance:
                print("Shape: Horizontal Line")
                return "hline"
            elif ver_tot > hor_ver_threshold and hor_tot < vertical_tolerance:
                print("Shape: Vertical Line")
                return "vline"
            else:
                print("Shape: Diagonal Line")
                return "dline"

        if corner == 2:
            print("Shape: Triangle")
            return "triangle"
        elif corner == range(3,6):
            print("Shape: Rectangle")
            return "rectangle"
        elif corner >5:
            print("Shape: Improper Circle")
            return "circle"
    else:
        print("Shape: Proper Circle")
        return "circle"
