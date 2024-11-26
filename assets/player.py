import pygame

class Player:
    def __init__(self, x, y):  # Initialisation du joueur avec une position x, y
        # Charger la sprite sheet contenant les sprites du joueur
        self.sprite_sheet = pygame.image.load("assets/pictures/players/aaanakin_skywalker.png").convert_alpha()
        

        # Dimensions d'une cellule de la grille (taille d'un sprite individuel)
        
        self.cell_width = 150  # Largeur de chaque sprite
        self.cell_height = 169  # Hauteur de chaque sprite
        

        self.scale_factor = 1



        self.slow_motion_timer = 0  # Timer pour le ralenti
        self.is_slow_motion = False  # Indique si le ralenti est actif

        # Découpe de la sprite sheet en sprites individuels
        self.sprites_idle = self.load_idle_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 11, 0)        
        self.sprites_run = self.load_run_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 12, 1)
        self.sprites_super_run = self.load_super_run_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 12, 2)
        self.sprites_jump = self.load_jump_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 9, 3)
        self.sprites_super_jump = self.load_super_jump_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 10, 4)
        self.attack_state = 0
        self.all_sprites_attack = [ 
            self.load_attack_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 9, 5),
            self.load_attack_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 9, 6),
            self.load_attack_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 8, 7) 
        ]
        self.sprites_super_attack = self.load_super_attack_sprites(self.sprite_sheet, self.cell_width, self.cell_height, 25, 8)

        # for i, sprite in enumerate(self.sprites_super_attack):
        #     print(f"Sprite {i}: {sprite.get_width()}x{sprite.get_height()}")


        


        # Initialisation
        self.image = self.sprites_idle[0]  # Commence avec le premier sprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Animation par changement d'image
        self.current_frame = 0
        self.timer = 0  # Timer pour le suivi du temps écoulé

        # Attributs pour gérer le mouvement et la physique
        self.velocity = 3  # Vitesse horizontale du joueur
        self.max_run_power = 6
        self.jump_power = 20  # Puissance minimale du saut
        self.max_jump_power = 19  # Puissance maximale du saut
        self.jump_charge_time = 0  # Temps accumulé d'appui sur Espace
        self.is_charging_jump = False  # Suivi de l'état de chargement du saut
        self.gravity = 1  # Gravité qui attire le joueur vers le bas
        self.original_gravity = self.gravity  # Stocke la gravité originale
        self.super_jump_gravity = self.gravity / 2  # Gravité réduite pour le super saut
        self.dy = 0  # Vitesse verticale initiale (aucun mouvement vertical au départ)
        self.on_ground = False  # Vérifie si le joueur est au sol
        self.facing_left = False  # Le joueur commence par regarder à droite
        self.jump_locked = False  # Verrou pour éviter les sauts continus
        self.is_super_jumping = False  # Indique si le joueur fait un super saut
        self.is_super_run = False  # Indique si le joueur fait un super saut
        self.attack_triggered = False
        self.is_attacking = False # Le joueur ne saute pas


        # Variable pour savoir si le joueur est en mouvement
        self.is_moving = False # Le joueur ne bouge pas
        self.is_jumping = False # Le joueur ne saute pas

    def load_idle_sprites(self, sheet, cell_width, cell_height, columns, line):
        """Découpe une ligne spécifique de sprites."""
        sprites = []
        y_offset = line * cell_height  # Calcul de l'offset vertical pour la ligne souhaitée
        for col in range(columns):  # Itère sur les colonnes
            x = col * cell_width  # Décalage horizontal
            sprite = sheet.subsurface(pygame.Rect(x, y_offset, cell_width, cell_height))
            sprites.append(sprite)
        return sprites
    
    def load_run_sprites(self, sheet, cell_width, cell_height, columns, line):
        """Découpe uniquement la deuxième ligne de sprites (run)."""
        sprites = []
        y_offset = line * cell_height  # Décalage en Y pour la deuxième ligne
        for col in range(columns):  # Itérer sur les colonnes
            x = col * cell_width
            sprite = sheet.subsurface(pygame.Rect(x, y_offset, cell_width, cell_height))
            sprites.append(sprite)
        return sprites
    
    def load_super_run_sprites(self, sheet, cell_width, cell_height, columns, line):
        """Découpe uniquement la deuxième ligne de sprites (run)."""
        sprites = []
        y_offset = line * cell_height  # Décalage en Y pour la deuxième ligne
        for col in range(columns):  # Itérer sur les colonnes
            x = col * cell_width
            sprite = sheet.subsurface(pygame.Rect(x, y_offset, cell_width, cell_height))
            sprites.append(sprite)
        return sprites
    
    def load_jump_sprites(self, sheet, cell_width, cell_height, columns, line):
        """Découpe uniquement la deuxième ligne de sprites (run)."""
        sprites = []
        y_offset = line * cell_height  # Décalage en Y pour la deuxième ligne
        for col in range(columns):  # Itérer sur les colonnes
            x = col * cell_width
            sprite = sheet.subsurface(pygame.Rect(x, y_offset, cell_width, cell_height))
            sprites.append(sprite)
        return sprites
    
    
    def load_super_jump_sprites(self, sheet, cell_width, cell_height, columns, line):
        """Découpe uniquement la deuxième ligne de sprites (run)."""
        sprites = []
        y_offset = line * cell_height  # Décalage en Y pour la deuxième ligne
        for col in range(columns):  # Itérer sur les colonnes
            x = col * cell_width
            sprite = sheet.subsurface(pygame.Rect(x, y_offset, cell_width, cell_height))
            sprites.append(sprite)
        return sprites
    
    def load_attack_sprites(self, sheet, cell_width, cell_height, columns, line):
        """Découpe uniquement la deuxième ligne de sprites (run)."""
        sprites = []
        y_offset = line * cell_height  # Décalage en Y pour la deuxième ligne
        for col in range(columns):  # Itérer sur les colonnes
            x = col * cell_width
            sprite = sheet.subsurface(pygame.Rect(x, y_offset, cell_width, cell_height))
            sprites.append(sprite)
        return sprites
    
    def load_super_attack_sprites(self, sheet, cell_width, cell_height, columns, line):
        """Découpe une ligne spécifique de sprites pour la super attaque."""
        sprites = []
        y_offset = line * cell_height  # Calcul de l'offset vertical pour la ligne souhaitée

        # Calcul dynamique des colonnes pour éviter de dépasser la largeur de la sprite sheet
        columns = 0
        current_x = 0
        while current_x + cell_width <= sheet.get_width():  # Tant qu'on reste dans les limites
            columns += 1
            current_x += cell_width

        current_x = 0  # Réinitialisation pour parcourir les sprites

        for col in range(columns):
            # Adapte la largeur en fonction de la colonne
            if 8 <= col <= 10:  # Colonnes 9, 10, 11 (indices 8, 9, 10 en partant de 0)
                width = cell_width * 4
            else:  # Colonnes normales
                width = cell_width

            # Vérifie si le sprite dépasse la largeur de la sprite sheet
            if current_x + width > sheet.get_width():
                print(f"Skipping sprite at Col {col} (X={current_x}, W={width}) as it exceeds the sprite sheet width.")
                break

            # Découpe le sprite
            sprite = sheet.subsurface(pygame.Rect(current_x, y_offset, width, cell_height))
            sprites.append(sprite)

            # Met à jour la position horizontale courante
            current_x += width

        return sprites
    
    def handle_input(self, keys):
        """Gère les entrées clavier pour mouvement et saut."""

            # Gestion du saut
        if keys[pygame.K_SPACE]:
            if not self.jump_locked and self.on_ground:  # Si le joueur est au sol
                self.is_jumping = True
                self.current_frame = 0  # Réinitialise l'animation du saut
                self.jump_locked = True  # Verrouille le saut
                self.on_ground = False  # Le joueur quitte le sol
                self.jump_charge_time = 0
                self.dy = -self.jump_power  # Saut normal

                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Super saut
                    self.dy = -self.max_jump_power  # Saut plus puissant
                    self.current_frame = 0  # Réinitialise l'animation du saut
                    self.is_super_jumping = True
                    self.is_slow_motion = True  # Active le ralenti
                    self.slow_motion_timer = 1.0

        elif not keys[pygame.K_SPACE]:  # Relâchement de la touche espace
            self.jump_locked = False  # Déverrouille le saut

        # Gestion des déplacements
        if keys[pygame.K_q]:  # Déplacement vers la gauche
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Super course
                self.rect.x -= self.max_run_power
                if not self.is_super_run:
                    self.current_frame = 0  # Réinitialise l'animation de super run
                self.is_super_run = True
            else:
                self.rect.x -= self.velocity
                self.is_super_run = False
            self.facing_left = True
            self.is_moving = True

        elif keys[pygame.K_d]:  # Déplacement vers la droite
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Super course
                self.rect.x += self.max_run_power
                if not self.is_super_run:
                    self.current_frame = 0  # Réinitialise l'animation de super run
                self.is_super_run = True
            else:
                self.rect.x += self.velocity
                self.is_super_run = False
            self.facing_left = False
            self.is_moving = True

        else:  # Pas de mouvement
            self.is_moving = False
            self.is_super_run = False

        # Déplacement gauche/droite
        if keys[pygame.K_q]:  # Si le joueur appuie sur Q (gauche)
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Si Shift est également appuyé
                self.rect.x -= self.max_run_power  # Applique la vitesse maximale
                if not self.is_super_run:  # Réinitialise uniquement à l'entrée dans le super run
                    self.current_frame = 0
                self.is_super_run = True  # Active le super run
            else:
                self.rect.x -= self.velocity  # Applique la vitesse normale
                self.is_super_run = False  # Désactive le super run
            self.facing_left = True
            self.is_moving = True

        elif keys[pygame.K_d]:  # Si le joueur appuie sur D (droite)
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Si Shift est également appuyé
                self.rect.x += self.max_run_power  # Applique la vitesse maximale
                if not self.is_super_run:  # Réinitialise uniquement à l'entrée dans le super run
                    self.current_frame = 0
                self.is_super_run = True  # Active le super run
            else:
                self.rect.x += self.velocity  # Applique la vitesse normale
                self.is_super_run = False  # Désactive le super run
            self.facing_left = False
            self.is_moving = True

        else:  # Si aucune touche de déplacement n'est appuyée
            self.is_moving = False
            self.is_super_run = False

        # Gestion de l'attaque
        if keys[pygame.K_s]:
            if not self.is_attacking and not self.attack_triggered:  # Nouvelle attaque seulement si pas déjà déclenchée
                self.is_attacking = True
                self.attack_triggered = True
                self.current_frame = 0

                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:  # Super attaque
                    self.sprites_attack = self.sprites_super_attack
                else:
                    # Alterner entre les attaques normales
                    self.sprites_attack = self.all_sprites_attack[self.attack_state]
                    self.attack_state = (self.attack_state + 1) % len(self.all_sprites_attack)
        else:
            # Réinitialise l'état déclenché lorsque la touche "S" est relâchée
            self.attack_triggered = False
            



    def handle_idle_animation(self, delta_time): 
        """Gère l'animation Idle."""
        max_frames = len(self.sprites_idle)  # Nombre total de frames dans l'animation Idle

        if self.current_frame < max_frames - 1:  # Continue l'animation jusqu'à la dernière frame
            if self.timer >= 0.1:  # Change de frame tous les 0.1s
                self.timer = 0
                self.current_frame += 1
        else:
            self.current_frame = max_frames - 1  # Reste sur la dernière frame

        # Affiche le sprite correspondant en fonction de l'orientation
        if self.facing_left:
            self.image = pygame.transform.flip(self.sprites_idle[self.current_frame], True, False)
        else:
            self.image = self.sprites_idle[self.current_frame]

    def handle_run_animation(self, delta_time):
        max_frames = 11  # Limiter l'animation à 11 sprites
        if self.timer >= 0.1:  # Contrôle du temps entre chaque frame
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= max_frames:
                self.current_frame = 0  # Recommence à 0 après 11 sprites

        # Appliquer l'image du sprite en fonction de l'orientation
        if self.facing_left:
            self.image = pygame.transform.flip(self.sprites_run[self.current_frame], True, False)
        else:
            self.image = self.sprites_run[self.current_frame]

    def handle_super_run_animation(self, delta_time):
        max_frames = 11  # Limiter l'animation à 11 sprites
        if self.timer >= 0.1:  # Contrôle du temps entre chaque frame
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= max_frames:
                self.current_frame = 0  # Recommence à 0 après 11 sprites

        # Appliquer l'image du sprite en fonction de l'orientation
        if self.facing_left:
            self.image = pygame.transform.flip(self.sprites_super_run[self.current_frame], True, False)
        else:
            self.image = self.sprites_super_run[self.current_frame]
            
    def handle_jump_animation(self, delta_time):
        """Anime le saut normal."""
        if self.timer >= 0.1:  # Temps pour changer de frame
            self.timer = 0
            self.current_frame += 1

        # Vérifie si l'animation atteint la fin
        if self.current_frame >= len(self.sprites_jump):
            self.current_frame = len(self.sprites_jump) - 1  # Reste sur la dernière frame
            self.is_jumping = False  # Termine l'animation de saut

        # Met à jour l'image actuelle
        if self.facing_left:
            self.image = pygame.transform.flip(self.sprites_jump[self.current_frame], True, False)
        else:
            self.image = self.sprites_jump[self.current_frame]

    def handle_super_jump_animation(self, delta_time):
        """Gère l'animation du super saut."""
        if self.timer >= 0.03:  # Temps pour changer de frame (ralenti pour le super saut)
            self.timer = 0
            self.current_frame += 1

            # Vérifie si on dépasse le nombre de frames
            if self.current_frame >= len(self.sprites_super_jump):
                self.current_frame = len(self.sprites_super_jump) - 1  # Dernière image
                self.is_jumping = False  # Termine le saut
                self.is_super_jumping = False  # Termine l'état de super saut

        # Affiche le sprite correspondant
        if self.current_frame < len(self.sprites_super_jump):
            if self.facing_left:
                self.image = pygame.transform.flip(self.sprites_super_jump[self.current_frame], True, False)
            else:
                self.image = self.sprites_super_jump[self.current_frame]       
    
    def handle_attack_animation(self, delta_time):
        """Anime l'attaque du joueur."""
        if self.timer >= 0.1:  # Vitesse de changement d'image pour l'attaque
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.sprites_attack):  # Vérifie la fin de l'animation
                self.is_attacking = False  # Termine l'attaque
                self.current_frame = 0  # Réinitialise l'animation

        # Applique l'image en fonction de l'orientation
        if self.facing_left:
            self.image = pygame.transform.flip(self.sprites_attack[self.current_frame], True, False)
        else:
            self.image = self.sprites_attack[self.current_frame]
    
    def handle_super_attack_animation(self, delta_time):
        """Anime la super attaque du joueur."""
        if self.timer >= 0.2:  # Vitesse de changement d'image pour la super attaque
            self.timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.sprites_super_attack):  # Vérifie la fin de l'animation
                self.is_attacking = False  # Termine l'attaque
                self.current_frame = 0  # Réinitialise l'animation

        # Applique l'image en fonction de l'orientation
        if self.facing_left:
            self.image = pygame.transform.flip(self.sprites_super_attack[self.current_frame], True, False)
        else:
            self.image = self.sprites_super_attack[self.current_frame]
    
    def apply_gravity(self):
        """Applique la gravité et vérifie si le joueur touche le sol."""
        if self.is_super_jumping:  # Pendant le super saut
            self.gravity = self.super_jump_gravity  # Utilise une gravité réduite
        else:
            self.gravity = self.original_gravity  # Restaure la gravité normale

        if not self.on_ground:  # Applique la gravité uniquement si le joueur n'est pas au sol
            self.dy += self.gravity  # Augmente la vitesse de descente

        self.rect.y += self.dy

        # Vérifie si le joueur touche le sol
        if self.rect.bottom >= 550:  # Sol fictif
            self.rect.bottom = 550
            self.dy = 0
            self.reset_jump_state()  # Réinitialise l'état de saut

    def reset_jump_state(self):
        """Réinitialise l'état du saut lorsque le joueur touche le sol."""
        self.dy = 0
        self.on_ground = True
        self.is_jumping = False
        self.is_super_jumping = False
        self.jump_locked = False  # Déverrouille les sauts pour permettre un autre saut

    def update(self, delta_time):
        """Met à jour l'état du joueur, ses animations et applique la gravité."""

        # Gérer le ralenti pour le super saut
        if self.is_slow_motion:
            delta_time *= 0.3  # Ralentit le temps pendant le super saut
            self.slow_motion_timer -= delta_time
            if self.slow_motion_timer <= 0:  # Désactive le ralenti une fois terminé
                self.is_slow_motion = False

        # Met à jour le timer pour l'animation
        self.timer += delta_time

    # Gestion des animations
        if self.is_jumping:
            if self.is_super_jumping:
                self.handle_super_jump_animation(delta_time)
            else:
                self.handle_jump_animation(delta_time)
        elif self.is_super_run:
            self.handle_super_run_animation(delta_time)
        elif self.is_moving:
            self.handle_run_animation(delta_time)
        elif self.is_attacking:
            if self.sprites_attack == self.sprites_super_attack:
                self.handle_super_attack_animation(delta_time)
            else:
                self.handle_attack_animation(delta_time)
        else:
            self.handle_idle_animation(delta_time)

        # Applique la gravité
        self.apply_gravity()

        # Vérifie si le joueur est au sol et réinitialise l'état si nécessaire
        if self.rect.bottom >= 450:  # Le sol fictif est défini à y = 450
            self.rect.bottom = 450
            self.dy = 0
            self.on_ground = True
            self.is_jumping = False
            self.is_super_jumping = False


    def draw(self, screen, ground_y=450, shadow_offset=-1):
        # Calculer la distance entre le joueur et le sol
        player_to_ground = ground_y - self.rect.bottom

        # Calculer la position de l'ombre en fonction de cette distance (effet miroir)
        shadow_y = ground_y + player_to_ground + shadow_offset  # Décalage supplémentaire pour abaisser l'ombre

        # Créer l'ombre
        shadow = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA)
        shadow.blit(self.image, (0, 0))

        # Appliquer une teinte sombre et ajuster la taille pour l'effet ombré
        shadow.fill((0, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
        shadow = pygame.transform.scale(
            shadow,
            (
                int(self.image.get_width() * 1.1),
                int(self.image.get_height() * 0.8),
            )
        )

        # Retourner l'ombre verticalement pour l'effet miroir
        shadow = pygame.transform.flip(shadow, False, True)

        # Position de l'ombre
        shadow_x = self.rect.centerx - shadow.get_width() // 2
        screen.blit(shadow, (shadow_x, shadow_y))

        # Agrandir l'image du joueur selon le facteur d'échelle
        scaled_image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * self.scale_factor),
                int(self.image.get_height() * self.scale_factor),
            )
        )

        # Ajuster la position pour centrer l'image agrandie
        offset_x = self.rect.x - ((self.scale_factor - 1) * self.rect.width // 2)
        offset_y = self.rect.y - ((self.scale_factor - 1) * self.rect.height // 2)

        # Dessiner le joueur avec l'agrandissement et l'ajustement des frames
        if self.is_attacking and self.sprites_attack == self.sprites_super_attack:
            if 8 <= self.current_frame <= 10:  # Frames spécifiques
                offset = 230 * self.scale_factor  # Décalage ajusté pour l'échelle
                screen.blit(scaled_image, (offset_x - offset, offset_y))
            else:
                # Dessiner normalement pour toutes les autres frames
                screen.blit(scaled_image, (offset_x, offset_y))
        else:
            # Dessiner normalement pour toutes les autres animations
            screen.blit(scaled_image, (offset_x, offset_y))