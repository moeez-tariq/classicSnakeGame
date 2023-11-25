import random
import os
path = os.getcwd() #gets path to current directory

#constants
BOARD_WIDTH = 600
BOARD_HEIGHT = 600
BOX_WIDTH = 30
BOX_HEIGHT = 30
TAIL_RADIUS = 15
VELOCITY = 30

#contains functions and attributes of the elements of the snake (head and tail)
class SnakeElements: 
    def __init__(self, x, y, R, G, B):
        self.x = x
        self.y = y
        self.r = R
        self.g = G
        self.b = B
        self.movement = "LR" #defines the current movement of the element
        #LR means the element is moving LEFT to RIGHT, UD means UP to DOWN, RL means RIGHT to LEFT and DU means DOWN to UP
        self.direction = {"UD": -(TAIL_RADIUS * 2), "DU": (TAIL_RADIUS * 2), "LR": -(TAIL_RADIUS * 2), "RL": (TAIL_RADIUS * 2)} #list to help with movement in the appropriate direction
    
    def addTail(self, R, G, B):
        if self.movement == "LR" or self.movement == "RL":
            game.appendtail(self.x + self.direction[self.movement], self.y, R, G, B) #calls function of game class to append tail in the Game class
        elif self.movement == "UD" or self.movement == "DU":
            game.appendtail(self.x, self.y + self.direction[self.movement], R, G, B)
    
    #displays elements of the snake
    def display(self):
        fill(self.r, self.g, self.b)
        circle(self.x,self.y, TAIL_RADIUS * 2)
        
class Snake(SnakeElements):
    def __init__(self,x,y,R,G,B):
        SnakeElements.__init__(self,x,y,R,G,B) #Snake Class inherits Snake Elements 
        self.frontx = "" #x coordinate of the element infront of the current element
        self.fronty = "" #y coordinate of the element infront of the current element
        self.frontmovement = "" #movement of the element infront of the current element
        self.verticalhead = loadImage(path + "/head_up.png") #load image using current path directory
        self.horizontalhead = loadImage(path + "/head_left.png")
    
    #rotating the head images provided to match the direction of movement
    def headimage(self, direction):
        if direction == "DU":
            image(self.verticalhead, game[0].x - TAIL_RADIUS, game[0].y - TAIL_RADIUS, BOX_WIDTH, BOX_HEIGHT, 0, 0, 30, 30)
        elif direction == "UD":
            image(self.verticalhead, game[0].x - TAIL_RADIUS, game[0].y - TAIL_RADIUS, BOX_WIDTH, BOX_HEIGHT, 0, 30, 30, 0)
        elif direction == "RL":
            image(self.horizontalhead, game[0].x - TAIL_RADIUS, game[0].y - TAIL_RADIUS, BOX_WIDTH, BOX_HEIGHT, 0, 0, 30, 30)
        elif direction == "LR":
            image(self.horizontalhead, game[0].x - TAIL_RADIUS, game[0].y - TAIL_RADIUS, BOX_WIDTH, BOX_HEIGHT, 30, 0, 0, 30)
    
    #movement of the head            
    def leader(self, item, directiontype):
        item.frontx = self.x #storing the coordinates of the head in a variable to be used later by the followers
        item.fronty = self.y
        item.frontmovement = self.movement
        if directiontype == 1: #head moves right
            self.x = self.x + VELOCITY
            self.movement = "LR"
        elif directiontype == 2: #head moves left
            self.x = self.x - VELOCITY
            self.movement = "RL"
        elif directiontype == 3: #head moves up
            self.y = self.y - VELOCITY
            self.movement = "DU"
        elif directiontype == 4:
            self.y = self.y + VELOCITY #head moves down
            self.movement = "UD"
            
    #movement of the tail elements that follow the element infront of them    
    def follower(self, item):
        tempx = self.x #current coordinates of the elements stored temporarily local variable
        tempy = self.y
        tempmovement = self.movement
        self.x = item.frontx #coordinates of the element infront are now the coordinates of the current element
        self.y = item.fronty
        self.movement = item.frontmovement
        item.frontx = tempx #the ex-current location and movement now stored for the elements that are next to come
        item.fronty = tempy
        item.frontmovement = tempmovement
        
    def rightkey(self, item):
        if self.movement != "RL": #to avoid snake going in a 180 degree movement
            if self == item: #if the current element is the first element in the list of elements (item)
                self.headimage("LR") #calls headimage function that sets the head image to the right direction
                self.leader(item, 1) 
            else: #if not the head of the snake
                self.follower(item)
        else:
            self.leftkey(item) #if snake is going right to left then keep going left
        
    def leftkey(self, item):
        if self.movement != "LR":
            if self == item:
                self.headimage("RL")
                self.leader(item, 2)
            else:
                self.follower(item)
        else:
            self.rightkey(item)
            
    def upkey(self, item):
        if self.movement != "UD":
            if self == item:
                self.headimage("DU")
                self.leader(item, 3)
            else:
                self.follower(item)
        else:
            self.downkey(item)
            
    def downkey(self, item):
        if self.movement != "DU":
            if self == item:
                self.headimage("UD")
                self.leader(item, 4)
            else:
                self.follower(item)
        else:
            self.upkey(item)

