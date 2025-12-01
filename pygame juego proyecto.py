"""=================================================
 PRESENTACIÓN: chessmagic 
================================================="""
# Archivo: pygame juego proyecto.py (o main.py)
# Descripción: Punto de entrada principal para el juego de Ajedrez con Habilidades.
# Este archivo contiene el bucle principal del juego, maneja eventos y coordina
# el dibujado en pantalla.

import pygame
import sys
import config
import os
from ui import draw_board, create_palette_rects, draw_top_bar, draw_bottom_ui, draw_menu, draw_info_popup
from board import Board
from game_logic import GameLogic
import database

class Game:
    """Clase principal que encapsula la lógica y el estado del juego."""
    def __init__(self):
        """Inicializa el juego y sus componentes."""
        pygame.init()
        pygame.mixer.init() # Inicializar el mezclador de audio
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT)) # type: ignore
        pygame.display.set_caption("ChessMagic")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = 'MENU' # Estados: MENU, PLAYING, INFO
        self.game_mode = None # Modos: 'indefinite', 'timed'
        self.menu_buttons = {}
        self.menu_video_frames = []
        self.current_video_frame = 0

        # Atributos para el título animado del menú
        # Paleta de colores neón sin amarillos
        self.title_colors = [
            (0, 255, 255),   # Cian Neón
            (255, 0, 255),   # Magenta Neón
            (57, 255, 20),    # Verde Neón
            (255, 0, 0)      # Rojo Brillante
        ]
        self.current_title_color_index = 0
        self.last_color_change_time = 0

        # Atributos para el cronómetro
        self.white_time = config.GAME_TIME_SECONDS
        self.black_time = config.GAME_TIME_SECONDS
        self.timer_winner = None
        self.move_sound = None

        # Estado del juego
        self.board_colors = {
            "light": config.DEFAULT_LIGHT_SQUARE,
            "dark": config.DEFAULT_DARK_SQUARE
        }
        self.selected_color = config.COLOR_PALETTE[0]
        self.selected_piece = None
        
        # Lógica del juego
        self.board = Board()
        self.game_logic = GameLogic(self.board)

        # UI: Calcula los rectángulos de la paleta una sola vez
        self.swatch_rects = create_palette_rects()
        self.change_color_button_rect = None # Se calculará en el primer render
        self.action_buttons_rects = {} # Para guardar, cargar, reiniciar

        # Inicializar la base de datos
        database.init_db()

        # Cargar recursos del menú (vídeo y música)
        self.load_menu_resources()

        # Cargar efectos de sonido del juego
        try:
            sound_path = os.path.join(config.SOUNDS_PATH, 'ficha-de-ajedrez.mp3')
            self.move_sound = pygame.mixer.Sound(sound_path)
            self.move_sound.set_volume(0.7)
        except pygame.error as e:
            print(f"Advertencia: No se pudo cargar el sonido de movimiento: {e}")

    def run(self):
        """Inicia y mantiene el bucle principal del juego."""
        while self.running:
            if self.game_state == 'MENU':
                self.handle_menu_events()
                self.render_menu()
            elif self.game_state == 'PLAYING':
                self.update()
                self.handle_game_events()
                self.render_game()
            elif self.game_state == 'INFO':
                self.handle_info_events()
                self.render_game(show_info=True)

            self.clock.tick(config.FPS)

        pygame.quit()
        sys.exit()

    def load_menu_resources(self):
        """Carga la música de fondo y los fotogramas del vídeo para el menú."""
        # Cargar música
        try:
            music_path = os.path.join(config.SOUNDS_PATH, 'fondo musica menu.mp3')
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1) # El -1 hace que se repita indefinidamente
            pygame.mixer.music.set_volume(0.5) # Ajustar volumen (0.0 a 1.0)
        except pygame.error as e:
            print(f"Advertencia: No se pudo cargar la música del menú: {e}")

        # Cargar fotogramas del vídeo
        try:
            # Obtener lista de archivos y ordenarla alfabéticamente para asegurar el orden correcto
            frame_files = sorted(os.listdir(config.VIDEO_FRAMES_PATH))
            for frame_file in frame_files:
                if frame_file.endswith(('.png', '.jpg', '.jpeg')):
                    frame_path = os.path.join(config.VIDEO_FRAMES_PATH, frame_file)
                    self.menu_video_frames.append(pygame.image.load(frame_path).convert())
        except FileNotFoundError:
            print(f"Advertencia: No se encontró la carpeta de fotogramas de vídeo en {config.VIDEO_FRAMES_PATH}")

    def handle_menu_events(self):
        """Gestiona eventos en la pantalla del menú."""
        # Lógica para cambiar el color del título cada segundo
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time > 1000: # 1000 ms = 1 segundo
            self.last_color_change_time = current_time
            self.current_title_color_index = (self.current_title_color_index + 1) % len(self.title_colors)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu_buttons['indefinite'].collidepoint(event.pos):
                    self.start_game('indefinite')
                elif self.menu_buttons['timed'].collidepoint(event.pos):
                    self.start_game('timed')

    def handle_game_events(self):
        """Procesa las entradas del usuario (ratón, teclado, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # El botón de info debe funcionar incluso si el juego ha terminado
                if self.action_buttons_rects.get('info') and self.action_buttons_rects['info'].collidepoint(event.pos):
                    self.game_state = 'INFO'
                    return
                
                # El resto de clics solo funcionan si el juego no ha terminado
                if not self.game_logic.game_over:
                    self.handle_mouse_click(event.pos)
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """Gestiona la lógica de un clic del ratón."""
        # Si el juego ha terminado, solo los botones de reinicio/carga/guardado deben funcionar
        if self.game_logic.game_over:
            self.handle_game_over_click(pos)
            return
        # Comprobar si se hizo clic en la paleta de colores
        for i, rect in enumerate(self.swatch_rects):
            if rect.collidepoint(pos):
                # Asegurarse de seleccionar siempre el color claro del par
                if i % 2 != 0: # Si el índice es impar (color oscuro)
                    self.selected_color = config.COLOR_PALETTE[i - 1]
                else: # Si el índice es par (color claro)
                    self.selected_color = config.COLOR_PALETTE[i]
                return # Termina la función para no procesar el clic en el tablero

        # Comprobar si se hizo clic en los botones de acción (Guardar, Cargar, Reiniciar)
        if self.action_buttons_rects.get('guardar') and self.action_buttons_rects['guardar'].collidepoint(pos):
            database.save_game_state(self.game_logic, self.board)
            return

        if self.action_buttons_rects.get('cargar') and self.action_buttons_rects['cargar'].collidepoint(pos):
            if database.load_game_state(self.game_logic, self.board):
                self.selected_piece = None # Deseleccionar pieza tras cargar
                # La habilidad se resetea dentro de load_game_state, pero la asignamos al nuevo turno
                self.game_logic.assign_random_ability()
            return

        if self.action_buttons_rects.get('reiniciar') and self.action_buttons_rects['reiniciar'].collidepoint(pos):
            self.reset_game()
            return

        if self.action_buttons_rects.get('menú') and self.action_buttons_rects['menú'].collidepoint(pos):
            self.game_state = 'MENU'
            # Detener la música del juego y empezar la del menú
            pygame.mixer.music.fadeout(500)
            # Reiniciar la música del menú si no está sonando
            self.play_menu_music()
            return

        if self.action_buttons_rects.get('info') and self.action_buttons_rects['info'].collidepoint(pos):
            self.game_state = 'INFO'
            return

        # Comprobar si se hizo clic en el botón "Cambiar Color"
        if self.action_buttons_rects.get('cambiar_color') and self.action_buttons_rects['cambiar_color'].collidepoint(pos):
            try:
                idx = config.COLOR_PALETTE.index(self.selected_color)
                # Asumimos que el color oscuro es el siguiente en la lista
                self.board_colors["light"] = self.selected_color
                self.board_colors["dark"] = config.COLOR_PALETTE[idx + 1]
            except (ValueError, IndexError):
                print("Error al cambiar el color del tablero.")
            return

        # Si no se hizo clic en la paleta, comprobar si fue en el tablero
        board_rect = pygame.Rect(0, config.TOP_UI_HEIGHT, config.BOARD_WIDTH, config.BOARD_HEIGHT)
        if board_rect.collidepoint(pos):
            col = pos[0] // config.SQUARE_SIZE
            row = (pos[1] - config.TOP_UI_HEIGHT) // config.SQUARE_SIZE
            
            clicked_piece = self.board.board[row][col]

            if self.selected_piece:
                # Si hay una pieza seleccionada, verificamos el clic.
                # 1. No se puede capturar una pieza del mismo color.
                if clicked_piece is not None and clicked_piece.color == self.selected_piece.color:
                    # Si se hace clic en otra pieza del mismo color, la seleccionamos.
                    self.selected_piece = clicked_piece
                    return

                # 2. Intentar mover la pieza a la nueva casilla (vacía o con enemigo).
                if self.game_logic.is_valid_move(self.selected_piece, row, col): # (Aquí iría la validación de movimiento de la pieza)
                    is_double_step_rook = self.selected_piece.ability == 'double_step_rook'
                    
                    # Si es el primer movimiento de la torre de doble paso
                    if is_double_step_rook and self.game_logic.double_step_rook_moved is None:
                        self.game_logic.double_step_rook_moved = self.selected_piece
                        self.board.move_piece(self.selected_piece, row, col, keep_ability=True)
                        if self.move_sound:
                            self.move_sound.play()
                        # No cambiamos de turno y no deseleccionamos la pieza.
                        # El jugador debe mover la torre de nuevo.
                        return

                    # Para cualquier otro movimiento (incluido el segundo de la torre)
                    self.board.move_piece(self.selected_piece, row, col)
                    
                    # Reproducir sonido de movimiento
                    if self.move_sound:
                        self.move_sound.play()
                    
                    # Comprobar si el movimiento resultó en la captura del rey
                    self.game_logic.check_king_capture(self.selected_piece.color)

                    # Si el juego no ha terminado por captura, pasar al siguiente turno
                    if not self.game_logic.game_over:
                        self.game_logic.next_turn()
                    self.selected_piece = None # Deseleccionar después del movimiento final
                else:
                    # Si el movimiento no es válido, deseleccionar la pieza
                    self.selected_piece = None
            else:
                # Si no hay pieza seleccionada y se hace clic en una pieza del color del turno, la seleccionamos.
                if clicked_piece is not None and clicked_piece.color == self.game_logic.turn:
                    self.selected_piece = clicked_piece

    def handle_game_over_click(self, pos):
        """Gestiona los clics después de que el juego ha terminado."""
        # Comprobar si se hizo clic en los botones de acción (Guardar, Cargar, Reiniciar)
        if self.action_buttons_rects.get('guardar') and self.action_buttons_rects['guardar'].collidepoint(pos):
            database.save_game_state(self.game_logic, self.board)
            return

        if self.action_buttons_rects.get('cargar') and self.action_buttons_rects['cargar'].collidepoint(pos):
            if database.load_game_state(self.game_logic, self.board):
                self.selected_piece = None # Deseleccionar pieza tras cargar
                self.game_logic.assign_random_ability()
            return

        if self.action_buttons_rects.get('reiniciar') and self.action_buttons_rects['reiniciar'].collidepoint(pos):
            self.reset_game()
            return

        if self.action_buttons_rects.get('menú') and self.action_buttons_rects['menú'].collidepoint(pos):
            self.game_state = 'MENU'
            # Detener la música del juego y empezar la del menú
            pygame.mixer.music.fadeout(500)
            # Reiniciar la música del menú si no está sonando
            self.play_menu_music()
            return

    def play_game_music(self):
        """Carga y reproduce la música de fondo para la partida."""
        try:
            music_path = os.path.join(config.SOUNDS_PATH, 'neon-city.mp3')
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1) # Repetir indefinidamente
            pygame.mixer.music.set_volume(0.4) # Un poco más bajo que el menú
        except pygame.error as e:
            print(f"Advertencia: No se pudo cargar la música del juego: {e}")

    def play_menu_music(self):
        """Carga y reproduce la música del menú, deteniendo cualquier otra que esté sonando."""
        try:
            music_path = os.path.join(config.SOUNDS_PATH, 'fondo musica menu.mp3')
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        except pygame.error as e:
            print(f"Advertencia: No se pudo reiniciar la música del menú: {e}")

    def handle_info_events(self):
        """Gestiona eventos mientras se muestra el pop-up de información."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Si se hace clic o se presiona una tecla, se cierra el pop-up
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.game_state = 'PLAYING'
                return



    def update(self):
        """Actualiza el estado del juego (lógica de piezas, turnos, etc.)."""
        if self.game_mode == 'timed' and not self.game_logic.game_over:
            # Obtener el tiempo transcurrido en segundos
            delta_time = self.clock.get_time() / 1000.0

            if self.game_logic.turn == 'white':
                self.white_time -= delta_time
                if self.white_time <= 0:
                    self.white_time = 0
                    self.game_logic.game_over = True
                    self.timer_winner = 'Black' # Ganan las negras
            else:
                self.black_time -= delta_time
                if self.black_time <= 0:
                    self.black_time = 0
                    self.game_logic.game_over = True
                    self.timer_winner = 'White' # Ganan las blancas

    def start_game(self, mode):
        """Configura e inicia una nueva partida en el modo seleccionado."""
        # Detener la música del menú al iniciar la partida
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500) # Desvanecer en 500 ms

        # Iniciar la música del juego
        self.play_game_music()

        self.game_mode = mode
        self.reset_game()
        self.game_state = 'PLAYING'

    def reset_game(self):
        """Reinicia el juego a su estado inicial."""
        print("Reiniciando partida...")
        self.board = Board()
        self.game_logic = GameLogic(self.board)
        self.white_time = config.GAME_TIME_SECONDS
        self.black_time = config.GAME_TIME_SECONDS
        self.timer_winner = None
        self.selected_piece = None
        self.game_logic.assign_random_ability() # Asignar habilidad para el primer turno
        self.game_logic.game_over = False

    def render_menu(self):
        """Dibuja la pantalla del menú principal."""
        # Dibuja el fondo (vídeo o color sólido)
        if self.menu_video_frames:
            # Escalar el fotograma al tamaño de la pantalla para que se adapte
            frame = pygame.transform.scale(self.menu_video_frames[self.current_video_frame], (config.WIDTH, config.HEIGHT))
            self.screen.blit(frame, (0, 0))
            
            # Avanzar al siguiente fotograma para la animación
            self.current_video_frame += 1
            if self.current_video_frame >= len(self.menu_video_frames):
                self.current_video_frame = 0 # Reiniciar para crear un bucle
        else:
            self.screen.fill(config.UI_BG) # Color de fondo si no hay vídeo

        # Dibuja los botones del menú encima del fondo
        current_title_color = self.title_colors[self.current_title_color_index]
        self.menu_buttons = draw_menu(self.screen, current_title_color)
        pygame.display.flip()

    def render_game(self, show_info=False):
        """Dibuja todos los elementos del juego en la pantalla."""
        self.screen.fill(config.BLACK) # Limpia la pantalla
        
        # Dibuja los componentes de la UI
        draw_top_bar(self.screen, self.game_logic, self.game_mode, self.black_time)
        draw_board(self.screen, self.board_colors)

        # Dibuja un aviso si el rey del turno actual está en jaque
        if self.game_logic.is_in_check(self.game_logic.turn):
            king = self.game_logic.find_king(self.game_logic.turn)
            if king:
                # Crea una superficie para el aura de jaque
                check_aura_color = (255, 0, 0, 120) # Rojo semi-transparente
                aura_surface = pygame.Surface((config.SQUARE_SIZE, config.SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(aura_surface, check_aura_color, (config.SQUARE_SIZE // 2, config.SQUARE_SIZE // 2), config.SQUARE_SIZE // 2)
                
                # Dibuja el aura en la posición del rey
                self.screen.blit(aura_surface, king.rect.topleft)

        self.board.draw_pieces(self.screen) # Dibuja las piezas sobre el tablero
        # Dibuja toda la UI inferior (paleta, iconos, etc.) y guarda sus rects
        self.action_buttons_rects = draw_bottom_ui(self.screen, self.selected_color, self.swatch_rects, self.game_mode, self.white_time)
        
        # Si el juego ha terminado, mostrar el mensaje correspondiente
        if self.game_logic.game_over:
            message = ""
            if self.timer_winner:
                message = f"Tiempo agotado! Ganan las {self.timer_winner}"
            elif self.game_logic.is_in_check(self.game_logic.turn):
                winner = 'Black' if self.game_logic.turn == 'white' else 'White'
                message = f"Jaque Mate! Ganan las {winner}"
            else:
                message = "Ahogado! Es un empate."

            # Crear una superficie semi-transparente para el fondo del texto
            overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Negro con 150 de alpha
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.SysFont(None, 50)
            text_surface = font.render(message, True, config.WHITE)
            text_rect = text_surface.get_rect(center=(config.WIDTH / 2, config.HEIGHT / 2))
            self.screen.blit(text_surface, text_rect)

        # Dibuja el pop-up de información si es necesario
        if show_info:
            draw_info_popup(self.screen)

        pygame.display.flip() # Actualiza la pantalla completa

def main():
    """Función principal que crea una instancia del juego y la ejecuta."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
