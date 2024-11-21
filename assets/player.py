import pygame

class Player:
    def __init__(self, x, y):  # Initialisation du joueur avec une position x, y
        # Charger la sprite sheet contenant les sprites du joueur
        self.sprite_sheet = pygame.image.load("assets/pictures/static_anakin_skywalker.png").convert_alpha()
        self.sprite_sheet_run = pygame.image.load("assets/pictures/running_anakin_skywalker.png").convert_alpha()  # Sprite de course

        # Dimensions d'une cellule de la grille (taille d'un sprite individuel)
        self.cell_width = 32  # Largeur de chaque sprite
        self.cell_height = 49  # Hauteur de chaque sprite

        # Dimensions d'une cellule de la grille (taille d'un sprite individuel)
        self.cell_width_run = 38  # Largeur de chaque sprite
        self.cell_height_run = 49  # Hauteur de chaque sprite

        # Découpe de la sprite sheet en sprites individuels
        self.sprites = self.load_sprites_from_sheet(self.sprite_sheet, self.cell_width, self.cell_height)
        self.sprites_run = self.load_sprites_from_sheet(self.sprite_sheet_run, self.cell_width_run, self.cell_height_run)

        # Initialisation
        self.image = self.sprites[0]  # Commence avec le premier sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Animation par changement d'image
        self.current_frame = 0
        self.timer = 0  # Timer pour le suivi du temps écoulé

        # Attributs pour gérer le mouvement et la physique
        self.velocity = 5  # Vitesse horizontale du joueur
        self.jump_power = 15  # Puissance du saut
        self.gravity = 1  # Gravité qui attire le joueur vers le bas
        self.dy = 0  # Vitesse verticale initiale (aucun mouvement vertical au départ)
        self.on_ground = False  # Vérifie si le joueur est au sol
        self.facing_left = False  # Le joueur commence par regarder à droite

        # Variable pour savoir si le joueur est en mouvement
        self.is_moving = False

    def load_sprites_from_sheet(self, sheet, cell_width, cell_height):
        """Découpe une sprite sheet en une liste de surfaces (sprites)."""
        sprites = []
        sheet_width = sheet.get_width()
        sheet_height = sheet.get_height()

        # Comme il n'y a qu'une seule ligne, on parcourt les colonnes uniquement
        columns = sheet_width // cell_width

        for x in range(columns):
            # Découpe chaque sprite à partir de la sprite sheet
            sprite_x = x * cell_width
            sprite_y = 0  # Une seule ligne de sprites
            sprite = sheet.subsurface(pygame.Rect(sprite_x, sprite_y, cell_width, cell_height))
            sprites.append(sprite)

        return sprites

    def handle_input(self, keys):  # Gère les entrées clavier pour le joueur
        # Saut (seulement si le joueur est au sol)
        if keys[pygame.K_SPACE] and self.on_ground:  # Seul le sol peut initier un saut
            self.dy = -self.jump_power  # Applique une force verticale vers le haut
            self.on_ground = False  # Le joueur quitte le sol

        # Déplacement vers la gauche
        if keys[pygame.K_q]:
            self.rect.x -= self.velocity  # Déplace le joueur vers la gauche
            if not self.facing_left:  # Si le joueur ne regardait pas déjà à gauche
                self.facing_left = True
                self.is_moving = True  # Le joueur se déplace
        # Déplacement vers la droite
        if keys[pygame.K_d]:
            self.rect.x += self.velocity  # Déplace le joueur vers la droite
            if self.facing_left:  # Si le joueur regardait à gauche
                self.facing_left = False
                self.is_moving = True  # Le joueur se déplace

        if not keys[pygame.K_q] and not keys[pygame.K_d]:
            self.is_moving = False  # Le joueur est immobile  

    def update(self, delta_time):
        """Met à jour l'animation du joueur, selon s'il est en mouvement ou immobile."""
        self.timer += delta_time

        # Animation de base quand le joueur est immobile
        if not self.is_moving:
            # Si le joueur est immobile, on fait défiler les images mais une seule fois
            if self.current_frame < len(self.sprites) - 1:
                if self.timer >= 0.3:  # Temps pour changer de frame
                    self.timer = 0
                    self.current_frame += 1  # Passe à la frame suivante
            else:
                # L'animation reste sur la dernière image une fois qu'elle a fini de défiler
                self.current_frame = len(self.sprites) - 1  # Garde la dernière image

            # Choisit le sprite de direction (flip si nécessaire)
            if self.facing_left:
                self.image = pygame.transform.flip(self.sprites[self.current_frame], True, False)
            else:
                self.image = self.sprites[self.current_frame]

        # Si le joueur est en mouvement (maintient une touche enfoncée)
        elif self.is_moving:
            # Animation de course
            if self.timer >= 0.1:  # Vérifie si le temps pour changer de frame est écoulé
                self.timer = 0
                if self.current_frame < len(self.sprites_run) - 1:
                    self.current_frame += 1  # Passe à la frame suivante
                else:
                    self.current_frame = len(self.sprites_run) - 1  # Reste à la dernière image

            # Met à jour l'image en fonction de la direction
            if self.facing_left:
                self.image = pygame.transform.flip(self.sprites_run[self.current_frame], True, False)
            else:
                self.image = self.sprites_run[self.current_frame]

        # Applique la gravité
        self.dy += self.gravity  # La gravité s'applique à chaque frame

        # Déplace le joueur verticalement en fonction de dy
        self.rect.y += self.dy

        # Vérifie si le joueur touche le sol (en utilisant la position y du joueur)
        if self.rect.bottom >= 550:  # Le sol fictif à y = 550
            self.rect.bottom = 550  # Empêche le joueur de passer sous le sol
            self.dy = 0  # Arrête la chute verticale
            self.on_ground = True  # Le joueur est de nouveau au sol


    def draw(self, screen):  # Affiche le joueur sur l'écran
        scaled_image = pygame.transform.scale(self.image, (self.cell_width * 1.5, self.cell_height * 1.5))  # 2x la taille originale
        screen.blit(scaled_image, self.rect)  # Affiche l'image redimensionnée
        
