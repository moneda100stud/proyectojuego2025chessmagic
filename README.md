# Proyecto: Ajedrez con Habilidades (Pygame)

Este documento describe la estructura y los componentes necesarios para desarrollar un juego de ajedrez con habilidades especiales para las piezas utilizando la librería Pygame en Python.

## 6. Estado Actual del Proyecto (Fase de Desarrollo Activa)

El juego se encuentra en una etapa funcional donde las mecánicas principales están implementadas y se están añadiendo características avanzadas y habilidades especiales.

### Características Implementadas

- **Motor de Ajedrez Básico:**
  - Tablero 8x8 completamente funcional.
  - Movimiento estándar para todas las piezas (Peón, Torre, Caballo, Alfil, Reina, Rey).
  - Sistema de turnos para Blanco y Negro.
  - Lógica de captura de piezas.
- **Sistema de Habilidades Especiales:**
  - Cada turno, una pieza aleatoria del jugador actual recibe una habilidad especial.
  - **Habilidades Funcionales:**
    - `Omni-Directional Pawn`: Un peón que puede moverse un paso en cualquier dirección.
    - `Double-Step Rook`: Una torre que puede realizar un segundo movimiento inmediatamente después del primero.
    - `Area Push Knight`: Un caballo que, al aterrizar, empuja las piezas enemigas adyacentes.
- **Reglas de Ajedrez Avanzadas:**
  - **Detección de Jaque (Check):** El sistema previene que un jugador realice un movimiento que deje a su propio rey en jaque.
- **Interfaz de Usuario (UI):**
  - Visualización del turno actual y de la habilidad activa.
  - Indicador visual (aura amarilla) sobre la pieza que posee la habilidad.
  - Indicador visual (aura roja) sobre el rey cuando está en jaque.
  - Paleta de colores para personalizar la apariencia del tablero en tiempo real.

## 1. Descripción del Juego

El proyecto consiste en crear un juego de ajedrez por turnos para dos jugadores. La principal característica que lo diferenciará del ajedrez tradicional es que algunas o todas las piezas tendrán "habilidades especiales" que podrán ser activadas durante la partida, añadiendo una capa extra de estrategia.

## 2. Requisitos

Para poder ejecutar el proyecto, necesitarás tener instalado Python y la librería Pygame.

```bash
# Instalar Pygame
pip install pygame
```

## 3. Estructura de Archivos Sugerida

Una buena organización del código es clave para un proyecto manejable. Se recomienda la siguiente estructura:

```
/
├── main.py             # Punto de entrada principal, contiene el bucle del juego.
├── board.py            # Clase para gestionar el tablero, su estado y las piezas.
├── config.py           # Constantes y variables de configuración.
├── pieces.py           # Clases para cada tipo de pieza (Peón, Torre, etc.) y su lógica.
├── game_logic.py       # Lógica de turnos, jaque, jaque mate y activación de habilidades.
├── ui.py               # Funciones o clases para dibujar la interfaz (tablero, menús, botones).
└── assets/
    ├── images/         # Directorio para las imágenes de las piezas, tablero, etc.
    │   ├── white_pawn.png
    │   ├── black_king.png
    │   └── ...
    └── sounds/         # (Opcional) Directorio para efectos de sonido.
```

## 4. Componentes Clave del Código

Estas son las secciones lógicas que tu código deberá implementar.

### a. Bucle Principal del Juego (`main.py`)
Basado en el ejemplo estándar de Pygame, este bucle será el corazón del programa.
- **Inicialización de Pygame:** Configura la ventana, el reloj y carga los recursos.
- **Manejo de Eventos:** Captura las entradas del usuario, como clics del ratón (para seleccionar y mover piezas) o el cierre de la ventana.
- **Actualización del Estado:** Llama a las funciones de `game_logic.py` para procesar los movimientos y cambiar el estado del juego.
- **Renderizado:** Llama a las funciones de `ui.py` para dibujar el estado actual del juego en la pantalla en cada fotograma.
- **Control de FPS:** Limita la velocidad de fotogramas para un rendimiento consistente.

### b. Representación del Tablero (`board.py`)
Esta clase se encargará de "saber" qué hay en cada casilla.
- **Estructura de datos:** Se puede usar una matriz 2D (lista de listas) de 8x8 para representar el tablero. Cada elemento de la matriz puede contener un objeto de tipo `Piece` o ser `None` si la casilla está vacía.
- **Gestión de piezas:** Métodos para añadir, mover y eliminar piezas del tablero.
- **Cálculo de movimientos:** Podría contener la lógica para determinar todos los movimientos legales para una pieza seleccionada, considerando las otras piezas en el tablero.

### c. Lógica de las Piezas (`pieces.py`)
Aquí es donde se define el comportamiento de cada pieza.
- **Clase base `Piece`:** Una clase base con atributos comunes (color, posición, si ha sido movida).
- **Clases heredadas:** Clases para cada pieza (`Pawn`, `Rook`, `Knight`, `Bishop`, `Queen`, `King`) que hereden de `Piece`.
- **Movimientos estándar:** Cada clase de pieza implementará un método para calcular sus movimientos válidos según las reglas del ajedrez.
- **Habilidades especiales:** Cada clase (o las que apliquen) tendrá un método para su habilidad especial. Por ejemplo, un `Caballo` que pueda saltar dos veces o un `Alfil` que pueda moverse a través de una pieza aliada.

### d. Lógica del Juego (`game_logic.py`)
Este módulo orquesta las reglas y el flujo de la partida.
- **Control de turnos:** Lleva la cuenta de a qué jugador le toca mover.
- **Validación de movimientos:** Confirma si un movimiento solicitado por el jugador es legal (p. ej., no deja al rey en jaque).
- **Detección de Jaque y Jaque Mate:** Funciones para comprobar si un rey está amenazado y si la partida ha terminado.
- **Activación de habilidades:** Lógica para gestionar cuándo y cómo se puede usar una habilidad especial (p. ej., una vez por partida, con un coste de "energía", etc.).

### e. Interfaz de Usuario (`ui.py`)
Todo lo relacionado con lo que el jugador ve en la pantalla.
- **Dibujar el tablero:** Renderizar el tablero con sus casillas de colores alternos.
- **Dibujar las piezas:** Cargar las imágenes desde la carpeta `assets/` y dibujarlas en sus posiciones correctas sobre el tablero.
- **Resaltar movimientos:** Dibujar indicadores visuales (círculos, casillas de otro color) para mostrar los movimientos válidos de una pieza seleccionada.
- **Mostrar información:** Renderizar texto para indicar el turno actual, si hay jaque, o menús para activar habilidades.

## 5. Próximos Pasos y Limitaciones

Es importante tener en cuenta que la primera versión del proyecto se centrará en la mecánica principal y tendrá las siguientes limitaciones:

- **No habrá un oponente de IA:** El juego está diseñado para dos jugadores locales en el mismo ordenador.
- **Sin modo multijugador en red:** No se implementará la funcionalidad para jugar en línea.
- **Reglas complejas:** Inicialmente, es posible que no se implementen todas las reglas especiales del ajedrez, como la captura *al paso* (en passant), el enroque o la promoción del peón. Estas se pueden añadir en futuras iteraciones.
- **No se guardarán partidas:** No habrá una función para guardar el estado de una partida y reanudarla más tarde.
- **Condiciones de Fin de Partida:** Aún falta por implementar la lógica de Jaque Mate y Tablas (Stalemate).

Con esta estructura, podrás desarrollar tu juego de manera ordenada y modular, lo que facilitará la implementación de nuevas características y la depuración de errores. ¡Mucho éxito con tu proyecto!