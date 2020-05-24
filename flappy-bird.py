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
    ANIMATION_TIME = 5
    ROT_VEL = 20

    def __init__(self, x, y):
        # inital x and y position of the bird
        self.x = x
        self.y = y
        # inital tilt or orientation of the bird
        self.tilt = 0
        # inital tick_count or time of the bird
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

        # limits the displacement in the downward direction to a max displacement value
        if displacement >= 16:
            displacement = 16

        # displacement
        self.y += displacement

        if self.tilt > -90:
            self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # to stop flapping animation of the bird as it falls down
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_image, pos = blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)
        win.blit(rotated_image, pos)

class Base:
    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        self.y = y
        # for cyclic rotation of the background image
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        


# to rotate image about it's centre: https://stackoverflow.com/a/54714144/4014678
def blitRotateCenter(win, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    return rotated_image, new_rect.topleft

def draw_window(win, bird, base):
    win.blit(bg_img, (0, 0))

    base.draw(win)
    bird.draw(win)
    
    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    bird = Bird(230, 350)
    base = Base(730)
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
        #bird.move()
        base.move()
        draw_window(win, bird, base)
    
    pygame.quit()
    quit()

main()