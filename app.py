# Import the pygame library and initialise the game engine
import pygame
import numpy as np

# Variables
COLOR = (139,23,137)
WHITE = (255,255,255)
PDL_WIDTH = 10
PDL_HEIGHT = 100
WIDTH = 800
HEIGHT = 600
PDL_SPEED = 10
RADIUS = 10
MAX_SCORE = 11

class Ball(pygame.sprite.Sprite):
    #This class represents a ball. It derives from the "Sprite" class in Pygame.
    
    def __init__(self, color, width, height, RADIUS):
        # Call the parent class (Sprite) constructor
        super().__init__()
        
        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        self.RADIUS = RADIUS
        self.width = width
        self.height = height
        self.velocity = [np.random.randint(2, 5), np.random.randint(-4, 5)]
 
        # Draw the ball (a circle)
        pygame.draw.circle(self.image, color, (self.width // 2, self.height //2), self.RADIUS)
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.centerx += self.velocity[0]
        self.rect.centery += self.velocity[1]
    
    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = np.random.uniform(-4, 5)

class Paddle(pygame.sprite.Sprite):
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
 
        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, self.width, self.hight])
        
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
    
    def moveUp(self, pixels):
        self.rect.y -= pixels
		#Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
          
    def moveDown(self, pixels):
        self.rect.y += pixels
	    #Check that you are not going too far (off the screen)
        if self.rect.y > (HEIGHT - self.hight):
          self.rect.y = (HEIGHT - self.hight)

# Open a new window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CameBush Pong")

paddleA = Paddle(COLOR, PDL_WIDTH, PDL_HEIGHT)
paddleA.rect.x = 0
paddleA.rect.y = (HEIGHT - PDL_HEIGHT) // 2

paddleB = Paddle(COLOR, PDL_WIDTH, PDL_HEIGHT)
paddleB.rect.x = WIDTH - PDL_WIDTH
paddleB.rect.y = (HEIGHT - PDL_HEIGHT) // 2

ball = Ball(COLOR, 2*RADIUS,2*RADIUS,RADIUS)
ball.rect.centerx = WIDTH // 2
ball.rect.centery = HEIGHT // 2

#This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the paddles to the list of sprites
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
finish = False

# The self.clock will be used to control how fast the self.screen updates
clock = pygame.time.Clock()

# initilize players scores
scoreA, scoreB= 0, 0

while not finish:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finish = True
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        paddleB.moveUp(PDL_SPEED)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(PDL_SPEED)
    if keys[pygame.K_a]:
        paddleA.moveUp(PDL_SPEED)
    if keys[pygame.K_q]:
        paddleA.moveDown(PDL_SPEED)
    
    # update ball position
    ball.update()

    # detect collision between de self.ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()
    #Check if the self.ball is bouncing against any of the 4 walls:
    if ball.rect.centerx > (WIDTH - RADIUS):
        (ball.rect.centerx, ball.rect.centery) = (WIDTH //2, HEIGHT //2)
        ball.velocity[0] *= -1
        scoreA +=1
    if ball.rect.centerx < RADIUS:
        (ball.rect.centerx, ball.rect.centery) = (WIDTH //2, HEIGHT //2)
        ball.velocity[0] *= -1
        scoreB += 1
    if ball.rect.centery > (HEIGHT - RADIUS):
        ball.velocity[1] *= -1
    if ball.rect.centery < RADIUS:
        ball.velocity[1] *= -1
    
    # --- Drawing code should go here
    # First, clear the self.screen to white. 
    screen.fill(WHITE)
    #Draw the net
    pygame.draw.line(screen, COLOR, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 5)

    #Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    #display scores
    pygame.font.init()
    font = pygame.font.Font(None,74)
    text = font.render(str(scoreA), 1, COLOR)
    screen.blit(text,(WIDTH // 4, 10))
    text = font.render(str(scoreB), 1, COLOR)
    screen.blit(text,(3*WIDTH // 4, 10))

    # --- Game logic should go here
    all_sprites_list.update()

    # --- Go ahead and update the self.screen with what we've drawn.
    pygame.display.flip()

    clock.tick(60)

    if scoreA == MAX_SCORE or scoreB == MAX_SCORE:
        finish = True
        pygame.quit()