import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

# Initialiser le début du jeu avant la boucle principale
game_start_time = time.time()

# Configuration de la fenêtre en plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
pygame.display.set_caption("1, 2, 3 Soleil")

# Charger et adapter les images
background_image = pygame.image.load("assets/img/background.jpg")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Charger deux images pour l'animation du personnage
player_image_1 = pygame.image.load("assets/img/perso.png")  # Première image
player_image_2 = pygame.image.load("assets/img/perso 2.png")  # Deuxième image
player_image_1 = pygame.transform.scale(player_image_1, (screen_width // 32, screen_height // 16))
player_image_2 = pygame.transform.scale(player_image_2, (screen_width // 32, screen_height // 16))

# Charger l'image de la poupée
doll_image = pygame.image.load("assets/img/poupe.png")
doll_image = pygame.transform.scale(doll_image, (screen_width // 8, screen_height // 6))

# Couleurs
text_color = (0, 0, 0)

# Positions initiales
player_pos = [50, screen_height // 2]
finish_line_x = screen_width - 100

# Variables de jeu
green_light = False  # Commencer directement avec la phase GO
running = True

# Charger la police personnalisée
font_path = "assets/police/police_squid_game.ttf"
font_size = screen_height // 10
font = pygame.font.Font(font_path, font_size)

small_font_size = screen_height // 20
small_font = pygame.font.Font(font_path, small_font_size)

# Variables pour l'animation
animation_frame = 0  # Pour alterner entre les images de marche
animation_time = 0  # Pour vérifier le temps écoulé depuis la dernière alternance des images

# Charger le fichier audio pour le jeu
pygame.mixer.init()
audio_path = "assets/sound/123soleil.mp3"
try:
    pygame.mixer.music.load(audio_path)
except pygame.error as e:
    print(f"Erreur : Impossible de charger le fichier audio : {audio_path}")
    print(f"Détails : {e}")
    exit()

# Charger le son de perte
lose_sound_path = "assets/sound/lose_sound.wav"  # Remplacez par le chemin réel du son de perte
try:
    lose_sound = pygame.mixer.Sound(lose_sound_path)
except pygame.error as e:
    print(f"Erreur : Impossible de charger le fichier audio de perte : {lose_sound_path}")
    print(f"Détails : {e}")
    exit()

# Charger les meilleurs temps depuis un fichier
def load_best_times(file_path):
    try:
        with open(file_path, 'r') as file:
            # Convertir chaque ligne en float pour stocker les temps précis
            times = [float(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        times = []  # Si le fichier n'existe pas encore, on initialise une liste vide
    return times

# Sauvegarder les meilleurs temps dans un fichier, uniquement les 5 meilleurs
def save_best_times(file_path, times):
    with open(file_path, 'w') as file:
        for time_value in times[:5]:
            # Formater le temps avec 2 décimales pour une meilleure lisibilité
            file.write(f"{time_value:.2f}\n")

# Ajouter un temps et trier les 5 meilleurs
def add_best_time(file_path, new_time):
    times = load_best_times(file_path)
    times.append(new_time)
    times.sort()  # Trier les temps en ordre croissant (les plus petits temps sont les meilleurs)
    save_best_times(file_path, times)

# Afficher les 5 meilleurs temps
def display_best_times(file_path):
    times = load_best_times(file_path)
    max_display = 5

    # Afficher un titre
    title_text = small_font.render("Meilleurs Temps:", True, text_color)
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
    screen.blit(title_text, title_rect)

    # Afficher chaque temps dans une colonne
    for i, time_value in enumerate(times[:max_display]):
        # Formatage du texte pour chaque temps
        time_text = small_font.render(f"{i + 1}. {time_value:.2f} sec", True, text_color)
        # Calcul de la position y en fonction de l'index
        time_rect = time_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50 + i * 40))
        screen.blit(time_text, time_rect)


# Afficher les meilleurs temps après avoir gagné
if player_pos[0] >= finish_line_x:
    game_time = time.time() - game_start_time
    add_best_time("temps.txt", game_time)

    win_text = font.render("Vous avez gagne!", True, text_color)
    win_rect = win_text.get_rect(center=(screen_width // 2, screen_height - 150))
    screen.blit(win_text, win_rect)

    display_best_times("temps.txt")

    # Rendre la phrase d'instruction invisible
    instruction_text = ""

    pygame.display.flip()
    time.sleep(5)  # Attendre 5 secondes avant de quitter
    running = False


# Initialisation des durées des phases
def set_random_phase():
    global green_light_duration, red_light_duration, phase_start_time, green_light
    green_light_duration = random.randint(2, 6)
    red_light_duration = random.randint(3, 7)
    phase_start_time = time.time()
    green_light = not green_light

# Dessiner la ligne d'arrivée
def draw_finish_line(screen, finish_line_x, screen_height, cell_size=40):
    finish_line_x = screen_width - (2 * cell_size)
    for row in range(screen_height // cell_size + 1):
        for col in range(2):
            x = finish_line_x + col * cell_size
            y = row * cell_size
            color = (0, 0, 0) if (row + col) % 2 == 0 else (255, 255, 255)
            pygame.draw.rect(screen, color, (x, y, cell_size, cell_size))

# Fonction de compte à rebours
def countdown():
    countdown_times = ["3", "2", "1", "GO!"]
    for time_text in countdown_times:
        screen.blit(background_image, (0, 0))
        countdown_text = font.render(time_text, True, text_color)
        countdown_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(countdown_text, countdown_rect)
        pygame.display.flip()
        pygame.time.delay(1000)

# Lancer le compte à rebours
countdown()
set_random_phase()  # Définir la première phase

# Marquer le temps de début de jeu
game_start_time = time.time()

def display_loss_page(file_path):
    try:
        # Ouvrir le fichier et lire son contenu
        with open(file_path, "r") as file:
            code = file.read()
        # Exécuter le code dans le contexte actuel
        exec(code, globals())  # Utiliser globals() pour éviter des problèmes de portée
    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} n'a pas été trouvé.")
    except Exception as e:
        print(f"Erreur lors de l'exécution du fichier : {e}")

# Boucle principale
while running:
    screen.blit(background_image, (0, 0))

    # Dessiner la ligne d'arrivée
    draw_finish_line(screen, finish_line_x, screen_height, screen_height // 20)

    # Afficher le personnage uniquement si le jeu n'est pas en phase Game Over
    if running:
        if green_light:
            # Phase GO : afficher "GO!" et les instructions
            go_text = font.render("GO!", True, text_color)
            go_rect = go_text.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(go_text, go_rect)

            instruction_text = small_font.render("Appuyez sur la fleche pour avancer", True, text_color)
            instruction_rect = instruction_text.get_rect(center=(screen_width // 2 - 50, screen_height - 50))  # Ajustement de la position à gauche
            screen.blit(instruction_text, instruction_rect)

            # Alterner entre les deux images uniquement si la touche droite est pressée
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                # Gérer l'animation de marche (alterner les images)
                current_time = time.time()
                if current_time - animation_time > 0.5:  # Alterner toutes les 0.5 secondes
                    animation_frame = 1 - animation_frame  # Alterner entre 0 et 1
                    animation_time = current_time

                # Choisir l'image en fonction du frame de l'animation
                player_image = player_image_1 if animation_frame == 0 else player_image_2

                # Avancer le joueur
                player_pos[0] += screen_width // 600  # Avance deux fois moins vite
            else:
                # Reste immobile si aucune touche n'est pressée
                player_image = player_image_1  # Ou n'importe quelle image fixe

            # Reprendre la musique pendant la phase "GO"
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()

        else:  # Phase "1, 2, 3 Soleil"
            player_image = player_image_1  # Le joueur reste immobile

            # Arrêter la musique pendant la phase "1, 2, 3 Soleil"
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            # Afficher la poupée
            doll_rect = doll_image.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(doll_image, doll_rect)

            # Afficher "1, 2, 3 Soleil"
            doll_text = font.render("1, 2, 3 Soleil", True, text_color)
            text_rect = doll_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(doll_text, text_rect)

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                # Jouer le son de perte
                lose_sound.play()

                # Afficher "Vous avez perdu!"
                lose_text = font.render("Vous avez perdu!", True, text_color)
                text_rect = lose_text.get_rect(
                    center=(screen_width // 2, screen_height // 1.25))  # Changé de 1.5 à 1.25
                screen.blit(lose_text, text_rect)

                # Afficher "Game Over"
                game_over_text = font.render("Game Over", True, text_color)
                game_over_text_rect = game_over_text.get_rect(
                    center=(screen_width // 2, screen_height // 1.1))  # Changé de 1.25 à 1.1
                screen.blit(game_over_text, game_over_text_rect)

                pygame.display.flip()
                time.sleep(2)  # Attendre 2 secondes avant de fermer le jeu

                # Afficher le contenu du fichier page_perdu.py
                display_loss_page("fin_un_deux_trois_soleil.py")  # Exécuter le fichier avant de quitter

                running = False  # Arrêter le jeu après l'exécution du fichier

        # Dessiner le joueur seulement si le jeu n'est pas terminé
        if running:
            player_rect = player_image.get_rect(midbottom=(player_pos[0], screen_height * 0.75))
            screen.blit(player_image, player_rect)

    # Gérer les événements utilisateur
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Vérifier le changement de phase
    current_time = time.time()

    # Si on est en phase "GO" et que le temps est écoulé
    if green_light and current_time - phase_start_time > green_light_duration - 0.5:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    if green_light and current_time - phase_start_time > green_light_duration:
        set_random_phase()

    # Si on est en phase "1, 2, 3 Soleil" et que le temps est écoulé
    elif not green_light and current_time - phase_start_time > red_light_duration:
        set_random_phase()

    if player_pos[0] >= finish_line_x:
        game_time = time.time() - game_start_time
        add_best_time("temps.txt", game_time)

        win_text = font.render("Vous avez gagne!", True, text_color)
        win_rect = win_text.get_rect(center=(screen_width // 2, screen_height - 150))
        screen.blit(win_text, win_rect)

    # Afficher les meilleurs temps
        display_best_times("temps.txt")

        pygame.display.flip()
        time.sleep(5)  # Attendre 5 secondes avant d'afficher les meilleurs temps

    # Exécuter "page perdu.py" après la victoire
        display_loss_page("fin_un_deux_trois_soleil.py")

        running = False


    # Rafraîchir l'écran
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()