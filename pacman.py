import pygame
import random

pygame.init()

# värvid
black = [0, 0, 0]
white = [255, 255, 255]
yellow = [255, 220, 0]
blue = [0, 0, 180]
darkBlue = [0, 0, 80]
red = [220, 40, 40]
pink = [255, 100, 180]
cyan = [80, 220, 255]
orange = [255, 150, 40]
green = [0, 200, 80]
gray = [120, 120, 120]

# mängukaart
RAW_MAP = [
    "####################",
    "#P......##......G..#",
    "#.####..##..####...#",
    "#o####..##..####..o#",
    "#..................#",
    "#.##.########.##...#",
    "#.##....##....##...#",
    "#.#####.##.#####...#",
    "#..................#",
    "###.##.######.##.###",
    "#...##...G....##...#",
    "#.#####.##.#####...#",
    "#..................#",
    "#.##.########.##...#",
    "#o...............o.#",
    "####################",
]

# ekraani seaded
TILE = 30
HUD_HEIGHT = 60

screenX = len(RAW_MAP[0]) * TILE
screenY = len(RAW_MAP) * TILE + HUD_HEIGHT

screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Pac-Man - Mängude kombineerimine")
clock = pygame.time.Clock()

# fondid
font = pygame.font.SysFont(None, 32)
bigFont = pygame.font.SysFont(None, 58)

# mängu seaded
FPS = 60
MOVE_DELAY = 8

# mänguseis
score = 0
lives = 3
level = 1
gameState = "menu"

# teksti kuvamine
def drawText(text, color, x, y, fontType):
    img = fontType.render(text, True, color)
    screen.blit(img, [x, y])

# ruudustik piksliteks
def gridToPixel(gridX, gridY):
    return gridX * TILE, gridY * TILE + HUD_HEIGHT

# seina kontroll
def isWall(gridX, gridY, walls):
    if gridX < 0 or gridY < 0:
        return True

    if gridY >= len(RAW_MAP) or gridX >= len(RAW_MAP[0]):
        return True

    return [gridX, gridY] in walls

# kaardi laadimine
def loadMap():
    walls = []
    pellets = []
    powerPellets = []
    ghosts = []
    playerStart = [1, 1]

    for y in range(len(RAW_MAP)):
        for x in range(len(RAW_MAP[y])):
            tile = RAW_MAP[y][x]

            if tile == "#":
                walls.append([x, y])

            elif tile == ".":
                pellets.append([x, y])

            elif tile == "o":
                powerPellets.append([x, y])

            elif tile == "P":
                playerStart = [x, y]

            elif tile == "G":
                ghosts.append({
                    "x": x,
                    "y": y,
                    "dirX": 0,
                    "dirY": 0,
                    "color": random.choice([red, pink, cyan, orange])
                })

    return walls, pellets, powerPellets, ghosts, playerStart

