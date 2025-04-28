import pygame
import esper
from src.create.prefab_creator import create_explosion
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.engine.service_locator import ServiceLocator

def system_collision_player_enemy(world:esper.World, player_entity:int, level_cfg:dict, explosion_cfg:dict):
    components = world.get_components(CSurface, CTransform, CTagEnemy)    
    pl_t = world.component_for_entity(player_entity, CTransform)
    pl_s = world.component_for_entity(player_entity, CSurface)
    
    pl_rect = CSurface.get_area_relative(pl_s.area, pl_t.pos)

    for enemy_entity, (c_s, c_t, _) in components:
        ene_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        if ene_rect.colliderect(pl_rect):
            collision_pos = pygame.Vector2(
                (pl_t.pos.x + ene_rect.x) / 2,
                (pl_t.pos.y + ene_rect.y) / 2
            )
            world.delete_entity(enemy_entity)
            ServiceLocator.sounds_service.play(level_cfg["sound_collision"])
            create_explosion(world, collision_pos, explosion_cfg)
            pl_t.pos.x = level_cfg["player_spawn"]["position"]["x"] - pl_s.surf.get_width() / 2
            pl_t.pos.y = level_cfg["player_spawn"]["position"]["y"] - pl_s.surf.get_height() / 2