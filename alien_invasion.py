import sys
from time import sleep

import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

class AlienInvasion :
    """
        all the elements that are required in the game
    """
    def __init__(self) :
        #initialise the game and create game resources

        pygame.init()
        #self.settings is an attribute + an instance of class Settings
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        #create an instance to store game stats
        # and create a scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        #create a group or list of all the bullets that were fired
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Make the play button
        self.play_button = Button(self, "Play")


    def run_game(self) :
        #Start the main loop for the game

        while True :
            #watch for keyboard and mouse events and update the screen accordingly
            self._check_events()

            if self.stats.game_active : 
              self.ship.update()
              self._update_bullets()
              self._update_aliens()

            self._update_screen()


    def _check_events(self) :
        #watch for keyboard and mouse events
        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                sys.exit()
                
            elif event.type == pygame.KEYDOWN :
                self._check_keydown_event(event)

            elif event.type == pygame.KEYUP :
                self._check_keyup_event(event)

            elif event.type == pygame.MOUSEBUTTONDOWN :
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _check_keydown_event(self, event) :
        if event.key == pygame.K_RIGHT :
            #move ship to right
            self.ship.move_right = True
        elif event.key == pygame.K_LEFT :
            #move ship to left
            self.ship.move_left = True
        elif event.key == pygame.K_q :
            sys.exit()
        elif event.key == pygame.K_SPACE :
            self._fire_bullet()


    def _check_keyup_event(self, event) :
        if event.key == pygame.K_RIGHT :
            #stop moving right
            self.ship.move_right = False
        if event.key == pygame.K_LEFT :
            #stop moving left
            self.ship.move_left = False


    def _check_play_button(self, mouse_pos) :
        """start a new game when player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active :
            #reset game settings
            self.settings.initialize_dynamic_settings()

            #reset the game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor
            pygame.mouse.set_visible(False)


    def _fire_bullet(self) :
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed :
          new_bullet = Bullet(self)
          self.bullets.add(new_bullet)


    def _update_bullets(self) : 
        """"update position of bullets and get rid of old bullets"""
        #update bullet position
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        #using a copy of bullets because for loop does not allow modifications to list
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
              self.bullets.remove(bullet)
              print(len(self.bullets))

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self) :
        #check for bullets that have hit aliens
        #if so, get rid of bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions :
            for aliens in collisions.values() :
              self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens :
            #destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level += 1
            self.sb.prep_level()


    def _ship_hit(self) :
        """respond to ship being hit by an alien"""
        #decrement ships left
        self.stats.ships_left -= 1 

        if self.stats.ships_left > 0 :
          #update scoreboard
          self.sb.prep_ships()

          #get rid of any remaining bullets and aliens
          self.bullets.empty()
          self.aliens.empty()

          #create a new fleet and center the ship
          self._create_fleet()
          self.ship.center_ship()

          #pause for 0.5 sec and the update the screen
          sleep(0.5)

        else :
            self.sb.prep_ships()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


    def _check_fleet_edges(self) :
        """respond if an alien has reached the edge"""
        for alien in self.aliens.sprites() :
            if alien.check_edges() :
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self) :
        """drop the entire fleet and change direction"""
        for alien in self.aliens.sprites() :
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


    def _update_aliens(self) :
        """
            check if the fleet is at an edge
            update the position of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien and ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens) :
            self._ship_hit()
 
        #look for aliens hitting the bottom of the screen
        self._check_alien_bottom()


    def _check_alien_bottom(self) :
        """to check if an alien has reached the bottom of the ship """
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites() :
            if alien.rect.bottom >= screen_rect.bottom :
                self._ship_hit()
                break


    def _create_alien(self, alien_number, row_number) :
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.y = alien_height + 2 * alien_height * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)


    def _create_fleet(self) :
        """create a fleet of aliens"""
        #create an alien and find the number of aliens in a row
        #spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        #number of rows that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - ship_height - (3*alien_height)
        number_rows = available_space_y // (2*alien_height)

        #create full fleet of aliens
        for row_number in range(number_rows) :
            for alien_number in range(number_aliens_x) :
              #create an alien and place it in a row
              self._create_alien(alien_number, row_number)


    def _update_screen(self) :
        
        #update image on the screen and flip to the new screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites() :
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        #draw the score information
        self.sb.show_score()

        #draw the play button if game is inactive
        if not self.stats.game_active :
            self.play_button.draw_button()

        #make the most recently drawn screen visible
        #any change made by event loop will be made visible to the user using this 
        pygame.display.flip()


if __name__ == '__main__' :
    #make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()