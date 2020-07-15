import pygame
import random
import math
from pygame import mixer
from flask import Flask
app = Flask(__name__)

@app.route("/")

def main():
    # initialize the pygame
    pygame.init()

    width = 1200
    height = 800

    # create screen (width, height)
    screen = pygame.display.set_mode((width, height))

    # background
    background = pygame.image.load("background.jpg")

    # background sound
    mixer.music.load("background.wav")
    mixer.music.play(-1)

    # title and icon
    pygame.display.set_caption("Space Invaders")
    icon = pygame.image.load("rocket.png")
    pygame.display.set_icon((icon))

    # player icon
    playerImg = pygame.image.load("attacker.png")
    playerX = 570
    playerY = 680
    playerX_change = 0
    playerY_change = 0

    # enemy icon
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 6

    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load("spaceship.png"))
        enemyX.append(random.randint(0, 1000))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

    # bullet
    bulletImg = pygame.image.load("bullet.png")
    bulletX = 0
    bulletY = 680
    bulletX_change = 0
    bulletY_change = 10
    bullet_state = "ready"  # you cant see the bullet on the screen

    # score
    score_value = 0
    font = pygame.font.Font("freesansbold.ttf", 32)
    textX = 10
    textY = 10

    crushed = pygame.font.Font("Crushed.ttf", 32)
    crushed_game = pygame.font.Font("Crushed.ttf", 80)


    def game_over_text():
        game_over_message = crushed_game.render("GAME OVER", True, (255, 255, 255))
        screen.blit(game_over_message, (250, 200))


    def show_credit(x, y):
        me = crushed.render("CRUSHED BY KENT", True, (255, 255, 255))
        screen.blit(me, (x, y))


    def show_score(x, y):
        score = font.render("Score: " + str(score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))


    # create the player icon with screen object and .blit
    def player(x, y):
        screen.blit(playerImg, (x, y))


    def enemy(x, y, i):
        screen.blit(enemyImg[i], (x, y))


    def fire_bullet(x, y):
        global bullet_state
        bullet_state = "fire"
        screen.blit(bulletImg, (x + 16, y + 10))


    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False


    # GAME LOOP
    game_over = False

    while not game_over:
        # RGB - red, green, blue
        screen.fill((208, 208, 208))
        # background imagine
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quits game when "close button" is clicked
                game_over = True

            # if key stroke is pressed check whether is right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -10
                if event.key == pygame.K_RIGHT:
                    playerX_change = 10
                # fire bullet
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletX = playerX
                        bullet_sound = mixer.Sound("laser.wav")
                        bullet_sound.play()
                        fire_bullet(bulletX, bulletY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0

        # player movement
        playerY += playerY_change
        if playerY <= 0:
            playerY = 0
        elif playerY >= 736:
            playerY = 736

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 1136:
            playerX = 1136

        # enemy movement
        for i in range(num_of_enemies):
            # game over
            if enemyY[i] > 600:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 5
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 1136:
                enemyX_change[i] = -5
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                bulletY = playerY
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 1130)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)


        #    def fire_bullet(x, y): # fire bullet function from above
                #global bullet_state
                #bullet_state = "fire"
                #screen.blit(bulletImg, (x + 16, y + 10))

        # bullet movement
        if bulletY <= 0: # if bullet is within the screen parameters for height
            bullet_state = "ready"
            bulletY = 680 # resets the bullet to y coordinate after it clears the screen

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
        show_credit(10, 740)
        pygame.display.update()

app.run()
