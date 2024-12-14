import pygame
import sys
import subprocess

pygame.init()
pygame.mixer.init()


X, Y = 900, 600
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Chargement")

# Charger le fond d'écran
background = pygame.image.load("assets/img/chargement.png")
background = pygame.transform.scale(background, (X, Y))

# Charger le son de chargement
pygame.mixer.music.load("assets/sound/chargement.mp3")

# Aide Couleurs
noir = (0, 0, 0)
rose = (207, 2, 115)

bar_width = 400
bar_height = 30
bar_x = (X - bar_width) // 2
bar_y = (Y - bar_height) // 1.25
progress = 0
max_progress = 100
clock = pygame.time.Clock()
pygame.mixer.music.play(loops=0, start=0.0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, noir, (bar_x, bar_y, bar_width, bar_height), 2)
    fill_width = (progress / max_progress) * bar_width
    pygame.draw.rect(screen, rose, (bar_x, bar_y, fill_width, bar_height))
    progress += 1
    if progress > max_progress:
        running = False
    pygame.display.flip()
    clock.tick(50)  # Durée de la barre de chargement
    
    
pygame.quit()
subprocess.run(["python", "menu.py"])
sys.exit()
