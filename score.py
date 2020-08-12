"""
Define score class
"""

import pygame
from config import basicfont


class Score(pygame.sprite.Sprite):

    def __init__(self, text, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.text = text
        self.image = basicfont.render(
            '{}: {}'.format(self.text, self.score),
            True, (255, 255, 255), (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self):
        """
        move missile or eliminate aliens
        """
        self.image = basicfont.render(
            '{}: {}'.format(self.text, self.score),
            True, (255, 255, 255), (0, 0, 0))
