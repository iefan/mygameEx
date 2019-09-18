import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()

curSurface = pygame.display.set_mode((400, 340), 0, 32)
pygame.display.set_caption("Animation")

catImg = pygame.image.load("image/cat.png")
catImg = pygame.transform.smoothscale(catImg, (100,80))
catImg = pygame.transform.flip(catImg, 1, 0)

catx = 10
caty = 10
direction = 'right'

#设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

# curSurface.fill(WHITE)

while True:
    curSurface.fill(WHITE)
    # time.sleep(0.1)

    if direction == "right":
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 5:
            direction = 'right'
    
    curSurface.blit(catImg, (catx, caty))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)