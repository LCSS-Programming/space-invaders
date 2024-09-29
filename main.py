# Initialization
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

global level
level = 1

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set title of the window
pygame.display.set_caption("Space Invaders")

# Load assets (images, sounds, etc.)
player_ship_image = pygame.image.load("player_ship.png")
asteroid_image = pygame.image.load("asteroid.png")
bullet_image = pygame.image.load("bullet.png")

# Define classes
class PlayerShip:
    def __init__(self, x, y):
        self.image = player_ship_image
        if self.image is None:
            print("Error loading player.png")
            sys.exit(1)
        # Set the desired width for the player
        desired_width = 50
        self.image = pygame.transform.scale(self.image, (
            desired_width, int(self.image.get_height() * desired_width / self.image.get_width())))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self): 
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.rect.y = 0
 
    def move_down(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height

class Asteroid:
    def __init__(self):

        global level

        self.image = asteroid_image
        if self.image is None:
            print("Error loading asteroid.png")
            sys.exit(1)
        # Set the desired width for the asteroid
        desired_width = 50
        self.image = pygame.transform.scale(self.image, (
        desired_width, int(self.image.get_height() * desired_width / self.image.get_width())))
        self.rect = self.image.get_rect()
        screen_width = pygame.display.get_surface().get_width()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(1, 5)
        if score>=19:
            if score<39:
                self.speed = random.randint(2,6)
                level=2
        if score>39:
            if score<69:
                self.speed = random.randint(3,7)
                level=3
        if score>69:
            if score<99:
                self.speed = random.randint(4,8)
                level=4
        if score>=99: 
                self.speed = random.randint(5,9)
                level=5
        

    def move(self):
        self.rect.y += self.speed

class Bullet:
    def __init__(self, x, y):
        self.image = bullet_image
        if self.image is None:
            print("Error loading bullet.png")
            sys.exit(1)
        # Set the desired width for the bullet
        desired_width = 10
        self.image = pygame.transform.scale(self.image, (
        desired_width, int(self.image.get_height() * desired_width / self.image.get_width())))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def draw_bullet(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.y -= self.speed

# Initialize variables
player_ship = PlayerShip(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
asteroids = []
bullets = []
score = 0
Lives = 3

# Game Loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type  == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player_ship.rect.x + player_ship.rect.width / 2, player_ship.rect.y)
                bullets.append(bullet)

    # Get a list of all keys currently being pressed down
    keys = pygame.key.get_pressed()

    # Move the player's ship
    if keys[pygame.K_LEFT]:
        player_ship.move_left()
    if keys[pygame.K_RIGHT]:
        player_ship.move_right()
    if keys[pygame.K_UP]:
        player_ship.move_up()
    if keys[pygame.K_DOWN]:
        player_ship.move_down()

    # Create new asteroids
    if random.randint(0, 100) < 5:
        asteroid = Asteroid()
        asteroids.append(asteroid)

    # Move asteroids
    for asteroid in asteroids:
        asteroid.move()
        if asteroid.rect.y > SCREEN_HEIGHT:
            asteroids.remove(asteroid)
            score -= 1

    # Move bullets
    for bullet in bullets:
        bullet.move()
        if bullet.rect.y < 0:
            bullets.remove(bullet)

    # Collision detection
    for asteroid in asteroids:
        if player_ship.rect.colliderect(asteroid.rect):
            if Lives==0:
                print("Game Over!")
                pygame.quit()
                sys.exit()
            else:
                Lives-=1
                asteroids.remove(asteroid)
        for bullet in bullets:
            if bullet.rect.colliderect(asteroid.rect):
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                score+=1
    if score==-1:
        print("Waring! Death immanent!")
    if score==-5:    
        print("Game Over!")
        pygame.quit()
        sys.exit()


    # Render the game screen
    screen.fill((35, 0, 32))
    screen.blit(player_ship.image, player_ship.rect)
    for asteroid in asteroids:
        screen.blit(asteroid.image, asteroid.rect)
    for bullet in bullets:
        screen.blit(bullet.image, bullet.rect)
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    text2 = font.render("Extra Lives: " + str(Lives), 1, (225, 225, 225))
    text3 = font.render("Level: " + str(level), 1, (225, 225, 225))
    screen.blit(text, (10, 10))
    screen.blit(text2, (10, 60))
    screen.blit(text3, (10, 110))
    pygame.display.flip()
    pygame.time.Clock().tick(60)