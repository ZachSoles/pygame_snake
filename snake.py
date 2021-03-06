import pygame
import sys
import random

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480

GRID_SIZE = 20
GRID_WIDTH = SCREEN_HEIGHT / GRID_SIZE
GRID_HEIGHT = SCREEN_WIDTH / GRID_SIZE

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17,24,47)

    def get_head_pos(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def rest(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2),(SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def move(self):
        cur = self.get_head_pos()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.rest()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class Food(object):
    def __init__(self):
        self.pos = (0, 0)
        self.color = (233, 163 ,49)
        self.randomize_pos()

    def randomize_pos(self):
        self.pos = (random.randint(0,GRID_WIDTH-1) * GRID_SIZE, random.randint(0,GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        r = pygame.Rect((self.pos[0], self.pos[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                r2 = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (84, 194, 205), r2)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    drawGrid(surface)

    snake = Snake()
    food = Food()
    myfont = pygame.font.SysFont("monospace", 16)
    score = 0
    while (True):
        clock.tick(10)
        snake.handle_input()
        drawGrid(surface)
        snake.move()
        if snake.get_head_pos() == food.pos:
            snake.length += 1
            score += 1
            food.randomize_pos()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render("Score {0}".format(score), 1, (0, 0, 0))
        screen.blit(text, (5,10))
        pygame.display.update()


main()
