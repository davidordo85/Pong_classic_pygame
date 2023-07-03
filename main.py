import pygame as pg
from pygame.locals import *
import sys, random
from sprites import Racket, Ball

BACKGROUND = (50,50,50)
YELLOW = (255, 255, 0)  
WHITE = (255, 255, 255)

WIN_GAME_SCORE = 10

clock = pg.time.Clock()
FPS = 60




class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        self.screen.fill(BACKGROUND)
        self.background = pg.image.load("./resources/images/background.jpg")
        self.ball = Ball()

        self.playerOne = Racket(30)
        self.playerTwo = Racket(770)
        self.playersGroup = pg.sprite.Group()
        self.playersGroup.add(self.playerOne)
        self.playersGroup.add(self.playerTwo)

        self.allSprites = pg.sprite.Group()
        self.allSprites.add(self.ball)
        self.allSprites.add(self.playersGroup)

        self.status = 'Games'

        self.font = pg.font.Font('./resources/font/font.ttf', 40)
        self.fontGrande = pg.font.Font('./resources/font/font.ttf', 60)

        self.markerOne = self.font.render("0", True, WHITE)
        self.markerTwo = self.font.render("0", True, WHITE)

        self.text_game_over = self.fontGrande.render("GAME OVER", True, YELLOW)
        self.text_insert_coin = self.font.render('<SPACE> - Inicio Games', True, WHITE)

        self.scoreOne = 0
        self.scoreTwo = 0
        pg.display.set_caption("Pong")


    def handleEvent(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.quit()
            
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.playerTwo.vy = -5

                if event.key == K_DOWN:
                    self.playerTwo.vy = 5

                if event.key == K_w:
                    self.playerOne.vy = -5

                if event.key == K_s:
                    self.playerOne.vy = 5
            
        key_pressed = pg.key.get_pressed()
        if key_pressed[K_UP]:
            self.playerTwo.vy -= 1
        elif key_pressed[K_DOWN]:
            self.playerTwo.vy += 1
        else:
            self.playerTwo.vy = 0

        if key_pressed[K_w]:
            self.playerOne.vy -= 1
        elif key_pressed[K_z]:
            self.playerOne.vy += 1
        else:
            self.playerOne.vy = 0
        
        return False

    def loop_Games(self):
        
        game_over = False
        self.scoreOne = 0
        self.scoreTwo = 0
        self.markerOne = self.font.render(str(self.scoreOne), True, WHITE)
        self.markerTwo = self.font.render(str(self.scoreOne), True, WHITE)

        while not game_over:
            clock.tick(FPS)
            game_over = self.handleEvent()

            self.allSprites.update(800, 600)

            self.ball.check_crash(self.playersGroup)

            if self.ball.vx == 0 and self.ball.vy == 0:
                if self.ball.rect.centerx >=800:
                    self.scoreOne += 1
                    self.markerOne = self.font.render(str(self.scoreOne), True, WHITE)
                if self.ball.rect.centerx <= 0:
                    self.scoreTwo += 1
                    self.markerTwo = self.font.render(str(self.scoreTwo), True, WHITE)

                if self.scoreOne == WIN_GAME_SCORE or self.scoreTwo == WIN_GAME_SCORE:
                    game_over = True

                self.ball.reset()

            self.screen.blit(self.background, (0, 0))
            self.allSprites.draw(self.screen)
            self.screen.blit(self.markerOne, (30, 10))
            self.screen.blit(self.markerTwo, (740, 10))

            pg.display.flip()

        self.status = 'Inicio'

    def loop_init(self):
        init_games = False
        while not init_games:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        init_games = True

            self.screen.fill((0,0, 255))
            self.screen.blit(self.text_game_over, (100, 100))
            self.screen.blit(self.text_insert_coin, (100, 200))     

            pg.display.flip()       

        self.status = 'Games'

    def loop_question(self):
        question_resolved = False
        while not question_resolved:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

                if event.type == KEYDOWN:
                    if event.key == K_r:
                        question_resolved = True

            self.screen.fill(DARK_GREY)
            self.screen.blit(self.ball.image, (self.ball.posx, self.ball.posy))
            pg.display.flip()

        self.status = 'Games'

                    



    def main_loop(self):

        while True:
            if self.status == 'Question':
                self.loop_question()
            elif self.status == 'Games':
                self.loop_Games()
            else:
                self.loop_init()


    def quit(self):
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    pg.init()
    game = Game()
    game.main_loop()
    game.quit()