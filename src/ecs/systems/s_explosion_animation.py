import esper
from src.ecs.components.c_animation import CAnimation, AnimationData
from src.ecs.components.tags.c_tag_explosion import CTagExplosion

def system_explosion_animation(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)
    
    for entity, (c_a, c_tag) in components:
        current_anim = c_a.animations_list[c_a.curr_anim]
        
        if c_a.curr_frame == current_anim.end:
            world.delete_entity(entity, immediate=True)