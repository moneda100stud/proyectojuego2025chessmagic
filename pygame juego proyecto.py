# Archivo: pygame juego proyecto.py (o main.py)
# Descripción: Punto de entrada principal para el juego de Ajedrez con Habilidades.
# Este archivo contiene el bucle principal del juego, maneja eventos y coordina
# el dibujado en pantalla.

import pygame
import sys
import config
from ui import draw_board, draw_ui, create_palette_rects, draw_top_bar, draw_change_color_button, draw_action_buttons
from board import Board
from game_logic import GameLogic
import database

class Game:
    """Clase principal que encapsula la lógica y el estado del juego."""
    def __init__(self):
        """Inicializa el juego y sus componentes."""
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption("Ajedrez con Habilidades")
        self.clock = pygame.time.Clock()
        self.running = True

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

    def run(self):
        """Inicia y mantiene el bucle principal del juego."""
        self.game_logic.assign_random_ability() # Asignar habilidad al inicio

        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(config.FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Procesa las entradas del usuario (ratón, teclado, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)

    def handle_mouse_click(self, pos):
        """Gestiona la lógica de un clic del ratón."""
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
        if self.action_buttons_rects.get('save') and self.action_buttons_rects['save'].collidepoint(pos):
            database.save_game_state(self.game_logic, self.board)
            return

        if self.action_buttons_rects.get('load') and self.action_buttons_rects['load'].collidepoint(pos):
            if database.load_game_state(self.game_logic, self.board):
                self.selected_piece = None # Deseleccionar pieza tras cargar
                # La habilidad se resetea dentro de load_game_state, pero la asignamos al nuevo turno
                self.game_logic.assign_random_ability()
            return

        if self.action_buttons_rects.get('reset') and self.action_buttons_rects['reset'].collidepoint(pos):
            self.reset_game()
            return

        # Comprobar si se hizo clic en el botón "Cambiar Color"
        if self.change_color_button_rect and self.change_color_button_rect.collidepoint(pos):
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
                        # No cambiamos de turno y no deseleccionamos la pieza.
                        # El jugador debe mover la torre de nuevo.
                        return

                    # Para cualquier otro movimiento (incluido el segundo de la torre)
                    self.board.move_piece(self.selected_piece, row, col)
                    self.game_logic.next_turn()
                    self.selected_piece = None # Deseleccionar después del movimiento final
                else:
                    # Si el movimiento no es válido, deseleccionar la pieza
                    self.selected_piece = None
            else:
                # Si no hay pieza seleccionada y se hace clic en una pieza del color del turno, la seleccionamos.
                if clicked_piece is not None and clicked_piece.color == self.game_logic.turn:
                    self.selected_piece = clicked_piece


    def update(self):
        """Actualiza el estado del juego (lógica de piezas, turnos, etc.)."""
        # (A implementar en el futuro)
        pass

    def reset_game(self):
        """Reinicia el juego a su estado inicial."""
        print("Reiniciando partida...")
        self.board = Board()
        self.game_logic = GameLogic(self.board)
        self.selected_piece = None
        self.game_logic.assign_random_ability() # Asignar habilidad para el primer turno

    def render(self):
        """Dibuja todos los elementos del juego en la pantalla."""
        self.screen.fill(config.BLACK) # Limpia la pantalla
        
        # Dibuja los componentes de la UI
        # Guardamos los rects de los botones de acción que se dibujan en la barra superior
        self.action_buttons_rects = draw_top_bar(self.screen, self.game_logic)
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
        draw_ui(self.screen, self.selected_color, self.swatch_rects) # Dibuja la paleta
        self.change_color_button_rect = draw_change_color_button(self.screen) # Dibuja el botón y guarda su rect
        
        pygame.display.flip() # Actualiza la pantalla completa

def main():
    """Función principal que crea una instancia del juego y la ejecuta."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
