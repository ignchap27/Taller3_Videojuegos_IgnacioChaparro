from enum import Enum
import pygame

class EnemyState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2

class CEnemyHunterState:
    def __init__(self, initial_pos: pygame.Vector2, 
                 chase_distance: float, return_distance: float,
                 chase_velocity: float, return_velocity: float) -> None:
        self.state = EnemyState.IDLE
        self.initial_pos = initial_pos.copy()
        self.chase_distance = chase_distance
        self.return_distance = return_distance
        self.chase_velocity = chase_velocity
        self.return_velocity = return_velocity