import pygame
import random

pygame.init()

# värvid
white = [255, 255, 255]
black = [0, 0, 0]
red = [213, 50, 80]
green = [0, 180, 0]
blue = [50, 153, 213]
gray = [100, 100, 100]

# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Snake Game - Takistused")
clock = pygame.time.Clock()

# mängu seaded
snakeBlock = 20
snakeSpeed = 12

# fondid
font = pygame.font.SysFont(None, 36)
bigFont = pygame.font.SysFont(None, 60)

# ussi joonistamine
def drawSnake(snakeList):
    for block in snakeList:
        pygame.draw.rect(screen, green, [block[0], block[1], snakeBlock, snakeBlock])

# uue toidu loomine
def newFood():
    foodX = random.randrange(0, screenX - snakeBlock, snakeBlock)
    foodY = random.randrange(40, screenY - snakeBlock, snakeBlock)
    return foodX, foodY

# takistuste loomine
def createWalls():
    walls = [
        [160, 160],
        [180, 160],
        [200, 160],
        [220, 160],
        [400, 300],
        [420, 300],
        [440, 300],
        [460, 300]
    ]
    return walls

# mängu tsükkel
def gameLoop():
    gameover = False
    gameclose = False

    # algkoordinaadid
    posX = screenX / 2
    posY = screenY / 2

    # liikumine
    speedX = 0
    speedY = 0

    # uss
    snakeList = []
    snakeLength = 1

    # toit ja takistused
    foodX, foodY = newFood()
    walls = createWalls()

    score = 0

    while not gameover:

        while gameclose:
            screen.fill(blue)

            loseText = bigFont.render("Mäng läbi!", True, red)
            scoreText = font.render("Skoor: " + str(score), True, white)
            againText = font.render("C - uuesti, Q - välju", True, white)

            screen.blit(loseText, [screenX / 2 - 130, screenY / 2 - 80])
            screen.blit(scoreText, [screenX / 2 - 60, screenY / 2 - 20])
            screen.blit(againText, [screenX / 2 - 140, screenY / 2 + 30])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = True
                    gameclose = False

                # klahvivajutus
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameover = True
                        gameclose = False

                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

            # klahvivajutus
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and speedX == 0:
                    speedX = -snakeBlock
                    speedY = 0

                elif event.key == pygame.K_RIGHT and speedX == 0:
                    speedX = snakeBlock
                    speedY = 0

                elif event.key == pygame.K_UP and speedY == 0:
                    speedY = -snakeBlock
                    speedX = 0

                elif event.key == pygame.K_DOWN and speedY == 0:
                    speedY = snakeBlock
                    speedX = 0

        # ussi liikumine
        posX += speedX
        posY += speedY

        # mängu piirid
        if posX >= screenX or posX < 0 or posY >= screenY or posY < 40:
            gameclose = True

        # taust
        screen.fill(blue)

        # info riba
        pygame.draw.rect(screen, black, [0, 0, screenX, 40])
        scoreText = font.render("Skoor: " + str(score), True, white)
        screen.blit(scoreText, [10, 8])

        # toit
        pygame.draw.rect(screen, red, [foodX, foodY, snakeBlock, snakeBlock])

        # takistused
        for wall in walls:
            pygame.draw.rect(screen, gray, [wall[0], wall[1], snakeBlock, snakeBlock])

        # ussi pea
        snakeHead = []
        snakeHead.append(posX)
        snakeHead.append(posY)
        snakeList.append(snakeHead)

        # ussi pikkuse hoidmine
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # enda vastu minemine
        for block in snakeList[:-1]:
            if block == snakeHead:
                gameclose = True

        # takistuse vastu minemine
        for wall in walls:
            if posX == wall[0] and posY == wall[1]:
                gameclose = True

        drawSnake(snakeList)

        pygame.display.update()

        # toidu söömine
        if posX == foodX and posY == foodY:
            foodX, foodY = newFood()
            snakeLength += 1
            score += 1

        clock.tick(snakeSpeed)

    pygame.quit()
    quit()

gameLoop()