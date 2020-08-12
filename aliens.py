"""
Define alien classes
"""

import pygame
import random
from config import MAX_HEALTH_ALIEN, WIDTH
from missiles import AlienMissile, BossMissile, GuidedMissile

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, image_normal, image_wounded):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.health = MAX_HEALTH_ALIEN
        self.image_normal = image_normal
        self.image_wounded = image_wounded
        self.image = pygame.image.load(self.image_normal)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.direction_x = random.choice(["left", "right"])
        self.direction_y = random.choice(["top", "bottom"])
        self.missile = AlienMissile
        self.fire_chance = [0.99, 0.01]  # 1% chance of firing

    def update(self):
        """
        Perform alien actions each round
        """
        self.move()
        self.transform()
        self.fire()

    def move(self):
        """
        Move alien in its previous direction or change directions at border
        """
        if self.direction_x == "left":
            if self.rect.x <= 10:
                self.direction_x = "right"
            else:
                self.rect.x -= 2
            
        if self.direction_x == "right":
            if self.rect.x >= WIDTH - 30:
                self.direction_x = "left"
            else:
                self.rect.x += 2

        if self.direction_y == "top":
            if self.rect.y <= 10:
                self.direction_y = "bottom"
            else:
                self.rect.y -= 2
            
        if self.direction_y == "bottom":
            if self.rect.y >= 180:
                self.direction_y = "top"
            else:
                self.rect.y += 2

    def transform(self):
        """
        If health is depleted die
        If health is less than half of max change appearance
        """
        if self.health <= 0:
            self.kill()
        elif self.health < MAX_HEALTH_ALIEN / 2:
            x, y = self.rect.x, self.rect.y
            self.image = pygame.image.load(self.image_wounded)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

    def fire(self):
        """
        Fire based on the predefined probabilities
        """
        from game import spawn_missile # this will avoid circular imports
        
        choice_fire = random.choices([0, 1], self.fire_chance)[0]
        if choice_fire:
            spawn_missile(self.rect, self.missile)
    
    def hit(self, damage):
        """
        Reduce health by the amount of damage
        """
        self.health -= damage


class NormalAlien(Alien):
    image_normal = "assets/alien.png"
    image_wounded = "assets/alien_low_health.png"

    def __init__(self, x, y):
        Alien.__init__(self, x, y, self.image_normal, self.image_wounded)


class BossAlien(Alien):
    image_normal = "assets/alien_boss.png"
    image_wounded = "assets/alien_boss_pissed.png"

    def __init__(self, x, y):
        Alien.__init__(self, x, y, self.image_normal, self.image_wounded)
        self.health = MAX_HEALTH_ALIEN * 10
        self.missile = BossMissile
        self.fire_chance = [0.9, 0.1]  # 10% chance of firing

    def transform(self):
        """
        If health is depleted die
        If health is less than half of max change appearance
        """
        if self.health <= 0:
            self.kill()
        elif self.health < (MAX_HEALTH_ALIEN * 10) / 2:
            x, y = self.rect.x, self.rect.y
            self.image = pygame.image.load(self.image_wounded)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y
            self.missile = GuidedMissile