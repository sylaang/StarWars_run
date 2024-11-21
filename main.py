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
BLACK = (0, 0, 0)

# Framerate
clock = pygame.time.Clock()
FPS = 60

# Chargement du joueur
player = Player(100, SCREEN_HEIGHT - 150)  # Position initiale du joueur

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    delta_time = clock.tick(60) / 1000.0  # Temps écoulé (en secondes) depuis la dernière frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des entrées clavier
    keys = pygame.key.get_pressed()
    player.handle_input(keys)

    # Mise à jour des éléments du jeu (inclut l'animation)
    player.update(SCREEN_WIDTH, SCREEN_HEIGHT, delta_time)

    # Dessin à l'écran
    screen.fill((255, 255, 255))  # Fond blanc
    player.draw(screen)

    pygame.display.flip()  # Mise à jour de l'écran