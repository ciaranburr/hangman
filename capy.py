import pygame
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60

screenwidth = 700
screenheight = 800

ground_scroll = 0
scroll_speed = 2

screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('Capybara Run')

bg = pygame.image.load('img/grass.png')
side = pygame.image.load('img/tree borders.png')
button_img = pygame.image.load('img/restart.png')


font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)
game_over = False
left = False
right = False
up = False
down = False
jump = False
past_obstacle = False
score = 0
start_game = 0
golf_frequency = 1500
highscore = 0
last_golf = pygame.time.get_ticks() - golf_frequency   # condition met right away


def reset_game():
    golf_group.empty()
    river_group.empty()
    ron.rect.x = int(screenwidth/2)
    ron.rect.y = int(screenheight-100)
    score = 0
    return score


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



class Capy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/still.png')
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        if game_over == False:
            if jump == False:
                self.image = pygame.image.load('img/still.png')
                self.movex = 0
                self.movey = 0
                if left == True and 150<self.rect.x:
                    self.movex += -2
                if right == True and self.rect.x<512:
                    self.movex += 2
                if up == True and self.rect.y>0:
                    self.movey += -2
                if down == True and self.rect.y<700:
                    self.movey += 3
                self.rect.x = self.rect.x + self.movex
                self.rect.y = self.rect.y + self.movey
            if jump == True:
                self.image = pygame.image.load('img/fly.png')
                self.image = pygame.transform.scale(self.image, (100, 80))
                if self.rect.y > 0:
                    self.movey = -5
                self.rect.y += self.movey
        if game_over == True:
            self.image = pygame.image.load('img/ded.png')

class Golf(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/golfer.png')
        self.image = pygame.transform.scale(self.image, (44.9, 80))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        self.rect.y += scroll_speed
        if self.rect.top > 800:
            self.kill()

class Rivers(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/river.png')
        self.image = pygame.transform.scale(self.image, (406, 30))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        self.rect.y += scroll_speed
        if self.rect.top > 800:
            self.kill()


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


capys = pygame.sprite.Group()
ron = Capy(int(screenwidth/2), int(screenheight - 100))
capys.add(ron)

golf_group = pygame.sprite.Group()

river_group = pygame.sprite.Group()

pass_group = pygame.sprite.Group()

button = Button(screenwidth//2-50, screenheight//2-100, button_img)


print("Welcome to Capybara run-Ciaran's very first coding project!")
print("\nThe controls are simple: WASD or the arrows to move")
print("\nAnd space allows you to jump over the rivers-but careful!")
print("\nYou can not move in the air, and still are out if you hit the golfers!")
print("\nAvoid falling in the river and the hitting golfers for the highest score possible")
x = input("If you are ready, enter space to begin")
while x != " ":
    x = input("Please enter space to begin")
run = True
start_game = pygame.time.get_ticks()

while run:
    clock.tick(fps)
    screen.blit(bg, (0, ground_scroll-60))
    screen.blit(side, (-2, 0))
    screen.blit(side, (551, 0))

    golf_group.draw(screen)
    river_group.draw(screen)
    capys.draw(screen)
    capys.update()
    draw_text("Highscore: " + str(highscore), font, white, 150, 20)


    if game_over == False:
        # generate new golfers
        time_now = pygame.time.get_ticks()
        if time_now - last_golf > golf_frequency:
            r = random.randint(1, 10)
            if r == 2 or r == 3 or r == 4:
                golf_width = random.randint(5, 174)
                golfer1 = Golf(golf_width+165, 0)
                golf_group.add(golfer1)
                golfer2 = Golf(530-golf_width, 0)
                golf_group.add(golfer2)
            elif r == 6:
                golf_width = random.randint(1, 116)
                golfer1 = Golf(165+golf_width, 0)
                golf_group.add(golfer1)
                golfer2 = Golf(280+golf_width, 0)
                golf_group.add(golfer2)
                golfer3 = Golf(395+golf_width, 0)
                golf_group.add(golfer3)
            elif r == 5 or r == 7 or r == 8:
                river = Rivers(350,0)
                river_group.add(river)
            else:
                golf_width = random.randint(165, 512)
                golfer = Golf(golf_width, 0)
                golf_group.add(golfer)
            last_golf = time_now
        ground_scroll += scroll_speed
        if abs(ground_scroll) > 48:
            ground_scroll = 0
        golf_group.update()
        river_group.update()
        score = (pygame.time.get_ticks()-start_game) // 100
        if score > highscore:
            highscore = score

    if pygame.sprite.groupcollide(capys, golf_group, False, False):
        game_over = True
    if jump == False:
        if pygame.sprite.groupcollide(capys, river_group, False, False):
            game_over = True


    #THIS IS THE MOST IMPORTANT PIECE, NO DISPLAY WITHOUT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                right = True
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                left = True
            if event.key == pygame.K_UP or event.key == ord('w'):
                up = True
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                down = True
            if event.key == pygame.K_SPACE:
                jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                right = False
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                left = False
            if event.key == pygame.K_UP or event.key == ord('w'):
                up = False
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                down = False
            if event.key == pygame.K_SPACE:
                jump = False
    draw_text(str(score), font, white, 500, 20)


    if game_over == True:
        capys.update()
        draw_text("RIP", font, white, int(screenwidth/2)-30, 200)
        if highscore == score:
            draw_text("New highscore!", font, white, int(screenwidth / 2)-150, 500)
        if button.draw() == True:
            game_over = False
            score = reset_game()
            start_game = pygame.time.get_ticks()
    pygame.display.update()
pygame.quit()
