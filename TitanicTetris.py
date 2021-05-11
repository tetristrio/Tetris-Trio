# imports
import pygame
from random import *
import random
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# sets the screen
screen_width = 1000
screen_height = 790
display_width = 600
display_height = 600

# how big the blocks are
block_size = 30

# sets the top corner of the screen
x_topleft = (screen_width - display_width) // 2
y_topleft = (screen_height - display_height)

# plays background music
pygame.mixer.music.load('TetrisSound.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# list of available shapes that can be used and their rotation
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....',],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

H = [['.....',
      '.000.',
      '.000.',
      '.000.',
      '.....']]

E = [['.....',
      '00000',
      '00000',
      '.....',
      '.....'],
     ['..00.',
      '..00.',
      '..00.',
      '..00.',
      '..00.']]

W = [['.....',
      '0.0.0',
      '00000',
      '.....',
      '.....'],
     ['..00.',
      '..0..',
      '..00.',
      '..0..',
      '..00.'],
     ['.....',
      '.....',
      '00000',
      '0.0.0',
      '.....'],
     ['.00..',
      '..0..',
      '.00..',
      '..0..',
      '.00..']]

J = [['.....',
      '.000.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '...0.',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.000.',
      '.....'],
     ['.....',
      '.0...',
      '.000.',
      '.0...',
      '.....']]

Y = [['.....',
      '.000.',
      '.0.0.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '...0.',
      '..00.',
      '.....'],
     ['.....',
      '.0.0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '.00..',
      '.0...',
      '.00..',
      '.....']]

blocks = [T, Z, S, O, I, L, J, H, E, W, J, Y]
blocks_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128), (200, 200, 200), (128, 128, 0), (200, 128, 128), (128, 0, 255), (255, 128, 128)]

# class creates the block and where it can be positioned
class Block(object):
    rows = 20
    columns = 20

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = blocks_colors[blocks.index(shape)]
        self.rotation = 0

# makes the playable grid
def make_grid(lock_positions = {}):
    grid = [[(0,0,0) for x in range(20)] for x in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in lock_positions:
                c = lock_positions[(j,i)]
                grid[i][j] = c
    return grid

# will change the shape after the shape can't move anymore
def format_changeshape(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i, position in enumerate(positions):
        positions[i] = (position[0] - 2, position[1] - 4)
    return positions

# function that determines the space that can be used
def space_valid(shape, grid):
    right_positions = [[(j, i) for j in range(20) if grid[i][j] == (0,0,0)] for i in range(20)]
    right_positions = [j for sub in right_positions for j in sub]
    formatted = format_changeshape(shape)
    for position in formatted:
        if position not in right_positions:
            if position[1] > -1:
                return False
    return True

# function that deletes blocks
def lost_blocks(positions):
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False

# will pick a random shape
def obtain_shape():
    global blocks, blocks_colors
    return Block(5, 0, random.choice(blocks))

# will draw the text to the top of the screen
def draw_text_top(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label, (x_topleft + display_width/2 - (label.get_width() / 2), 100))
    
# will draw the text to the middle of the screen
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label, (x_topleft + display_width/2 - (label.get_width() / 2), y_topleft + display_height/2 - label.get_height()/2))

# will draw the text near the bottom of the screen
def draw_text_bottom(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold = True)
    label = font.render(text, 1, color)
    surface.blit(label, (x_topleft + display_width/2 - (label.get_width() / 2), 570))

#draws the grid that will be played on
def draw_grid(surface, row, col):
    sx = x_topleft
    sy = y_topleft
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i*30), (sx + display_width, sy + i*30))
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*30, sy), (sx + j*30, sy + display_height))

#function that clears the rows once a full row is completed
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
                
    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc
                
# function will display the next shape that is going to be displayed
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('bold', 40)
    label = font.render('Next Shape', 1, (255, 0, 255))
    sx = x_topleft + display_width - 200
    sy = 30
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30 +100, sy + i*30 +30 , 30, 30), 0)
    surface.blit(label, (sx + 100, sy + 10))

