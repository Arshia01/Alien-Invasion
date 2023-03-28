import pygame
from pygame.sprite import Sprite

class Ship(Sprite) :
    def __init__(self, ai_game) :
        """initialize the ship and its starting position"""
        
        super().__init__()
        #accessing screen's rect attribute
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #update the x value not rect
        self.x = float(self.rect.x)

        #movement flag
        self.move_right = False
        self.move_left = False


    def update(self) :
        if self.move_right and self.rect.right < self.screen_rect.right: 
            self.x += self.settings.ship_speed

        if self.move_left and self.rect.left > 0 : 
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x


    def blitme(self) :
        #draw the ship at its current location
        self.screen.blit(self.image, self.rect)


    def center_ship(self) :
        """
           center the ship on the screen
           we never make more than one ship; we make only one ship instance for the 
           whole game and recenter it whenever the ship has been hit
        """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)