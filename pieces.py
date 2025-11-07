# Archivo: pieces.py
# Descripción: Define la clase base Piece y las clases para cada tipo de pieza.
import pygame
import os
from config import SQUARE_SIZE, ASSETS_PATH, TOP_UI_HEIGHT
import copy

class Piece:
    # Diccionario para almacenar las imágenes ya cargadas y evitar lecturas de disco repetidas.
    # Es un atributo de clase, compartido por todas las instancias.
    _images = {}

    """Clase base para todas las piezas de ajedrez."""
    def __init__(self, row, col, color, name):
        self.row = row
        self.col = col
        self.color = color
        self.name = name
        self.has_moved = False
        self.ability = None # Atributo para almacenar la habilidad especial
        self.image = None
        self._load_image()
        if self.image: # Asegúrate de que la imagen se haya cargado correctamente antes de obtener el rect.
            self.rect = self.image.get_rect()
            self.calculate_pixel_pos()

    def _load_image(self):
        """Carga la imagen de la pieza desde la carpeta de assets."""
        image_key = f"{self.color}_{self.name}"
        if image_key not in Piece._images:
            # Si la imagen no ha sido cargada, la carga y la guarda en el diccionario.
            image_path = os.path.join(ASSETS_PATH, f"{image_key}.png")
            original_image = pygame.image.load(image_path)
            Piece._images[image_key] = pygame.transform.scale(original_image, (SQUARE_SIZE, SQUARE_SIZE))
        self.image = Piece._images[image_key] # Asigna la imagen cargada o ya existente
        # Asegúrate de que self.image no sea None antes de llamar a get_rect()
        if self.image:
            self.rect = self.image.get_rect()
    def calculate_pixel_pos(self):
        """Calcula la posición en píxeles de la esquina superior izquierda de la casilla."""
        self.rect.x = self.col * SQUARE_SIZE
        self.rect.y = self.row * SQUARE_SIZE + TOP_UI_HEIGHT

    def draw(self, screen):
        """Dibuja la pieza en la pantalla."""
        # Dibuja un aura si la pieza tiene una habilidad
        if self.ability:
            aura_color = (255, 223, 0, 100) # Amarillo dorado semi-transparente
            aura_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, aura_color, (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 2)
            screen.blit(aura_surface, self.rect.topleft)

        screen.blit(self.image, self.rect)

    def get_valid_moves(self, board):
        """
        Devuelve una lista de movimientos válidos (fila, columna) para la pieza.
        Este método será sobrescrito por cada pieza específica.
        """
        return []

    def __deepcopy__(self, memo):
        """
        Implementación personalizada de deepcopy para evitar copiar superficies de Pygame.
        Crea una nueva instancia de la pieza y copia solo los atributos lógicos.
        """
        # Evita la recursión infinita
        if id(self) in memo:
            return memo[id(self)]
        
        # Crea una nueva instancia de la misma clase sin llamar a __init__
        cls = self.__class__
        new_piece = cls.__new__(cls)
        memo[id(self)] = new_piece

        # Copia los atributos lógicos, pero no los de Pygame (image, rect)
        for k, v in self.__dict__.items():
            if k not in ['image', 'rect']:
                setattr(new_piece, k, copy.deepcopy(v, memo))
        
        # Deja los atributos de Pygame como None en la copia
        new_piece.image = None
        new_piece.rect = None
        
        return new_piece

# --- Clases para cada pieza ---

class Pawn(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, 'pawn')

    def get_valid_moves(self, board):
        # Si el peón tiene la habilidad 'omni_directional_pawn'
        if self.ability == 'omni_directional_pawn':
            moves = []
            # Movimiento de 1 paso en las 8 direcciones
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    r, c = self.row + dr, self.col + dc
                    if 0 <= r < 8 and 0 <= c < 8 and (board[r][c] is None or board[r][c].color != self.color):
                        moves.append((r, c))
            return moves

        moves = []
        direction = -1 if self.color == 'white' else 1

        # Movimiento de 1 casilla hacia adelante
        if 0 <= self.row + direction < 8 and board[self.row + direction][self.col] is None:
            moves.append((self.row + direction, self.col))
            # Movimiento de 2 casillas en el primer turno
            if not self.has_moved and board[self.row + 2 * direction][self.col] is None:
                moves.append((self.row + 2 * direction, self.col))

        # Capturas en diagonal
        for d_col in [-1, 1]:
            if 0 <= self.col + d_col < 8:
                target_piece = board[self.row + direction][self.col + d_col]
                if target_piece is not None and target_piece.color != self.color:
                    moves.append((self.row + direction, self.col + d_col))
        return moves

