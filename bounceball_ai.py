# Import the pygame library and initialise the game engine
import pygame
import numpy as np

# Variables
COLOR = (139,23,137)
WHITE = (255,255,255)
WIDTH = 800
HEIGHT = 600
RADIUS = 10
PLATFORM_PIXELS = 10
PLATFORM_WIDTH = 80
PLATFORM_HEIGHT = 10
LIFES = 3
BLOCK_WIDTH = 30
BLOCK_HEIGHT = 10
BLOCK_COLOR = (139,123,137)
VELOCITY_MAX = 9


class Platform(pygame.sprite.Sprite):
    #This class represents a paddle. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, hight):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the paddle, and its x and y position, width and hight.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, hight])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.width = width
        self.hight = hight
        self.velocity = [0,0]
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.hight])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def startPosition(self):
        self.rect.x = (WIDTH - self.width) //2
        self.rect.y = (HEIGHT - self.hight)

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        #Check that you are not going too far (off the screen)
        if self.rect.x < 0:
            self.rect.x = 0
        self.velocity[0] = -1
        #print('Platform velocity:', self.velocity[0])

    def moveRight(self, pixels):
        self.rect.x += pixels 
        #Check that you are not going too far (off the screen)
        if self.rect.x > (WIDTH - self.width):
            self.rect.x = (WIDTH - self.width)
        self.velocity[0] = +1
        #print('Platform velocity:', self.velocity[0])

    def moveAi(self, ball_position_x):
        if ball_position_x > self.rect.x + PLATFORM_WIDTH // 2:
            self.moveRight(PLATFORM_PIXELS)
        if ball_position_x < self.rect.x + PLATFORM_WIDTH // 2:
            self.moveLeft(PLATFORM_PIXELS)


class Ball(pygame.sprite.Sprite):
    #This class represents a ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, radius):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.radius = radius
        self.width = width
        self.height = height
        self.velocity = [0,0]
 
        # Draw the ball (a circle)
        pygame.draw.circle(self.image, color, (self.width // 2, self.height //2), self.radius)
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def startPosition(self, platform):
        self.rect.centerx = platform.rect.x + (PLATFORM_WIDTH //2)
        self.rect.centery = platform.rect.y - RADIUS
        self.Start = True

    def launch(self):
        self.velocity = [2,-2]
        self.Start = False

    def update(self):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]
    
    def bounce(self, object):
        print("Bounce")
        print("initial ball velocity: ", self.velocity)
        print('object velocity:', object.velocity)

        self.velocity[0] = self.velocity[0] + object.velocity[0]
        if self.velocity[0] > int(VELOCITY_MAX):
            self.velocity[0] = int(VELOCITY_MAX)
            print("Velocity limit")
        if self.velocity[0] < -int(VELOCITY_MAX):
            self.velocity[0] = - int(VELOCITY_MAX)
            print("Velocity limit")

        self.velocity[1] = -(self.velocity[1] + object.velocity[1])
        if self.velocity[1] > int(VELOCITY_MAX):
            self.velocity[1] = int(VELOCITY_MAX)
            print("Velocity limit")
        if self.velocity[1] < -int(VELOCITY_MAX):
            self.velocity[1] = - int(VELOCITY_MAX)
            print("Velocity limit")

        print("final ball velocity: ", self.velocity)

class Block(pygame.sprite.Sprite):
    #This class represents a ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, life, modifier):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.width = width
        self.height = height
        self.life = life
        self.modifier = modifier
        self.killed = False
        self.velocity = [0,0]
    
        # Draw the ball (a circle)
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.height])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def position(self, x_ref, y_ref):
        self.rect.x = (x_ref - self.width
                       
                       
                       )
        if self.rect.x > (WIDTH - self.width):
            self.rect.x = (BLOCK_WIDTH)
            self.rect.y -= BLOCK_HEIGHT

        self.rect.y = (y_ref - self.height)
        if self.rect.x > (HEIGHT - self.width):
            self.rect.x = (HEIGHT - self.width)

    def checkDestroy(self):
        self.life -= 1
        if self.life == 0:
            self.killed = True
            self.kill()
        
    

# Open a new window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bounce Ball")

platform = Platform(COLOR, PLATFORM_WIDTH, PLATFORM_HEIGHT)
platform.startPosition()

ball = Ball(COLOR, 2*RADIUS,2*RADIUS,RADIUS)
ball.startPosition(platform)

blocks = [Block(BLOCK_COLOR, BLOCK_WIDTH, BLOCK_HEIGHT,1,0) for i in range(6)]
print('Blocks created: ',len(blocks))
bw = WIDTH//2
bh = HEIGHT//2
for block in blocks:
    block.position(bw, bh)
    bw += BLOCK_WIDTH



#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the paddles to the list of sprites
all_sprites_list.add(platform)
all_sprites_list.add(ball)
all_sprites_list.add(blocks)

# The loop will carry on until lifes = 0
lifes = LIFES
score = 0
finish = False

# The self.clock will be used to control how fast the self.screen updates
clock = pygame.time.Clock()

while finish == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        elif event.type == pygame.K_ESCAPE:
            finish = True
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        platform.moveRight(PLATFORM_PIXELS)
        if ball.Start == True:
            ball.startPosition(platform)
    if keys[pygame.K_LEFT]:
        platform.moveLeft(PLATFORM_PIXELS)
        if ball.Start == True:
            ball.startPosition(platform)
    if keys[pygame.K_UP]:
        if ball.Start == True:
            ball.launch()
    platform.moveAi(ball.rect.centerx)

  
    # update ball position
    ball.update()

    # detect collision between de self.ball and the paddles
    if pygame.sprite.collide_mask(ball, platform):
        ball.bounce(platform)
        print('Platform', ball.velocity)
    for block in blocks:
        if pygame.sprite.collide_mask(ball, block):
            ball.bounce(block)
            print('Block', ball.velocity)
            block.checkDestroy()
            if block.killed == True:
                blocks.remove(block)
                score +=1
            print('Remaining blocks: ',len(blocks))
    #Check if the self.ball is bouncing against any of the 4 walls:
    if ball.rect.centerx > (WIDTH - RADIUS):
        ball.velocity[0] *= -1  # right wall
        print('Wall-Right', ball.velocity)
    if ball.rect.centerx < RADIUS:
        ball.velocity[0] *= -1  # left wall
        print('Wall-Left', ball.velocity)
    if ball.rect.centery > (HEIGHT - RADIUS):
        lifes = lifes -  1
        ball.velocity = [0,0]
        platform.startPosition()
        ball.startPosition(platform)
    if ball.rect.centery < RADIUS:
        ball.velocity[1] *= -1
        print('Wall-Top', ball.velocity)
    
        
    # --- Drawing code should go here
    # First, clear the self.screen to white. 
    screen.fill(WHITE)

    #Now let's draw all the sprites in one go.
    all_sprites_list.draw(screen)

    #display scores
    pygame.font.init()
    font = pygame.font.Font(None,54)
    textLifes = font.render('lifes '+str(lifes), 1, COLOR)
    textScore = font.render('score '+str(score), 1, COLOR)
    screen.blit(textLifes,(3*WIDTH // 4, 10))
    screen.blit(textScore,(WIDTH // 8, 10))

    # --- Game logic should go here
    all_sprites_list.update()

    # --- Go ahead and update the self.screen with what we've drawn.
    pygame.display.flip()

    clock.tick(60)

    if lifes == 0 or len(blocks) == 0:
        finish = True

    
    
