# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 11:32:52 2021

@author: Daniel
"""
import os

os.chdir("PROJECT DIRECTORY PATH")
import pygame
import sys
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from virion import Virion
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class CovidInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initializes Game"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((1200, 800))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Covid Invasion")
        # Create an Instance to store game statistics
        # Create Scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.virions = pygame.sprite.Group()
        self._create_fleet()
        # Make play button.
        self.play_button = Button(self, "Play")
        self.bg_color = (230, 230, 230)
        # Create an instance to store game statistics.

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            if self.stats.game_active == True:
                self.ship.update()
                self._update_bullets()
                self._update_virions()
            self._update_screen()

    def _check_events(self):
        """Watches keyboard and mouse for events (user input)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start new game when player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings()
            if self.play_button.rect.collidepoint(mouse_pos):
                self.stats.reset_stats()
                self.stats.game_active = True
                self.sb.prep_score()
                self.sb.prep_level()
                self.sb.prep_ships()
                # Get rid of any remaining virions or bullets.
                self.virions.empty()
                self.bullets.empty()
                # Create a new fleet and center ship.
                self._create_fleet()
                self.ship.center_ship()
                # Hide the mouse cursor.
                pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # move ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Updates postion of bullets and gets rid of old bullets"""
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_virion_collision()

    def _check_bullet_virion_collision(self):
        # Check for any bullets that may have hit virions.
        # If so, get rid of the bullet and virion.
        collisions = pygame.sprite.groupcollide(self.bullets, self.virions, True, True)
        if collisions:
            for virions in collisions.values():
                self.stats.score += self.settings.virion_points * len(virions)
                self.sb.prep_score()
                self.sb.check_high_score()
        if not self.virions:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # Increase Level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Creates a fleet of Virions"""
        # Creates a Virion and finds the number of virions in a row
        # Spacing between each virion is equal to one virion width
        virion = Virion(self)
        virion_width, virion_height = virion.rect.size
        available_space_x = self.settings.screen_width - (2 * virion_width)
        number_virions_x = available_space_x // (2 * virion_width)

        # Determine the # of virions that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (3 * virion_height) - ship_height
        )
        number_rows = available_space_y // (2 * virion_height)
        # Create the full fleet of virions
        for row_number in range(number_rows):
            for virion_number in range(number_virions_x):
                self._create_virion(virion_number, row_number)

    def _create_virion(self, virion_number, row_number):
        # create a virion and place it in the row.
        virion = Virion(self)
        virion_width, virion_height = virion.rect.size
        virion.x = virion_width + 2 * virion_width * virion_number
        virion.rect.x = virion.x
        virion.rect.y = virion_height + 2 * virion.rect.height * row_number
        self.virions.add(virion)

    def _update_virions(self):
        """ Update the position of all virions in the fleet."""
        self._check_fleet_edges()
        self.virions.update()
        if pygame.sprite.spritecollideany(self.ship, self.virions):
            print("Ship hit!!!")
            self._ship_hit()
        # Check if virions hit the bottom of screen
        self._check_virions_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any virions have reached an edge """
        for virion in self.virions.sprites():
            if virion.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ Drop the entire fleet and change the fleet's direction."""
        for virion in self.virions.sprites():
            virion.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an virion."""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining virions/bullets
            self.virions.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_virions_bottom(self):
        """ Checks if any virions have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for virion in self.virions.sprites():
            if virion.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_screen(self):
        """ Updates images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.virions.draw(self.screen)
        # Draw score information
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    ai = CovidInvasion()
    ai.run_game()
