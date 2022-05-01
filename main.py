from colorsys import hsv_to_rgb
import pygame
from pygame.locals import *
import math

pygame.init()

### načítanie obrázkov ###

background = pygame.image.load("Background.png")
dirt_img = pygame.image.load("dirt.png")
grass_img = pygame.image.load("grass.png")
plocha = pygame.image.load("plocha.png")
sand = pygame.image.load("sand.png")
Golf_Ball = pygame.image.load("Golf_Ball.png")

### premenné ###

wScreen = 1250
hScreen = 700
rect = background.get_rect()
rect = Golf_Ball.get_rect()
rect.x = 0
rect.y = 0
tile_size = 50
barrier_up = pygame.Rect(0,0,1300,10)
barrier_left = pygame.Rect(0,0,10,800)
barrier_right = pygame.Rect(1270,0,10,800)
barrier_down = pygame.Rect(0,710,1300,10)
run = True
time = 0
power = 0
angle = 0
shoot = False
clock = pygame.time.Clock()

### Okno ###

win = pygame.display.set_mode((wScreen,hScreen))
pygame.display.set_caption('Golf')

def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(win, (255, 255, 255), (0, line * tile_size), (wScreen, line * tile_size))
        pygame.draw.line(win, (255, 255, 255), (line * tile_size, 0), (line * tile_size, hScreen))

class ball(object):
    def __init__(self,x,y,radius,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.hitbox = (self.x - 7, self.y - 7, 14, 14)

    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x,self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius-1)
        self.hitbox = (self.x - 7, self.y - 7, 14, 14)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    @staticmethod
    def ballPath(startx, starty, power, ang, time):
        global velx, vely

        angle = ang

        velx = math.cos(angle) * power
        vely = math.sin(angle) * power

        distX = velx * time
        distY = (vely * time) + ((-4.9 * (time ** 2)) / 2)

        newx = round(distX + startx)
        newy = round(starty - distY)

        return (newx, newy)

class World():
    def __init__(self, data):
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    img = pygame.transform.scale(plocha, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 4:
                    img = pygame.transform.scale(sand, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            win.blit(tile[0], tile[1])
            pygame.draw.rect(win, (255,255,255), tile[1], 2)

### Obraz-hry ###

def redrawWindow():
    win.fill((64,64,64))
    win.blit(background, (rect.x, rect.y))
    world.draw()
    golfBall.draw(win)
    pygame.draw.line(win, (0,0,0),line[0], line[1])

### kolízie ###

### vypočítanie uhlu ###

def findAngle(pos):
    sX = golfBall.x
    sY = golfBall.y
    try:
        angle = math.atan((sY - pos[1]) / (sX - pos[0]))
    except:
        angle = math.pi / 2

    if pos[1] < sY and pos[0] > sX:
        angle = abs(angle)
    elif pos[1] < sY and pos[0] < sX:
        angle = math.pi - angle
    elif pos[1] > sY and pos[0] < sX:
        angle = math.pi + abs(angle)
    elif pos[1] > sY and pos[0] > sX:
        angle = (math.pi * 2) - angle

    return angle

golfBall = ball(300,hScreen - 56,5,(255,255,255))

world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 3, 0, 0, 0, 3, 4, 4, 4, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3, 3, 1], 
[1, 0, 0, 0, 0, 3, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],  
[1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 2, 0, 0, 0, 0, 0, 3, 1, 1, 1, 1, 1, 1],  
[1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1]
]

world = World(world_data)

run = True

while run:
    clock.tick(200)
    if shoot:
        #---zabránenie hráčovi aby odišiel z mapy---
        if golfBall.y < 650 - golfBall.radius:
            time += 0.05
            po = ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[0]
            golfBall.y = po[1]

        elif golfBall.x > 1200 - golfBall.radius:
            time += 0.05
            po = ball.ballPath(x, y, power, angle, time)
            golfBall.x = po[1]
            golfBall.y = po[0]
    
        else:
            shoot = False
            time = 0
            golfBall.y = hScreen - 56

    line = [(golfBall.x, golfBall.y), pygame.mouse.get_pos()]
    redrawWindow()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not shoot:
                x = golfBall.x
                y = golfBall.y
                pos =pygame.mouse.get_pos()
                shoot = True
                power = math.sqrt((line[1][1]-line[0][1])**2 +(line[1][0]-line[0][1])**2)/8
                angle = findAngle(pos)



    pygame.display.update()


pygame.quit()
