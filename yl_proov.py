# Impordime pygame teegi, mida kasutatakse akna, graafika, klaviatuuri ja mängutsükli jaoks
import pygame

# Impordime random teegi, et saaksime toitu ja takistusi juhuslikesse kohtadesse paigutada
import random

# Impordime time teegi
# NB! Selles programmis seda tegelikult ei kasutata, seega selle võiks ka eemaldada
import time


# Käivitame pygame'i moodulid
# Ilma selleta ei tööta pygame'i aken, fondid ega sündmused korrektselt
pygame.init()


# -----------------------------
# VÄRVID
# -----------------------------
# Värvid on kirjas RGB-vormingus: [punane, roheline, sinine]
# Iga väärtus saab olla 0 kuni 255

# Valge värv, kasutatakse näiteks teksti jaoks
white = [255, 255, 255]

# Must värv, kasutatakse ülemise infokasti taustaks
black = [0, 0, 0]

# Punane värv, kasutatakse tavalise toidu ja mängu lõpu teksti jaoks
red = [213, 50, 80]

# Roheline värv, kasutatakse ussi joonistamiseks
green = [0, 180, 0]

# Sinine värv, kasutatakse mänguala taustaks
blue = [50, 153, 213]

# Kollane värv, kasutatakse eritoidu jaoks
yellow = [255, 255, 102]

# Hall värv, kasutatakse takistuste ehk seinaplokkide jaoks
gray = [120, 120, 120]

# Lilla värv
# NB! Praeguses koodis seda värvi ei kasutata
purple = [140, 70, 200]


# -----------------------------
# EKRAANI SEADED
# -----------------------------

# Mänguakna laius pikslites
screenX = 640

# Mänguakna kõrgus pikslites
screenY = 480

# Loome pygame'i akna suurusega 640 x 480 pikslit
screen = pygame.display.set_mode([screenX, screenY])

# Määrame akna pealkirja
pygame.display.set_caption("Snake Game")

# Loome kellaobjekti, millega kontrollime mängu kiirust ehk FPS-i
clock = pygame.time.Clock()


# -----------------------------
# MÄNGU ALGSEADED
# -----------------------------

# Ühe ussi ploki suurus pikslites
# Sama suurust kasutatakse ka toidu ja takistuste jaoks
snakeBlock = 20

# Ussi algkiirus
# See määrab, mitu korda sekundis mängutsükkel töötab
snakeSpeed = 12

# Mängija skoor alguses
score = 0

# Mängu tase alguses
level = 1


# -----------------------------
# FONDID
# -----------------------------

# Tavaline font väiksema teksti jaoks
# None tähendab, et pygame kasutab vaikimisi fonti
# 32 tähendab fondi suurust
font = pygame.font.SysFont(None, 32)

# Suurem font näiteks "Mäng läbi!" teksti jaoks
bigFont = pygame.font.SysFont(None, 50)


# -----------------------------
# USSI JOONISTAMISE FUNKTSIOON
# -----------------------------

def drawSnake(snakeBlock, snakeList):
    """
    Joonistab kogu ussi ekraanile.

    snakeBlock:
        ühe ussi kehaosa suurus pikslites

    snakeList:
        list kõikidest ussi kehaosadest
        iga kehaosa on kujul [x, y]
    """

    # Käime kõik ussi kehaosad ükshaaval läbi
    for block in snakeList:

        # Joonistame iga kehaosa rohelise ristkülikuna
        # block[0] on x-koordinaat
        # block[1] on y-koordinaat
        # snakeBlock on ristküliku laius ja kõrgus
        pygame.draw.rect(screen, green, [block[0], block[1], snakeBlock, snakeBlock])


# -----------------------------
# TEKSTI KUVAMISE FUNKTSIOON
# -----------------------------

def drawText(text, color, x, y, fontType):
    """
    Kuvab ekraanile teksti.

    text:
        tekst, mida soovime kuvada

    color:
        teksti värv

    x, y:
        teksti asukoht ekraanil

    fontType:
        font, mida teksti kuvamiseks kasutatakse
    """

    # Loome tekstist pygame'i pildi
    # True tähendab, et tekst silutakse, et see näeks parem välja
    message = fontType.render(text, True, color)

    # Kuvame loodud teksti ekraanile määratud asukohta
    screen.blit(message, [x, y])


# -----------------------------
# TOIDU LOOMISE FUNKTSIOON
# -----------------------------

