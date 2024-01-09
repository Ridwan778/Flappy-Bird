import pygame as py
from pygame.locals import *
import math
import random

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
        self.vel= 0
    
    def getX(self):
        return self.rect.left

    def update(self):
        if gameOver == False:
            self.counter +=1
            if self.counter >=6:
                self.currentSprite = (self.currentSprite+1)%len(self.sprites)
                self.image = self.sprites[self.currentSprite]
                self.counter = 0
            
            #up and down movement
            keys = py.key.get_pressed()
            if keys[py.K_SPACE] and self.rect.top-5>0: 
                self.rect.y -= 7  # Move the bird upward
                self.vel = -6
            else:
                self.vel += 0.4
                if self.rect.bottom<SCREEN_HEIGHT:
                    self.rect.y += self.vel  # Move the bird downward
                else:
                    self.rect.y += 0
            self.image = py.transform.rotate(self.sprites[self.currentSprite], self.vel*-2)

class Pillar(py.sprite.Sprite):
    def __init__(self,pos_x, pos_y,flipped=False):
        py.sprite.Sprite.__init__(self)
        self.image = py.image.load('pipe.png')
        self.rect = self.image.get_rect(topleft = (0,30))
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.flipped = flipped
        self.status = True #true if it is infront of the bird, else false
        self.direction()
    
    def changeStatus(self):
        self.status = False

    def getstatus(self):
        return self.status
    
    def getX(self):
        return self.rect.right
    
    def getFlipped(self):
        return self.flipped

    def direction(self):
        if self.flipped == True:
            self.image = py.transform.flip(self.image, False, True)
            self.rect.bottomleft = [self.pos_x,self.pos_y-PILLAR_SPACE//2]
        else:
            self.rect.topleft = [self.pos_x,self.pos_y+PILLAR_SPACE//2]

    def update(self):
        self.rect.x -= scroll_speed 

py.init()

SCREEN_WIDTH = 865
SCREEN_HEIGHT = 768
PILLAR_SPACE = 200

screen = py.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
py.display.set_caption("FlappyBird")
bg_img = py.image.load('bg.png').convert()

clock = py.time.Clock()
scroll_speed = 6
bg_x = 0

pillar_interval = 2000
time_recent_pipe = py.time.get_ticks() - pillar_interval

bird_group = py.sprite.Group()
bird = Bird(100, SCREEN_HEIGHT//2)
bird_group.add(bird)

pillar_group = py.sprite.Group()
pillarBottom = Pillar(400,SCREEN_HEIGHT//2,False)
pillarTop = Pillar(400,SCREEN_HEIGHT//2,True)

pillar_group.add(pillarTop)
pillar_group.add(pillarBottom)

text_size = 50
score = 0

gameOver = False

running = True

while running:
    clock.tick(40)

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN and gameOver == True:
            gameOver = False
            score = 0
            pillar_group.empty()
            bird_group.empty()
            bird = Bird(100, SCREEN_HEIGHT//2)
            bird_group.add(bird)

            pillarBottom = Pillar(400,SCREEN_HEIGHT//2,False)
            pillarTop = Pillar(400,SCREEN_HEIGHT//2,True)

            pillar_group.add(pillarTop)
            pillar_group.add(pillarBottom)
            #time_recent_pipe = py.time.get_ticks() - pillar_interval
            

    # Update the background position
    bg_x -= scroll_speed

    # If the first background is out of the screen, reset its position to the right of the second one
    if bg_x <= -SCREEN_WIDTH:
        bg_x = 0

    # Draw two background images continuously scrolling
    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + SCREEN_WIDTH, 0))
    
    #draw and update bird
    bird_group.draw(screen)
    bird.update()

    #draw the pillars
    time = py.time.get_ticks()
    if (time - time_recent_pipe) > pillar_interval:
        pillar_height = random.randint(SCREEN_HEIGHT//3,(SCREEN_HEIGHT//3)*2)
        pillar_group.add(Pillar(SCREEN_WIDTH,pillar_height,False))
        pillar_group.add(Pillar(SCREEN_WIDTH,pillar_height,True))
        time_recent_pipe = time 

    pillar_group.draw(screen)
    pillar_group.update()

    #update score
    for i in pillar_group:
        if i.getX() < bird.getX() and i.getstatus() == True:
            if(i.getFlipped() == True and gameOver == False):
                score += 1
            i.changeStatus()

    collision = py.sprite.spritecollideany(bird, pillar_group)
    if collision:
        gameOver = True
    if gameOver:
        game_over_text = py.font.SysFont('arial', text_size).render("Game Over", True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - text_size))
        screen.blit(game_over_text, game_over_text_rect)

        restart_text = py.font.SysFont('arial', text_size).render("Click On Screen to Restart Game", True, (255, 255, 255))
        restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + text_size))
        screen.blit(restart_text, restart_text_rect)

    score_text = py.font.SysFont('arial', text_size).render("Score: " + str(score), True, (255, 255, 255))
    score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
    screen.blit(score_text, score_text_rect)

    py.display.update()

py.quit()
