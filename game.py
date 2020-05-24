import os
import sys

#pygame version number and welcome message hidden.
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
# initiallise font
pygame.font.init()

from flappybird import main, bg_img, STAT_FONT

WIN_WIDTH = 500
WIN_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def write_on_window(win, text, color, posx, posy, fontsize, inCenter = False):
    text_msg = STAT_FONT.render(text, 1, color)
    if(inCenter):
        text_position = text_msg.get_rect(center = (posx, posy))
    else:
        text_position = text_msg.get_rect(topleft = (posx, posy))
    win.blit(text_msg, text_position)

def draw_button(win, button):
    pygame.draw.rect(win, button['color'], button['button position'], 1)
    win.blit(button['text surface'], button['text rectangle'])

def create_button(posx, posy, width, height, label, callback, optional_arguments = None):
    text_msg = STAT_FONT.render(label, True, WHITE)

    button_position = pygame.Rect(posx, posy, width, height)
    text_rectangle = text_msg.get_rect(topleft = (posx + 10, posy + 5))
    button = {
        'button position': button_position,
        'text surface': text_msg,
        'text rectangle': text_rectangle,
        'color': WHITE,
        'callback': callback,
        'args': optional_arguments,
        }
    return button

def menu(play_again = False):
    pygame.init()
    pygame.display.set_caption("Flappy Bird | AI Project")
    size = (WIN_WIDTH, WIN_HEIGHT)
    win = pygame.display.set_mode(size)

    win.blit(bg_img, (0, 0))

    def play():
        main()

    play_button = None
    if play_again:
        play_button = create_button(150, 320, 200, 40, "Play Again", play)
    else:
        play_button = create_button(200, 320, 100, 40, "Play", play)
    quit_button = create_button(200, 400, 100, 40, 'Quit', sys.exit)

    button_list = [play_button, quit_button]

    while True:
        write_on_window(win, "Flappy Bird", WHITE , 250, 100, 60, True)
        if play_again:
            write_on_window(win, "Game Over!", WHITE , 250, 175, 30, True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in button_list:
                        if button['button position'].collidepoint(event.pos):
                            button['callback']()
            
            elif event.type == pygame.MOUSEMOTION:
                for button in button_list:
                    if button['button position'].collidepoint(event.pos):
                        button['color'] = BLACK
                    else:
                        button['color'] = WHITE

        for button in button_list:
            draw_button(win, button)

        pygame.display.update()

if __name__ == '__main__':
    menu()
