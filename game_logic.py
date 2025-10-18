# Archivo: game_logic.py
# Descripción: Orquesta las reglas del juego, como turnos, validación de movimientos y condiciones de victoria.
import random

# Lista de habilidades disponibles en el juego
POSSIBLE_ABILITIES = [
    'omni_directional_pawn', # Un peón que puede moverse un paso en cualquier dirección
    'double_step_rook',      # Una torre que puede dar un segundo paso después de moverse
    'area_push_knight'       # Un caballo que empuja piezas a su alrededor al aterrizar (ejemplo, no implementado aún)
]

class GameLogic:
    """
    Gestiona el estado y las reglas del juego de ajedrez.
    """
    def __init__(self, board):
        self.board = board
        self.turn = 'white'  # Las blancas siempre empiezan
        self.selected_piece = None
        self.piece_with_ability = None

    def next_turn(self):
        """Pasa al siguiente turno."""
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.assign_random_ability()

    def assign_random_ability(self):
        """Asigna una habilidad aleatoria a una pieza aleatoria del jugador actual."""
        # Limpiar habilidad anterior
        if self.piece_with_ability:
            self.piece_with_ability.ability = None
            self.piece_with_ability = None

        player_pieces = [p for row in self.board.board for p in row if p and p.color == self.turn]
        
        if not player_pieces:
            return

        chosen_piece = random.choice(player_pieces)
        chosen_ability = random.choice(POSSIBLE_ABILITIES)
        chosen_piece.ability = chosen_ability
        self.piece_with_ability = chosen_piece
        print(f"¡Habilidad '{chosen_ability}' asignada a {chosen_piece.name} en ({chosen_piece.row}, {chosen_piece.col})!")

    def is_valid_move(self, piece, target_row, target_col):
        """
        Verifica si un movimiento es válido según las reglas del ajedrez.
        Por ahora, solo comprueba las reglas de movimiento de la pieza.
        (Futuro: jaque, jaque mate, etc.)
        """
        if not piece:
            return False
        valid_moves = piece.get_valid_moves(self.board.board)
        return (target_row, target_col) in valid_moves

    def activate_ability(self, piece):
        """
        Activa la habilidad especial de una pieza.
        (A implementar: lógica de cooldowns, coste, efectos, etc.)
        """
        print(f"Habilidad de {piece} activada!")
        # Aquí se implementaría qué hace cada habilidad.
        pass