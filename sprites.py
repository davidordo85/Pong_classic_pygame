import pygame as pg
from pygame.locals import *
import sys, random


DARK_GREY = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 3

class Ball(pg.sprite.Sprite):
    vx = 0
    vy = 0
    num_sprites = 12

    def __init__(self):
        super().__init__()
        self.image = pg.Surface((20, 20), pg.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.images = self.loadImages()
        self.image_act = 0
        self.image.blit(self.images[self.image_act], (0, 0))
        self.reset()

        self.imToxic = False
        
        self.ping = pg.mixer.Sound('./resources/sounds/ping.wav')
        self.lost_point = pg.mixer.Sound('./resources/sounds/lost-point.wav')

    def loadImages(self):
        '''
        images = []
        for i in range(self.num_sprites):
            image = pg.image.load("./resources/sprites/f_{}.png".format(i))
            images.append(image)
        return images
        '''
        return [pg.image.load("./resources/sprites/f_{}.png".format(i)) for i in range(self.num_sprites)]
        


    def reset(self):
        self.vx = random.choice([-7, -5, 5, 7])
        self.vy = random.choice([-7, -5, 5, 7]) 
        self.rect.centerx = 400
        self.rect.centery = 300

    def check_crash(self, group):
        candidate_list = pg.sprite.spritecollide(self, group, False)
        if len(candidate_list) > 0:
            self.vx *= -random.uniform(0.8, 1.3)
            self.vy *= random.uniform(0.8, 1.3)

            self.rect.centerx += self.vx
            self.rect.centery += self.vy
            self.ping.play()

    '''
    def comprobarChoque(self, something):
        dx = abs(self.rect.centerx - something.rect.centerx)
        dy = abs(self.rect.centery - something.rect.centery)
        if dx < (self.rect.w + something.rect.w)//2 and dy < (self.rect.h +something.rect.h) // 2:
            self.vx *= -random.uniform(0.8, 1.3)
            self.vy *= random.uniform(0.8, 1.3)
            self.rect.centerx += self.vx
            self.rect.centery += self.vy
            self.ping.play()
    '''
    def update(self, limSupX, limSupY):
        if self.rect.centerx >= limSupX or self.rect.centerx <=0:
            self.vx = 0
            self.vy = 0
            self.lost_point.play()

        if self.rect.centery >= limSupY or self.rect.centery <=0:
            self.vy *= -1
            self.ping.play()
                
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        #animar bola
        '''
        self.image_act += 1
        if self.image_act >= self.num_sprites:
            self.image_act = 0
        self.image_act +=1
        self.image_act = self.image_act % self.num_sprites
        '''

        self.image_act = (self.image_act + 1) % self.num_sprites
        self.image.blit(self.images[self.image_act], (0, 0))

class Racket(pg.sprite.Sprite):
    vx = 0
    vy = 0
    __color = WHITE

    def __init__(self, centerx):
        super().__init__()
        self.image = pg.Surface((25, 100))
        self.image.fill(self.__color)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = 400
        self.impact = False

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, tuple_color):
        self.__color = tuple_color
        self.image.fill(self.__color)


    def update(self, limSupX, limSupY):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

        if self.rect.centery < self.rect.h //2:
            self.rect.centery = self.rect.h // 2

        if self.rect.centery > limSupY - self.rect.h // 2:
            self.rect.centery = limSupY - self.rect.h // 2