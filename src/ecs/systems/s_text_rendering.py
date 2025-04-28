import pygame

from src.engine.service_locator import ServiceLocator

def system_text_rendering(screen: pygame.Surface, level_cfg: dict, is_paused: bool = False):
    # Load fonts
    title_font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 18)
    instruction_font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 12)
    pause_font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 24)
    
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
    
    if is_paused:
        # Obtener el ancho de la pantalla completa para centrado correcto
        real_screen_width = screen.get_width()
        
        # Handle pause text - break into multiple lines if needed
        pause_text = level_cfg["paused"]
        # Test if pause text is too wide
        test_surface = pause_font.render(pause_text, True, pygame.Color(255, 255, 255))
        if test_surface.get_width() > real_screen_width - 40:
            # Split into multiple lines
            words = pause_text.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + word + " "
                # Check if adding this word exceeds max width
                if pause_font.size(test_line)[0] > real_screen_width - 60:
                    lines.append(current_line)
                    current_line = word + " "
                else:
                    current_line = test_line
            
            if current_line:
                lines.append(current_line)
            
            # Create background for pause text
            total_height = len(lines) * pause_font.get_linesize()
            pause_bg_rect = pygame.Rect(
                0, (screen.get_height() // 2) - (total_height // 2) - 20,
                real_screen_width, total_height + 40
            )
            
            pause_bg_surf = pygame.Surface((pause_bg_rect.width, pause_bg_rect.height), pygame.SRCALPHA)
            pause_bg_surf.fill((0, 0, 0, 200))
            screen.blit(pause_bg_surf, pause_bg_rect)
            
            # Draw each line
            y_pos = (screen.get_height() // 2) - (total_height // 2)
            for line in lines:
                line_surf = pause_font.render(line, True, pygame.Color(255, 100, 100))
                line_rect = line_surf.get_rect(centerx=real_screen_width//2, y=y_pos)
                
                # Add semitransparent shadow effect
                shadow_surf = pause_font.render(line, True, pygame.Color(80, 0, 0, 180))
                shadow_rect = line_rect.copy()
                shadow_rect.x += 2
                shadow_rect.y += 2
                
                screen.blit(shadow_surf, shadow_rect)
                screen.blit(line_surf, line_rect)
                y_pos += pause_font.get_linesize()
        else:
            # Single line pause text
            pause_surf = pause_font.render(pause_text, True, pygame.Color(255, 100, 100))
            pause_rect = pause_surf.get_rect(center=(real_screen_width//2, screen.get_height()//2))
            
            # Create background for pause text
            pause_bg_rect = pause_rect.inflate(40, 20)
            pause_bg_surf = pygame.Surface((pause_bg_rect.width, pause_bg_rect.height), pygame.SRCALPHA)
            pause_bg_surf.fill((0, 0, 0, 200))
            
            # Add semitransparent shadow effect
            shadow_surf = pause_font.render(pause_text, True, pygame.Color(80, 0, 0, 180))
            shadow_rect = pause_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            
            # Draw pause text with background and shadow
            screen.blit(pause_bg_surf, pause_bg_rect)
            screen.blit(shadow_surf, shadow_rect)
            screen.blit(pause_surf, pause_rect)
    
    
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