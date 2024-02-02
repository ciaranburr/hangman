import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60

screen_width = 700
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hangman')
white = (255, 255, 255)
screen.fill(white)
og = pygame.image.load('img/hang.png')
button_img = pygame.image.load('img/restart.png')
black = (0,0,0)
font = pygame.font.SysFont('Bauhaus 93', 30)
font1 = pygame.font.SysFont('Bauhaus 93', 60)
head = pygame.image.load('img/head.png')
leye = pygame.image.load('img/leye.png')
reye = pygame.image.load('img/reye.png')
leg = pygame.image.load('img/leg.png')
reg = pygame.image.load('img/reg.png')
larm = pygame.image.load('img/larm.png')
rarm = pygame.image.load('img/rarm.png')
nose = pygame.image.load('img/nose.png')
mouth = pygame.image.load('img/mouth.png')
body = pygame.image.load('img/body.png')

def getMin():
    while True:
        try:
            num = int(input('Please enter a minimum word length before starting'))
            break
        except ValueError:
            print('Please enter a valid number!')
    while True:
        if 1 <= int(num) <= 31:
            break
        elif int(num) < 1 or int(num) > 31:
            num = input('Error! Please enter a minimum word length between 0 and 32')
    return num


def getWords(words, minLength):
    wordBank = []
    for each in words:
        each = each.strip()
        if len(each) > int(minLength):
            wordBank.append(each)
    return wordBank


def handleInputDifficulty():
    while True:
        mode = input('Please enter e or h for easy or hard mode').lower()
        if mode == 'e':
            mode = 'easy'
            break
        elif mode =='h':
            mode = 'hard'
            break
        print('Please enter just the letter!')
    return mode


def getWord(bank):
    word = bank[random.randint(0, len(bank))]
    return word


def letterGuess(alphabet):
    while True:
        let = input('Please input a letter').lower()
        if len(let) == 1 and let in alphabet:
            break
    alphabet = alphabet.replace(let, ' ')
    return [let, alphabet]


def updateWord(guessWord, guessWordasList, letterGuess):
    i = 0
    for let in guessWord:
        if let == letterGuess:
            guessWordasList[i] = letterGuess
        i += 1
    return guessWordasList


def processGuess(letterGuess, guessWord, missesLeft):
    if letterGuess in guessWord:
        guess = True
    else:
        guess = False
        missesLeft -= 1
    return [guess, missesLeft]


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def wordDisplay(wordAsList):
    display = ""
    for let in wordAsList:
        display = display + let + " "
    return display


def beforeGame():
    print("Welcome to hangman-made by Ciaran himself!")
    min = getMin()
    difficulty = handleInputDifficulty()
    print('You have selected ' + difficulty + ' mode.')
    if difficulty == 'easy':
        print('Try to guess as many words in a row as possible. You have ten guesses for each word.')
        guesses = 10
    else:
        print('Try to guess as many words in a row as possible. You have seven guesses for each word.')
        guesses = 7
    return [min, difficulty, guesses]


def reset_game():
    global missesLeft, guessWordAsList, alphabet, guessWord, i, difficulty
    file = open('words_alpha.txt')
    content = file.readlines()
    wordBank = getWords(content, initial[0])
    missesLeft = initial[2]
    guessWord = getWord(wordBank)
    guessWordAsList = ['_' for let in guessWord]
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    screen.fill(white)
    i = 0


def update():
    if missesLeft < 10 and difficulty == 'easy':
        screen.blit(head, (100,100))
    if missesLeft < 9 and difficulty == 'easy':
        screen.blit(body, (150,200))
    if missesLeft < 8 and difficulty == 'easy':
        screen.blit(larm, (75,230))
    if missesLeft < 7 and difficulty == 'easy':
        screen.blit(rarm, (150,230))
    if missesLeft < 6 and difficulty == 'easy':
        screen.blit(leg, (97,345))
    if missesLeft < 5 and difficulty == 'easy':
        screen.blit(reg, (150,345))
    if missesLeft < 4 and difficulty == 'easy':
        screen.blit(reye, (162,130))
    if missesLeft < 3 and difficulty == 'easy':
        screen.blit(leye, (124,130))
    if missesLeft < 2 and difficulty == 'easy':
        screen.blit(nose, (140,150))
    if missesLeft < 1 and difficulty == 'easy':
        screen.blit(mouth, (135,175))
    if missesLeft < 7 and difficulty == 'hard':
        screen.blit(head, (100,100))
    if missesLeft < 6 and difficulty == 'hard':
        screen.blit(body, (150,200))
    if missesLeft < 5 and difficulty == 'hard':
        screen.blit(larm, (75,230))
    if missesLeft < 4 and difficulty == 'hard':
        screen.blit(rarm, (150,230))
    if missesLeft < 3 and difficulty == 'hard':
        screen.blit(leg, (97,345))
    if missesLeft < 2 and difficulty == 'hard':
        screen.blit(reg, (150,345))
    if missesLeft < 1 and difficulty == 'hard':
        screen.blit(reye, (162, 130))
        screen.blit(leye, (124, 130))
        screen.blit(nose, (140, 150))
        screen.blit(mouth, (135, 175))


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check if mouse is over button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


initial = beforeGame()
game_over = False
file = open('words_alpha.txt')
content = file.readlines()
wordBank = getWords(content, initial[0])
difficulty = initial[1]
missesLeft = initial[2]
guessWord = getWord(wordBank)
guessWordAsList = ['_' for let in guessWord]
alphabet = 'abcdefghijklmnopqrstuvwxyz'
button = Button(screen_width//2-50, screen_height//2-100, button_img)
streak = 0
highscore = 0
i = 0


run = True
while run == True:
    p = False
    screen.fill(white)
    screen.blit(og, (150, 50))
    draw_text(wordDisplay(guessWordAsList), font1, black, 50, 600)
    draw_text(alphabet, font1, black, 50, 700)
    draw_text('Highscore: ' + str(highscore), font, black, 500, 50)
    draw_text('Streak: ' + str(streak), font, black, 500, 300)
    update()
    if game_over == True:
        if i == 0:
            if missesLeft > 0:
                print('Congrats, you won with ' + str(missesLeft) + " guesses left! The word was " + guessWord + '.')
                print('If you wish to continue the streak, please press the button.')
                streak += 1
                if streak > highscore:
                    highscore = streak
                i += 1
            else:
                print('You lost! The word was ' + guessWord + '.')
                print('Press the button to restart your streak.')
                streak = 0
                i += 1
        if button.draw() == True:
            game_over = False
            p = True
            reset_game()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    if game_over == False and p == False:
        response = letterGuess(alphabet)
        alphabet = response[1]
        guessWordAsList = updateWord(guessWord, guessWordAsList, response[0])
        processed = processGuess(response[0], guessWord, missesLeft)
        missesLeft = processed[1]
        correct = processed[0]
        print(alphabet)
        if correct == True:
            print('You are correct! Good guess.')
        else:
            print('Uh oh, you missed. You have ' + str(missesLeft) + ' guesses left')
        if missesLeft <= 0 or ([item for item in guessWordAsList if item=='_']) == []:
            print('game over')
            game_over = True
print('Game over! Your highscore was ' + highscore)
pygame.quit()
