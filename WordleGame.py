import pygame
from WordleWords import WORDS, checkWord, enterWord
import string
import time
import random

pygame.init()
width = 860
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 70)
input_length = 390
input_height = 60
user_text = ''
running = True

TITLE = [['n','u','g','g','l','e']]
ALPHABET = list(string.ascii_lowercase) + list(string.ascii_uppercase)
VOWELS = [['A','E','I','O','U']]
CONSONENTS = [letter for letter in list(string.ascii_uppercase) if letter not in VOWELS[0]]
CONSONENTS_CHUNKS = [CONSONENTS[x:x+6] for x in range(0, len(CONSONENTS), 6)]
print(CONSONENTS_CHUNKS)
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
HISCORE = 0

class inputSquare():
    
    def __init__(self, screen, colour1, colour2, x, y):
        self.square = pygame.draw.rect(screen, colour1,(x,y,60,60), 0)
        self.border = pygame.draw.rect(screen, colour2,(x,y,61,61), 2)
        
        
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

def buildTitle(TITLE, TITLE_SIZE,screen, x, y):
    n = 0
    for k in range(TITLE_SIZE):
        letter = inputLetter(TITLE, n, k, 'white').letter
        title_box = inputSquare(screen, "darkseagreen","darkseagreen1", x, y).square
        title_width, title_height = font.size(TITLE[n][k])
        title_box.center = (x+30-(title_width//2), y+(title_height//5))
        screen.blit(letter, title_box.center)
        x += 70
    return x

def buildAlphabet(SIZE, VOWELS, CONSONENTS_CHUNKS,  screen, x, y):
    XYZ = [CONSONENTS_CHUNKS[-1]]
    CONSONENTS_CHUNKS = CONSONENTS_CHUNKS[:-1]
    try:
        GUESS_LETTERS = [Letter for Lst in GUESSES for Letter in Lst]
    except:
        GUESS_LETTERS = None
    n = 0
    original = x
    x = x + 35
    for k in range(SIZE):
        COLOUR = 'black'
        if VOWELS[n][k] not in GOAL and GUESS_LETTERS != None and VOWELS[n][k] in GUESS_LETTERS:
            COLOUR = 'grey'
        letter = inputLetter(VOWELS, n, k, 'white').letter
        letter_box = inputSquare(screen, COLOUR,"white", x, y).square
        letter_width, letter_height = font.size(VOWELS[n][k])
        letter_box.center = (x+30-(letter_width//2), y+(letter_height//5))
        screen.blit(letter, letter_box.center)
        x += 70
    x =  original
    y += 70
    for n in range(len(CONSONENTS_CHUNKS)):
        for k in range(SIZE+1):
            COLOUR = 'black'
            if CONSONENTS_CHUNKS[n][k] not in GOAL and GUESS_LETTERS != None and CONSONENTS_CHUNKS[n][k] in GUESS_LETTERS:
                COLOUR = 'grey'
            letter = inputLetter(CONSONENTS_CHUNKS, n, k, 'white').letter
            letter_box = inputSquare(screen, COLOUR,"white", x, y).square
            letter_width, letter_height = font.size(CONSONENTS_CHUNKS[n][k])
            letter_box.center = (x+30-(letter_width//2), y+(letter_height//5))
            screen.blit(letter, letter_box.center)
            x += 70
        x =  original
        y += 70
    x = original + 105 
    n = 0
    for k in range(3):
        COLOUR = 'black'
        if XYZ[n][k] not in GOAL and GUESS_LETTERS != None and XYZ[n][k] in GUESS_LETTERS:
            COLOUR = 'grey'
        letter = inputLetter(XYZ, n, k, 'white').letter
        letter_box = inputSquare(screen, COLOUR,"white", x, y).square
        letter_width, letter_height = font.size(XYZ[n][k])
        letter_box.center = (x+30-(letter_width//2), y+(letter_height//5))
        screen.blit(letter, letter_box.center)
        x += 70
    return x

def colourSelect(COLOUR, EXACTS, GUESSES, GUESSCOUNT, STATE, i, j):
    GOALCOUNT = GOAL.count(GUESSES[i][j])
    VALUE = EXACTS.get(j)
    if VALUE != None:
        COLOUR = 'darkseagreen1'
    elif GUESSCOUNT < GOALCOUNT:
        GUESSCOUNT += 1
        COLOUR = 'gold'
    else:
        COLOUR = 'tomato'
    return COLOUR, STATE

def stringMatch(GUESSES, i):
    RESULT = []
    EXACTS = {}
    for index, letter in enumerate(GUESSES[i]):
            if letter == GOAL[index]:
                RESULT.append(True)
            else:
                RESULT.append(False)
    for index, state in enumerate(RESULT):
        if state:
            EXACTS[index] = GUESSES[i][index]
    return EXACTS

def buildSquares(LIMIT, WORDSIZE, COLOUR, STATE, screen, x, y):
    for i in range(LIMIT):
        for j in range(WORDSIZE):
            if len(GUESSES) > 0 and len(GUESSES) > i:
                EXACTS = stringMatch(GUESSES, i)
                GUESSCOUNT = sum(1 for value in EXACTS.values() if value == GUESSES[i][j])
            try: 
                COLOUR, STATE = colourSelect(COLOUR, EXACTS, GUESSES, GUESSCOUNT, STATE, i, j)
                letter = inputLetter(GUESSES, i, j, 'black').letter
                box = inputSquare(screen, COLOUR, "white", x, y).square
                box_width, box_height = font.size(GUESSES[i][j])
                box.center = (x+30-(box_width//2), y+(box_height//5))
                screen.blit(letter, box.center)
            except:  
                box = inputSquare(screen, "black", "white", x, y)
            x += 80
        x = 25
        y += 70
    return x, y

def buildInput(user_text, screen, x_pos, y_pos, input_length, input_height):
    user_width, user_height = font.size(user_text.strip())
    input_box = inputRect(screen, 'white', x_pos, y_pos, input_length, input_height)
    input_box.center = (((input_length//2)+15)-(user_width//2), 517.5)
    text_surface = font.render(user_text, True, 'white')
    screen.blit(text_surface, input_box.center)
    return user_width

def defaultState():
    GUESSES = []
    user_text = ''
    STATE = None
    INDEX = random.randint(0, len(WORDS)-1)
    GOAL = WORDS[INDEX]
    return GUESSES, user_text, STATE, GOAL

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
                        HISCORE = 0
                    user_text = ''
                else:
                    while True:
                        user_text = nonWord(screen, user_text, user_width, x_pos, y_pos, input_length, input_height)
                        break
            if event.unicode in ALPHABET and len(user_text) < 5:
                user_text += event.unicode
            
            if STATE == True:
                user_text = 'R to replay'
            if STATE == False:
                user_text = 'R to replay'
        if event.type == pygame.KEYDOWN and STATE != None:
            if event.key == pygame.K_r:
                    GUESSES, user_text, STATE, GOAL = defaultState()
                    HISCORE += 1
                    print(GOAL, HISCORE)
    screen.fill("black")
    x, y = 10, 10
    x = buildTitle(TITLE, LIMIT,screen, x, y)
    x += 10
    y += 70
    buildAlphabet(WORDSIZE, VOWELS, CONSONENTS_CHUNKS, screen,x, y)
    y = 80
    x = 25
    x, y = buildSquares(LIMIT, WORDSIZE, COLOUR,STATE, screen, x, y)
    x = 10
    x_pos = x * 2
    y_pos = y + 10
    user_text = user_text.upper()
    user_width = buildInput(user_text, screen, x_pos, y_pos, input_length, input_height)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()