#fruit class deals with all matters related to fruit
class Fruit:
    def __init__(self):
        self.fruitx = 0
        self.fruity = 0
        self.type = 0
        self.bananaimage = loadImage(path + "/banana.png") #loads image provided for banana
        self.appleimage = loadImage(path + "/apple.png")
        self.randomizefruit()
        
    #randomizes location for fruit
    def randomizefruit(self):
        #ensuring the coordinates are always the top-left corner of an imaginary box in the imaginary grid
        col = (random.randint(0, BOARD_WIDTH))//BOX_WIDTH 
        row = (random.randint(0, BOARD_HEIGHT))//BOX_HEIGHT
        self.fruitx = col * BOX_WIDTH
        self.fruity = row * BOX_HEIGHT
        
        #ensuring the coordinates of fruit do not overlap with coordinates of element in the snake
        for element in game:
            if element.x - TAIL_RADIUS == self.fruitx and element.y - TAIL_RADIUS == self.fruity:
                self.randomizefruit()
        self.type = random.randint(1, 2) #chooses fruit
    
    #ensuring fruit eaten    
    def fruiteaten(self):
        #since snake elements are circles so -TAIL_RADIUS to match with top left corner 
        if self.fruitx == game[0].x - TAIL_RADIUS and self.fruity == game[0].y - TAIL_RADIUS:
            if self.type == 1: #banana
                r = 251
                g = 226
                b = 76
            else: #apple
                r = 173
                g = 48
                b = 32
            game[len(game) - 1].addTail(r, g, b) #add the element to the end of the tail and pass the colour corresponding to the fruit eaten
            game.score += 1 #increment game score
            self.randomizefruit() #generate new fruit
    
    #display randomly generated fruit    
    def display(self):
        if game.gameover == False: #do not display fruit if game is over
            if self.type == 1: #banana
                image(self.bananaimage, self.fruitx, self.fruity, BOX_WIDTH, BOX_HEIGHT)
            else: #apple
                image(self.appleimage, self.fruitx, self.fruity, BOX_WIDTH, BOX_HEIGHT)

