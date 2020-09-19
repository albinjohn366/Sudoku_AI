import pygame as pg
import sys
from game_logic import values as hints
from game_logic import unknown

pg.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
small_font = pg.font.Font(pg.font.get_default_font(), 10)
medium_font = pg.font.Font(pg.font.get_default_font(), 18)
large_font = pg.font.Font(pg.font.get_default_font(), 30)
largest_font = pg.font.Font(pg.font.get_default_font(), 80)

# Setting the screen
size = (width, height) = (420, 440)
screen = pg.display.set_mode(size)
pg.display.set_caption('Sudoku')

# Setting initial variables
game_over = False
initial_page = True
active = False
selection = False
unknown_space = dict()
answers = dict()

# Setting variables
welcome_text = large_font.render('WELCOME', True, WHITE)
instruction_text = medium_font.render('Please enter your name:', True,
                                      WHITE)
text_box = pg.Rect(width / 4 - 2, height / 2 - 10, 211, 30)
name = ''


# Returning the result text
def resultt(answers):
    for key in answers:
        try:
            if hints[key] != int(answers[key]):
                return 'YOU LOST'
        except ValueError:
            return 'YOU LOST'
    return 'YOU WON'


while True:

    # Setting bg color
    screen.fill((0, 102, 102))

    # Setting the initial page
    if initial_page:
        # Setting positions
        welcome_text_rect = welcome_text.get_rect()
        welcome_text_rect.center = (width / 2, 70)
        instruction_text_rect = instruction_text.get_rect()
        instruction_text_rect.center = (width / 2, height / 2 - 30)
        screen.blit(welcome_text, welcome_text_rect)
        screen.blit(instruction_text, instruction_text_rect)
        pg.draw.rect(screen, WHITE, text_box)
        name_text = medium_font.render(name, True, BLACK)
        name_text_rect = name_text.get_rect()
        name_text_rect.center = text_box.center
        screen.blit(name_text, name_text_rect)
        if selection:
            pg.draw.rect(screen, RED, text_box, 1)
    else:
        # Printing the greeting message
        greeting = medium_font.render('Hello {}'.format(name[:-1]), True, WHITE)
        greeting_rect = greeting.get_rect()
        greeting_rect.center = (width / 2, 10)
        screen.blit(greeting, greeting_rect)

        # Drawing the large box
        outline = pg.Rect(0, 20, 420, 420)
        pg.draw.rect(screen, WHITE, outline)

        # Drawing the 9 big boxes
        for row in range(3):
            start_hor = (0, 20 + row * 420 / 3)
            end_hor = (420, 20 + row * 420 / 3)
            start_ver = (row * width / 3, 20)
            end_ver = (row * width / 3, 440)
            pg.draw.line(screen, BLACK, start_hor, end_hor, 2)
            pg.draw.line(screen, BLACK, start_ver, end_ver, 2)

        # Drawing all lines
        for row in range(9):
            start_hor = (0, 20 + row * 420 / 9)
            end_hor = (420, 20 + row * 420 / 9)
            start_ver = (row * width / 9, 20)
            end_ver = (row * width / 9, 440)
            pg.draw.line(screen, BLACK, start_hor, end_hor, 1)
            pg.draw.line(screen, BLACK, start_ver, end_ver, 1)

        # Adding values to each cell
        half_cell = width / 18
        for value in hints:
            # Answers player found out
            if str(value) in answers.keys():
                text = medium_font.render(str(answers[value]), True, RED)
                text_rect = text.get_rect()
                text_rect.center = (int(value[1]) * width / 9 + half_cell,
                                    20 + int(value[4]) *
                                    width / 9 + half_cell)
                screen.blit(text, text_rect)

            # If value is in unknown list
            if value in unknown:
                unknown_space[value] = pg.Rect(int(value[1]) * width / 9 + 1,
                                               int(value[4]) * width / 9 + 21,
                                               width / 9, width / 9)
                if value == selection:
                    pg.draw.rect(screen, RED, unknown_space[value], 1)
                pg.draw.rect(screen, WHITE, unknown_space[value], -1)
                continue

            # Providing the values to the spaces
            text = medium_font.render(str(hints[value]), True, (0, 102, 51))
            text_rect = text.get_rect()
            text_rect.center = (int(value[1]) * width / 9 + half_cell,
                                20 + int(value[4]) *
                                width / 9 + half_cell)
            screen.blit(text, text_rect)

    # To end the window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if not game_over:
            # If it is the initial page
            if initial_page:
                # If mouse is pressed at right position
                if event.type == pg.MOUSEBUTTONDOWN:
                    if text_box.collidepoint(event.pos):
                        active = True
                        selection = True
                    else:
                        active = False
                        selection = False

                # If key is pressed at active state
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            initial_page = False
                            active = False
                            selection = False
                        if event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        else:
                            name += event.unicode
            else:
                # If mouse is pressed at right position
                if event.type == pg.MOUSEBUTTONDOWN:
                    for key in unknown_space:
                        if unknown_space[key].collidepoint(event.pos):
                            selection = key

                # If a key is pressed
                if selection and event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        selection = False
                    else:
                        answers[selection] = event.unicode
                        if len(answers) == len(unknown):
                            game_over = True

    if game_over:
        result_text = largest_font.render(resultt(answers), True, BLACK)
        result_text_rect = result_text.get_rect()
        result_text_rect.center = (width / 2, height / 2)
        screen.blit(result_text, result_text_rect)

    # Updating the screen
    pg.display.update()
