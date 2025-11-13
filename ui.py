# Archivo: ui.py
# Descripción: Contiene las funciones para dibujar la interfaz de usuario del juego.

import pygame as pg
import config

def draw_board(screen, colors):
    """Dibuja el tablero de ajedrez en la pantalla."""
    for row in range(config.ROWS):
        for col in range(config.COLS):
            # Alternar colores para crear el patrón de tablero
            if (row + col) % 2 == 0:
                color = colors["light"]
            else:
                color = colors["dark"]
            pg.draw.rect(screen, color, (col * config.SQUARE_SIZE, row * config.SQUARE_SIZE + config.TOP_UI_HEIGHT, config.SQUARE_SIZE, config.SQUARE_SIZE))

def create_palette_rects():
    """Calcula y devuelve los rectángulos para la paleta de colores. Se llama una sola vez."""
    # El área total disponible para la paleta (aprox. la mitad izquierda de la UI inferior)
    available_width = config.WIDTH // 2 - 40 # Dejamos un margen
    num_colors = len(config.COLOR_PALETTE)

    # Calculamos el tamaño de cada swatch dinámicamente
    # Asumimos un 80% para el color y 20% para el espaciado
    total_swatch_width = available_width / num_colors
    swatch_size = int(total_swatch_width * 0.8)
    padding = int(total_swatch_width * 0.2)

    # Centramos la paleta en su área designada
    palette_width = num_colors * (swatch_size + padding) - padding
    start_x = (available_width - palette_width) // 2 + 20 # 20px de margen izquierdo
    
    swatch_rects = []
    for i, color in enumerate(config.COLOR_PALETTE):
        y_pos = config.TOP_UI_HEIGHT + config.BOARD_HEIGHT + (config.BOTTOM_UI_HEIGHT - swatch_size) // 2
        rect = pg.Rect(start_x + i * (swatch_size + padding), y_pos, swatch_size, swatch_size)
        swatch_rects.append(rect)
    return swatch_rects

def draw_change_color_button(screen):
    """Dibuja el botón 'Cambiar Color' y devuelve su rectángulo."""
    font = pg.font.SysFont(None, config.UI_FONT_SIZE)
    text = "Cambiar Color"
    text_surface = font.render(text, True, config.BLACK)
    
    button_width = text_surface.get_width() + 20
    button_height = text_surface.get_height() + 20
    
    # Posicionamos el botón a la derecha de la paleta
    button_x = config.WIDTH // 2 + 20
    button_y = config.TOP_UI_HEIGHT + config.BOARD_HEIGHT + (config.BOTTOM_UI_HEIGHT - button_height) // 2
    
    button_rect = pg.Rect(button_x, button_y, button_width, button_height)
    
    pg.draw.rect(screen, config.UI_FONT_COLOR, button_rect, border_radius=5)
    screen.blit(text_surface, (button_x + 10, button_y + 10))
    
    return button_rect

def draw_action_buttons(screen):
    """Dibuja los botones de acción (Guardar, Cargar, Reiniciar) y devuelve sus rectángulos."""
    buttons = {}
    font = pg.font.SysFont(None, config.UI_FONT_SIZE - 4)
    button_texts = ["Guardar", "Cargar", "Reiniciar"]
    
    button_width = 50
    button_height = 30
    padding = 10
    
    # Posicionamos los botones en la esquina superior derecha
    start_x = config.WIDTH - padding
    
    for i, text in enumerate(reversed(button_texts)): # Dibujar de derecha a izquierda
        button_x = start_x - (i + 1) * (button_width + padding) + padding
        button_y = (config.TOP_UI_HEIGHT - button_height) // 2
        
        rect = pg.Rect(button_x, button_y, button_width, button_height)
        
        # Dibujar botón
        pg.draw.rect(screen, config.UI_FONT_COLOR, rect, border_radius=5)
        
        # Dibujar texto
        text_surface = font.render(text, True, config.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        
        # Guardar el rect del botón con una clave
        if text == "Guardar":
            buttons['save'] = rect
        elif text == "Cargar":
            buttons['load'] = rect
        elif text == "Reiniciar":
            buttons['reset'] = rect
            
    return buttons

def draw_ui(screen, selected_color, swatch_rects):
    """Dibuja la interfaz de usuario con la paleta de colores."""
    # Fondo de la UI
    pg.draw.rect(screen, config.UI_BG, (0, config.TOP_UI_HEIGHT + config.BOARD_HEIGHT, config.WIDTH, config.BOTTOM_UI_HEIGHT))

    # Dibuja cada swatch de color usando los rectángulos pre-calculados
    for i, rect in enumerate(swatch_rects):
        pg.draw.rect(screen, config.COLOR_PALETTE[i], rect, border_radius=3)
        # Dibuja un borde si es el color seleccionado
        if config.COLOR_PALETTE[i] == selected_color:
            pg.draw.rect(screen, config.WHITE, rect, 3)  # Borde de 3px

def draw_top_bar(screen, game_logic):
    """Dibuja la barra superior con información del estado del juego."""
    # Fondo de la barra superior
    pg.draw.rect(screen, config.UI_BG, (0, 0, config.WIDTH, config.TOP_UI_HEIGHT))
    # Texto del turno
    font = pg.font.SysFont(None, config.UI_FONT_SIZE)
    turn_text = f"Turno: {game_logic.turn.capitalize()}"
    turn_surface = font.render(turn_text, True, config.UI_FONT_COLOR)
    turn_rect = turn_surface.get_rect(center=(config.WIDTH / 2, config.TOP_UI_HEIGHT / 3))
    screen.blit(turn_surface, turn_rect)

    # Texto de la habilidad activa
    if game_logic.piece_with_ability:
        ability_text = f"Habilidad Activa: {game_logic.piece_with_ability.ability.replace('_', ' ').title()}"
        ability_font = pg.font.SysFont(None, config.UI_FONT_SIZE - 4) # Un poco más pequeño
        ability_surface = ability_font.render(ability_text, True, config.ABILITY_FONT_COLOR)
        ability_rect = ability_surface.get_rect(center=(config.WIDTH / 2, config.TOP_UI_HEIGHT * 2 / 3))
        screen.blit(ability_surface, ability_rect)
    
    return draw_action_buttons(screen) # Dibuja los botones y devuelve sus rects