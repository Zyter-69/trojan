import pygame
import sys
import random
import os

pygame.init()

# Fenêtre
largeur = 600
hauteur = 400
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Snake Game")

# Chargement du fond
background = pygame.image.load("jeu/background.jpg")
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
if not os.path.exists("jeu/highscore.txt"):
    with open("jeu/highscore.txt", "w") as f:
        f.write("0")

with open("jeu/highscore.txt", "r") as f:
    high_score = int(f.read())


def save_high_score(score):
    with open("jeu/highscore.txt", "w") as f:
        f.write(str(score))


# ----- Fonction Principale du Jeu -----
def jeu():
    global high_score

    snake_x = 300
    snake_y = 200
    vx = 20
    vy = 0

    snake = []
    longueur = 3

    food_x = random.randrange(0, largeur, taille_bloc)
    food_y = random.randrange(0, hauteur, taille_bloc)

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
            vitesse += 0.3

            # Nouvelle nourriture
            food_x = random.randrange(0, largeur, taille_bloc)
            food_y = random.randrange(0, hauteur, taille_bloc)
        else:
            if len(snake) > longueur:
                del snake[0]

        # ----- AFFICHAGE -----
        fenetre.blit(background, (0, 0))

        # POMME STYLE RONDE
        pygame.draw.circle(fenetre, (220, 0, 0),
                            (food_x + taille_bloc // 2, food_y + taille_bloc // 2),
                            taille_bloc // 2)

        # Petite feuille verte
        pygame.draw.circle(fenetre, (0, 200, 0),
                            (food_x + 12, food_y + 4), 4)



        for i, bloc in enumerate(snake):
            x, y = bloc
            if i == len(snake) - 1:
                # TÊTE DU SERPENT
                pygame.draw.circle(fenetre, (35, 5, 229),
                                    (x + taille_bloc // 2, y + taille_bloc // 2),
                                    taille_bloc // 2)

                # YEUX
                pygame.draw.circle(fenetre, (0, 0, 0),
                                    (x + 6, y + 6), 3)
                pygame.draw.circle(fenetre, (0, 0, 0),
                                    (x + 14, y + 6), 3)
            else:
                # CORPS DU SERPENT
                pygame.draw.circle(fenetre, (35, 5, 229),
                                    (x + taille_bloc // 2, y + taille_bloc // 2),
                                    taille_bloc // 2)

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
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    jeu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# Lancement
jeu()
