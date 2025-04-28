import pygame
import esper
from src.ecs.components.c_enemy_hunter_state import CEnemyHunterState, EnemyState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_animation import CAnimation
from src.engine.service_locator import ServiceLocator

def system_enemy_hunter(world: esper.World, player_pos: pygame.Vector2, delta_time: float, hunter_info:dict):
    components = world.get_components(CEnemyHunterState, CTransform, CVelocity, CAnimation, CSurface)
    
    for _, (c_state, c_trans, c_vel, c_anim, c_surf) in components:
        entity_center = pygame.Vector2(
            c_trans.pos.x + c_surf.area.width / 2,
            c_trans.pos.y + c_surf.area.height / 2
        )
        
        # Calculate distances
        to_player = player_pos - entity_center
        to_origin = c_state.initial_pos - entity_center
        
        distance_to_player = to_player.length()
        distance_to_origin = to_origin.length()
        
        # State transitions
        if c_state.state == EnemyState.IDLE:
            if distance_to_player <= c_state.chase_distance:
                ServiceLocator.sounds_service.play(hunter_info["sound_chase"])
                c_state.state = EnemyState.CHASE
                _set_animation(c_anim, 0)  # MOVE animation
        elif c_state.state == EnemyState.CHASE:
            if distance_to_origin >= c_state.return_distance:
                c_state.state = EnemyState.RETURN
                _set_animation(c_anim, 0)  # MOVE animation
        elif c_state.state == EnemyState.RETURN:
            if distance_to_origin <= 5.0:  # Close enough to origin
                c_state.state = EnemyState.IDLE
                _set_animation(c_anim, 1)  # IDLE animation
                c_vel.vel = pygame.Vector2(0, 0)
        
        # Update velocity based on state
        if c_state.state == EnemyState.CHASE:
            if to_player.length() > 0:
                direction = to_player.normalize()
                c_vel.vel = direction * c_state.chase_velocity
        elif c_state.state == EnemyState.RETURN:
            if to_origin.length() > 0:
                direction = to_origin.normalize()
                c_vel.vel = direction * c_state.return_velocity

def _set_animation(c_a: CAnimation, num_anim: int):
    if c_a.curr_anim == num_anim:
        return
    c_a.curr_anim = num_anim
    c_a.curr_anim_time = 0
    c_a.curr_frame = c_a.animations_list[c_a.curr_anim].start