import pygame
import random
import time

pygame.init()

# värvid
white = [255, 255, 255]
black = [0, 0, 0]
red = [213, 50, 80]
green = [0, 180, 0]
blue = [50, 153, 213]
yellow = [255, 255, 102]
gray = [120, 120, 120]
purple = [140, 70, 200]

# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# mängu seaded
snakeBlock = 20
snakeSpeed = 12
score = 0
level = 1

# fondid
font = pygame.font.SysFont(None, 32)
bigFont = pygame.font.SysFont(None, 50)

# ussi joonistamine
def drawSnake(snakeBlock, snakeList):
    for block in snakeList:
        pygame.draw.rect(screen, green, [block[0], block[1], snakeBlock, snakeBlock])

# teksti kuvamine
def drawText(text, color, x, y, fontType):
    message = fontType.render(text, True, color)
    screen.blit(message, [x, y])

# toidu loomine
def newFood():
    foodX = round(random.randrange(0, screenX - snakeBlock) / 20.0) * 20.0
    foodY = round(random.randrange(40, screenY - snakeBlock) / 20.0) * 20.0
    return foodX, foodY

# takistuste loomine
def createWalls():
    walls = []

    for i in range(6):
        wallX = random.randrange(0, screenX - snakeBlock, snakeBlock)
        wallY = random.randrange(80, screenY - snakeBlock, snakeBlock)
        walls.append([wallX, wallY])

    return walls

# mängu tsükkel
def gameLoop():
    global snakeSpeed
    global score
    global level

    gameover = False
    gameclose = False

    # algkoordinaadid
    posX = screenX / 2
    posY = screenY / 2

    # liikumise muutujad
    speedX = 0
    speedY = 0

    # ussi andmed
    snakeList = []
    snakeLength = 1

    # toit
    foodX, foodY = newFood()

    # eritoit
    bonusFood = False
    bonusX = 0
    bonusY = 0
    bonusCounter = 0

    # takistused
    walls = createWalls()

    while not gameover:

        while gameclose:
            screen.fill(blue)

            drawText("Mäng läbi!", red, screenX / 2 - 100, screenY / 2 - 70, bigFont)
            drawText("Skoor: " + str(score), white, screenX / 2 - 70, screenY / 2 - 20, font)
            drawText("Vajuta C - uuesti või Q - välju", white, screenX / 2 - 170, screenY / 2 + 25, font)

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
                        score = 0
                        level = 1
                        snakeSpeed = 12
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

        # seina kokkupõrge
        if posX >= screenX or posX < 0 or posY >= screenY or posY < 40:
            gameclose = True

        # ussi liikumine
        posX += speedX
        posY += speedY

        # taust
        screen.fill(blue)

        # ülemine infokast
        pygame.draw.rect(screen, black, [0, 0, screenX, 40])
        drawText("Skoor: " + str(score), white, 10, 10, font)
        drawText("Tase: " + str(level), white, 140, 10, font)
        drawText("Kiirus: " + str(snakeSpeed), white, 250, 10, font)

        # toit
        pygame.draw.rect(screen, red, [foodX, foodY, snakeBlock, snakeBlock])

        # eritoit
        if bonusFood:
            pygame.draw.rect(screen, yellow, [bonusX, bonusY, snakeBlock, snakeBlock])

        # takistused
        for wall in walls:
            pygame.draw.rect(screen, gray, [wall[0], wall[1], snakeBlock, snakeBlock])

        # ussi pea
        snakeHead = []
        snakeHead.append(posX)
        snakeHead.append(posY)
        snakeList.append(snakeHead)

        # ussi pikkuse piiramine
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

        drawSnake(snakeBlock, snakeList)

        pygame.display.update()

        # tavalise toidu söömine
        if posX == foodX and posY == foodY:
            foodX, foodY = newFood()
            snakeLength += 1
            score += 1

            # iga 5 punkti järel tõuseb tase ja kiirus
            if score % 5 == 0:
                level += 1
                snakeSpeed += 2
                walls = createWalls()

            # mõnikord tekib eritoit
            if random.randint(1, 4) == 1:
                bonusFood = True
                bonusX, bonusY = newFood()
                bonusCounter = 300

        # eritoidu söömine
        if bonusFood and posX == bonusX and posY == bonusY:
            bonusFood = False
            snakeLength += 2
            score += 3

        # eritoidu aeg
        if bonusFood:
            bonusCounter -= 1
            if bonusCounter <= 0:
                bonusFood = False

        clock.tick(snakeSpeed)

    pygame.quit()
    quit()

gameLoop()