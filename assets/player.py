import pygame

class Player:
    def __init__(self, x, y):  # Initialisation du joueur avec une position x, y
        # Charger la sprite sheet contenant les sprites du joueur
        self.sprite_sheet = pygame.image.load("assets/pictures/testanakin_skywalker.png").convert_alpha()

        # Dimensions d'une cellule de la grille (taille d'un sprite individuel)
        self.cell_width = 27  # Largeur d'un sprite en pixels
        self.cell_height = 32  # Hauteur d'un sprite en pixels

        # Découpe de la sprite sheet en plusieurs sprites individuels
        self.sprites = self.load_sprites_from_sheet(self.sprite_sheet, self.cell_width, self.cell_height)

        # Animation
        self.current_frame = 0  # Index du sprite courant
        self.animation_speed = 0.5  # Temps en secondes avant de passer à l'image suivante
        self.animation_timer = 0  # Accumulateur de temps
        self.max_frames = 10  # Nombre maximum d'images à parcourir

        # Sélection de la première image (sprite) pour l'affichage initial
        self.image = self.sprites[self.current_frame]
        self.rect = self.image.get_rect()  # Récupère les dimensions et position du sprite
        self.rect.topleft = (x, y)  # Positionne le joueur à la position initiale

        # Attributs pour gérer le mouvement et la physique
        self.velocity = 5  # Vitesse horizontale du joueur
        self.jump_power = 15  # Puissance du saut
        self.gravity = 1  # Gravité qui attire le joueur vers le bas
        self.dy = 0  # Vitesse verticale initiale (aucun mouvement vertical au départ)

    def load_sprites_from_sheet(self, sheet, cell_width, cell_height):
        """Découpe une sprite sheet en une liste de surfaces (sprites)."""
        sprites = []  # Liste pour stocker les sprites individuels
        sheet_width = sheet.get_width()  # Largeur totale de la sprite sheet
        sheet_height = sheet.get_height()  # Hauteur totale de la sprite sheet

        # Calcul du nombre de colonnes (sprites par ligne) et de lignes (sprites par colonne)
        columns = sheet_width // cell_width  # Nombre de sprites sur une ligne
        rows = sheet_height // cell_height  # Nombre de sprites sur une colonne

        # Parcours de chaque ligne et colonne pour découper les sprites
        for y in range(rows):
            for x in range(columns):
                # Coordonnées du sprite courant dans la sprite sheet
                sprite_x = x * cell_width
                sprite_y = y * cell_height
                # Vérifie que le sprite est bien dans les limites de la sprite sheet
                if sprite_x + cell_width <= sheet_width and sprite_y + cell_height <= sheet_height:
                    # Découpe un sprite à l'aide des coordonnées et dimensions
                    sprite = sheet.subsurface(pygame.Rect(sprite_x, sprite_y, cell_width, cell_height))
                    sprites.append(sprite)  # Ajoute le sprite découpé à la liste

        return sprites  # Retourne la liste des sprites découpés

    def handle_input(self, keys):  # Gère les entrées clavier pour le joueur
        # Déplacement vers la gauche
        if keys[pygame.K_q]:
            self.rect.x -= self.velocity  # Déplace le joueur vers la gauche
        # Déplacement vers la droite
        if keys[pygame.K_d]:
            self.rect.x += self.velocity  # Déplace le joueur vers la droite

        # Saut (seulement si le joueur est au sol)
        if keys[pygame.K_SPACE] and self.rect.bottom >= 550:  # Sol fictif à y = 550
            self.dy = -self.jump_power  # Applique une force verticale vers le haut

    def update(self, screen_width, screen_height, delta_time):  # Met à jour la position et la physique du joueur
        # Appliquer la gravité en augmentant la vitesse verticale
        self.dy += self.gravity
        self.rect.y += self.dy  # Met à jour la position verticale en fonction de dy

        # Empêcher le joueur de sortir de l'écran horizontalement
        if self.rect.left < 0:  # Si le joueur dépasse la bordure gauche
            self.rect.left = 0  # Bloque à la bordure gauche
        if self.rect.right > screen_width:  # Si le joueur dépasse la bordure droite
            self.rect.right = screen_width  # Bloque à la bordure droite

        # Empêcher le joueur de tomber en dehors de l'écran verticalement
        if self.rect.bottom >= 550:  # Si le joueur atteint le sol fictif
            self.rect.bottom = 550  # Le bloque au sol
            self.dy = 0  # Réinitialise la vitesse verticale

        # Gérer le changement d'image
        self.change_frame(delta_time)

    def change_frame(self, delta_time):
        """Change l'image actuelle pour passer à la suivante."""
        self.animation_timer += delta_time  # Ajoute le temps écoulé

        if self.animation_timer >= self.animation_speed:  # Si le temps écoulé dépasse le seuil
            self.animation_timer = 0  # Réinitialise le timer
            self.current_frame += 1  # Passe à l'image suivante

            # Si on dépasse les 10 premières images, reste sur la dernière
            if self.current_frame >= self.max_frames:
                self.current_frame = self.max_frames - 1  # Reste sur la 10ème image

            # Met à jour l'image affichée
            self.image = self.sprites[self.current_frame]

    def draw(self, screen):  # Affiche le joueur sur l'écran
        screen.blit(self.image, self.rect)  # Dessine le sprite actuel à la position rect
