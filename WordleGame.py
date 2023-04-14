import pygame
from WordleWords import WORDS, checkWord, enterWord
import string
import time
import random

pygame.init()
width = 360
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 70)
input_length = 320
input_height = 60
user_text = ''
running = True

TITLE = [['b','i','r','d','s']]
ALPHABET = list(string.ascii_lowercase) + list(string.ascii_uppercase)
INDEX = random.randint(0, len(WORDS)-1)
GOAL = WORDS[INDEX]
GUESSES = []
DELAY = 0.2
LEFT = 0.5
RIGHT = 1.5
ROW = 0
LIMIT = 6
WORDSIZE = 5
COLOUR = 'White'
STATE = None
print(GOAL)

class inputSquare():
    
    def __init__(self, screen, colour, x, y, fill):
        self.square = pygame.draw.rect(screen, colour,(x,y,60,60), fill)
        
        
class inputLetter():
    
    def __init__(self, text, n, k, colour):
        self.letter = font.render(text[n][k], True, colour)
        
class inputRect():
    
    def __init__(self, screen, colour, x, y, length, height):
        self.rect = pygame.draw.rect(screen, colour, pygame.Rect(x, y, length, height), 2)

def nonWord(screen, user_text, user_width, x_pos, y_pos, input_length, input_height):
    input_box = inputRect(screen, 'white', x_pos, y_pos, input_length, input_height)
    input_box.center = (((input_length//2)+15)-(user_width//2), 517.5)
    text_surface = font.render(user_text, True, 'red')
    screen.blit(text_surface, input_box.center)
    user_text = ''
    time.sleep(DELAY)
    pygame.display.update(input_box)
    input_box = inputRect(screen, 'black', x_pos, y_pos, input_length, input_height)
    pygame.display.update(input_box)
    input_box = inputRect(screen, 'red', x_pos-LEFT, y_pos, input_length, input_height)
    pygame.display.update(input_box)
    time.sleep(DELAY)
    input_box = inputRect(screen, 'black', x_pos-LEFT, y_pos, input_length, input_height)
    pygame.display.update(input_box)
    input_box = inputRect(screen, 'red', x_pos+RIGHT, y_pos, input_length, input_height)
    pygame.display.update(input_box)
    time.sleep(DELAY)
    input_box = inputRect(screen, 'black', x_pos+RIGHT, y_pos, input_length, input_height)
    pygame.display.update(input_box)
    return user_text

def buildTitle(TITLE, WORDSIZE,screen, x, y):
    n = 0
    for k in range(WORDSIZE):
        letter = inputLetter(TITLE, n, k, 'white').letter
        title_box = inputSquare(screen, "darkseagreen1", x, y, 2).square
        title_width, title_height = font.size(TITLE[n][k])
        title_box.center = (x+30-(title_width//2), y+(title_height//5))
        screen.blit(letter, title_box.center)
        x += 70
    return x

def colourSelect(COLOUR, GUESSES, STATE, i, j):
    GUESSCOUNT = GUESSES[i].count(GUESSES[i][j])
    GOALCOUNT = GOAL.count(GUESSES[i][j])
    if GUESSES[i][j] == GOAL[j]:
        COLOUR = 'darkseagreen1'
    elif GUESSES[i][j] in GOAL:
        if GUESSCOUNT <= GOALCOUNT:
            COLOUR = 'gold'
        elif GUESSCOUNT > GOALCOUNT:
            if GUESSES[i][j] in GUESSES[i][:j]:
                COLOUR = 'tomato'
            else:
                COLOUR = 'gold'       
    else:
        COLOUR = 'tomato'
    return COLOUR, STATE

def buildSquares(LIMIT, WORDSIZE, COLOUR, STATE, screen, x, y):
    for i in range(LIMIT):
        for j in range(WORDSIZE):
            try: 
                COLOUR, STATE = colourSelect(COLOUR, GUESSES, STATE, i, j)
                letter = inputLetter(GUESSES, i, j, 'black').letter
                box = inputSquare(screen, COLOUR, x, y, 0).square
                box_width, box_height = font.size(GUESSES[i][j])
                box.center = (x+30-(box_width//2), y+(box_height//5))
                screen.blit(letter, box.center)
            except:  
                box = inputSquare(screen, "white", x, y, 2)
            x += 70
        x = 10
        y += 70
    return x, y

def buildInput(user_text, screen, x_pos, y_pos, input_length, input_height):
    user_width, user_height = font.size(user_text.strip())
    input_box = inputRect(screen, 'white', x_pos, y_pos, input_length, input_height)
    input_box.center = (((input_length//2)+15)-(user_width//2), 517.5)
    text_surface = font.render(user_text, True, 'white')
    screen.blit(text_surface, input_box.center)
    return user_width

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and STATE == None:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            if event.key == pygame.K_RETURN and len(user_text) == WORDSIZE and len(GUESSES) < LIMIT:
                TEST = checkWord(user_text)
                if TEST == True:
                    enterWord(user_text, GUESSES)
                    ROW += 1
                    if user_text == GOAL:
                        STATE = True
                    if ROW == LIMIT:
                        STATE = False
                    user_text = ''
                else:
                    while True:
                        user_text = nonWord(screen, user_text, user_width, x_pos, y_pos, input_length, input_height)
                        break
            if event.unicode in ALPHABET and len(user_text) < 5:
                user_text += event.unicode
            
            if STATE == True:
                user_text = 'PASS'
            if STATE == False:
                user_text = 'FAIL'
    screen.fill("black")
    x, y = 10, 10
    x = buildTitle(TITLE, WORDSIZE,screen, x, y)
    y += 70
    x = 10
    x, y = buildSquares(LIMIT, WORDSIZE, COLOUR,STATE, screen, x, y)
    x_pos = x * 2
    y_pos = y + 10
    user_text = user_text.upper()
    user_width = buildInput(user_text, screen, x_pos, y_pos, input_length, input_height)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()