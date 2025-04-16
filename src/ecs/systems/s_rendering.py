
import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface

def system_rendering(world:esper.World, screen:pygame.Surface):
    components = world.get_components(CTransform, CSurface)
    
    for _, (c_t, c_s) in components:
        ent_rect = c_s.surf.get_rect(topleft = c_t.pos)
        screen_inflated_rect = screen.get_rect().inflate(100, 100)
        if screen_inflated_rect.contains(ent_rect):
            screen.blit(c_s.surf, c_t.pos)