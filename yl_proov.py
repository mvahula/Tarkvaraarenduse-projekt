import pygame
pygame.init()

# värvid
# Siin määrame värvid, mida mängus kasutame.
# lBlue on hele sinine taustavärv.
# black on must värv, mida kasutame skoori teksti kirjutamiseks.
lBlue = [153, 204, 255]
black = [0, 0, 0]

# ekraani seaded
# screenX ja screenY määravad mänguakna laiuse ja kõrguse pikslites.
# Ülesandes oli öeldud, et mängu suurus peab olema 640x480.
screenX = 640
screenY = 480

# Loome mänguakna, mille suurus on screenX ja screenY.
# set_caption määrab akna ülemisele ribale pealkirja.
screen = pygame.display.set_mode([screenX, screenY])
pygame.display.set_caption("Pall ja alus")

# Täidame ekraani alguses heleda taustavärviga.
screen.fill(lBlue)

# Clock aitab mängu kiirust kontrollida.
# Hiljem kasutame clock.tick(60), et mäng töötaks umbes 60 kaadrit sekundis.
clock = pygame.time.Clock()

# pall
# Loome palli jaoks Rect objekti.
# Rect määrab palli asukoha ja suuruse.
# Esimesed kaks arvu on palli algne x- ja y-koordinaat.
# Viimased kaks arvu on palli laius ja kõrgus.
# Ülesandes oli öeldud, et palli suurus peab olema 20x20.
ball = pygame.Rect(0, 0, 20, 20)

# Laeme palli pildi failist.
# Pilt peab olema kaustas img ja faili nimi peab olema pall.png.
ballImage = pygame.image.load("pall.png")

# Muudame palli pildi täpselt sama suureks nagu ball Rect objekt.
# Kasutame ball.width ja ball.height väärtuseid, et suurus tuleks 20x20.
ballImage = pygame.transform.scale(ballImage, [ball.width, ball.height])

# Need muutujad määravad, kui kiiresti pall liigub.
# ballSpeedX muudab palli x-koordinaati ehk liigutab palli vasakule või paremale.
# ballSpeedY muudab palli y-koordinaati ehk liigutab palli üles või alla.
ballSpeedX = 4
ballSpeedY = 4

# alus
# Loome aluse jaoks Rect objekti.
# Aluse x-koordinaat on alguses 200.
# Aluse y-koordinaat on screenY / 1.5, mis tähendab, et alus asub ekraani keskosast allpool.
# Aluse suurus on 120x20, nagu ülesandes nõutud.
base = pygame.Rect(200, screenY / 1.5, 120, 20)

# Laeme aluse pildi failist.
# Pilt peab olema kaustas img ja faili nimi peab olema alus.png.
baseImage = pygame.image.load("alus.png")

# Muudame aluse pildi sama suureks nagu base Rect objekt.
# Nii sobib pilt täpselt aluse ristküliku sisse.
baseImage = pygame.transform.scale(baseImage, [base.width, base.height])

# See muutuja määrab, kui kiiresti alus liigub vasakule ja paremale.
# Kui väärtus on positiivne, liigub alus paremale.
# Kui väärtus muutub negatiivseks, liigub alus vasakule.
baseSpeedX = 3

# skoor
# score hoiab mängija punkte.
# Kui pall puudutab alust, saab mängija ühe positiivse punkti.
# Kui pall puudutab alumist äärt, saab mängija ühe negatiivse punkti.
score = 0

# Loome fondi, millega skoori ekraanile kirjutame.
# None tähendab, et kasutatakse Pygame'i vaikimisi fonti.
# 36 on teksti suurus.
font = pygame.font.SysFont(None, 36)

