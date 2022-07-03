import cv2 as cv
import numpy as np
import randomcolor
import random
import tqdm

N = 300 

N_colors = 3

grid = np.zeros((N, N, 3),  np.uint8) + 255

rand_color = randomcolor.RandomColor()
str_colors = rand_color.generate( count=N_colors, format_='rgb')
colors = []

show_grid = False
use_colors = True

thresh = 2

for color in str_colors:
	col = tuple(map(int, color[4:-1].split(', ')))
	colors.append(col)
if use_colors:
    for i in tqdm.tqdm(range(N)):
        for j in range(N):
            grid[i, j] = random.choice(colors)

else:
    for i in tqdm.tqdm(range(N)):
        for j in range(N):
            grid[i, j] = random.choice([0, 255, 255])


def out_of_bounds(i, j):
    if i<0 or j<0 or i>=N or j>=N:
        return True

def can_live(i, j):
    alive_count = 0
    mv = [-1, 0 , 1]
    for dx in mv:
        for dy in mv:
            
            nx, ny = i+dx, j+dy
            
            if out_of_bounds(nx, ny) or (dx==0 and dy==0):
                continue

            if grid[nx, ny][0] == 0:
                alive_count+=1

    if alive_count < 2: #loneliness
        return False
    
    if alive_count > 3: #overcrowding
        return False

    return True

def cyclic_automaton():
   
    if show_grid:
        cv.imshow('grid', grid)
        cv.waitKey(0)
    
    def check_next_neighbours(i, j, idx):
                
        next_idx = (idx+1) % N_colors
        count_next_neighbours = 0
        
        mv = [-1, 0 , 1]
        
        for dx in mv:
            for dy in mv:
                nx, ny = i+dx, j+dy
            
                if out_of_bounds(nx, ny) or (dx==0 and dy==0):
                    continue

                if tuple(grid[nx, ny]) == colors[next_idx]:
                    count_next_neighbours+=1
        
        if count_next_neighbours >= thresh:
            return True
        
        return False
        
    epochs = 50

    for ep in range(epochs):
        
        for i in range(N):
            
            for j in range(N):
                idx = -1
                
                for k in range(N_colors):
                    if colors[k] == tuple(grid[i, j]):
                        idx = k
                       
                if check_next_neighbours(i, j, idx):
                    grid[i, j] = colors[(idx + 1) % N_colors]
        print('Tick: ', ep)
        cv.imwrite('img'+str(ep)+'.jpg', grid)
        if show_grid:
            cv.imshow('Grid', grid)
            cv.waitKey(1)
cyclic_automaton()
exit()

def play():
    epochs = 50
    for i in range(epochs):
        for i in range(N):
            for j in range(N):
                if(can_live(i, j)):
                    grid[i, j] = 0
                else: 
                    grid[i, j] = 255 #die

        cv.imshow('Grid', grid)
        cv.waitKey(1)

cv.imshow('Initial Grid', grid)
cv.waitKey(0)
play()

cv.imshow('Grid', grid)
cv.waitKey(0)
cv.destroyAllWindows()
#cv.waitKey(1)    
