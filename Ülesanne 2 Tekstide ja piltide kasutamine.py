#impordin pygame
import pygame
import math

pygame.init()

#Loon uue pygame mängu
screen = pygame.display.set_mode([640, 480])

#Panen mängule nimeks ülesande numbri
pygame.display.set_caption("2")


#See funktsioon eemaldab tordilt heleda/valge ruudulise tausta
def remove_light_background(image):
    image = image.convert_alpha()
    width = image.get_width()
    height = image.get_height()

    for x in range(width):
        for y in range(height):
            r, g, b, a = image.get_at((x, y))

            #Kui piksel on hele ja hallikas/valge, teen selle läbipaistvaks
            if r > 205 and g > 205 and b > 205 and abs(r - g) < 20 and abs(g - b) < 20:
                image.set_at((x, y), (r, g, b, 0))

    return image


#Lisan taustapildi
bg = pygame.image.load("bg_shop.jpg")
screen.blit(bg, [0, 0])


#Lisan VIKK logo vasakusse ülemisse nurka
logo = pygame.image.load("VIKK logo.png").convert_alpha()
logo = pygame.transform.scale(logo, (250, 50))
screen.blit(logo, [10, 25])


#Lisan logo parema külje juurde kaarega teksti
font = pygame.font.SysFont("comicsansms", 13)
def draw_curved_text(surface, text, center, radius):
    for i, char in enumerate(text):
        angle = math.radians(270 + i * (180 / len(text)))
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)

        char_surf = font.render(char, True, (255, 255, 255))
        rect = char_surf.get_rect(center=(x, y))
        surface.blit(char_surf, rect)
draw_curved_text(screen, "TULEVIK 2050", (230, 55), 50)

#Lisan seinale mõõga
sword = pygame.image.load("Mõõk.png").convert_alpha()
sword = pygame.transform.scale(sword, (170, 120))
sword = pygame.transform.rotate(sword, -60)
screen.blit(sword, [-50, 100])


#Lisan laua peale tordi
cake = pygame.image.load("tort.png").convert_alpha()

#Võtan tordilt heleda tausta ära
cake = remove_light_background(cake)

#Muudan tordi suurust
cake = pygame.transform.scale(cake, (85, 65))

#Panen tordi natuke ülespoole, et see oleks rohkem laua peal
screen.blit(cake, [460, 228])


#Lisan pildi müüjast ja muudan suurust
seller = pygame.image.load("seller.png").convert_alpha()
seller = pygame.transform.scale(seller, (300, 375))
screen.blit(seller, [100, 100])


#Lisan pildi jutumullist
Chat = pygame.image.load("chat.png").convert_alpha()
screen.blit(Chat, [300, 10])


#Lisan jutumulli sisse teksti
font = pygame.font.SysFont("Times New Roman", 25)
text = font.render("Tere, Olen Meriel Vahula", True, (255, 255, 255))
screen.blit(text, [320, 100])


#Uuendan ekraani, et kõik pildid ja tekst nähtavale tuleksid
pygame.display.flip()


#Mängu tsükkel, et aken kohe kinni ei läheks
running = True
while running:
    for event in pygame.event.get():
        #Kui kasutaja vajutab akna X-nuppu, pannakse mäng kinni
        if event.type == pygame.QUIT:
            running = False


#Lõpetan pygame'i töö
pygame.quit()