#Game class that inherits from a list        
class Game(list):
    def __init__(self,x,y):
        self.head = Snake(x + BOX_WIDTH, y, 0, 125, 0) #append head 
        self.append(self.head)
        self.append(Snake(x, y, 80, 153, 32)) #append two tail elements where the second element is in the middle
        self.append(Snake(x - BOX_WIDTH, y, 80, 153, 32))
        self.__temp = ""
        self.gameover = False
        self.win = False
        self.score = 0
        self.restart = True #used to stop motion due to keyCode when game is restarted
    
    def appendtail(self,x, y, R, G, B):
        self.append(Snake(x, y, R, G, B)) #appends the new element of the tail to the end of Game class
    
    #controls the motion of the snake
    def keypress(self):
        #start of the game, the head looks to the right
        if self.__temp == "":
            image(self.head.horizontalhead, BOARD_WIDTH/2 + BOX_WIDTH, BOARD_HEIGHT/2, BOX_WIDTH, BOX_HEIGHT, 30, 0, 0, 30)
        if self.restart == False: #don't move until a key is pressed
            
            if keyCode == RIGHT or keyCode == LEFT or keyCode == UP or keyCode == DOWN:
                self.__temp = keyCode #ensures that the snake keeps moving even if the key is released
            for element in self: #every element moves one by one
                if keyCode == RIGHT or self.__temp == RIGHT:
                    element.rightkey(self[0]) #passes the first element (head) so that it can be the leader
                elif keyCode == LEFT or self.__temp == LEFT:
                    element.leftkey(self[0])
                elif keyCode == UP or self.__temp == UP:
                    element.upkey(self[0])
                elif keyCode == DOWN or self.__temp == DOWN:
                    element.downkey(self[0])
    
    #checks for collision
    def collision(self):
        self.gameover = False #sets the variable back to its initial state
        if self[0].x <= 0 or self[0].x  >= BOARD_WIDTH or self[0].y  <= 0 or self[0].y  >= BOARD_HEIGHT: #checks for border detection
            self.gameover = True
            return self.gameover
        for element in self:
            if element != self[0]:
                if element.x == self[0].x and element.y == self[0].y: #checks if the head collides with any other element in the snake
                    self.gameover = True        
        return self.gameover
    
    #checks to see if you have won the game
    def win(self):
        if len(self) == (BOARD_WIDTH/BOX_WIDTH) * (BOARD_HEIGHT/BOX_HEIGHT): #if the elements in the snake are equal to the number of boxes in the game
            self.win = True
            self.gameover = True
            
    #displays score
    def score_display(self):
        fill(0, 0, 0)
        textSize(15)
        text("Score: " + str(self.score), BOARD_WIDTH - 78, 15)
   
    def display(self):
        if self.collision() == False: #ensures snake elements dont get displayed when the game is over
            for elements in self:
                elements.display()
            self.score_display()
            self.keypress()

        
game = Game(BOARD_WIDTH/2 + BOX_WIDTH/2, BOARD_HEIGHT/2 + BOX_HEIGHT/2) #ensures initial elements placed centre of the board
fruit = Fruit()

#grid lines commented out
#def gridlines():
#    for i in range(BOARD_HEIGHT + 1):
#       if i % BOX_WIDTH == 0:
#          line(i,0,i,BOARD_WIDTH)
#          line(0,i,BOARD_HEIGHT,i)

def setup():
    size(BOARD_WIDTH, BOARD_HEIGHT)
    
def draw():
    if frameCount % 6 == 0 and game.gameover == False: #framecount % 6 == 0 to make it slower (but faster than %12)
        background(205)
        #gridlines()
        fruit.fruiteaten()
        fruit.display()
        game.display()
    if game.gameover == True:
        background(205) #redraws only the background
        textSize(60)
        #displays appropriate messages
        if game.win == False:
            text("GAME OVER!", BOARD_WIDTH/2 - 170, BOARD_HEIGHT/2 - 50)
            textSize(28)
            text("Score: " + str(game.score), BOARD_WIDTH/2 - 55, BOARD_HEIGHT/2)
        else:
            text("GAME OVER!", BOARD_WIDTH/2 - 170, BOARD_HEIGHT/2 - 50)
            textSize(28)
            text("YOU WIN!", BOARD_WIDTH/2 - 55, BOARD_HEIGHT/2)
        
def keyPressed():
    game.restart = False #only causes movement when a key is pressed


def mouseClicked():
    global game, fruit, restart
    if game.gameover == True:
        game = Game(BOARD_WIDTH/2 + BOX_WIDTH/2, BOARD_HEIGHT/2 + BOX_HEIGHT/2) #restarts game and resets all the attributes
        fruit = Fruit()
