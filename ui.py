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

def draw_top_bar(screen, game_logic, game_mode, black_time):
    """Dibuja la barra superior con información del estado del juego."""
    # Fondo de la barra superior
    pg.draw.rect(screen, config.UI_BG, (0, 0, config.WIDTH, config.TOP_UI_HEIGHT))
    # Texto del turno
    font = pg.font.SysFont(None, config.UI_FONT_SIZE + 4)
    turn_text = f"Turno: {game_logic.turn.capitalize()}"
    turn_surface = font.render(turn_text, True, config.UI_FONT_COLOR)
    turn_rect = turn_surface.get_rect(center=(config.WIDTH / 2, config.TOP_UI_HEIGHT / 3))
    screen.blit(turn_surface, turn_rect)

    # Texto de la habilidad activa
    if game_logic.piece_with_ability and game_logic.piece_with_ability.ability:
        ability_text = f"Habilidad Activa: {game_logic.piece_with_ability.ability.replace('_', ' ').title()} ({game_logic.piece_with_ability.name.title()})"
        ability_font = pg.font.SysFont(None, config.UI_FONT_SIZE - 4) # Un poco más pequeño
        ability_surface = ability_font.render(ability_text, True, config.ABILITY_FONT_COLOR)
        ability_rect = ability_surface.get_rect(center=(config.WIDTH / 2, config.TOP_UI_HEIGHT * 2 / 3))
        screen.blit(ability_surface, ability_rect)

    # Mostrar cronómetro de las negras en la parte superior si el modo es 'timed'
    if game_mode == 'timed':
        timer_font = pg.font.SysFont(None, config.UI_FONT_SIZE + 6)
        
        # Cronómetro Negro
        black_minutes, black_seconds = divmod(int(black_time), 60)
        black_text = f"{black_minutes:02}:{black_seconds:02}"
        black_surface = timer_font.render(black_text, True, config.UI_FONT_COLOR)
        black_rect = black_surface.get_rect(midleft=(20, config.TOP_UI_HEIGHT / 2))
        screen.blit(black_surface, black_rect)

def draw_bottom_ui(screen, selected_color, swatch_rects, game_mode, white_time):
    """Dibuja toda la UI inferior, incluyendo paleta, botones y cronómetro."""
    buttons = {}
    
    # Fondo de la UI
    pg.draw.rect(screen, config.UI_BG, (0, config.TOP_UI_HEIGHT + config.BOARD_HEIGHT, config.WIDTH, config.BOTTOM_UI_HEIGHT))

    # --- Paleta de Colores (Izquierda) ---
    for i, rect in enumerate(swatch_rects):
        pg.draw.rect(screen, config.COLOR_PALETTE[i], rect, border_radius=3)
        if config.COLOR_PALETTE[i] == selected_color:
            pg.draw.rect(screen, config.WHITE, rect, 3)

    # --- Botón "Cambiar Color" (junto a la paleta) ---
    cc_button_rect = draw_change_color_button(screen)
    buttons['cambiar_color'] = cc_button_rect

    # --- Iconos de Acción (Derecha) ---
    action_icons = draw_action_icons(screen)
    buttons.update(action_icons)

    # --- Cronómetro de las blancas (si está en modo 'timed') ---
    if game_mode == 'timed':
        timer_font = pg.font.SysFont(None, config.UI_FONT_SIZE + 6)
        white_minutes, white_seconds = divmod(int(white_time), 60)
        white_text = f"{white_minutes:02}:{white_seconds:02}"
        white_surface = timer_font.render(white_text, True, config.UI_FONT_COLOR)

        # Posicionar el cronómetro debajo de la paleta de colores, a la izquierda.
        # Usamos el primer swatch de la paleta como referencia para la posición X.
        palette_start_x = swatch_rects[0].left
        white_rect = white_surface.get_rect(midleft=(palette_start_x, config.TOP_UI_HEIGHT + config.BOARD_HEIGHT + config.BOTTOM_UI_HEIGHT * 0.75))
        screen.blit(white_surface, white_rect)

    return buttons

