"""
Define missile classes
"""

from math import radians, degrees, cos, sin, atan2
import pygame
from config import DAMAGE_NORMAL, DAMAGE_POWERFUL, DAMAGE_ALIEN
from config import channel_hero_bullets, sound_shoot, HEIGHT, WIDTH


class Missile(pygame.sprite.Sprite):

    def __init__(self, spaceship_position, file=""):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.size
        self.rect.x = (spaceship_position.x +
                       spaceship_position.size[0]//2 - self.width//2)
        self.rect.y = spaceship_position.y - self.height
        self.angle = radians(-90)

    def update(self):
        """
        move or eliminate missile
        """
        self.transform()
        self.move()
    
    def move(self):
        """
        move missile
        """
        self.rect.x += 4 * cos(self.angle)
        self.rect.y += 4 * sin(self.angle)

    def transform(self):
        """
        kill missile if out of bounds
        use any other transformations
        """
        if not 0 <= self.rect.x <= WIDTH:
            self.kill()
        if not 0<= self.rect.y <= HEIGHT:
            self.kill()

class NormalMissile(Missile):  # defined by "l" in the spec sheet
    damage = DAMAGE_NORMAL  # class variable shared by all instances

    def __init__(self, spaceship_position):
        Missile.__init__(self, spaceship_position, "assets/normal.png")
        channel_hero_bullets.play(sound_shoot)


class PowerfulMissile(Missile):  # defined by "i" in the spec sheet
    damage = DAMAGE_POWERFUL  # class variable shared by all instances

    def __init__(self, spaceship_position):
        Missile.__init__(self, spaceship_position, "assets/powerful.png")


class AlienMissile(Missile):
    damage = DAMAGE_ALIEN

    def __init__(self, spaceship_position):
        Missile.__init__(self, spaceship_position, "assets/bullet_alien.png")
        self.angle = radians(90)
        self.rect.y = spaceship_position.y + self.height + 20


class BossMissile(Missile):
    damage = DAMAGE_ALIEN

    def __init__(self, spaceship_position, enemy_position):
        Missile.__init__(self, spaceship_position, "assets/missile_boss.png")
        self.angle = atan2(enemy_position.centery - spaceship_position.centery,
                           enemy_position.centerx - spaceship_position.centerx)
        self.rect.y = spaceship_position.y + self.height + 50


class GuidedMissile(Missile):
    damage = DAMAGE_ALIEN

    def __init__(self, spaceship_position, enemy_position):
        Missile.__init__(self, spaceship_position, "assets/missile_boss.png")
        self.angle = atan2(enemy_position.centery - spaceship_position.centery,
                           enemy_position.centerx - spaceship_position.centerx)
        self.rect.y = spaceship_position.y + self.height + 50

    def update(self):
        self.modify_angle()
        self.transform()
        self.move()
    
    def modify_angle(self):
        """
        set angle of missile so it's directed towards hero
        """
        from game import hero
        enemy_position = hero.rect
        self.angle = atan2(enemy_position.centery - self.rect.centery,
                           enemy_position.centerx - self.rect.centerx)
