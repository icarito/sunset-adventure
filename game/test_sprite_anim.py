#!/bin/env python2
"""
Sprite strip animator demo

Requires spritesheet.spritesheet and the Explode1.bmp through Explode5.bmp
found in the sprite pack at
http://lostgarden.com/2005/03/download-complete-set-of-sweet-8-bit.html

I had to make the following addition to method spritesheet.image_at in
order to provide the means to handle sprite strip cells with borders:

            elif type(colorkey) not in (pygame.Color,tuple,list):
                colorkey = image.get_at((colorkey,colorkey))
"""
import sys
import pygame
from pygame.locals import *
#import spritesheet
from sprite_strip_anim import SpriteStripAnim

surface = pygame.display.set_mode((640,640))
FPS = 60
frames = FPS / 12
strips = [
    SpriteStripAnim('art/alicia.png', (0,0,64,64), 8, 1, True, frames),
    SpriteStripAnim('art/alicia.png', (0,64,64,64), 8, 1, True, frames),
    SpriteStripAnim('art/alicia.png', (0,128,64,64), 8, 1, True, frames),
    SpriteStripAnim('art/alicia.png', (0,196,64,64), 8, 1, True, frames),
#    SpriteStripAnim('Explode1.bmp', (0,0,24,24), 8, 1, True, frames),
#    SpriteStripAnim('Explode2.bmp', (0,0,12,12), 7, 1, True, frames),
#    SpriteStripAnim('Explode3.bmp', (0,0,48,48), 4, 1, True, frames) +
#    SpriteStripAnim('Explode3.bmp', (48,48,48,48), 4, 1, True, frames),
#    SpriteStripAnim('Explode4.bmp', (0,0,24,24), 6, 1, True, frames),
#    SpriteStripAnim('Explode5.bmp', (0,0,48,48), 4, 1, True, frames) +
#    SpriteStripAnim('Explode5.bmp', (48,48,48,48), 4, 1, True, frames),
]
black = Color('black')
clock = pygame.time.Clock()
n = 2
strips[n].iter()
image = strips[n].next()
while True:
    for e in pygame.event.get():
        if e.type == QUIT:
            exit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                sys.exit()
            elif e.key == K_DOWN:
                n=2
            elif e.key == K_UP:
                n=0
            elif e.key == K_RIGHT:
                n=3
            elif e.key == K_LEFT:
                n=1
            elif e.key == K_RETURN:
                n += 1
                if n >= len(strips):
                    n = 0
                strips[n].iter()
    surface.fill(black)
    image=pygame.transform.scale(image,(640,640))
    surface.blit(image, (0,0))
    pygame.display.flip()
    image = strips[n].next()
    clock.tick(FPS)
