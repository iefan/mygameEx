import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

curSurface = pygame.display.set_mode((400, 340), 0, 32)
pygame.display.set_caption("Animation")

catImg = pygame.image.load("image/cat.png")
catImg2 = pygame.image.load("image/cat2.png")
catImg_right = pygame.transform.smoothscale(catImg, (100,80))
catImg_right2 = pygame.transform.smoothscale(catImg2, (100,80))
catImg_left = pygame.transform.flip(catImg_right, 1, 0)
catImg_left2 = pygame.transform.flip(catImg_right2, 1, 0)

catx = 10
caty = 100
direction = 'right'

#设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# curSurface.fill(WHITE)
flag = True
while True:
    curSurface.fill(WHITE)
    # flag = not flag
    # time.sleep(0.1)

    if direction == "right":
        catx += 5
        if catx == 280:
            direction = 'left'
        
        if flag:
            curSurface.blit(catImg_right, (catx, caty))
        else:
            curSurface.blit(catImg_right2, (catx, caty))
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'right'
        curSurface.blit(catImg_left, (catx, caty))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)