def draw_action_icons(screen):
    """Dibuja los botones de acción como iconos en una cuadrícula 3x2 en la esquina inferior derecha."""
    buttons = {}
    icon_font = pg.font.SysFont('Arial', config.ICON_SIZE // 2, bold=True)
    
    # Definimos los iconos (texto) y sus claves
    icons = [('guardar', 'S'), ('cargar', 'L'), ('reiniciar', 'R'), ('menú', 'M'), ('info', '?')]
    
    grid_cols = 3
    start_x = config.WIDTH - (grid_cols * (config.ICON_SIZE + config.ICON_PADDING)) - config.ICON_PADDING
    start_y = config.TOP_UI_HEIGHT + config.BOARD_HEIGHT + (config.BOTTOM_UI_HEIGHT - 2 * config.ICON_SIZE - config.ICON_PADDING) / 2

    for i, (key, symbol) in enumerate(icons):
        col = i % grid_cols
        row = i // grid_cols
        x = start_x + col * (config.ICON_SIZE + config.ICON_PADDING)
        y = start_y + row * (config.ICON_SIZE + config.ICON_PADDING)
        
        rect = pg.Rect(x, y, config.ICON_SIZE, config.ICON_SIZE)
        pg.draw.rect(screen, config.UI_FONT_COLOR, rect, border_radius=5)
        
        text_surface = icon_font.render(symbol, True, config.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        buttons[key] = rect
        
    return buttons

def draw_bottom_right_buttons(screen):
    """Dibuja el botón 'Cambiar Color' y los botones de acción en la esquina inferior derecha."""
    buttons = {}
    font = pg.font.SysFont(None, config.UI_FONT_SIZE - 4)
    
    # --- Botones de Acción ---
    action_texts = ["Guardar", "Cargar", "Reiniciar", "Menú", "Info"]
    button_width = 55
    button_height = 30
    padding = 8
    
    # Posicionamos los botones en la esquina inferior derecha
    start_x = config.WIDTH - padding
    
    for i, text in enumerate(reversed(action_texts)): # Dibujar de derecha a izquierda
        button_x = start_x - (i + 1) * (button_width + padding) + padding
        button_y = config.TOP_UI_HEIGHT + config.BOARD_HEIGHT + (config.BOTTOM_UI_HEIGHT - button_height) / 2
        
        rect = pg.Rect(button_x, button_y, button_width, button_height)
        
        pg.draw.rect(screen, config.UI_FONT_COLOR, rect, border_radius=5)
        text_surface = font.render(text, True, config.BLACK)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        
        # Guardar el rect del botón con una clave
        buttons[text.lower().replace(' ', '_')] = rect

    # --- Botón Cambiar Color ---
    # Lo posicionamos a la izquierda de los botones de acción
    change_color_text = "Cambiar Color"
    change_color_font = pg.font.SysFont(None, config.UI_FONT_SIZE - 2)
    change_color_surface = change_color_font.render(change_color_text, True, config.BLACK)
    
    cc_button_width = change_color_surface.get_width() + 15
    cc_button_height = change_color_surface.get_height() + 15
    cc_button_x = start_x - len(action_texts) * (button_width + padding) - cc_button_width
    cc_button_y = config.TOP_UI_HEIGHT + config.BOARD_HEIGHT + (config.BOTTOM_UI_HEIGHT - cc_button_height) / 2

    cc_rect = pg.Rect(cc_button_x, cc_button_y, cc_button_width, cc_button_height)
    pg.draw.rect(screen, config.UI_FONT_COLOR, cc_rect, border_radius=5)
    screen.blit(change_color_surface, (cc_button_x + 7.5, cc_button_y + 7.5))
    buttons['cambiar_color'] = cc_rect
            
    return buttons

def draw_menu(screen, title_color):
    """Dibuja la pantalla del menú principal y devuelve los rects de los botones."""
    buttons = {}
    
    # Título
    title_font = pg.font.SysFont(None, 74)
    title_surface = title_font.render("ChessMagic", True, title_color)
    title_rect = title_surface.get_rect(center=(config.WIDTH / 2, config.HEIGHT / 4))
    screen.blit(title_surface, title_rect)

    # Botones
    button_font = pg.font.SysFont(None, 40) # Tamaño de fuente reducido para que encaje
    button_options = {
        'indefinite': "Modo Clásico (Sin Tiempo)",
        'timed': "Modo Cronómetro (10 min)"
    }
    
    button_height = 60
    button_width = 400
    
    for i, (key, text) in enumerate(button_options.items()):
        y_pos = config.HEIGHT / 2 + i * (button_height + 20)
        rect = pg.Rect((config.WIDTH - button_width) / 2, y_pos, button_width, button_height)
        buttons[key] = rect
        pg.draw.rect(screen, config.DEFAULT_DARK_SQUARE, rect, border_radius=10)
        text_surface = button_font.render(text, True, (0, 255, 255)) # Cian Neón para mejor contraste
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
        
    return buttons

def draw_info_popup(screen):
    """Dibuja una ventana emergente con la descripción de las habilidades."""
    # Fondo semi-transparente
    overlay = pg.Surface((config.WIDTH, config.HEIGHT), pg.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Panel principal
    panel_width = 500
    panel_height = 300
    panel_x = (config.WIDTH - panel_width) / 2
    panel_y = (config.HEIGHT - panel_height) / 2
    panel_rect = pg.Rect(panel_x, panel_y, panel_width, panel_height)
    pg.draw.rect(screen, config.UI_BG, panel_rect, border_radius=15)
    pg.draw.rect(screen, config.WHITE, panel_rect, 2, border_radius=15)

    # Título
    title_font = pg.font.SysFont(None, 40)
    title_surface = title_font.render("Habilidades Disponibles", True, config.ABILITY_FONT_COLOR)
    title_rect = title_surface.get_rect(center=(config.WIDTH / 2, panel_y + 40))
    screen.blit(title_surface, title_rect)

    # --- Lógica de ajuste de texto para las descripciones ---
    desc_font = pg.font.SysFont(None, 24)
    current_y = panel_y + 90 # Posición Y inicial para el contenido
    max_width = panel_width - 60 # Ancho máximo para el texto (panel - márgenes)

    for ability, desc in config.ABILITY_DESCRIPTIONS.items():
        # Nombre de la habilidad
        ability_name = ability.replace('_', ' ').title()
        name_surface = desc_font.render(f"• {ability_name}:", True, config.WHITE)
        screen.blit(name_surface, (panel_x + 30, current_y))
        current_y += 25 # Mover hacia abajo para la descripción

        # Descripción con ajuste de texto
        words = desc.split(' ')
        line = ""
        for word in words:
            test_line = line + word + " "
            if desc_font.size(test_line)[0] < max_width:
                line = test_line
            else:
                # Dibujar la línea actual y empezar una nueva
                line_surface = desc_font.render(line, True, config.UI_FONT_COLOR)
                screen.blit(line_surface, (panel_x + 40, current_y))
                current_y += 20 # Espacio entre líneas
                line = word + " "
        # Dibujar la última línea restante
        line_surface = desc_font.render(line, True, config.UI_FONT_COLOR)
        screen.blit(line_surface, (panel_x + 40, current_y))
        current_y += 40 # Espacio antes de la siguiente habilidad

    # Mensaje para cerrar
    close_font = pg.font.SysFont(None, 20)
    close_surface = close_font.render("Haz clic fuera para cerrar", True, config.UI_FONT_COLOR)
    close_rect = close_surface.get_rect(center=(config.WIDTH / 2, panel_y + panel_height - 20))
    screen.blit(close_surface, close_rect)