import pygame, random
pygame.init()

# värvid
black = [0, 0, 0]
lBlue = [153, 204, 255]

# ekraani seaded
screenX = 640
screenY = 480
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Hiirega juhtimine")
screen.fill(lBlue)
clock = pygame.time.Clock()

# ringide andmed
rings = []
ringSize = 10

gameover = False
while not gameover:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

        # hiireklikk
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos

            # suvaline värv
            color = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ]

            # lisame ringi listi
            rings.append([mouseX, mouseY, ringSize, color])

            # järgmine ring tuleb suurem
            ringSize += 3

            # kui ringe on rohkem kui 10, kustutame esimese
            if len(rings) > 10:
                rings.pop(0)

    # taust
    screen.fill(lBlue)

    # ringide joonistamine
    for ring in rings:
        pygame.draw.circle(screen, ring[3], [ring[0], ring[1]], ring[2])

    pygame.display.flip()

pygame.quit()