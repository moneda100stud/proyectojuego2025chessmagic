# Archivo: game_logic.py
# Descripción: Orquesta las reglas del juego, como turnos, validación de movimientos y condiciones de victoria.
import random
import copy
from pieces import AreaPushKnight

# Lista de habilidades disponibles en el juego
POSSIBLE_ABILITIES = [
    'omni_directional_pawn', # Un peón que puede moverse un paso en cualquier dirección,
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
        self.double_step_rook_moved = None # Para rastrear la torre que acaba de moverse

    def next_turn(self):
        """Pasa al siguiente turno."""
        # Si la torre de doble paso acaba de hacer su segundo movimiento, reseteamos su estado.
        if self.double_step_rook_moved:
            self.double_step_rook_moved = None
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

    def find_king(self, color, board_state=None):
        """Encuentra la pieza del rey de un color específico en el tablero."""
        board_to_check = board_state if board_state is not None else self.board.board
        for r in range(8):
            for c in range(8):
                piece = board_to_check[r][c]
                if piece and piece.name == 'king' and piece.color == color:
                    return piece
        return None

    def is_in_check(self, color, board_state=None):
        """Verifica si el rey de un color específico está en jaque."""
        board_to_check = board_state if board_state is not None else self.board.board
        king = self.find_king(color, board_to_check)
        if not king:
            return False # No hay rey, no puede estar en jaque.

        opponent_color = 'white' if color == 'black' else 'black'
        for r in range(8):
            for c in range(8):
                piece = board_to_check[r][c]
                if piece and piece.color == opponent_color:
                    # Para el AreaPushKnight, sus movimientos de ataque son los de un caballo normal.
                    if isinstance(piece, AreaPushKnight):
                        valid_moves = piece.get_valid_moves(board_to_check)
                    else:
                        valid_moves = piece.get_valid_moves(board_to_check)
                    
                    if (king.row, king.col) in valid_moves:
                        return True
        return False

    def is_valid_move(self, piece, target_row, target_col):
        """
        Verifica si un movimiento es válido según las reglas del ajedrez.
        Comprueba las reglas de la pieza y si el movimiento deja al rey en jaque.
        """
        if not piece:
            return False

        valid_moves = piece.get_valid_moves(self.board.board)
        if (target_row, target_col) not in valid_moves:
            return False # El movimiento no es legal para la pieza.

        # Simular el movimiento para ver si el rey queda en jaque
        temp_board = copy.deepcopy(self.board.board)
        temp_board[piece.row][piece.col] = None
        temp_board[target_row][target_col] = piece

        # Si después de mover, el rey del jugador actual está en jaque, el movimiento no es válido.
        if self.is_in_check(piece.color, temp_board):
            return False

        return True

    def activate_ability(self, piece):
        """
        Activa la habilidad especial de una pieza.
        (A implementar: lógica de cooldowns, coste, efectos, etc.)
        """
        print(f"Habilidad de {piece} activada!")
        # Aquí se implementaría qué hace cada habilidad.
        pass