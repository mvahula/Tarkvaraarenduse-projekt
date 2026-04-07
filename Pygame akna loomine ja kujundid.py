'''
#Pygame akna loomine ja kujundid

#PyGame akna loomine

#Impordin Pygame mooduli
import pygame

#Käivitan mooduli
pygame.init()

#Tekitan akna mõõtudega 640x480px
screen = pygame.display.set_mode([640, 480])

#Lisan mänguaknale nimetuse
pygame.display.set_caption("My Screen")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
'''

#pygame.RESZABLE
'''
import pygame
pygame.init()

#Kasutan pygame.RESIZABLE et saaks akent nurgast suuremaks ja
#väiksemaks lohistada
screen = pygame.display.set_mode([640, 480], pygame.RESIZABLE)

pygame.display.set_caption("My Screen")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
'''
'''
#Värvide loomine

#laen pygame teegi
import pygame

#pygame käivitamine
pygame.init()

#tekitan akna 640x480
screen = pygame.display.set_mode([640, 480])

#kuvan ekraani nime
pygame.display.set_caption("My Screen")

#muudan taustavärvi
screen.fill([204, 255, 255])

#värskendan ekraani
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
'''

#Kujundite loomine

import pygame
pygame.init()

#ekraani seaded
screen = pygame.display.set_mode([640, 480])
pygame.display.set_caption("My Screen")
screen.fill([204, 255, 255])

#joonistamine
pygame.draw.line(screen, [255, 0, 0], [100, 100], [200, 200], 2)

#ristkülik
pygame.draw.rect(screen, [0, 255, 0], [50, 80, 200, 300], 2)

#ring
pygame.draw.circle(screen, [0, 0, 255], [150, 200], 100, 1)

#hulknurk
pygame.draw.polygon(screen, [255, 0, 255], [[50, 50], [100, 50], [100, 150], [250, 50], [350, 250], [50, 250]], 2)

#ovaal
pygame.draw.ellipse(screen, [0, 225, 0], [50, 80, 200, 300], 2)

#kaar
pygame.draw.arc(screen,[0,0,0], [100,100,250,200], 0, 3.14*1.5, 1)

pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()