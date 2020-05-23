import os
import time
import neat
import pygame
import random

WIN_WIDTH = 500
WIN_HEIGHT = 800

bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird" + str(x) + ".png"))) for x in range(1,4)]
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))


class Bird:
    IMGS = bird_imgs

    def __init__(self, x, y):
        # inital x and y position of the bird
        self.x = x
        self.y = y
        # tick_count for time
        self.tick_count = 0
        # inital velocity of the bird
        self.vel = 0
        # inital image of the bird to be displayed
        self.img_count = 0
        self.img = self.IMGS[0]

    def move(self):
        # increasing time as move occured every "second" or tick
        self.tick_count += 1

        # s = u * t + 0.5 * a * t^2
        displacement = self.vel * self.tick_count + 0.5 * 3 * (self.tick_count**2)

        # displacement
        self.y += displacement
        print(str(self.y) + " : " + str(displacement))

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

def draw_window(win, bird):
    win.blit(bg_img, (0, 0))
    bird.draw(win)
    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    bird = Bird(200, 200)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.move()
        if bird.y > 800:
            bird.y = 0
        draw_window(win, bird)
    
    pygame.quit()
    quit()

main()