def newFood():
    """
    Loob toidu juhuslikku kohta mänguväljal.

    Toit paigutatakse 20 pikslise ruudustiku järgi,
    et see kattuks ussi liikumise sammuga.
    """

    # Valime juhusliku x-koordinaadi
    # random.randrange valib arvu vahemikus 0 kuni screenX - snakeBlock
    # Jagame 20-ga, ümardame ja korrutame uuesti 20-ga,
    # et toit paikneks täpselt ruudustikul
    foodX = round(random.randrange(0, screenX - snakeBlock) / 20.0) * 20.0

    # Valime juhusliku y-koordinaadi
    # Algus on 40, sest ekraani ülemised 40 pikslit on infokasti jaoks
    foodY = round(random.randrange(40, screenY - snakeBlock) / 20.0) * 20.0

    # Tagastame toidu x- ja y-koordinaadi
    return foodX, foodY


# -----------------------------
# TAKISTUSTE LOOMISE FUNKTSIOON
# -----------------------------

def createWalls():
    """
    Loob mänguväljale juhuslikud takistused.

    Tagastab listi, kus iga takistus on kujul [x, y].
    """

    # Tühi list takistuste hoidmiseks
    walls = []

    # Loome 6 takistust
    for i in range(6):

        # Valime juhusliku x-koordinaadi ruudustiku järgi
        wallX = random.randrange(0, screenX - snakeBlock, snakeBlock)

        # Valime juhusliku y-koordinaadi
        # Algus on 80, et takistused ei tekiks liiga üles infokasti lähedale
        wallY = random.randrange(80, screenY - snakeBlock, snakeBlock)

        # Lisame takistuse listi
        walls.append([wallX, wallY])

    # Tagastame kõik loodud takistused
    return walls


# -----------------------------
# PÕHILINE MÄNGUTSÜKKEL
# -----------------------------

