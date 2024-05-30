# Installing pygame
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install pygame if not already installed
try:
    import pygame
except ImportError:
    install('pygame')

import math
import random
import pygame
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))  # Change the screen size to 800x600

# Background
background = pygame.image.load(r'C:\Users\bilga\OneDrive\Desktop\Pyhton Project\background.jpg')
background = pygame.transform.scale(background, (800, 600))  # Resize the background to fit the screen

# Sound
mixer.music.load(r"C:\Users\bilga\OneDrive\Desktop\Pyhton Project\background.mp3")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load(r'C:\Users\bilga\OneDrive\Desktop\Pyhton Project\ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(r'C:\Users\bilga\OneDrive\Desktop\Pyhton Project\ufo.gif')
playerImg = pygame.transform.scale(playerImg, (50, 50))  # Resize player image to 50x50
playerX = 370
playerY = 530  # Place the player at the bottom of the screen
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12  

for i in range(num_of_enemies):
    enemy_image = pygame.image.load(r'C:\Users\bilga\OneDrive\Desktop\Pyhton Project\enemy.png')
    enemy_image = pygame.transform.scale(enemy_image, (50, 50))  
    enemyImg.append(enemy_image)
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load(r'C:\Users\bilga\OneDrive\Desktop\Pyhton Project\bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (50, 50))  
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

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
    screen.blit(bulletImg, (x + 20, y + 10))  # Adjust bullet position

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

# Game Loop
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
                bulletSound = mixer.Sound(r"C:\Users\bilga\OneDrive\Desktop\Pyhton Project\shoot.wav")
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
                explosionSound = mixer.Sound(r"C:\Users\bilga\OneDrive\Desktop\Pyhton Project\explosion.wav")
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
    clock.tick(60)  # Cap the frame rate to 60 FPS

pygame.quit()
sys.exit()
