import pygame as py
from pygame.locals import *
import math

class Bird(py.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        py.sprite.Sprite.__init__(self)
        self.sprites = [py.image.load('bird1.png'),
                        py.image.load('bird2.png'),
                        py.image.load('bird3.png')]
        
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.counter = 0
        self.speed = 5 #up and down speed

    def update(self):
        self.counter +=1
        if self.counter >=6:
            self.currentSprite = (self.currentSprite+1)%len(self.sprites)
            self.image = self.sprites[self.currentSprite]
            self.counter = 0
        
        #up and down movement
        keys = py.key.get_pressed()
        if keys[py.K_UP] and self.rect.y-5>0:  # Change this to the desired key
            self.rect.y -= self.speed  # Move the bird upward
        if keys[py.K_DOWN] and self.rect.y+5>0:  # Change this to the desired key
            self.rect.y += self.speed  # Move the bird upward

    


py.init()

SCREEN_WIDTH = 865
SCREEN_HEIGHT = 768

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
py.display.set_caption("FlappyBird")
bg_img = py.image.load('bg.png').convert()

clock = py.time.Clock()
scroll_speed = 5
bg_x = 0

sprite_group = py.sprite.Group()
bird = Bird(100, SCREEN_HEIGHT//2)
sprite_group.add(bird)

running = True

while running:
    clock.tick(40)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # Update the background position
    bg_x -= scroll_speed

    # If the first background is out of the screen, reset its position to the right of the second one
    if bg_x <= -SCREEN_WIDTH:
        bg_x = 0

    # Draw two background images continuously scrolling
    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + SCREEN_WIDTH, 0))
    
    #draw and update bird
    sprite_group.draw(screen)
    bird.update()
    py.display.update()

py.quit()