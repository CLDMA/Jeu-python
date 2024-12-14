import pygame
import sys
import subprocess  # Ajouté pour lancer le script externe

pygame.init()
pygame.mixer.init()
X, Y = 900, 600
screen = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Menu")

# Aide couleur
blanc = (255, 255, 255)
noir = (0, 0, 0)
gris = (200, 200, 200)
rose = (207, 2, 115)
cyan = (36, 159, 156)

# Charger le fond d'écran
background = pygame.image.load("assets/img/background.png")
background = pygame.transform.scale(background, (X, Y))

# Charger la musique
musique = pygame.mixer.music.load("./assets/sound/musique_menu.mp3")
pygame.mixer.music.play(10, 0.0)

# Charger la police Squid Game
button_font = pygame.font.Font("assets/police/police_squid_game.ttf", 50)
credit_font = pygame.font.Font("assets/police/police_squid_game.ttf", 25)
font = pygame.font.Font(None, 50)

buttons = {
    "Mode Histoire": pygame.Rect(X // 2 - 100, 255, 250, 50),
    "Jeu Libre": pygame.Rect(X // 2 - 100, 330, 250, 50),
    "Statistiques": pygame.Rect(X // 2 - 100, 405, 250, 50),
    "Quitter": pygame.Rect(X // 2 - 100, 480, 250, 50),
    "Credit": pygame.Rect(X // 2 - -215, 545, 150, 30),
}

# Définir le bouton "Retour" pour les crédits
credit_buttons = {
    "Retour": pygame.Rect(X // 2 - 50, Y - 70, 150, 50)
}

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def histoire():
    screen.blit(background, (0, 0))  # Garder le fond d'écran
    draw_text("Entrez votre numero de joueur", credit_font, rose, screen, X // 2, Y // 2 - 50)
    draw_text("Appuyez sur Entree pour continuer", credit_font, rose, screen, X // 2, Y // 2 + 100)

    # Input du numéro
    pygame.draw.rect(screen, gris, pygame.Rect(X // 2 - 100, Y // 2 + 0, 200, 40))
    draw_text(joueur_text, font, noir, screen, X // 2, Y // 2 + 0 + 20)
    pygame.display.flip()

def statistique():
    # Charger et trouver le meilleur score (le plus bas)
    try:
        with open("high_scores.txt", "r") as f:
            scores = f.readlines()
            best_score_line = None
            best_score = float('inf')  # Initialisation à un score très élevé
            for line in scores:
                line = line.strip()  # Enlever espaces et sauts de ligne inutiles
                if ',' in line:  # Vérifier la présence d'une virgule pour séparer score et joueur
                    parts = line.split(',')  # Séparer en deux parties (joueur, score)
                    try:
                        score = float(parts[1])  # Convertir la deuxième partie (score) en flottant
                        if score < best_score:  # Vérifier si c'est le score le plus bas
                            best_score = score
                            best_score_line = line  # Garder la ligne correspondante
                    except ValueError:
                        pass  # Ignorer si la conversion échoue
            if best_score_line:
                best_score_text = f"{best_score_line.split(',')[0]} avec un score de {int(best_score)}"
            else:
                best_score_text = "Aucun score enregistré"
    except FileNotFoundError:
        best_score_text = "Aucun score enregistré"

    # Charger et trouver le meilleur temps
    try:
        with open("temps.txt", "r") as f:
            times = f.readlines()
            # Extraire uniquement les temps valides (nombres flottants)
            times = [line.strip() for line in times if line.strip().replace('.', '', 1).isdigit()]
            times = [float(time) for time in times]  # Convertir en flottants
            best_time = min(times) if times else "Aucun temps enregistré"
    except FileNotFoundError:
        best_time = "Aucun temps enregistré"

    # Afficher les statistiques
    screen.blit(background, (0, 0))
    draw_text("Statistiques du joueur :", credit_font, rose, screen, X // 2, Y // 2 - 50)
    draw_text(f"Meilleur score: {best_score_text}", credit_font, cyan, screen, X // 2, Y // 2)
    draw_text(f"Meilleur temps: {best_time}", credit_font, rose, screen, X // 2, Y // 2 + 50)

    # Dessiner le bouton "Retour"
    for button_text, button_rect in credit_buttons.items():
        draw_text(button_text, button_font, cyan, screen, button_rect.centerx, button_rect.centery)



def credit():
    screen.fill(noir)
    draw_text("Credit", button_font, rose, screen, X // 2, Y // 3 - 110)
    draw_text("LE DREN MARTINET-ANDRIEUX Celian", credit_font, cyan, screen, X // 2, Y // 3 - 50)
    draw_text("POULAIN Mailys", credit_font, rose, screen, X // 2, Y // 3)
    draw_text("DJEDIDEN Nadir", credit_font, cyan, screen, X // 2, Y // 3 + 50)
    draw_text("MALLET Samuel", credit_font, rose, screen, X // 2, Y // 3 + 100)

    # Dessiner le bouton "Retour"
    for button_text, button_rect in credit_buttons.items():
        draw_text(button_text, button_font, cyan, screen, button_rect.centerx, button_rect.centery)

running = True
montrer_credit = False
montrer_histoire = False
montrer_statistique = False

# Variable pour stocker le n° du joueur
joueur_text = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if montrer_credit:
                    if credit_buttons["Retour"].collidepoint(event.pos):
                        print("Retour au menu principal depuis les crédits")
                        montrer_credit = False
                        montrer_histoire = False
                        montrer_statistique = False  # Assurez-vous de désactiver toutes les autres vues
                elif montrer_statistique:  # Ajoutez cette condition pour la partie statistique
                    if credit_buttons["Retour"].collidepoint(event.pos):
                        print("Retour au menu principal depuis les statistiques")
                        montrer_statistique = False
                        montrer_histoire = False
                        montrer_credit = False
                else:
                    if buttons["Mode Histoire"].collidepoint(event.pos):
                        print("Mode Histoire ouvert")
                        montrer_histoire = True
                    elif buttons["Jeu Libre"].collidepoint(event.pos):
                        print("Jeu Libre ouvert")
                        import sous_menu
                        pygame.quit()
                        sys.exit()
                    elif buttons["Statistiques"].collidepoint(event.pos):
                        print("Statistiques ouvertes")
                        montrer_statistique = True
                    elif buttons["Quitter"].collidepoint(event.pos):
                        print("Jeu quitté")
                        pygame.quit()
                        sys.exit()
                    elif buttons["Credit"].collidepoint(event.pos):
                        print("Credits ouverts")
                        montrer_credit = True
                        montrer_histoire = False
                        montrer_statistique = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                joueur_text = joueur_text[:-1]
            elif event.key == pygame.K_RETURN and joueur_text != "":
                pseudo = f"Joueur {joueur_text}"
                print(f"Bienvenue, {pseudo}, à Squid Game !")
                
                # Enregistrer le pseudo dans le fichier joueur.txt
                with open("joueur.txt", "w") as f:
                    f.write(pseudo)  # Écrit le pseudo dans le fichier

                screen.fill(noir)
                screen.blit(background, (0, 0))
                draw_text(f"Bienvenue, {pseudo}, à Squid Game !", font, rose, screen, X // 2, Y // 2)
                pygame.display.flip()
                pygame.time.wait(3000)  # Attendre 3 secondes avant de quitter
                
                # Fermer pygame et lancer le script "un_deux_trois_soleil.py"
                pygame.quit()
                subprocess.run(["python", "un_deux_trois_soleil.py"])  # Lancer le script
                sys.exit()  # Quitter le programme principal

            else:
                if event.unicode.isalnum():
                    joueur_text += event.unicode

    if montrer_credit:
        credit()
    elif montrer_histoire:
        histoire()
    elif montrer_statistique:
        statistique()
    else:
        screen.blit(background, (0, 0))
        for button_text, button_rect in buttons.items():
            draw_text(button_text, button_font, rose, screen, button_rect.centerx, button_rect.centery)

    pygame.display.flip()
