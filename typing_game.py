import pygame
import sys
import random

pygame.init()

# Taille de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clavier d'or")

# Police
font = pygame.font.Font(None, 64)

# Générer une lettre au hasard
def random_letter():
    return chr(random.randint(65, 90))  # A-Z

target = random_letter()
score = 0

clock = pygame.time.Clock()

while True:
    screen.fill((30, 30, 30))  # arrière-plan sombre

    # Afficher la lettre à taper
    letter_text = font.render(target, True, (255, 255, 0))
    screen.blit(letter_text, (WIDTH//2 - 20, HEIGHT//2 - 20))

    # Afficher le score
    score_text = font.render(f"Score : {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.unicode.upper() == target:
                score += 1
                target = random_letter()  # nouvelle lettre

    pygame.display.flip()
    clock.tick(60)
