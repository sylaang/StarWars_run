import pygame
from assets.player import Player

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Star Wars")

# Couleurs
WHITE = (255, 255, 255)

# Framerate
clock = pygame.time.Clock()
FPS = 60

# Chargement du joueur
player = Player(100, SCREEN_HEIGHT - 150)  # Position initiale du joueur

# Boucle principale
running = True

while running:
    delta_time = clock.tick(FPS) / 1000.0  # Temps écoulé (en secondes) depuis la dernière frame

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des entrées clavier
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    # Mise à jour des éléments du jeu (mouvement et animation)
    player.update(delta_time)

    # Dessin à l'écran
    screen.fill(WHITE)  # Fond blanc
    player.draw(screen)

    pygame.display.flip()  # Mise à jour de l'écran

# Quitter pygame proprement
pygame.quit()
