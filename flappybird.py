import os
import time
import neat
import random

#pygame version number and welcome message hidden.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

# initiallise font
pygame.font.init()

GEN = 0
DRAW_LINES = True

WIN_WIDTH = 500
WIN_HEIGHT = 800
FLOOR = 730

bird_imgs = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird" + str(x) + ".png"))) for x in range(1,4)]
pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 50)

class Bird:
    IMGS = bird_imgs
    ANIMATION_TIME = 5
    ROT_VEL = 20
    MAX_ROTATION = 25

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
        # inital height of the bird
        self.height = self.y
        # inital image of the bird to be displayed
        self.img_count = 0
        self.img = self.IMGS[0]
    
    def jump(self):
        # reseting tick_count (time) = 0 to denote the instant at which the jump occured
        self.tick_count = 0
        # storing the height at which the jump occured
        self.height = self.y
        # the velocity with which the bird moves up when it jumps
        # NOTE vel is negative cause the top left corner of the pygame window is (0, 0)
        self.vel = -10.5

    def move(self):
        # increasing time as move occured every "second" or tick
        self.tick_count += 1

        # s = u * t + 0.5 * a * t^2
        displacement = self.vel * self.tick_count + 0.5 * 3 * (self.tick_count**2)

        # limits the displacement in the downward direction to a max displacement value
        if displacement >= 16:
            displacement = 16
        
        # limits the displacement in the upward direction to a max displacement value
        if displacement < 0:
            displacement -= 2

        # displacement
        self.y += displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
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
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0

        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        # getting the masks for the images
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # calculating the rectangle offset of the images
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        top_point = bird_mask.overlap(top_mask, top_offset)
        bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

        if top_point or bottom_point:
            return True # collision occured
        return False

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

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    win.blit(bg_img, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    base.draw(win)
    
    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255, 0, 0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), 
                        (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255, 0, 0), (bird.x + bird.img.get_width()/2, bird.y + bird.img.get_height()/2), 
                        (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        bird.draw(win)
    
    # score
    score_label = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    if gen > 0:
        # generation count
        gen_label = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
        win.blit(gen_label, (10, 10))

        # alive
        alive_label = STAT_FONT.render("Alive: " + str(len(birds)), 1, (255, 255, 255))
        win.blit(alive_label, (10, 50))

    pygame.display.update()

def eval_genome(genomes, config):
    global GEN
    GEN += 1

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        # creates a neural network for the genome (bird[i] in one generation)
        # eval_genome function is called multiple times for each generation
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        # creating a bird object to be kept track off
        birds.append(Bird(230, 350))
        # initalizing the fitness value of the bird
        g.fitness = 0
        ge.append(g)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    base = Base(FLOOR)
    pipes = [Pipe(700)]

    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # determine whether to use the first or second pipe on the screen for neural network input
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        for x, bird in enumerate(birds):
            # give each bird a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            bird.move()

            # the input to the neural network is bird location, top pipe location and bottom pipe location
            # and determine from network whether to jump or not
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            # using a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            # check config file [DefaultGenome] for details
            # output from the nn is always a list, in our case we have only one output so output[0]
            if output[0] > 0.5:
                bird.jump()

        add_pipe = False
        pipes_to_remove = []
        for pipe in pipes:
            # iterate over the birds list to the index and bird
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    # reduced the fitness of the bird as it has collided
                    ge[x].fitness -= 1
                    # removing the bird, it's nn and it's genome from the list
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # to check if the pipe has left the game window
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            # increasing fitness of bird as it passes threw the pipes
            for g in ge:
                g.fitness+=5
            pipes.append(Pipe(600))
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        for x, bird in enumerate(birds):
            # to check if the bird hits the floor or hits the ceiling
            if bird.y + bird.img.get_height() >= FLOOR or bird.y < 0:
                # not reducing the fitness here
                # removing the bird, it's nn and it's genome from the list
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, GEN, pipe_ind)

        # break if score gets large enough
        if score >= 20:
            break

# this is the actual main function which will be called when a Human want's to play
# call happens from game.py
def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    bird = Bird(230, 350)
    base = Base(FLOOR)
    pipes = [Pipe(700)]

    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
        
        bird.move()
        add_pipe = False
        pipes_to_remove = []
        for pipe in pipes:
            if pipe.collide(bird):
                run = False
            # to check if the pipe has left the game window
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                pipes_to_remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        if bird.y + bird.img.get_height() >= FLOOR:
            run = False

        base.move()
        draw_window(win, [bird], pipes, base, score, GEN, 0)
    
    pygame.time.wait(2000)

def run(config_file):
    # loading the config file and it's details with the headings:
    # [DefaultGenome], [DefaultReproduction], [DefaultSpeciesSet], [DefaultStagnation]
    # [NEAT] is not required to be mentioned as it's a mandatory config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # this is used to set the population details from the config file
    p = neat.Population(config)

    # this is used to give the output
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # represents the no of generations to run the fitness funtion
    generations = 50
    # the "main" function is our fitness function
    # the function has to be modified to run for more than one bird
    # i.e., the entire population in that generation
    # calling it eval_genome and rewriting the function
    winner = p.run(eval_genome, generations)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_file = os.path.join(local_dir + 'config-feedforward.txt')
    run(config_file)
