class Settings :
    #Stores all the settings of the game

    def __init__(self) :
        #initialize game's static settings

        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0,0,0)

        #ship settings
        self.ship_speed = 1.5
        self.ship_limit = 3

        #bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (45, 143, 43)
        self.bullets_allowed = 3

        #alien settings
        self.fleet_drop_speed = 10

        #how quickly the game speeds up
        self.speedup_scale = 1.1

        #how quickly the value of alien point increases, aliens have more value as level increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self): 
        """initialize settings that change throughout the game"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #fleet_direction 1 means right
        self.fleet_direction = 1

        #scoring
        self.alien_points = 50


    def increase_speed(self) :
        """increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        