# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 12:34:44 2021

@author: Daniel
"""


class Settings:
    """ Class that contains all settings for game attributes"""

    def __init__(self):
        """Initializes the settings class"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # Ship Settings
        self.ship_speed = 1.5
        # Bullet settings
        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 240)
        self.bullets_allowed = 3
        # Virion Settings
        self.virion_speed = 0.25
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
        # Ship Limit
        self.ship_limit = 3
        self.speedup_scale = 1.1
        # How quickly the alien point values increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize setting that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.virion_speed = 1.0

        # fleet_direction of 1 == Right, -1 == left.
        self.fleet_direction = 1
        # Scoring
        self.virion_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.virion_speed *= self.speedup_scale
        self.virion_points = int(self.virion_points * self.score_scale)
        print(self.virion_points)
