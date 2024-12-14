import pygame
import random
import time
import os
import subprocess

# Constantes
LARGEUR = 900
HAUTEUR = 600
FPS = 60
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
VERT = (207, 2, 115)
ROUGE = (255, 0, 0)

# Touche
TOUCHES_POSSIBLES = [
    pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h,
    pygame.K_i, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p,
    pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t, pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x,
    pygame.K_y, pygame.K_z
]

# Initialisation de Pygame et des polices
pygame.init()
pygame.font.init()

# Charger la police personnalisée ou une police par défaut
try:
    ma_police = pygame.font.Font("assets/police/police_squid_game.ttf", 25)
except FileNotFoundError:
    print("Impossible de trouver la police personnalisée, utilisation de la police par défaut.")
    ma_police = pygame.font.Font(None, 25)

# Charger une image d'arrière-plan
try:
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (LARGEUR, HAUTEUR))
except pygame.error:
    print("Impossible de charger l'image d'arrière-plan.")
    background_image = None


class TirALaCorde:
    def __init__(self):
        # Initialisation de la fenêtre de jeu et des paramètres de base
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Tir à la Corde")
        self.clock = pygame.time.Clock()
        self.position_corde = LARGEUR // 2
        self.touche_actuelle = random.choice(TOUCHES_POSSIBLES)
        self.dernier_changement = time.time()
        self.temps_entre_changements = 3  # Délai en secondes avant changement de touche

        # Initialisation du score
        self.score = 0
        self.high_score = 0
        self.tous_les_scores = []
        self.nom_joueur = self.charger_nom_joueur()

        # Charger les scores depuis un fichier
        try:
            with open("high_scores.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        self.tous_les_scores.append(int(parts[1]))
                        if int(parts[1]) > self.high_score:
                            self.high_score = int(parts[1])
        except (FileNotFoundError, ValueError):
            self.tous_les_scores = []

        # Indicateurs de l'état du jeu
        self.partie_terminee = False
        self.gagnant = None
        self.police = ma_police
        self.vitesse = 0

        # Chargement des images avec gestion des erreurs
        self.image_ordi = self.charger_image("assets/img/bonhomme_ordinateur.png", (70, 110))
        self.image_corde = self.charger_image("assets/img/corde.png", (1000, 90))
        self.image_noeud = self.charger_image("assets/img/noeud.png", (50, 70))
        self.image_perso = self.charger_image("assets/img/perso_vert.png", (150, 120))

    def charger_image(self, chemin, taille):
        try:
            image = pygame.image.load(chemin)
            return pygame.transform.scale(image, taille)
        except pygame.error:
            print(f"Impossible de charger l'image {chemin}")
            return None

    def charger_nom_joueur(self):
        """
        Charge le nom du joueur depuis le fichier joueur.txt.
        Si le fichier n'existe pas ou est vide, retourne 'Joueur'.
        """
        try:
            with open("joueur.txt", "r") as f:
                nom = f.readline().strip()
                return nom if nom else "Joueur"
        except FileNotFoundError:
            print("Fichier joueur.txt non trouvé. Utilisation du nom 'Joueur'.")
            return "Joueur"

    def changer_touche(self):
        temps_actuel = time.time()
        if temps_actuel - self.dernier_changement >= self.temps_entre_changements:
            self.touche_actuelle = random.choice(TOUCHES_POSSIBLES)
            self.dernier_changement = temps_actuel

    def obtenir_nom_touche(self):
        return pygame.key.name(self.touche_actuelle).upper()

    def sauvegarder_score(self):
        """
        Sauvegarde tous les scores dans le fichier high_scores.txt.
        """
        try:
            if self.score > 0:  # Ne sauvegarde que les scores non nuls
                self.tous_les_scores.append(self.score)
            with open("high_scores.txt", "w") as f:
                for score in self.tous_les_scores:
                    f.write(f"{self.nom_joueur},{score}\n")
        except IOError:
            print("Erreur lors de la sauvegarde des scores.")

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sauvegarder_score()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == self.touche_actuelle:
                    self.score += 1

                if self.partie_terminee and event.key == pygame.K_m:
                    self.sauvegarder_score()
                    pygame.quit()
                    subprocess.run(['python', 'menu.py'])
                    return False

        if not self.partie_terminee:
            self.changer_touche()
            touches = pygame.key.get_pressed()
            if touches[self.touche_actuelle]:
                self.vitesse -= 0.15
            else:
                self.vitesse += 0.08
            self.vitesse = max(-1.0, min(0.8, self.vitesse))
            self.vitesse *= 0.95
            self.position_corde += self.vitesse

        if pygame.key.get_pressed()[pygame.K_r] and self.partie_terminee:
            self.sauvegarder_score()
            self.__init__()
        return True

    def mettre_a_jour(self):
        if not self.partie_terminee:
            self.changer_touche()
            if self.position_corde <= LARGEUR * 0.2:
                self.partie_terminee = True
                self.gagnant = self.nom_joueur
            elif self.position_corde >= LARGEUR * 0.8:
                self.partie_terminee = True
                self.gagnant = "Homme masqué"

    def dessiner(self):
        if background_image:
            self.ecran.blit(background_image, (0, 0))
        else:
            self.ecran.fill(BLANC)

        if self.image_corde:
            self.ecran.blit(self.image_corde, (LARGEUR - 900, HAUTEUR // 2 - 40))

        if self.image_perso:
            self.ecran.blit(self.image_perso, (50, HAUTEUR // 2 - 40))
        else:
            pygame.draw.rect(self.ecran, BLEU, (50, HAUTEUR // 2 - 40, 40, 80))

        if self.image_ordi:
            self.ecran.blit(self.image_ordi, (LARGEUR - 90, HAUTEUR // 2 - 40))
        else:
            pygame.draw.rect(self.ecran, (255, 0, 0), (LARGEUR - 90, HAUTEUR // 2 - 40, 40, 80))

        if self.image_noeud:
            x = int(self.position_corde - self.image_noeud.get_width() // 2)
            y = int(HAUTEUR // 2 - self.image_noeud.get_height() // 2)
            self.ecran.blit(self.image_noeud, (x, y))
        else:
            pygame.draw.circle(self.ecran, NOIR, (int(self.position_corde), HAUTEUR // 2), 10)

        texte_score = self.police.render(f"Score: {self.score}", True, VERT)
        rect_score = texte_score.get_rect(topright=(LARGEUR - 20, 100))
        self.ecran.blit(texte_score, rect_score)

        texte_high_score = self.police.render(f"Meilleur score: {self.high_score}", True, VERT)
        rect_high_score = texte_high_score.get_rect(topright=(LARGEUR - 20, 130))
        self.ecran.blit(texte_high_score, rect_high_score)

        if not self.partie_terminee:
            texte_touche = self.police.render(f"Appuyez sur : {self.obtenir_nom_touche()}", True, VERT)
            rect_touche = texte_touche.get_rect(center=(LARGEUR // 2, 50))
            self.ecran.blit(texte_touche, rect_touche)

            temps_restant = int(self.temps_entre_changements - (time.time() - self.dernier_changement))
            texte_temps = self.police.render(f"Changement dans : {temps_restant}", True, VERT)
            rect_temps = texte_temps.get_rect(center=(LARGEUR // 2, 100))
            self.ecran.blit(texte_temps, rect_temps)

        else:
            # Positionner les textes plus bas
            hauteur_texte = 400
            espacement = 50

            if self.gagnant == self.nom_joueur:
                texte_fin = self.police.render(f"Félicitations {self.nom_joueur}, vous avez gagne !", True, VERT)
            else:
                texte_fin = self.police.render(f"Vous avez perdu contre {self.gagnant}.", True, ROUGE)

            rect_fin = texte_fin.get_rect(center=(LARGEUR // 2, hauteur_texte))
            self.ecran.blit(texte_fin, rect_fin)

            texte_recommencer = self.police.render("Appuyez sur R pour recommencer.", True, VERT)
            rect_recommencer = texte_recommencer.get_rect(center=(LARGEUR // 2, hauteur_texte + espacement))
            self.ecran.blit(texte_recommencer, rect_recommencer)

            texte_menu = self.police.render("Appuyez sur M pour retourner au menu.", True, VERT)
            rect_menu = texte_menu.get_rect(center=(LARGEUR // 2, hauteur_texte + espacement * 2))
            self.ecran.blit(texte_menu, rect_menu)

    def boucle_principale(self):
        en_cours = True
        while en_cours:
            self.clock.tick(FPS)
            en_cours = self.gerer_evenements()
            self.mettre_a_jour()
            self.dessiner()
            pygame.display.flip()

# Démarrage du jeu
if __name__ == "__main__":
    jeu = TirALaCorde()
    jeu.boucle_principale()
    pygame.quit()
