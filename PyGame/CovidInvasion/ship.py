# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:54:57 2021

@author: Daniel
"""
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ This class contains all pertinent info to our ships"""

    def __init__(self, ai_game):
        """Initialize the ship and set starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        # Load the ship image to get its rect.
        self.image = pygame.image.load(
            r"PROJECT_DIRECTORY_PATH\images\masked_earth.bmp"
        )
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom
        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        # Movement Flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        # Update rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """Centers ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """ Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
