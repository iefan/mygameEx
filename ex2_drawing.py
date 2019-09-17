import pygame, sys, math
from pygame.locals import *

pygame.init()

curSurface = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption("Drawing")

#设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)


curSurface.fill(WHITE)
pygame.draw.polygon(curSurface, GREEN, ((146,0), (291, 106), (236, 277), (56,277), (0, 106)))
pygame.draw.lines(curSurface, RED, False, ((146,0), (291, 106), (236, 277)))
pygame.draw.line(curSurface, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(curSurface, BLUE, (120, 60), (60, 120))
pygame.draw.line(curSurface, BLUE, (60, 120), (120, 120), 4)
pygame.draw.circle(curSurface, BLUE, (300,50), 30, 1)
pygame.draw.circle(curSurface, BLUE, (250,300), 30, 0)
pygame.draw.ellipse(curSurface, RED, (300, 250, 40, 80), 1)
pygame.draw.rect(curSurface, RED, (200, 150, 100, 50))

# pygame.draw.aalines(curSurface, BLUE, False, ((140,0), (280, 106), (226, 277)), 1)
# pygame.draw.aaline(curSurface, BLUE, (100,100), (300,300), 4)
# pygame.draw.line(curSurface, RED, (150,80), (300,300), 1)
# pygame.draw.arc(curSurface, BLACK, (100, 40, 340, 340), 0, math.pi, 1)
# pygame.draw.arc(curSurface, BLUE, (100, 200, 340, 150), math.pi, 2*math.pi, 1)

pixObj = pygame.PixelArray(curSurface)
pixObj[480][380] = BLACK
pixObj[482][382] = BLACK
pixObj[484][384] = BLACK
pixObj[486][386] = BLACK
pixObj[488][388] = BLACK
print(curSurface.get_locked())
del pixObj
print(curSurface.get_locked())

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
