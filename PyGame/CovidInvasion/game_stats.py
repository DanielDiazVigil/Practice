# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:56:44 2021

@author: Daniel
"""
from settings import Settings


class GameStats:
    def __init__(self, ai_game):
        """ Initialize game statistics """
        self.settings = ai_game.settings
        self.reset_stats()
        # Start Covid Invasion in an active state.
        self.game_active = False
        # High Score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1