# kaardi joonistamine
def drawMap(walls, pellets, powerPellets):
    for wall in walls:
        px, py = gridToPixel(wall[0], wall[1])
        pygame.draw.rect(screen, blue, [px, py, TILE, TILE])
        pygame.draw.rect(screen, darkBlue, [px + 3, py + 3, TILE - 6, TILE - 6])

    for pellet in pellets:
        px, py = gridToPixel(pellet[0], pellet[1])
        pygame.draw.circle(screen, white, [px + TILE // 2, py + TILE // 2], 4)

    for power in powerPellets:
        px, py = gridToPixel(power[0], power[1])
        pygame.draw.circle(screen, yellow, [px + TILE // 2, py + TILE // 2], 9)

# mängija joonistamine
def drawPlayer(playerX, playerY, directionX):
    px, py = gridToPixel(playerX, playerY)

    pygame.draw.circle(screen, yellow, [px + TILE // 2, py + TILE // 2], TILE // 2 - 3)

    if directionX < 0:
        pygame.draw.polygon(screen, black, [
            [px + TILE // 2, py + TILE // 2],
            [px, py + 6],
            [px, py + TILE - 6]
        ])
    else:
        pygame.draw.polygon(screen, black, [
            [px + TILE // 2, py + TILE // 2],
            [px + TILE, py + 6],
            [px + TILE, py + TILE - 6]
        ])

# kummituste joonistamine
def drawGhosts(ghosts, powerMode):
    for ghost in ghosts:
        px, py = gridToPixel(ghost["x"], ghost["y"])

        if powerMode > 0:
            color = gray
        else:
            color = ghost["color"]

        pygame.draw.rect(screen, color, [px + 4, py + 6, TILE - 8, TILE - 8])
        pygame.draw.circle(screen, color, [px + TILE // 2, py + 10], TILE // 2 - 4)

        pygame.draw.circle(screen, white, [px + 11, py + 13], 4)
        pygame.draw.circle(screen, white, [px + 20, py + 13], 4)
        pygame.draw.circle(screen, black, [px + 11, py + 13], 2)
        pygame.draw.circle(screen, black, [px + 20, py + 13], 2)

# info kuvamine
def drawHud(powerMode):
    pygame.draw.rect(screen, black, [0, 0, screenX, HUD_HEIGHT])

    drawText("Skoor: " + str(score), white, 10, 18, font)
    drawText("Elud: " + str(lives), white, 170, 18, font)
    drawText("Tase: " + str(level), white, 290, 18, font)

    if powerMode > 0:
        drawText("Boonus!", yellow, 420, 18, font)

# kummituse võimalikud suunad
def getPossibleDirections(x, y, walls):
    possible = []

    directions = [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1]
    ]

    for direction in directions:
        newX = x + direction[0]
        newY = y + direction[1]

        if not isWall(newX, newY, walls):
            possible.append(direction)

    return possible

# kummituste liikumine
def moveGhosts(ghosts, walls):
    for ghost in ghosts:
        possible = getPossibleDirections(ghost["x"], ghost["y"], walls)

        if len(possible) > 0:
            direction = random.choice(possible)
            ghost["dirX"] = direction[0]
            ghost["dirY"] = direction[1]

            ghost["x"] += ghost["dirX"]
            ghost["y"] += ghost["dirY"]

# asukohtade taastamine
def resetPositions(playerStart, ghosts):
    playerX = playerStart[0]
    playerY = playerStart[1]

    for ghost in ghosts:
        if ghost["color"] == red:
            ghost["x"] = 17
            ghost["y"] = 1
        elif ghost["color"] == pink:
            ghost["x"] = 9
            ghost["y"] = 10
        else:
            ghost["x"] = random.choice([9, 17])
            ghost["y"] = random.choice([1, 10])

    return playerX, playerY

# mängu põhitsükkel
def gameLoop():
    global score
    global lives
    global level
    global gameState

    walls, pellets, powerPellets, ghosts, playerStart = loadMap()

    playerX = playerStart[0]
    playerY = playerStart[1]

    directionX = 0
    directionY = 0

    nextDirectionX = 0
    nextDirectionY = 0

    moveCounter = 0
    ghostCounter = 0
    powerMode = 0

    gameover = False

    while not gameover:
        clock.tick(FPS)

        # sündmused
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

            if event.type == pygame.KEYDOWN:
                if gameState == "menu" and event.key == pygame.K_RETURN:
                    gameState = "play"

                elif gameState == "gameover" and event.key == pygame.K_RETURN:
                    score = 0
                    lives = 3
                    level = 1
                    gameState = "play"
                    gameLoop()

                elif gameState == "win" and event.key == pygame.K_RETURN:
                    score = 0
                    lives = 3
                    level = 1
                    gameState = "play"
                    gameLoop()

                elif event.key == pygame.K_p:
                    if gameState == "play":
                        gameState = "pause"
                    elif gameState == "pause":
                        gameState = "play"

                elif gameState == "play":
                    if event.key == pygame.K_LEFT:
                        nextDirectionX = -1
                        nextDirectionY = 0

                    elif event.key == pygame.K_RIGHT:
                        nextDirectionX = 1
                        nextDirectionY = 0

                    elif event.key == pygame.K_UP:
                        nextDirectionX = 0
                        nextDirectionY = -1

                    elif event.key == pygame.K_DOWN:
                        nextDirectionX = 0
                        nextDirectionY = 1

        # menüü
        if gameState == "menu":
            screen.fill(black)
            drawText("PAC-MAN", yellow, screenX / 2 - 105, 150, bigFont)
            drawText("Vajuta ENTER, et alustada", white, screenX / 2 - 150, 230, font)
            drawText("Nooleklahvid - liikumine", white, screenX / 2 - 135, 270, font)
            drawText("P - paus", white, screenX / 2 - 50, 310, font)
            pygame.display.update()
            continue

        # paus
        if gameState == "pause":
            drawText("PAUS", yellow, screenX / 2 - 55, screenY / 2 - 20, bigFont)
            drawText("Vajuta P, et jätkata", white, screenX / 2 - 110, screenY / 2 + 35, font)
            pygame.display.update()
            continue

        # kaotus
        if gameState == "gameover":
            screen.fill(black)
            drawText("MÄNG LÄBI", red, screenX / 2 - 135, 160, bigFont)
            drawText("Lõppskoor: " + str(score), white, screenX / 2 - 90, 230, font)
            drawText("Vajuta ENTER, et uuesti mängida", white, screenX / 2 - 180, 280, font)
            pygame.display.update()
            continue

        # võit
        if gameState == "win":
            screen.fill(black)
            drawText("VÕITSID!", green, screenX / 2 - 95, 160, bigFont)
            drawText("Lõppskoor: " + str(score), white, screenX / 2 - 90, 230, font)
            drawText("Vajuta ENTER, et uuesti mängida", white, screenX / 2 - 180, 280, font)
            pygame.display.update()
            continue

        # liikumine
        moveCounter += 1
        ghostCounter += 1

        if moveCounter >= MOVE_DELAY:
            moveCounter = 0

            if not isWall(playerX + nextDirectionX, playerY + nextDirectionY, walls):
                directionX = nextDirectionX
                directionY = nextDirectionY

            if not isWall(playerX + directionX, playerY + directionY, walls):
                playerX += directionX
                playerY += directionY

            # punktide söömine
            if [playerX, playerY] in pellets:
                pellets.remove([playerX, playerY])
                score += 10

            if [playerX, playerY] in powerPellets:
                powerPellets.remove([playerX, playerY])
                score += 50
                powerMode = 45

            if powerMode > 0:
                powerMode -= 1

        # kummitused
        if ghostCounter >= MOVE_DELAY + 4 - min(level, 3):
            ghostCounter = 0
            moveGhosts(ghosts, walls)

        # kokkupõrge kummitustega
        for ghost in ghosts:
            if playerX == ghost["x"] and playerY == ghost["y"]:
                if powerMode > 0:
                    score += 200
                    ghost["x"] = random.choice([9, 17])
                    ghost["y"] = random.choice([1, 10])
                else:
                    lives -= 1
                    playerX, playerY = resetPositions(playerStart, ghosts)
                    directionX = 0
                    directionY = 0
                    nextDirectionX = 0
                    nextDirectionY = 0

                    if lives <= 0:
                        gameState = "gameover"

        # järgmine tase
        if len(pellets) == 0 and len(powerPellets) == 0:
            level += 1

            if level > 3:
                gameState = "win"
            else:
                walls, pellets, powerPellets, ghosts, playerStart = loadMap()
                playerX = playerStart[0]
                playerY = playerStart[1]
                directionX = 0
                directionY = 0
                nextDirectionX = 0
                nextDirectionY = 0

        # joonistamine
        screen.fill(black)

        drawHud(powerMode)
        drawMap(walls, pellets, powerPellets)
        drawPlayer(playerX, playerY, directionX)
        drawGhosts(ghosts, powerMode)

        pygame.display.update()

    pygame.quit()


gameLoop()