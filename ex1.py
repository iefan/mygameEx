import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
anotherSurface = DISPLAYSURF.convert_alpha()
anotherSurface.fill((128,0,0,250))
pygame.draw.rect(anotherSurface, (0, 0, 200, 250), pygame.Rect(0, 0, 400, 300))
pygame.display.set_caption('你好!')
print(DISPLAYSURF)
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()