# gameover määrab, kas mäng veel kestab.
# Alguses on väärtus False, sest mäng ei ole läbi.
# while tsükkel töötab seni, kuni gameover on False.
gameover = False
while not gameover:
    # Piirame mängu kiiruse 60 kaadrini sekundis.
    # See teeb liikumise ühtlasemaks ja takistab mängu liiga kiireks minemast.
    clock.tick(60)

    # mängu sulgemine ristist
    # Kontrollime, kas kasutaja vajutas akna sulgemise nuppu.
    # Kui sündmuse tüüp on pygame.QUIT, siis lõpetame while-tsükli.
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break

    # palli liikumine
    # Igas tsükli korduses muudame palli x- ja y-koordinaati.
    # Selle tulemusena liigub pall ekraanil edasi.
    ball.x += ballSpeedX
    ball.y += ballSpeedY

    # pall põrkub seintest tagasi
    # Kui palli vasak serv läheb vastu ekraani vasakut äärt
    # või palli parem serv läheb vastu ekraani paremat äärt,
    # siis muudame x-suuna vastupidiseks.
    if ball.left <= 0 or ball.right >= screenX:
        ballSpeedX = -ballSpeedX

    # Kui palli ülemine serv puudutab ekraani ülemist äärt,
    # siis muudame y-suuna vastupidiseks.
    # See tähendab, et pall hakkab ülevalt alla tagasi liikuma.
    if ball.top <= 0:
        ballSpeedY = -ballSpeedY

    # kui pall puudutab alumist äärt
    # Kui palli alumine serv puudutab ekraani alumist äärt,
    # siis muudame palli y-suuna vastupidiseks,
    # et pall põrkaks alt tagasi üles.
    # Samal ajal võtame mängijalt ühe punkti maha.
    if ball.bottom >= screenY:
        ballSpeedY = -ballSpeedY
        score -= 1

    # aluse liikumine
    # Igas tsükli korduses muudame aluse x-koordinaati.
    # Nii liigub alus automaatselt vasakule või paremale.
    base.x += baseSpeedX

    # alus põrkub seintest tagasi
    # Kui aluse vasak serv puudutab ekraani vasakut äärt
    # või aluse parem serv puudutab ekraani paremat äärt,
    # siis muudame aluse liikumise suuna vastupidiseks.
    if base.left <= 0 or base.right >= screenX:
        baseSpeedX = -baseSpeedX

    # kokkupõrke tuvastamine
    # colliderect kontrollib, kas palli Rect ja aluse Rect puutuvad kokku.
    # Lisaks kontrollime, et ballSpeedY oleks suurem kui 0.
    # See tähendab, et pall liigub kokkupõrke hetkel alla.
    # Kui seda kontrolli ei oleks, võib pall aluse sees mitu korda suunda muuta
    # ja hakata kokkupuutel imelikult värisema.
    if ball.colliderect(base) and ballSpeedY > 0:
        # Muudame palli y-suuna vastupidiseks,
        # et pall põrkaks aluse pealt üles.
        ballSpeedY = -ballSpeedY

        # Kui pall puudutab alust, saab mängija ühe punkti juurde.
        score += 1

    # joonistamine
    # Enne uue kaadri joonistamist värvime kogu ekraani taustavärviga üle.
    # Kui seda ei teeks, jääksid vanad palli ja aluse asukohad ekraanile alles.
    screen.fill(lBlue)

    # Kuvame palli pildi ekraanile palli Rect objekti asukohta.
    screen.blit(ballImage, ball)

    # Kuvame aluse pildi ekraanile aluse Rect objekti asukohta.
    screen.blit(baseImage, base)

    # skoori kuvamine
    # Loome skoori tekstist pildi, mida saab ekraanile kuvada.
    # str(score) muudab numbri tekstiks, et seda saaks tekstiga kokku liita.
    scoreText = font.render("Skoor: " + str(score), True, black)

    # Kuvame skoori ekraani ülemisse vasakusse nurka.
    # [10, 10] tähendab, et tekst algab 10 pikslit vasakust ja 10 pikslit ülevalt.
    screen.blit(scoreText, [10, 10])

    # Uuendame ekraani.
    # Kõik eelnevalt joonistatud asjad muutuvad nüüd mänguaknas nähtavaks.
    pygame.display.flip()

# Kui mängutsükkel lõppeb, sulgeme Pygame'i korralikult.
pygame.quit()