import pygame
import numpy

class snake():
    def __init__(self, r, g, b, gridsize, speed, screen) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.gridsize = gridsize
        self.speed = speed
        self.speedx = 1
        self.speedy = 0
        self.screen = screen
        self.spawning = True
    def screensize(self, height, width) -> None:
        self.height = height
        self.width = width
        self.size = self.gridsize - 10
    def playgame(self) -> None:
        randomize = True # Used for when a new red fruit is spawned and is then spawned randomly
        itempositionx = 0  # Position of the item (fruit) x-cord
        lastpositionsx = [] #records the last position of the head of the snake. The length of the list is dependent on the length of the snake. For x-cord.
        movelist = [] #Helps when player does multiple inputs before a move (Ex. W,A,S; the next 3 moves would be those inputs) 
        moved = False #Sees if a key in movelist moved the snakes direction
        lastpositionsy = [] #records the last position of the head of the snake. The length of the list is dependent on the length of the snake. For y-cord.
        posiblist = [[0 for i in range(2)] for i in range((self.width // self.gridsize)**2)] # For all possible grid positions. Init.
        amount = 1 # How long the snake is
        itempositiony = 0 # Position of the item (fruit) y-cord
        decamountblue = int(numpy.floor(self.b/(self.width // self.gridsize)**2)) # Following decamount vars help with the gradient affect on snake
        decamountred = int(numpy.floor(self.r/(self.width // self.gridsize)**2))
        decamountgreen = int(numpy.floor(self.g/(self.width // self.gridsize)**2))
        running = True # Condition for running game
        tick = 0 # How often the snake moves
        coun = 0
        for i in range((self.width // self.gridsize)):
            for j in range((self.height // self.gridsize)):
                posiblist[coun][0] = i * self.gridsize
                posiblist[coun][1] = j * self.gridsize
                coun+=1
        def checkclick(): # function checks if W,A,S, or D is clicked
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if amount == 1:
                            self.speedx = 0
                            self.speedy = -1
                            movelist.append("W")
                        else:
                            if self.speedy != 1:
                               self.speedx = 0
                               movelist.append("W")
                    if event.key == pygame.K_s:
                        if amount == 1:
                            self.speedx = 0
                            self.speedy = 1
                            movelist.append("S")
                        else:
                            if self.speedy != -1:
                               self.speedx = 0
                               movelist.append("S")
                    if event.key == pygame.K_d:
                        if amount == 1:
                            self.speedx = 1
                            self.speedy = 0
                            movelist.append("D")
                        else:
                            if self.speedx != -1:
                               self.speedy = 0
                               movelist.append("D")
                    if event.key == pygame.K_a:
                        if amount == 1:
                            self.speedx = -1
                            self.speedy = 0
                            movelist.append("A")
                        else:
                            if self.speedx != 1:
                               self.speedy = 0
                               movelist.append("A")
        def randomitemspawn(randomize, x, y, lastposx, lastposy): # Randomly puts fruit where snake isn't
            if randomize:
                l3 = posiblist.copy()
                for i in range(amount):
                    try:
                        l3.remove([lastposx[i] - int((self.gridsize - self.size)/2), lastposy[i] - int((self.gridsize - self.size)/2)])
                    except Exception as e:
                        pass
                randoms = numpy.random.randint(0, len(l3))
                randomintx = l3[randoms][0] + int((self.gridsize - self.size)/2)
                randominty = l3[randoms][1] + int((self.gridsize - self.size)/2)
                rectang = pygame.Rect(randomintx, randominty, self.size, self.size)
                pygame.draw.rect(self.screen, pygame.Color(255,0,0), rectang)
                return randomintx, randominty
            else:
                rectang = pygame.Rect(x, y, self.size, self.size)
                pygame.draw.rect(self.screen, pygame.Color(255,0,0), rectang)
                return x, y 
        while running:
            checkclick()
            self.screen.fill((0,0,0)) # Fills the screen
            f = False
            for i in range(self.width // self.gridsize): # Makes checker pattern
                switched = False
                for j in range(self.height // self.gridsize):
                    rectang = pygame.Rect(i * self.gridsize, j * self.gridsize, self.gridsize, self.gridsize)
                    if i != 0 and not switched:
                        f = not f
                        switched = True 
                    if f:
                        pygame.draw.rect(self.screen, pygame.Color(0,255,0), rectang)
                    else:
                        pygame.draw.rect(self.screen, pygame.Color(0,100,0), rectang)
                    f = not f
            tick += .01 * self.speed # Adding the speed to tick
            if self.spawning:
                position = [0,0]
                position[0] = ((self.gridsize)) 
                position[1] = ((self.gridsize)) 
                lastpositionsx.append(position[0])
                lastpositionsy.append(position[1])
            checkclick()
            self.spawning = False
            if tick >= 1: # Once tick is greater than 1 move the snake
                tick = 0
                counter = 0
                counter2 = 0
                for i in movelist: # movelist seeing if there were multiple inputs before move
                    counter += 1
                    if counter < 2:
                        if i == "W":
                            self.speedy = -1
                            self.speedx = 0
                            position[1] += -1 * self.gridsize
                        elif i == "S":
                            self.speedy = 1
                            self.speedx = 0
                            position[1] += 1 * self.gridsize
                        elif i == "D":
                            self.speedx = 1
                            self.speedy = 0
                            position[0] += 1 * self.gridsize
                        elif i == "A":
                            self.speedx = -1
                            self.speedy = 0
                            position[0] += -1 * self.gridsize
                    moved = True
                if not moved: # If no more inputs move in constant direction
                    position[0] += self.speedx * self.gridsize
                    position[1] += self.speedy * self.gridsize
                lastpositionsx.append(position[0] + int((self.gridsize - self.size)/2)) # Adding position to where the snake is and has been
                lastpositionsy.append(position[1] + int((self.gridsize - self.size)/2))
                templist = movelist
                movelist = []
                for i in templist: # Doing next move in movelist next move
                    counter2 += 1
                    if counter2 > 1:
                        movelist.append(i)
            ix, iy = randomitemspawn(randomize, itempositionx, itempositiony, lastpositionsx, lastpositionsy) #Random item spawn
            moved = False

            itempositionx = ix
            itempositiony = iy
            if position[0]  + int((self.gridsize - self.size)/2) == itempositionx and position[1]  + int((self.gridsize - self.size)/2) == itempositiony: #If the fruit and the head of the snake have the same position then increase snake length
                randomize = True
                amount+=1
            else:
                randomize = False
            if len(lastpositionsx) > amount: # Only have the most recent move(s) depending on length of snake
                lastpositionsx.pop(0)
                lastpositionsy.pop(0)
            for i in range(len(lastpositionsx) - 1): # Checking if snake is intercepting its self
                if position[0] + int((self.gridsize - self.size)/2) == lastpositionsx[i] and position[1] + int((self.gridsize - self.size)/2) == lastpositionsy[i] and i != len(lastpositionsy) - 1:
                    running = False
            if position[0] > self.width - self.size or position[0] < 0 or position[1] > self.height - self.size or position[1] < 0: #Checking if snake gets out of arena
                running = False
                print("Outside of arena")
            for i in range(amount): # Depending on the amount, the snake will be a certain length and the position of the next square of the snake is in lastpositionx or y. Gradient changes based on how far from head.
                try:
                    rectang = pygame.Rect(lastpositionsx[i], lastpositionsy[i], self.size, self.size)
                    pygame.draw.rect(self.screen, pygame.Color(self.r - decamountred * (amount - i), self.g - decamountgreen * (amount - i), self.b - decamountblue * (amount - i)), rectang)
                except Exception as e:
                    pass
            if amount == (self.width // self.gridsize)**2: # If the length of the snake is the amount of grids there are, then you win
                running = False
            for event in pygame.event.get(): # If player gets out of window quit game
                if event.type == pygame.QUIT:
                    running = False
            checkclick()
            pygame.display.update() # Updates game

background_color = (0,0,0) 
  
# Define the dimensions of 
# screen object(width,height) 
screen = pygame.display.set_mode((600, 600)) 
  
# Set the caption of the screen 
pygame.display.set_caption('Geeksforgeeks') 
  
# Fill the background colour to the screen 
screen.fill(background_color) 
  
# Update the display using flip 
pygame.display.flip() 
  
# Variable to keep our game loop running 
running = True
game = snake(r=0,g=100,b=255, gridsize=100, speed=.75, screen=screen) #r,g,b is the color of the snake
game.screensize(600, 600)
# game loop 

game.playgame()

