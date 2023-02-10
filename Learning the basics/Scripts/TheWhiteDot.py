#Importing the modules
import sys, pygame, keyboard
from pygame import gfxdraw
pygame.init()

######################
## DISPLAY VARIBLES ################################################################################
######################

#Window name
pygame.display.set_caption('The White Dot')
#Window icon
icon = pygame.image.load('Images/TheWhiteDot_Logo.png')
pygame.display.set_icon(icon)

#Creating the graphical window
display_width = 960
display_height = 540

#Setting the display size varible
size = width, height = display_width, display_height

#Setting the game colours
background_colour = (50,50,50)

#Setting the screen variable
screen = pygame.display.set_mode(size)

######################
## PLAYER VARIABLES ###############################################################################
######################

#The location of the player
player_x = display_width/2
player_y = display_height/2

#The colour of the player
player_colour = (200,200,200)

#The speed of the player
player_speed = 0.25

#The radius of the player
player_radius = 15


#Setting the border collision for the player 

#Right
border_width_right = display_width - player_radius 
#Left
border_width_left = 0 + player_radius
#Bottom
border_height_bottom = display_height - player_radius
#Top
border_height_top = 0 + player_radius


##################################################
#Creates an infinte loop to keep the game open ###
###################################################
#Essentially a step event like in Gamemaker  Studio 2
#Game Loop
while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    #Colour of the window background
    screen.fill(background_colour)

    if keyboard.is_pressed('d') or keyboard.is_pressed('right'):
        player_x += player_speed

    if keyboard.is_pressed('a') or keyboard.is_pressed('left'):
        player_x += -player_speed

    if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
        player_y += -player_speed

    if keyboard.is_pressed('s') or keyboard.is_pressed('down'):
        player_y += player_speed

    if keyboard.is_pressed('esc'):
        exit()

#set the right boundary 
    if player_x > border_width_right:
        player_x = border_width_right
#set the left boundary
    if player_x < border_width_left:
        player_x = border_width_left
#set the bottom boundary
    if player_y > border_height_bottom:
        player_y = border_height_bottom
#set the top boundary
    if player_y < border_height_top:
        player_y = border_height_top
            
    # Draws the circle on the screen
    pygame.draw.circle(screen, player_colour, (player_x, player_y), player_radius)

    pygame.display.flip()