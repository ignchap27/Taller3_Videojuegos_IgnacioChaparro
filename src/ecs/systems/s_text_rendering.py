import pygame

from src.engine.service_locator import ServiceLocator

def system_text_rendering(screen: pygame.Surface, level_cfg: dict):
    # Load fonts
    title_font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 18)
    instruction_font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 12)
    
    # Render title with a shadow effect
    shadow_color = pygame.Color(0, 0, 0)
    title_shadow = title_font.render(level_cfg["title"], True, shadow_color)
    title_text = title_font.render(level_cfg["title"], True, pygame.Color(255, 255, 255))
    
    # Position for title (centered at top with shadow)
    title_rect = title_text.get_rect(centerx=screen.get_width() // 2, y=20)
    shadow_rect = title_rect.copy()
    shadow_rect.x += 2
    shadow_rect.y += 2
    
    # Draw title with shadow
    screen.blit(title_shadow, shadow_rect)
    screen.blit(title_text, title_rect)
    
    # Instructions - handle multi-line text
    instructions = level_cfg["instructions"]
    words = instructions.split(' ')
    current_line = ""
    y_position = screen.get_height() - 40
    max_width = screen.get_width() - 60
    
    for word in words:
        test_line = current_line + word + " "
        # Check if adding this word exceeds max width
        test_width = instruction_font.size(test_line)[0]
        
        if test_width > max_width:
            # Render current line
            if current_line:
                text_surface = instruction_font.render(current_line, True, pygame.Color(200, 200, 200))
                text_rect = text_surface.get_rect(centerx=screen.get_width() // 2, y=y_position)
                screen.blit(text_surface, text_rect)
                
                # Move to next line
                y_position += instruction_font.get_linesize()
                current_line = word + " "
        else:
            current_line = test_line
    
    # Render the last line
    if current_line:
        text_surface = instruction_font.render(current_line, True, pygame.Color(200, 200, 200))
        text_rect = text_surface.get_rect(centerx=screen.get_width() // 2, y=y_position)
        screen.blit(text_surface, text_rect)