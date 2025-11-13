# Archivo: database.py
# Descripción: Gestiona la interacción con la base de datos SQLite para
# guardar y cargar el estado del juego.

import sqlite3
import json

DB_FILE = "chess_magic.db"

def init_db():
    """Inicializa la base de datos y crea las tablas si no existen."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Tabla para almacenar partidas guardadas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        turn TEXT NOT NULL,
        board_state TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_game_state(game_logic, board, save_name="quicksave"):
    """Guarda el estado actual del tablero y el turno en la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Serializar el tablero a un formato de texto (JSON es ideal)
    board_state = []
    for row in range(8):
        row_state = []
        for col in range(8):
            piece = board.board[row][col]
            if piece:
                piece_data = {
                    "type": piece.name, # Usamos 'name' que ya tienes ('pawn', 'rook', etc.)
                    "color": piece.color,
                    "ability": piece.ability,
                    "has_moved": piece.has_moved
                }
                row_state.append(piece_data)
            else:
                row_state.append(None)
        board_state.append(row_state)

    board_state_json = json.dumps(board_state)
    turn = game_logic.turn

    # Usar INSERT OR REPLACE para sobrescribir una partida con el mismo nombre (ej. "quicksave")
    cursor.execute("""
    INSERT OR REPLACE INTO saved_games (name, turn, board_state)
    VALUES (?, ?, ?)
    """, (save_name, turn, board_state_json))

    conn.commit()
    conn.close()
    print(f"Partida '{save_name}' guardada correctamente.")

def load_game_state(game_logic, board, save_name="quicksave"):
    """Carga un estado de juego desde la base de datos y lo aplica al juego."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT turn, board_state FROM saved_games WHERE name = ?", (save_name,))
    result = cursor.fetchone()
    conn.close()

    if result:
        turn, board_state_json = result
        board_state = json.loads(board_state_json)

        # Aplicar el estado cargado
        game_logic.turn = turn
        board.load_from_state(board_state)
        game_logic.piece_with_ability = None # Resetear habilidad activa
        game_logic.double_step_rook_moved = None
        print(f"Partida '{save_name}' cargada correctamente.")
        return True
    else:
        print(f"No se encontró una partida guardada con el nombre '{save_name}'.")
        return False