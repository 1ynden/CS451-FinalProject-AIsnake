from pygame import display, time, draw, QUIT, init
from random import randint
import pygame
from numpy import sqrt
init()

done = False
BLACK = (0, 0, 0)
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

def getAction(food, snake):
    food.prev = []
    for seg in snake:
        seg.prev = []
    openset = [snake[-1]]
    closedset = []
    returnDir = 0
    while True:
        # PANIC MODE!
        # Originally this made a new path targeting the closest tail segment like this:
        #   return getAction(snake[0], snake[1:])
        # This was very effective, but the snake would occasionally just pass through
        # itself because the snake was reduced to account for new tail. 
        # Instead, I just have the snake traverse to some random location that it can access
        # in hopes that wasting time will open up the body of the snake to reveal the food!
        if not openset:
            dummyfood = grid[0][0]
            while True:
                dummyfood = grid[randint(0, rows - 1)][randint(0, cols - 1)]
                if not (dummyfood in snake):
                    break
            return getAction(dummyfood, snake)
        
        # Pick the next space based on the computed minimum distance score
        min = 65535
        for place in openset:
            if(place.distScore < min):
                min = place.distScore
                head = place
        
        # Move currently investigated space from open to closed set
        openset.remove(head)
        closedset.append(head)
        
        for action in head.legalActions:
            if action not in closedset and action not in snake:
                tempMin = action.moveDist + 1
                if action in openset:
                    if tempMin < action.moveDist:
                        action.moveDist = tempMin
                else:
                    action.moveDist = tempMin
                    openset.append(action)
                
                # Distance score is computed as a combination of our Manhattan ...
                # ...distance (manDist) and distance traveled from starting point (moveDist)
                action.manDist = sqrt((action.x - food.x) ** 2 + (action.y - food.y) ** 2)
                action.distScore = action.moveDist + action.manDist
                action.prev = head
        
        # Exit the while loop when we get to the destination
        if head == food:
            break
    
    # The last entry will be returned (because it's in reverse order)
    while head.prev:
        if head.x == head.prev.x and head.y > head.prev.y:
            returnDir = 0
        elif head.x > head.prev.x and head.y == head.prev.y:
            returnDir = 1
        elif head.x == head.prev.x and head.y < head.prev.y:
            returnDir = 2
        elif head.x < head.prev.x and head.y == head.prev.y:
            returnDir = 3
        
        head = head.prev
    # Clean up the grid spaces
    for i in range(rows):
        for j in range(cols):
            grid[i][j].prev = []
            grid[i][j].distScore = 0
            grid[i][j].moveDist = 0
            grid[i][j].manDist = 0
    return returnDir


class Space:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.distScore = 0
        self.moveDist = 0
        self.manDist = 0
        self.legalActions = []
        self.prev = []

    def getLegalActions(self):
        if self.x > 0:
            self.legalActions.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.legalActions.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.legalActions.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.legalActions.append(grid[self.x][self.y + 1])


grid = [[Space(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].getLegalActions()

snake = [grid[rows//2][cols//2]]
food = grid[randint(0, rows-1)][randint(0, cols-1)]
head = snake[-1]

while not done:
    clock.tick(12)
    dis.fill(BLACK)
    if dir == 0:
        snake.append(grid[head.x][head.y + 1])
    elif dir == 1:
        snake.append(grid[head.x + 1][head.y])
    elif dir == 2:
        snake.append(grid[head.x][head.y - 1])
    elif dir == 3:
        snake.append(grid[head.x - 1][head.y])
    head = snake[-1]

    if head.x == food.x and head.y == food.y:
        while True:
            food = grid[randint(0, rows - 1)][randint(0, cols - 1)]
            if not (food in snake):
                break
    else:
        snake.pop(0)
        
    dir = getAction(food, snake)

    for seg in snake:
        draw.rect(dis, GREEN, [seg.x*blockH, seg.y*blockW, blockH, blockW])

    draw.rect(dis, RED, [food.x*blockH, food.y*blockW, blockH, blockW])
    display.flip()