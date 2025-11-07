# Archivo: board.py
# Descripción: Contiene la clase Board, que representa el estado del tablero de ajedrez.
import pygame as pg
from config import ROWS, COLS
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    """
    Gestiona el estado interno del tablero, incluyendo la posición de las piezas.
    """
    def __init__(self):
        self.board = []
        self.create_board() # Primero crea la matriz vacía
        self.setup_pieces() # Luego, llena la matriz con piezas

    def create_board(self):
        """Crea la estructura de datos del tablero (matriz 8x8)."""
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

    def setup_pieces(self):
        """Coloca las piezas en sus posiciones iniciales."""
        # Piezas Negras (se asignan directamente a las filas)
        self.board[0] = [Rook(0, 0, 'black'), Knight(0, 1, 'black'), Bishop(0, 2, 'black'), Queen(0, 3, 'black'), King(0, 4, 'black'), Bishop(0, 5, 'black'), Knight(0, 6, 'black'), Rook(0, 7, 'black')] # type: ignore
        self.board[1] = [Pawn(1, i, 'black') for i in range(COLS)] # type: ignore

        # Piezas Blancas
        self.board[6] = [Pawn(6, i, 'white') for i in range(COLS)] # type: ignore
        self.board[7] = [Rook(7, 0, 'white'), Knight(7, 1, 'white'), Bishop(7, 2, 'white'), Queen(7, 3, 'white'), King(7, 4, 'white'), Bishop(7, 5, 'white'), Knight(7, 6, 'white'), Rook(7, 7, 'white')] # type: ignore

    def draw_pieces(self, screen):
        """Dibuja todas las piezas en el tablero."""
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(screen)

    def move_piece(self, piece, row, col, keep_ability=False):
        """Mueve una pieza a una nueva posición en el tablero."""
        self.board[piece.row][piece.col] = None
        self.board[row][col] = piece
        piece.row = row
        piece.col = col
        if not keep_ability:
            # Al moverse, la pieza pierde su habilidad especial
            piece.ability = None
        piece.has_moved = True # Marcar que la pieza ya se ha movido
        piece.calculate_pixel_pos()