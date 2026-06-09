import pygame
pygame.init()

# värvid
lBlue = [153, 204, 255]
black = [0, 0, 0]

# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("PingPong")
screen.fill(lBlue)
clock = pygame.time.Clock()

# taustamuusika
pygame.mixer.music.load("2.mp3")
pygame.mixer.music.play(-1)

# pall
ball = pygame.Rect(100, 100, 20, 20)
ballImage = pygame.image.load("pall.png")
ballImage = pygame.transform.scale(ballImage, [ball.width, ball.height])

ballSpeedX = 4
ballSpeedY = 4

# alus
base = pygame.Rect(200, screenY / 1.5, 120, 20)
baseImage = pygame.image.load("alus.png")
baseImage = pygame.transform.scale(baseImage, [base.width, base.height])

baseSpeedX = 5

# skoor
score = 0
font = pygame.font.SysFont(None, 36)

gameover = False
while not gameover:
    clock.tick(60)

    # mängu sulgemine ristist
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

    # klahvide kontroll
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        base.x -= baseSpeedX

    if keys[pygame.K_RIGHT]:
        base.x += baseSpeedX

    # alus ei lähe piiridest välja
    if base.left < 0:
        base.left = 0

    if base.right > screenX:
        base.right = screenX

    # palli liikumine
    ball.x += ballSpeedX
    ball.y += ballSpeedY

    # pall põrkub seintest tagasi
    if ball.left <= 0 or ball.right >= screenX:
        ballSpeedX = -ballSpeedX

    if ball.top <= 0:
        ballSpeedY = -ballSpeedY

    # kui pall puudutab alumist äärt
    if ball.bottom >= screenY:
        gameover = True

    # kokkupõrke tuvastamine
    if ball.colliderect(base) and ballSpeedY > 0:
        ballSpeedY = -ballSpeedY
        score += 1

    # joonistamine
    screen.fill(lBlue)

    screen.blit(ballImage, ball)
    screen.blit(baseImage, base)

    # skoori kuvamine
    scoreText = font.render("Skoor: " + str(score), True, black)
    screen.blit(scoreText, [10, 10])

    pygame.display.flip()

pygame.quit()