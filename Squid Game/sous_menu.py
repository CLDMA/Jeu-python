import pygame
import sys
import subprocess

pygame.init()
pygame.mixer.init() 
X, Y = 900, 600
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Menu")

#Aide couleur
blanc = (255, 255, 255)
noir = (0, 0, 0)
gris = (200, 200, 200)
rose = (207, 2, 115)
cyan = (36,159,156)

# Charger le fond d'écran
background = pygame.image.load("assets/img/background.png")
background = pygame.transform.scale(background, (X, Y))

# Charger la musique
musique = pygame.mixer.music.load("assets/sound/musique_menu.mp3")
pygame.mixer.music.play(10, 0.0)

# Charger la police Squid Game
button_font = pygame.font.Font("assets/police/police_squid_game.ttf", 50)
credit_font = pygame.font.Font("assets/police/police_squid_game.ttf", 25)
font = pygame.font.Font(None, 50)


buttons = {
    "1,2,3 Soleil": pygame.Rect(X // 2 - 100, 255, 250, 50),
    "Tir a la corde": pygame.Rect(X // 2 - 100, 330, 250, 50),
    "PROCHAINEMENT": pygame.Rect(X // 2 - 100, 405, 250, 50),
    "Retour": pygame.Rect(X // 2 - 100, 480, 250, 50),
}

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Boucle principale
running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: #Clic Gauche
                if buttons["1,2,3 Soleil"].collidepoint(event.pos):
                    print("1,2,3 Soleil ouvert")
                    pygame.quit()
                    subprocess.run([sys.executable, "un_deux_trois_soleil.py"])  # Lancer le script 1,2,3 Soleil
                    sys.exit()
                elif buttons["Tir a la corde"].collidepoint(event.pos):
                    print("Tir a la corde ouvert")
                    pygame.quit()
                    subprocess.run([sys.executable, "tire_corde.py"])  # Lancer le script Tir à la corde
                    sys.exit()
                elif buttons["PROCHAINEMENT"].collidepoint(event.pos):
                    print("Pierre de gues ouvertes")
                elif buttons["Retour"].collidepoint(event.pos):
                    print("Retour fait")
                    import menu
                    pygame.quit()
                    sys.exit()

    # Dessiner les boutons
    for button_text, button_rect in buttons.items():
        draw_text(button_text, button_font, rose, screen, button_rect.centerx, button_rect.centery)

    # Mettre à jour l'affichage
    pygame.display.flip()
 
    