def gameLoop():
    """
    See funktsioon sisaldab kogu mängu põhiloogikat:
    - sündmuste kontroll
    - ussi liikumine
    - kokkupõrked
    - toidu söömine
    - skoori ja taseme muutmine
    - ekraani uuendamine
    """

    # Kasutame globaalseid muutujaid,
    # sest neid muudetakse funktsiooni sees
    global snakeSpeed
    global score
    global level

    # gameover määrab, kas mäng peab täielikult lõppema
    gameover = False

    # gameclose määrab, kas mängija on kaotanud
    # Kui see on True, kuvatakse mängu lõpu ekraan
    gameclose = False

    # -----------------------------
    # USSI ALGASUKOHT
    # -----------------------------

    # Ussi algne x-koordinaat on ekraani keskel
    posX = screenX / 2

    # Ussi algne y-koordinaat on ekraani keskel
    posY = screenY / 2

    # -----------------------------
    # LIIKUMISE MUUTUJAD
    # -----------------------------

    # speedX määrab, kui palju uss liigub x-teljel igas kaadris
    # Alguses on 0, seega uss ei liigu enne klahvivajutust
    speedX = 0

    # speedY määrab, kui palju uss liigub y-teljel igas kaadris
    speedY = 0

    # -----------------------------
    # USSI ANDMED
    # -----------------------------

    # snakeList hoiab kõiki ussi kehaosi
    # Iga kehaosa on list kujul [x, y]
    snakeList = []

    # Ussi algpikkus on 1 plokk
    snakeLength = 1

    # -----------------------------
    # TOIT
    # -----------------------------

    # Loome esimese tavalise toidu
    foodX, foodY = newFood()

    # -----------------------------
    # ERITOIT
    # -----------------------------

    # bonusFood näitab, kas eritoit on hetkel ekraanil olemas
    bonusFood = False

    # Eritoidu algsed koordinaadid
    bonusX = 0
    bonusY = 0

    # Loendur, kui kaua eritoit ekraanil püsib
    bonusCounter = 0

    # -----------------------------
    # TAKISTUSED
    # -----------------------------

    # Loome algsed takistused
    walls = createWalls()

    # -----------------------------
    # PEAMINE WHILE-TSÜKKEL
    # -----------------------------

    # See tsükkel töötab seni, kuni mäng pole täielikult läbi
    while not gameover:

        # -----------------------------
        # MÄNGU LÕPU EKRAAN
        # -----------------------------

        # Kui mängija kaotab, muutub gameclose True väärtuseks
        # Siis näidatakse mängu lõpu ekraani
        while gameclose:

            # Täidame tausta sinise värviga
            screen.fill(blue)

            # Kuvame mängu lõpu teksti
            drawText("Mäng läbi!", red, screenX / 2 - 100, screenY / 2 - 70, bigFont)

            # Kuvame lõppskoori
            drawText("Skoor: " + str(score), white, screenX / 2 - 70, screenY / 2 - 20, font)

            # Kuvame juhised, kuidas uuesti alustada või väljuda
            drawText("Vajuta C - uuesti või Q - välju", white, screenX / 2 - 170, screenY / 2 + 25, font)

            # Uuendame ekraani, et tekst nähtavaks muutuks
            pygame.display.update()

            # Kontrollime kasutaja tegevusi mängu lõpu ekraanil
            for event in pygame.event.get():

                # Kui kasutaja sulgeb akna ristist
                if event.type == pygame.QUIT:
                    gameover = True
                    gameclose = False

                # Kui kasutaja vajutab klahvi
                if event.type == pygame.KEYDOWN:

                    # Kui vajutatakse Q, lõpetatakse mäng
                    if event.key == pygame.K_q:
                        gameover = True
                        gameclose = False

                    # Kui vajutatakse C, alustatakse mäng uuesti
                    if event.key == pygame.K_c:

                        # Lähtestame skoori
                        score = 0

                        # Lähtestame taseme
                        level = 1

                        # Lähtestame kiiruse
                        snakeSpeed = 12

                        # Käivitame mängutsükli uuesti
                        gameLoop()

        # -----------------------------
        # SÜNDMUSTE KONTROLL
        # -----------------------------

        # Käime läbi kõik pygame'i sündmused
        # Näiteks klahvivajutused või akna sulgemine
        for event in pygame.event.get():

            # Kui kasutaja sulgeb mänguakna
            if event.type == pygame.QUIT:
                gameover = True

            # Kui kasutaja vajutab mingit klahvi
            if event.type == pygame.KEYDOWN:

                # Vasakule liikumine
                # Kontroll speedX == 0 takistab ussil kohe vastassuunda pööramist
                if event.key == pygame.K_LEFT and speedX == 0:
                    speedX = -snakeBlock
                    speedY = 0

                # Paremale liikumine
                elif event.key == pygame.K_RIGHT and speedX == 0:
                    speedX = snakeBlock
                    speedY = 0

                # Üles liikumine
                elif event.key == pygame.K_UP and speedY == 0:
                    speedY = -snakeBlock
                    speedX = 0

                # Alla liikumine
                elif event.key == pygame.K_DOWN and speedY == 0:
                    speedY = snakeBlock
                    speedX = 0

        # -----------------------------
        # EKRAANI ÄÄREGA KOKKUPÕRGE
        # -----------------------------

        # Kui ussi pea läheb ekraani piiridest välja,
        # siis mängija kaotab
        # posY < 40 tähendab, et uss läks ülemisse infokasti
        if posX >= screenX or posX < 0 or posY >= screenY or posY < 40:
            gameclose = True

        # -----------------------------
        # USSI LIIKUMINE
        # -----------------------------

        # Muudame ussi pea x-koordinaati vastavalt liikumiskiirusele
        posX += speedX

        # Muudame ussi pea y-koordinaati vastavalt liikumiskiirusele
        posY += speedY

        # -----------------------------
        # TAUSTA JOONISTAMINE
        # -----------------------------

        # Täidame kogu ekraani sinise taustaga
        # Seda tehakse igal kaadril, et vana pilt ära kustutada
        screen.fill(blue)

        # -----------------------------
        # ÜLEMINE INFOKAST
        # -----------------------------

        # Joonistame ülemise musta riba,
        # kus kuvatakse skoor, tase ja kiirus
        pygame.draw.rect(screen, black, [0, 0, screenX, 40])

        # Kuvame skoori
        drawText("Skoor: " + str(score), white, 10, 10, font)

        # Kuvame taseme
        drawText("Tase: " + str(level), white, 140, 10, font)

        # Kuvame kiiruse
        drawText("Kiirus: " + str(snakeSpeed), white, 250, 10, font)

        # -----------------------------
        # TOIDU JOONISTAMINE
        # -----------------------------

        # Joonistame tavalise toidu punase ruuduna
        pygame.draw.rect(screen, red, [foodX, foodY, snakeBlock, snakeBlock])

        # -----------------------------
        # ERITOIDU JOONISTAMINE
        # -----------------------------

        # Kui eritoit on olemas, joonistame selle kollase ruuduna
        if bonusFood:
            pygame.draw.rect(screen, yellow, [bonusX, bonusY, snakeBlock, snakeBlock])

        # -----------------------------
        # TAKISTUSTE JOONISTAMINE
        # -----------------------------

        # Käime kõik takistused läbi
        for wall in walls:

            # Joonistame iga takistuse halli ruuduna
            pygame.draw.rect(screen, gray, [wall[0], wall[1], snakeBlock, snakeBlock])

        # -----------------------------
        # USSI PEA LISAMINE
        # -----------------------------

        # Loome uue listi ussi pea koordinaatide jaoks
        snakeHead = []

        # Lisame pea x-koordinaadi
        snakeHead.append(posX)

        # Lisame pea y-koordinaadi
        snakeHead.append(posY)

        # Lisame pea kogu ussi keha listi lõppu
        snakeList.append(snakeHead)

        # -----------------------------
        # USSI PIKKUSE PIIRAMINE
        # -----------------------------

        # Kui kehaosade arv on suurem kui lubatud ussi pikkus,
        # eemaldame kõige vanema kehaosa
        # See tekitab liikumise efekti
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # -----------------------------
        # KOKKUPÕRGE ISEENDAGA
        # -----------------------------

        # Kontrollime kõiki kehaosi peale viimase,
        # sest viimane on ussi pea
        for block in snakeList[:-1]:

            # Kui pea asukoht kattub mõne kehaosaga,
            # siis uss sõitis iseendale otsa
            if block == snakeHead:
                gameclose = True

        # -----------------------------
        # KOKKUPÕRGE TAKISTUSEGA
        # -----------------------------

        # Käime kõik takistused läbi
        for wall in walls:

            # Kui ussi pea koordinaadid kattuvad takistuse koordinaatidega,
            # siis mängija kaotab
            if posX == wall[0] and posY == wall[1]:
                gameclose = True

        # -----------------------------
        # USSI JOONISTAMINE
        # -----------------------------

        # Joonistame ussi ekraanile
        drawSnake(snakeBlock, snakeList)

        # Uuendame ekraani, et kõik joonistatud objektid nähtavaks muutuksid
        pygame.display.update()

        # -----------------------------
        # TAVALISE TOIDU SÖÖMINE
        # -----------------------------

        # Kui ussi pea asukoht kattub toidu asukohaga,
        # tähendab see, et uss sõi toidu ära
        if posX == foodX and posY == foodY:

            # Loome uue toidu uude juhuslikku kohta
            foodX, foodY = newFood()

            # Suurendame ussi pikkust ühe ploki võrra
            snakeLength += 1

            # Suurendame skoori ühe punkti võrra
            score += 1

            # -----------------------------
            # TASEME JA KIIRUSE TÕSTMINE
            # -----------------------------

            # Iga 5 punkti järel tõuseb tase
            # Näiteks skoor 5, 10, 15 jne
            if score % 5 == 0:

                # Suurendame taset ühe võrra
                level += 1

                # Suurendame ussi kiirust
                snakeSpeed += 2

                # Loome uued takistused, et mäng muutuks raskemaks
                walls = createWalls()

            # -----------------------------
            # ERITOIDU TEKKIMINE
            # -----------------------------

            # random.randint(1, 4) annab juhusliku arvu 1 kuni 4
            # Kui arv on 1, tekib eritoit
            # See tähendab umbes 25% võimalust
            if random.randint(1, 4) == 1:

                # Märgime, et eritoit on nüüd olemas
                bonusFood = True

                # Loome eritoidule juhusliku asukoha
                bonusX, bonusY = newFood()

                # Määrame, kui kaua eritoit ekraanil püsib
                bonusCounter = 300

        # -----------------------------
        # ERITOIDU SÖÖMINE
        # -----------------------------

        # Kui eritoit on olemas ja ussi pea on selle kohal,
        # siis uss sööb eritoidu ära
        if bonusFood and posX == bonusX and posY == bonusY:

            # Eemaldame eritoidu ekraanilt
            bonusFood = False

            # Suurendame ussi pikkust kahe võrra
            snakeLength += 2

            # Suurendame skoori kolme võrra
            score += 3

        # -----------------------------
        # ERITOIDU AJAPIIRANG
        # -----------------------------

        # Kui eritoit on olemas, vähendame selle loendurit
        if bonusFood:

            # Iga mängutsükli sammuga väheneb loendur ühe võrra
            bonusCounter -= 1

            # Kui loendur jõuab nulli,
            # siis eritoit kaob ekraanilt
            if bonusCounter <= 0:
                bonusFood = False

        # -----------------------------
        # MÄNGU KIIRUSE KONTROLL
        # -----------------------------

        # clock.tick piirab, mitu korda sekundis tsükkel töötab
        # snakeSpeed suureneb taseme tõustes,
        # seega uss hakkab kiiremini liikuma
        clock.tick(snakeSpeed)

    # Kui mängutsükkel lõpeb, sulgeme pygame'i
    pygame.quit()

    # Lõpetame programmi
    quit()


# Käivitame mängu
gameLoop()