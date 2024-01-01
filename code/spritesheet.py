import pygame


class SpriteSheet():
    def __init__(self, image):
        self.sheet = image
    
    def get_image(self, width, height, start_x, start_y, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (start_x, start_y, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        
        return image