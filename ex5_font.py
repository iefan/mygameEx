import pygame, sys
from pygame.locals import *

pygame.init()

# FPS = 30
# fpsClock = pygame.time.Clock()
#设置颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

curSurface = pygame.display.set_mode((400, 340), 0, 32)
pygame.display.set_caption("font")

fontObj = pygame.font.Font('simsunb.ttf', 32)
textSurfaceObj = fontObj.render("hello world!", True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (200, 150)

soundObj = pygame.mixer.Sound('sound/secosmic_lo.wav')
soundObj.play()


# catImg = pygame.image.load("image/cat.png")
# catImg2 = pygame.image.load("image/cat2.png")
# catImg_right = pygame.transform.smoothscale(catImg, (100,80))
# catImg_right2 = pygame.transform.smoothscale(catImg2, (100,80))
# catImg_left = pygame.transform.flip(catImg_right, 1, 0)
# catImg_left2 = pygame.transform.flip(catImg_right2, 1, 0)

# catx = 10
# caty = 100
# direction = 'right'


# curSurface.fill(WHITE)
# flag = True
while True:
    curSurface.fill(WHITE)
    curSurface.blit(textSurfaceObj, textRectObj)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    # fpsClock.tick(FPS)