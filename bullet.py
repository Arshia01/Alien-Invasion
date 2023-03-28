import pygame
from pygame.sprite import Sprite

class Bullet(Sprite) :
    """"A class to manage bullets fired from ship"""

    def __init__(self, ai_game) :
        #create a bullet object at ships current location
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        #define a bullet and place it at its correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    
    def update(self) :
        """"Move the bullet up the screen"""
        #update the decimal position of the bullet
        self.y -= self.settings.bullet_speed

        #update rect position 
        self.rect.y = self.y

    
    def draw_bullet(self) :
        pygame.draw.rect(self.screen, self.color, self.rect)

