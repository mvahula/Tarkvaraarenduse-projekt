#Impordin pygame ja random mooduli
import pygame
import random

pygame.init()

#Loon uue pygame mängu suurusega 640x480
screen = pygame.display.set_mode([640, 480])

#Panen mängule nimeks ülesande numbri
pygame.display.set_caption("Ülesanne 4 - Vahula")


#Lisan taustapildi
taust = pygame.image.load("bg_rally.jpg")
taust = pygame.transform.scale(taust, (640, 480))


#Lisan punase auto
punane_auto = pygame.image.load("f1_red.png").convert_alpha()
punane_auto = pygame.transform.scale(punane_auto, (60, 90))

#Punase auto asukoht all keskel
punane_x = 290
punane_y = 370


#Lisan sinise auto pildi
sinine_pilt = pygame.image.load("f1_blue.png").convert_alpha()
sinine_pilt = pygame.transform.scale(sinine_pilt, (60, 90))

#Kui sinine auto on vales suunas, keeran selle ümber
sinine_pilt = pygame.transform.rotate(sinine_pilt, 180)


#Kolme raja x-koordinaadid
rajad = [170, 290, 410]


#Loon siniste autode nimekirja
sinised_autod = []

#Iga raja peale tekib ainult 1 sinine auto
for rada_x in rajad:
    auto = {
        "x": rada_x,
        "y": random.randint(-500, -50),
        "kiirus": random.randint(3, 6)
    }
    sinised_autod.append(auto)


#Loon skoori
skoor = 0

#Loon fondi skoori kuvamiseks
font = pygame.font.SysFont("Times New Roman", 30)


#Teen kella, et mäng liiga kiiresti ei liiguks
clock = pygame.time.Clock()


#Mängu tsükkel
running = True
while running:
    for event in pygame.event.get():
        #Kui kasutaja vajutab akna X-nuppu, pannakse mäng kinni
        if event.type == pygame.QUIT:
            running = False


    #Joonistan tausta
    screen.blit(taust, [0, 0])


    #Joonistan punase auto alla keskele
    screen.blit(punane_auto, [punane_x, punane_y])


    #Liigutan ja joonistan siniseid autosid
    for auto in sinised_autod:
        #Sinine auto liigub ülevalt alla
        auto["y"] += auto["kiirus"]

        #Kui auto jõuab alla, tekib ta samal rajal uuesti üleval
        if auto["y"] > 480:
            auto["y"] = random.randint(-300, -50)
            auto["kiirus"] = random.randint(3, 6)

            #Kui sinine auto jõuab alla, lisatakse skoorile punkt
            skoor += 1

        #Joonistan sinise auto ekraanile
        screen.blit(sinine_pilt, [auto["x"], auto["y"]])


    #Kuvan skoori
    skoor_tekst = font.render("Skoor: " + str(skoor), True, (20, 0, 0))
    screen.blit(skoor_tekst, [20, 20])


    #Uuendan ekraani, et animatsioon nähtavale tuleks
    pygame.display.flip()

    #Mäng jookseb 60 kaadrit sekundis
    clock.tick(60)


#Lõpetan pygame'i töö
pygame.quit()