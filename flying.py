import pygame
from pygame.locals import *
import sys
import random

class Flying:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 600))
        self.background = pygame.image.load("images/sky.jpeg")
        self.cloud = pygame.image.load("images/cloud.png")
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.SysFont("comicsansms", 20)
        self.cloud_1 = pygame.image.load("images/cloud.png")
        self.player = pygame.image.load("images/tanya.jpg")
        self.player_1 = pygame.image.load("images/tanya_1.jpg")
        self.spring = pygame.image.load("images/bird.png")
        self.spring_1 = pygame.image.load("images/bird_1.png")
        self.playerx = 200
        self.playery = 400
        self.platforms = [[200,550,0,0]]
        self.springs = [] 
        self.cameray = 0
        self.jump = 0
        self.gravity = 0
        self.xmovement = 0
    
    def updatePlayer(self):
        if not self.jump:        
            self.playery += self.gravity
            self.gravity += 1
        elif self.jump:
            self.playery -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerx > 425: 
            self.playerx = -25
        elif self.playerx < -25:
            self.playerx = 425
        self.playerx += self.xmovement
        if self.playery - self.cameray <= 200:
            self.cameray -= 20
        if self.jump:
            self.screen.blit(self.player_1, (self.playerx, self.playery - self.cameray))
        else:
            self.screen.blit(self.player, (self.playerx, self.playery - self.cameray))

    def updatePlatforms(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0], p[1], self.cloud.get_width() - 10, self.cloud.get_height())
            player = pygame.Rect(self.playerx, self.playery, self.player.get_width() - 10, self.player_1.get_height())
            if rect.colliderect(player) and self.gravity and self.playery < (p[1] - self.cameray):
                self.jump = 15
                self.gravity = 0
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 5
                    if p[0] > 300:
                        p[-1] = 0
                else:
                    p[0] -= 5
                    if p[0] <= 0:
                        p[-1] = 1

    def drawPlatforms(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 600:
                platform = random.randint(0, 500)
                if platform < 400:
                    platform = 0
                else:
                    platform = 1

                self.platforms.append([random.randint(0, 300), self.platforms[-1][1] - 120, platform, 0])
                coords = self.platforms[-1]
                check = random.randint(0, 500)
                if check > 450 and platform == 0:
                    self.springs.append([coords[0], coords[1] - 25, 0])
                self.platforms.pop(0)
                self.score += 100
            if p[2] == 0:
                self.screen.blit(self.cloud, (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.cloud_1, (p[0], p[1] - self.cameray))
    
        for spring in self.springs:
            if spring[-1]:
                self.screen.blit(self.spring_1, (spring[0], spring[1] - self.cameray))
            else:
                self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            if pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height()).colliderect(pygame.Rect(self.playerx, self.playery, self.player.get_width(), self.player.get_height())):
                self.jump = 30
                self.cameray -= 30

    def generatePlatforms(self):
        on = 600
        while on > -120:
            x = random.randint(0,300)
            platform = random.randint(0, 500)
            if platform < 400:
                platform = 0
            else:
                platform = 1
            self.platforms.append([x, on, platform, 0])
            on -= 120

    def run(self):
        clock = pygame.time.Clock()
        self.generatePlatforms()
        while True:
            self.screen.fill((207,242,248))
            self.screen.blit(self.background, (0,0))
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            if self.playery - self.cameray > 600:
                self.cameray = 0
                self.score = 0
                self.springs = []
                self.platforms = [[200,550,0,0]]
                self.generatePlatforms()
                self.playerx = 200
                self.playery = 550
            self.drawPlatforms()
            self.updatePlayer()
            self.updatePlatforms()
            self.screen.blit(self.font.render("Scores: " + str(self.score), -1, (0, 0, 0)), (25, 25))
            pygame.display.flip()  


Flying().run()
