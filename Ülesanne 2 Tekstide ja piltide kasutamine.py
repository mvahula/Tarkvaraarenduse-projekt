#impordin pygame
import pygame
pygame.init()

#Loon uue pygame mängu
screen = pygame.display.set_mode([640, 480])

#panen mängule nimeks ülesande numbri
pygame.display.set_caption("2")

#Lisan pildid
#Panen tausta backroundiks
bg = pygame.image.load("bg_shop.jpg")
screen.blit(bg, [0, 0])

#Lisan pildi müüjast ja muudan suurust
pygame.transform.scale(screen, screen.get_size())
seller = pygame.image.load("seller.png")
seller = pygame.transform.scale(seller, (300, 375))
screen.blit(seller, [100, 100])

#Lisan pildi jutumullist
Chat = pygame.image.load("chat.png")
screen.blit(Chat, [300, 10])

#Lisan teksti
font = pygame.font.SysFont("Times New Roman", 25)
text = font.render("Tere, Olen Meriel Vahula", True, (255, 255, 255))
screen.blit(text, [320,100])

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

