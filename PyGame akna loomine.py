#Pygame akna loomine
#Panin kommentaarid ainult kohtadesse, mida muutsin või juurde kirjutasin

import pygame
pygame.init()
laius = 800
korgus = 600
ekraan = pygame.display.set_mode((laius, korgus))
pygame.display.set_caption("Liikuv ruut")
#vahetan tausta värvi
taust = (245, 200, 220)
sinine = (0, 100, 255)

ruudu_suurus = 50
#panen ruudu täpselt ekraani keskele
x = laius // 2 - ruudu_suurus // 2
y = korgus // 2 - ruudu_suurus // 2

kiirus = 1
too_kaib = True
while too_kaib:
    for sundmus in pygame.event.get():
        if sundmus.type == pygame.QUIT:
            too_kaib = False
    klahvid = pygame.key.get_pressed()
    if 0 <= x <= 750 and 0 <= y <= 550:
        if klahvid[pygame.K_LEFT]:
            x -= kiirus
        if klahvid[pygame.K_RIGHT]:
            x += kiirus
        if klahvid[pygame.K_UP]:
            y -= kiirus
        if klahvid[pygame.K_DOWN]:
            y += kiirus
    else:
        #kui ruut on vasaku ääre vastas, siis ma ei teha et x koordinaat läheks negatiivseks
        #panen koordinaadiks 0 ja teen nii, et vasaku noolega ei saaks rohkem vasakule minna
        #teen sama teiste klahvide ja ekraani äärtega
        if x < 0:
            x = 0
            #ruut ei tohi rohkem vasakule minna
            if klahvid[pygame.K_LEFT]:
                pass
            if klahvid[pygame.K_RIGHT]:
                x += kiirus
            if klahvid[pygame.K_UP]:
                y -= kiirus
            if klahvid[pygame.K_DOWN]:
                y += kiirus
        #lahutan ruudu pikkuse ekraani pikkusest, et ruutu oleks terviklikult näha ja et ta ei läheks äärest väljapoole
        #800-50=750
        if x > 750:
            x = 750
            if klahvid[pygame.K_LEFT]:
                x -= kiirus
            #ruut ei tohi rohkem paremale minna
            if klahvid[pygame.K_RIGHT]:
                pass
            if klahvid[pygame.K_UP]:
                y -= kiirus
            if klahvid[pygame.K_DOWN]:
                y += kiirus
        #ruut ei tohi üle minna ülemisest äärest
        if y < 0:
            y = 0
            if klahvid[pygame.K_LEFT]:
                x -= kiirus
            if klahvid[pygame.K_RIGHT]:
                x += kiirus
            #ruut ei tohi rohkem üles minna
            if klahvid[pygame.K_UP]:
                pass
            if klahvid[pygame.K_DOWN]:
                y += kiirus
        #600-50=550
        #kuna ekraan on 600 pikslit pikk ja koordinaate loetakse pygameis vasakult paremale ja ülevalt alla,
        #siis lahutan ruudu pikkuse sellest, et ruut jääks ekraani piiridesse
        if y > 550:
            y = 550
            if klahvid[pygame.K_LEFT]:
                x -= kiirus
            if klahvid[pygame.K_RIGHT]:
                x += kiirus
            if klahvid[pygame.K_UP]:
                y -= kiirus
            #ruut ei tohi rohkem alla minna
            if klahvid[pygame.K_DOWN]:
                pass

    ekraan.fill(taust)
    pygame.draw.rect(ekraan, sinine, (x, y, ruudu_suurus, ruudu_suurus))
    pygame.display.flip()
pygame.quit()
