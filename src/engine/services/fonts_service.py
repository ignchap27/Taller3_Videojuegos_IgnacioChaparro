import pygame


class FontService():
    def __init__(self):
        self._fonts = {}
    
    def get(self, path: str, size: int) -> pygame.font.Font:
        key = f"{path}_{size}"
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(path, size)
        return self._fonts[key]