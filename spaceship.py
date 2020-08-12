"""
Class for spaceship
"""

import pygame
from pygame.locals import K_a, K_d, K_SPACE, K_s
from config import HERO_MAX_LIFE, AMMO_NORMAL, AMMO_POWERFUL
from config import HEIGHT, WIDTH
from config import channel_hero_hit, sound_hero_hit
from missiles import PowerfulMissile, NormalMissile


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        """
            image: The image loaded for spaceship
            max_x: The max x position of battlefield
            max_y: the max y position of battlefield
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/spaceship.png')
        self.rect = self.image.get_rect()
        self.width, self.height = self.rect.size
        self.rect.y = HEIGHT - self.height
        self.health = HERO_MAX_LIFE
        self.ammo_normal = AMMO_NORMAL
        self.ammo_powerful = AMMO_POWERFUL

    def update(self):
        """
        Update position of spaceship or pawn a missile
        """
        import game  # this will avoid circular imports

        key = pygame.key.get_pressed()

        if key[K_a]:
            # move left and check boundary
            self.rect.x = max(0, self.rect.x - 4)

        if key[K_d]:
            # move left and check boundary
            self.rect.x = min(WIDTH - self.width, self.rect.x + 4)

        if key[K_SPACE]:
            # shoot a powerful missile
            if (self.ammo_powerful > 0 and
                    game.spawn_missile(self.rect, PowerfulMissile)):
                self.ammo_powerful -= 1
            else:
                pass  # show user warning out of ammo

        if key[K_s]:
            # shoot a normal missile
            if self.ammo_normal > 0:
                self.ammo_normal -= 1
                game.spawn_missile(self.rect, NormalMissile)

    def hit(self, damage):
        """decrease health due to damage"""
        self.health -= damage
        channel_hero_hit.play(sound_hero_hit)
