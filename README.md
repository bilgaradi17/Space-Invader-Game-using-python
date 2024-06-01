# Space-Invader-Game-using-python

## How to Play
Move Left: Press the left arrow key.
Move Right: Press the right arrow key.
Shoot: Press the spacebar.


## Game Elements
Player: The spaceship controlled by the player.
Enemies: Multiple enemies that move horizontally and descend towards the player.
Bullet: The projectile fired by the player to hit the enemies.
Score: The player's score, which increases when an enemy is hit.
Game Over: The state when an enemy reaches the bottom of the screen.


## Detailed Explanation of the Code
### Libraries and Initialization
```
import subprocess
import sys
import pygame
import random
from pygame import mixer

# Initialize Pygame
pygame.init()

# Create the screen (800x600)
screen = pygame.display.set_mode((800, 600))
```
pygame.init(): Initializes all the Pygame modules.
pygame.display.set_mode(): Creates a window of size 800x600 pixels.


### Background and Sound
```
# Load and resize background image
background = pygame.image.load('path/to/background.jpg')
background = pygame.transform.scale(background, (800, 600))

# Load and play background music
mixer.music.load('path/to/background.mp3')
mixer.music.play(-1)
```
pygame.image.load(): Loads an image file.
pygame.transform.scale(): Resizes the image to fit the screen.
mixer.music.load(): Loads the background music file.
mixer.music.play(-1): Plays the background music in a loop.


### Caption and Icon
```
# Set window caption and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('path/to/ufo.png')
pygame.display.set_icon(icon)
```
pygame.display.set_caption(): Sets the window title.
pygame.display.set_icon(): Sets the window icon.


### Player Setup
```
# Load and resize player image
playerImg = pygame.image.load('path/to/ufo.gif')
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = 370
playerY = 530
playerX_change = 0
```
playerImg: The player’s spaceship image, resized to 50x50 pixels.
playerX, playerY: Initial position of the player.


### Enemy Setup
```
# Enemy setup
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

for i in range(num_of_enemies):
    enemy_image = pygame.image.load('path/to/enemy.png')
    enemy_image = pygame.transform.scale(enemy_image, (50, 50))
    enemyImg.append(enemy_image)
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)
```
enemyImg: List to store enemy images.
enemyX, enemyY: Lists to store the positions of enemies.
random.randint(): Generates random positions for enemies.


### Bullet Setup
```
# Bullet setup
bulletImg = pygame.image.load('path/to/bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (50, 50))
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"
bulletImg: Bullet image, resized to 50x50 pixels.
bullet_state: Indicates if the bullet is ready to be fired or is currently moving.
Score Display
python
Copy code
# Score display
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10
```
score_value: Stores the player’s score.
pygame.font.Font(): Loads the font for displaying the score.


### Game Over Display
```
# Game Over display
over_font = pygame.font.Font('freesansbold.ttf', 64)
```
over_font: Loads a larger font for the game over text.


###Utility Functions
```
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (240, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    bullet_rect = pygame.Rect(bulletX, bulletY, 10, 20)
    enemy_rect = pygame.Rect(enemyX, enemyY, 50, 50)
    return bullet_rect.colliderect(enemy_rect)

def reset_game():
    global playerX, playerY, playerX_change, bulletX, bulletY, bullet_state, score_value
    playerX = 370
    playerY = 530
    playerX_change = 0
    bulletX = 0
    bulletY = playerY
    bullet_state = "ready"
    score_value = 0
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 750)
        enemyY[i] = random.randint(50, 150)
```
show_score(): Displays the score on the screen.
game_over_text(): Displays the game over message.
player(): Draws the player image.
enemy(): Draws an enemy image.
fire_bullet(): Fires a bullet from the player’s position.
isCollision(): Checks if a bullet has collided with an enemy.
reset_game(): Resets the game state to initial values.


Game Loop
```
# Game loop
running = True
clock = pygame.time.Clock()
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bulletSound = mixer.Sound('path/to/shoot.wav')
                bulletSound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
            if game_over and event.key == pygame.K_y:
                game_over = False
                reset_game()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over:
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 750:
            playerX = 750

        for i in range(num_of_enemies):
            if enemyY[i] > 480:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                game_over = True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 750:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound('path/to/explosion.wav')
                explosionSound.play()
                bulletY = playerY
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 750)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = playerY
            bullet_state = "ready"
        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)

    if game_over:
        game_over_text()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
```
while running: Main game loop that runs until the game window is closed.
pygame.event.get(): Handles user input and game events.
player movement and boundary checks: Ensures the player stays within screen boundaries.
enemy movement and collision detection: Handles enemy behavior and checks for collisions with bullets.
game over conditions: Ends the game if enemies reach the bottom of the screen.
pygame.display.update(): Updates the screen with the latest game state.
clock.tick(60): Limits the game to 60 frames per second.
pygame.quit() and sys.exit(): Cleanly exits the game.


## Conclusion
This Space Invaders game demonstrates fundamental game development concepts using Pygame. By understanding and modifying the provided code, you can create your own variations of the game and enhance your game development skills. Enjoy coding and have fun playing!
