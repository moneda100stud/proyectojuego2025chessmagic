# Proyecto: ChessMagic (Pygame)

**ChessMagic** es una variante estratégica del ajedrez clásico desarrollada en Python con la librería Pygame. El juego introduce un sistema de habilidades especiales que se asignan aleatoriamente a las piezas, añadiendo una capa de imprevisibilidad y nuevas tácticas a cada partida.

para una informacion mas completa y profunda pueden ir al wiki profundo de este repositorio : 
https://deepwiki.com/moneda100stud/proyectojuego2025chessmagic/1.1-getting-started
ACONTINUACION SE HABLARA DE LAS CARACTERISTICAS Y PARTICULARIDADES DE ESTE REPOSITORIO Y PROYECTO PARA LAS PARTES MAS ESENCIALES :

## 1. Características Principales

El juego se encuentra en una fase funcional y robusta, con las siguientes características implementadas:

### Motor de Ajedrez
- **Reglas Clásicas:** Movimiento estándar para todas las piezas (Peón, Torre, Caballo, Alfil, Reina, Rey).
- **Sistema de Turnos:** Alternancia correcta entre el jugador de piezas blancas y negras.
- **Lógica de Captura:** Las piezas pueden capturar a las del oponente.
- **Reglas Avanzadas:**
  - **Detección de Jaque (Check):** El sistema detecta y avisa visualmente cuando un rey está amenazado.
  - **Prevención de Movimientos Ilegales:** Un jugador no puede realizar un movimiento que deje a su propio rey en jaque.
  - **Condiciones de Fin de Partida:** El juego concluye correctamente al detectar **Jaque Mate**, **Ahogado** (empate) o por **captura directa del rey**.

### Sistema de Habilidades Especiales
- **Asignación Aleatoria:** Al comienzo de cada turno, una pieza aleatoria del jugador activo recibe una habilidad especial.
- **Indicadores Visuales:** La pieza con habilidad se resalta con un aura de color distintivo para su fácil identificación.
- **Habilidades Implementadas:**
  - **`Omni-Directional Pawn`**: Un peón que puede moverse y capturar una casilla en cualquiera de las 8 direcciones.
  - **`Double-Step Rook`**: Una torre que, tras su primer movimiento, puede realizar un segundo movimiento de forma inmediata.

### Modos de Juego
- **Menú Principal Dinámico:** Al iniciar, el jugador es recibido con un menú con fondo de vídeo animado, música y un título con colores neón que cambian con el tiempo.
- **Modo Clásico:** Partida de ajedrez tradicional por turnos, sin límite de tiempo.
- **Modo Cronómetro:** Cada jugador dispone de un tiempo limitado (10 minutos). La partida termina si un jugador agota su tiempo.

### Interfaz de Usuario (UI) y Experiencia (UX)
- **Diseño Moderno:** La interfaz está organizada en barras superior e inferior para una visualización limpia de la información.
  - **Barra Superior:** Muestra el turno actual, la habilidad activa y el cronómetro del jugador negro.
  - **Barra Inferior:** Contiene la paleta de colores y el botón "Cambiar Color" a la izquierda, el cronómetro del jugador blanco, y una cuadrícula de iconos de acción a la derecha.
- **Personalización del Tablero:** El jugador puede cambiar los colores del tablero en tiempo real usando la paleta de colores.
- **Iconos de Acción:** Una cuadrícula compacta de iconos (3x2) permite un acceso rápido a las funciones principales:
  - **S (Guardar):** Guarda el estado actual de la partida.
  - **L (Cargar):** Carga la última partida guardada.
  - **R (Reiniciar):** Inicia una nueva partida.
  - **M (Menú):** Vuelve al menú principal.
  - **? (Info):** Abre una ventana emergente que explica las habilidades disponibles.

### Audio Inmersivo
- **Música de Fondo:** Pistas de música diferentes para el menú principal y para las partidas, con transiciones suaves entre ellas.
- **Efectos de Sonido:** Se reproduce un efecto de sonido al mover una pieza, mejorando la retroalimentación al jugador.

### Persistencia de Datos
- **Guardado y Carga:** Gracias a la integración con **SQLite**, los jugadores pueden guardar una partida en curso y cargarla más tarde, preservando el estado del tablero, el turno y las habilidades.

### Portabilidad
- **Rutas Relativas:** Todas las rutas a los recursos del juego (imágenes, sonidos, fotogramas de vídeo) son relativas. Esto asegura que el proyecto se pueda ejecutar en cualquier ordenador sin necesidad de modificar el código.

## 2. Requisitos

Para poder ejecutar el proyecto, necesitarás tener **Python** y la librería **Pygame** instalados.

```bash
# Instalar Pygame
pip install pygame
```

## 3. Estructura de Archivos Sugerida

Una buena organización del código es clave para un proyecto manejable. Se recomienda la siguiente estructura:
```
/
├── pygame juego proyecto.py # Punto de entrada principal, contiene el bucle del juego.
├── board.py                 # Clase para gestionar el tablero, su estado y las piezas.
├── config.py                # Constantes y variables de configuración.
├── pieces.py                # Clases para cada tipo de pieza (Peón, Torre, etc.) y su lógica.
├── game_logic.py            # Lógica de turnos, jaque, jaque mate y activación de habilidades.
├── ui.py                    # Funciones o clases para dibujar la interfaz (tablero, menús, botones).
├── database.py              # Módulo para la interacción con la base de datos SQLite.
└── assets/
    ├── images/              # Directorio para las imágenes de las piezas, tablero, etc.
    └── sounds/              # Directorio para efectos de sonido.
    └── video UL/            # (Asumiendo que es un directorio para archivos de video)
```   
    
Descripción de Componentes :

pygame juego proyecto.py: El punto de entrada principal. Aquí se inicializa Pygame y se contiene el bucle principal del juego.

board.py: Contiene la lógica para la clase que maneja el estado del tablero, las posiciones y la interacción general.

config.py: Almacena constantes (tamaños, colores, etc.) y variables de configuración global.

pieces.py: Define las clases para cada pieza de ajedrez (o del juego) y su lógica de movimiento específica.

game_logic.py: Maneja las reglas de turnos, condiciones de victoria (jaque/jaque mate) y cualquier lógica compleja del juego.

ui.py: Dedicado a todo lo relacionado con el dibujo de la interfaz gráfica, menús y elementos visuales.

database.py: Módulo para la persistencia de datos (por ejemplo, guardar puntuaciones o estados del juego) utilizando SQLite.

assets/: Un directorio para todos los recursos externos.

assets/images/: Para archivos gráficos como sprites de piezas y el tablero.

assets/sounds/: Para efectos de sonido y música.

assets/video UL/: Para almacenar archivos de video, si son necesarios para el proyecto.


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
