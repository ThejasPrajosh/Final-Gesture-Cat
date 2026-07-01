import pygame
import mouse_d as ms
import math

pygame.init()
running = True
attack = None

#getting available screen size, choosing default size
screen_size = pygame.display.get_desktop_sizes()

#screen for game loop
game_screen = pygame.display.set_mode(screen_size[0],pygame.FULLSCREEN )

#screen for mouse activity
drawing_screen = pygame.Surface(screen_size[0])
max_x = screen_size[0][0] 
max_y = screen_size[0][1]
center = (max_x // 2,max_y // 2)
pygame.display.set_caption("Gesture Cat Game")

#background image load
bg = pygame.image.load("/Users/thejas/Projects/Final_Gesture_Cat/pictures/bg1.jpg")
bg = pygame.transform.scale(bg, screen_size[0])

while running:
    game_screen.fill((0,0,0)) #clear
    game_screen.blit(bg,(0,0)) #pasting the background

    #placing drawing_screen above game screen
    game_screen.blit(drawing_screen,(0,0))
    drawing_screen.set_colorkey((0,0,0))  #transparency
    
    #for loop for events
    for event in pygame.event.get():
        #exit the program - x button or 'q'
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            ms.mouse_loc.clear()
            start_pos1 = pygame.mouse.get_pos()
            ms.drawing = True

        if event.type == pygame.MOUSEBUTTONUP:
            ms.drawing = False
            attack = ms.detection(drawing_screen) # clears screen and tells shape
        
        #when the mouse is moving and it is held down
        if event.type == pygame.MOUSEMOTION and ms.drawing:
            current_pos = pygame.mouse.get_pos()
            #if the list is empy or if the mouse is atleast 5 pixels away, append to the list
            if len(ms.mouse_loc) == 0 or math.dist(current_pos, ms.mouse_loc[-1]) >5:
                ms.mouse_loc.append(current_pos)
                ms.drawing_lines(drawing_screen,start_pos1,current_pos)
                start_pos1 = current_pos #update for next loop
    pygame.display.update()
pygame.quit() 
