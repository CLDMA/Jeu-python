import pygame
import subprocess
import os
import sys
import time

def run_game():
    # Initialisation de Pygame
    pygame.init()

    # Définir la taille de la fenêtre en plein écran
    screen_width = pygame.display.Info().current_w  # Largeur de l'écran
    screen_height = pygame.display.Info().current_h  # Hauteur de l'écran
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Menu Principal")

    # Charger l'image de fond
    try:
        background = pygame.image.load("assets/img/background.jpg")
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except pygame.error:
        print("Erreur : Fichier d'image non trouvé.")

    # Définir les couleurs
    BLACK = (0, 0, 0)

    # Charger la police personnalisée
    try:
        font = pygame.font.Font("assets/police/police_squid_game.ttf", 40)
    except IOError:
        print("Erreur : Impossible de charger la police. Assurez-vous que le chemin est correct.")

    def draw_button(surface, text, x, y, width, height, font):
        text_surface = font.render(text, True, BLACK)
        button_rect = pygame.Rect(x, y, width, height)
        surface.blit(text_surface,
                     (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))
        return button_rect

    def run_script(script_name):
        try:
            # Ouvre le script dans un nouveau processus
            subprocess.Popen(['python', script_name])
            time.sleep(2)
            pygame.quit()
            sys.exit()
        except FileNotFoundError:
            print(f"Erreur : Le fichier {script_name} n'a pas été trouvé.")

    def main():
        running = True
        button_width = 200
        button_height = 50
        button_x = (screen_width - button_width) // 3
        total_button_height = 4 * button_height + 3 * 10
        button_y_start = (screen_height - total_button_height) // 2

        while running:
            screen.fill((255, 255, 255))  # Fond blanc par défaut
            screen.blit(background, (0, 0))

            # Dessiner les boutons
            button_rejouer = draw_button(screen, "Rejouer", button_x, button_y_start, button_width, button_height, font)
            button_tir = draw_button(screen, "Tir a la corde", button_x, button_y_start + button_height + 10, button_width, button_height, font)
            button_accueil = draw_button(screen, "Accueil", button_x, button_y_start + 2 * (button_height + 10), button_width, button_height, font)
            button_quitter = draw_button(screen, "Quitter", button_x, button_y_start + 3 * (button_height + 10), button_width, button_height, font)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_rejouer.collidepoint(mouse_pos):
                        run_script('un_deux_trois_soleil.py')  # Lien corrigé pour le jeu "1,2,3 Soleil"
                    elif button_tir.collidepoint(mouse_pos):
                        run_script('tire_corde.py')
                    elif button_accueil.collidepoint(mouse_pos):
                        run_script('menu.py')  # Lien corrigé pour le script "Accueil"
                    elif button_quitter.collidepoint(mouse_pos):
                        running = False
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()

        pygame.quit()

    main()

if __name__ == "__main__":
    while True:
        run_game()  # Relance le jeu après une fermeture
