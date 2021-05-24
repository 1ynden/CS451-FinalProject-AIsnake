from pygame import display, time, draw, QUIT, init, KEYDOWN, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_q
from random import randint
import pygame
from numpy import sqrt
init()

done = False
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

cols = 30
rows = 30

width = 600
height = 600

blockW = width/cols
blockH = height/rows
dir = 1

dis = display.set_mode([width, height])
display.set_caption("Snake")
clock = time.Clock()

font_style = pygame.font.SysFont("consolas", 25)

class Space:
    def __init__(self, x, y):
        self.x = x
        self.y = y


grid = [[Space(i, j) for j in range(cols)] for i in range(rows)]

snake = [grid[rows//2][cols//2]]
food = grid[randint(0, rows-1)][randint(0, cols-1)]
head = snake[-1]
game_over = False

while not done:
    clock.tick(12)
    dis.fill(BLACK)
    
    while game_over == True:
            dis.fill(WHITE)
            mesg = font_style.render("Game Over! Press Q to quit!", True, RED)
            dis.blit(mesg, [width / 6, height / 3])
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        elif event.type == KEYDOWN:
            if event.key == K_UP and not dir == 0:
                dir = 2
            elif event.key == K_LEFT and not dir == 1:
                dir = 3
            elif event.key == K_DOWN and not dir == 2:
                dir = 0
            elif event.key == K_RIGHT and not dir == 3:
                dir = 1
    
    if dir == 0:
        if(head.y+1 >= cols):
            game_over = True
        else:
            snake.append(grid[head.x][head.y + 1])
    elif dir == 1:
        if(head.x+1 >= rows):
            game_over = True
        else:
            snake.append(grid[head.x + 1][head.y])
    elif dir == 2:
        if(head.y-1 < 0):
            game_over = True
        else:
            snake.append(grid[head.x][head.y - 1])
    elif dir == 3:
        if(head.x-1 < 0):
            game_over = True
        else:
            snake.append(grid[head.x - 1][head.y])
    head = snake[-1]
    
    if head.x >= rows or head.x < 0 or head.y >= cols or head.y < 0:
            game_over = True
    for x in snake[:-1]:
            if x == head:
                game_over = True

    if head.x == food.x and head.y == food.y:
        while 1:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food in snake):
                break
    else:
        snake.pop(0)

    for seg in snake:
        draw.rect(dis, GREEN, [seg.x*blockH, seg.y*blockW, blockH, blockW])

    draw.rect(dis, RED, [food.x*blockH, food.y*blockW, blockH, blockW])
    display.flip()