# function displays the window
def draw_window(surface, score = 0):
    root.blit(background3,(0,0))
    font = pygame.font.SysFont('bold', 60)
    label = font.render('Titanic Tetris', 1, (255, 0, 255))
    surface.blit(label, (x_topleft + display_width / 2 - (label.get_width() / 2), 30))
    
    font = pygame.font.SysFont('bold', 60)
    label = font.render('Score: ' + str(score), 1, (255, 0, 255))
    sx = x_topleft - 200
    sy = y_topleft
    surface.blit(label, (sx, 30))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (x_topleft + j*30, y_topleft + i*30, 30, 30), 0)
    draw_grid(surface, 20, 20)
    pygame.draw.rect(surface, (255, 255, 0), (x_topleft, y_topleft, display_width, display_height), 5)
    
# main program
def mainProgram():
    global grid

    # locks the position after the piece can't move anymore
    lock_position = {}
    grid = make_grid(lock_position)

    change_block = False
    run = True
    current_block = obtain_shape()
    next_block = obtain_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    while run:
        #sets the fall speed of each block
        global fall_speed
        fall_speed = 0.27
        if score >= 100:
            fall_speed -= 0.10

        if score >= 200:
            fall_speed -= 0.13

        if score >= 300:
            fall_speed -= 0.17

        if score >= 500:
            fall_speed -= 0.2

        grid = make_grid(lock_position)
        fall_time += clock.get_rawtime()
        clock.tick(60)

        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_block.y += 1
            if not(space_valid(current_block, grid)) and current_block.y > 0:
                current_block.y -= 1
                change_block = True

        # for if the player isn't playing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            #if the key equals down, the game starts
            if event.type == pygame.KEYDOWN:
                
                # if the key equals left, moves block to the left
                if event.key == pygame.K_LEFT:
                    current_block.x -= 1
                    if not space_valid(current_block, grid):
                        current_block.x += 1

                # if key equals right, block moves to the right
                elif event.key == pygame.K_RIGHT:
                    current_block.x += 1
                    if not space_valid(current_block, grid):
                        current_block.x -= 1

                # if key equals up, the block rotation is different
                elif event.key == pygame.K_UP:
                    current_block.rotation = current_block.rotation + 1 % len(current_block.shape)
                    if not space_valid(current_block, grid):
                        current_block.rotation = current_block.rotation - 1 % len(current_block.shape)

                # if key equals down, block moves down a level
                elif event.key == pygame.K_DOWN:
                    current_block.y += 1
                    if not space_valid(current_block, grid):
                        current_block.y -= 1
                #if key equals space, block moves down to last level
                elif event.key == pygame.K_SPACE:
                    while space_valid(current_block, grid):
                        current_block.y += 1
                    current_block.y -= 1
                

        shape_position = format_changeshape(current_block)

        # changes the roation based on the list of shapes
        for i in range(len(shape_position)):
            x, y = shape_position[i]
            if y > -1:
                grid[y][x] = current_block.color

        # changes the block based on where it is positioned
        if change_block:
            for position in shape_position:
                p = (position[0], position[1])
                lock_position[p] = current_block.color
            current_block = next_block
            next_block = obtain_shape()
            change_block = False
            score += clear_rows(grid, lock_position) * 10
            if clear_rows(grid, lock_position) == 4:
                score += 10

        # draws the window and puts the block in the grid
        draw_window(root, score)
        draw_next_shape(next_block, root)
        pygame.display.update()

        if lost_blocks(lock_position):
            run = False

    # game over image
    root.blit(background2, (0, 0))
    # delay for text to be displayed
    pygame.display.update()
    pygame.time.delay(5000)
    
# function creates the main window that displays the game
def main_window():
    run = True
    while run:
        # Background Image
        root.blit(background, (0, 0))
        # displays the title
        draw_text_top('Titanic Tetris', 80, (255, 0, 255), root)
        # displays the press any key
        draw_text_bottom('Press the button to start...', 59, (255, 0, 255), root)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                mainProgram()

    pygame.quit()

# sets the display to properly display images
root = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Titanic Tetris')

# Main menu background
background = pygame.image.load('TetrisImage.jpg')

# Game over background
background2 = pygame.image.load('TitanicTetrisImage.jpg')

# Ship image
background3 = pygame.image.load('TitanicShip.jpg')

# runs the main window
main_window()
