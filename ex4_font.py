import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30

curSurface = pygame.display.set_mode((400, 340), 0, 32)
pygame.display.set_caption("font")

#设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

fontObj = pygame.font.Font("SourceCodePro-It.ttf", 32)
textSurfaceObj = fontObj.render("hello world", True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
print(textRectObj)
textRectObj.center = (200, 150)
print(textRectObj)

while True:
    curSurface.fill(WHITE)
    curSurface.blit(textSurfaceObj, textRectObj)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
