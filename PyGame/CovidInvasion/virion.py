# -*- coding: utf-8 -*-
"""
Created on Sun Oct 10 15:52:12 2021

@author: Daniel
"""
import pygame
from pygame.sprite import Sprite


class Virion(Sprite):
    """ A class to represent a signle Virion in a Fleet of Virions """

    def __init__(self, ai_game):
        """Initializes the virion and sets its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # load the Virion image and set its rect attribute
        self.image = pygame.image.load(r"PROJECT_DIRECTORY_PATH\images\virion_two.bmp")
        self.rect = self.image.get_rect()

        # Start each new virion at the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the virion's exact horizontal position/
        self.x = float(self.rect.x)

    def check_edges(self):
        """ Return True if virion is at the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """ Move the virion to the right """
        self.x += self.settings.virion_speed * self.settings.fleet_direction
        self.rect.x = self.x