class Rook(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, 'rook')

    def get_valid_moves(self, board):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Derecha, Izquierda, Abajo, Arriba
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = self.row + dr * i, self.col + dc * i
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else: # Pieza aliada
                    break
        return moves        # Si la torre tiene la habilidad 'double_step_rook'

class Knight(Piece): # La clase AreaPushKnight sobrescribe este __init__ si se usa.
    def __init__(self, row, col, color):
        super().__init__(row, col, color, 'knight')


    def get_valid_moves(self, board):
        moves = []
        possible_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in possible_moves:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves


class AreaPushKnight(Knight):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.ability = 'area_push_knight'

    def get_valid_moves_with_ability(self, board): # Renombrado para evitar ocultar el método base
        # Obtiene los movimientos normales del caballo
        normal_moves = super().get_valid_moves(board)
        return normal_moves

    def activate_ability(self, board, target_row, target_col):
        """Activa la habilidad 'area_push_knight'. Empuja piezas enemigas adyacentes a la casilla de destino del caballo."""
        print(f"Habilidad 'Area Push' activada por el caballo en ({self.row}, {self.col}) hacia ({target_row}, {target_col})!")

        # Definir el área de efecto alrededor de la casilla de destino
        # Por ejemplo, un cuadrado de 3x3 centrado en la casilla de destino
        push_radius = 1

        for r_offset in range(-push_radius, push_radius + 1):
            for c_offset in range(-push_radius, push_radius + 1):
                if r_offset == 0 and c_offset == 0:
                    continue # No empujar la casilla donde aterriza el caballo

                affected_row, affected_col = target_row + r_offset, target_col + c_offset

                # Asegurarse de que la casilla afectada esté dentro del tablero
                if 0 <= affected_row < 8 and 0 <= affected_col < 8:
                    piece_to_push = board[affected_row][affected_col]

                    # Si hay una pieza enemiga en la casilla afectada
                    if piece_to_push and piece_to_push.color != self.color:
                        print(f"Empujando pieza enemiga: {piece_to_push.name} en ({affected_row}, {affected_col})")

                        # Determinar la dirección de empuje (alejándose de la casilla de destino del caballo)
                        push_dr = affected_row - target_row
                        push_dc = affected_col - target_col

                        new_row, new_col = affected_row + push_dr, affected_col + push_dc

                        # Comprobar si la nueva posición está dentro del tablero
                        if 0 <= new_row < 8 and 0 <= new_col < 8:
                            # Si la casilla de destino del empuje está vacía
                            if board[new_row][new_col] is None:
                                print(f"Pieza empujada a ({new_row}, {new_col})")
                                # Mover la pieza
                                board[affected_row][affected_col] = None
                                board[new_row][new_col] = piece_to_push
                                piece_to_push.row, piece_to_push.col = new_row, new_col
                                piece_to_push.calculate_pixel_pos()
                        else:
                            # La pieza es empujada fuera del tablero y es capturada
                            print(f"Pieza empujada fuera del tablero desde ({affected_row}, {affected_col})")
                            board[affected_row][affected_col] = None

class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, 'bishop')

    def get_valid_moves(self, board):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # Diagonales
        for dr, dc in directions:
            for i in range(1, 8):
                r, c = self.row + dr * i, self.col + dc * i
                if not (0 <= r < 8 and 0 <= c < 8):
                    break
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else: # Pieza aliada
                    break
        return moves

class Queen(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, 'queen')

    def get_valid_moves(self, board):
        # La reina combina los movimientos de la torre y el alfil
        rook_moves = Rook.get_valid_moves(self, board) # type: ignore
        bishop_moves = Bishop.get_valid_moves(self, board) # type: ignore
        return rook_moves + bishop_moves

class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color, 'king')

    def get_valid_moves(self, board):
        moves = []
        possible_moves = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in possible_moves:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves