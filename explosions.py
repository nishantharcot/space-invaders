"""
Define Explosion class
"""

import pygame
from config import channels_explosion, IMGS_EXPLOSION, sound_explosion


class Explosion(pygame.sprite.Sprite):

    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMGS_EXPLOSION[0]
        self.rect = self.image.get_rect(center=center)
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 54
        for channel in channels_explosion:
            if not channel.get_busy():
                channel.play(sound_explosion)
                break

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
        if self.frame >= len(IMGS_EXPLOSION):
            self.kill()
        else:
            self.image = IMGS_EXPLOSION[self.frame]
            self.rect = self.image.get_rect(center=self.rect.center)
