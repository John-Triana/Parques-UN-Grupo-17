import pygame
import random
import sys
import os

# Inicializar pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((720, 720), pygame.RESIZABLE)
pygame.display.set_caption("Parqués UN")

# Pedir al usuario el modo de juego
modo_juego = input("Selecciona el modo de juego (1: Real, 2: Desarrollador): ")
while modo_juego not in ["1", "2"]:
    modo_juego = input("Opción inválida. Selecciona el modo de juego (1: Real, 2: Desarrollador): ")
modo_desarrollador = modo_juego == "2"

# Diccionario de casillas con coordenadas en el tablero
casillas = {
    0: (330, 600), 1: (330, 600), 2: (415, 600), 3: (415, 575), 4: (415, 550),
    5: (415, 525), 6: (415, 500), 7: (415, 475), 8: (420, 440), 9: (435, 415),
    10: (460, 400), 11: (485, 390), 12: (515, 390), 13: (538, 390), 14: (558, 390),
    15: (583, 390), 16: (606, 390), 17: (630, 390), 18: (630, 290), 19: (630, 215),
    20: (606, 215), 21: (583, 215), 22: (558, 215), 23: (534, 215), 24: (510, 215),
    25: (488, 215), 26: (465, 215), 27: (455, 190), 28: (455, 170), 29: (450, 145),
    30: (450, 125), 31: (450, 105), 32: (450, 85), 33: (450, 60), 34: (450, 40),
    35: (360, 40), 36: (285, 40), 37: (285, 60), 38: (285, 80), 39: (285, 105),
    40: (285, 130), 41: (285, 155), 42: (275, 182), 43: (265, 205), 44: (245, 230),
    45: (220, 250), 46: (188, 250), 47: (160, 250), 48: (140, 250), 49: (115, 250),
    50: (90, 250), 51: (65, 250), 52: (65, 340), 53: (65, 415), 54: (90, 415),
    55: (115, 415), 56: (140, 415), 57: (165, 415), 58: (185, 415), 59: (205, 415),
    60: (225, 425), 61: (245, 435), 62: (245, 455), 63: (245, 475), 64: (245, 495),
    65: (245, 520), 66: (245, 545), 67: (245, 570), 68: (245, 600)
}

# Salidas de cada equipo
salidas = {'rojo': 6, 'azul': 57, 'verde': 23, 'amarillo': 40}

# Cargar imágenes
ruta = os.path.dirname(__file__)
fichas_img = {
    'rojo': pygame.image.load(os.path.join(ruta, "Imagenes", "Rojo 1.png")),
    'azul': pygame.image.load(os.path.join(ruta, "Imagenes", "Azul 1.png")),
    'verde': pygame.image.load(os.path.join(ruta, "Imagenes", "Verde 1.png")),
    'amarillo': pygame.image.load(os.path.join(ruta, "Imagenes", "Amarillo 1.png"))
}
tablero_img = pygame.image.load(os.path.join(ruta, "Imagenes", "Tablero.jpg"))
modo_real_img = pygame.image.load(os.path.join(ruta, "Imagenes", "Modo real.png"))
modo_desarrollador_img = pygame.image.load(os.path.join(ruta, "Imagenes", "Modo desarrollador.jpg"))

# Clase Tablero
class Tablero:
    def __init__(self):
        self.casillas_externas = casillas  # Casillas numeradas del 1 al 68
        self.casillas_internas = {i: [] for i in range(1, 5)}  # Casillas internas para cada equipo (4 equipos)
        self.seguro = [1, 6, 13, 18, 23, 30, 35, 40, 47, 52, 57, 64]  # Casillas seguras de cada equipo
        self.carceles = {'rojo': [], 'azul': [], 'verde': [], 'amarillo': []}  # Cárceles de los equipos
        self.bloqueos = {}  # Para controlar las casillas bloqueadas
        self.salidas = salidas

    def dibujar(self, pantalla):
        pantalla.blit(tablero_img, (0, 0))

    def dibujar_fichas(self, pantalla, equipos):
        for equipo, fichas in equipos.items():
            for ficha in fichas:
                if ficha.posicion in casillas:
                    x, y = casillas[ficha.posicion]
                    pantalla.blit(fichas_img[equipo], (x, y))

# Clase Ficha
class Ficha:
    def __init__(self, equipo):
        self.equipo = equipo
        self.posicion = salidas[equipo]  # Empieza fuera del tablero

    def mover(self, pasos):
        if self.posicion is not None:
            self.posicion += pasos
            print(f"Ficha {self.equipo} movida a la casilla {self.posicion}")

# Clase principal del juego
class Parques:
    def __init__(self):
        self.turno = 0
        self.equipos = {
            'rojo': [Ficha('rojo') for _ in range(4)],
            'azul': [Ficha('azul') for _ in range(4)],
            'verde': [Ficha('verde') for _ in range(4)],
            'amarillo': [Ficha('amarillo') for _ in range(4)]
        }
        self.tablero = Tablero()

    def obtener_turno_actual(self):
        return list(self.equipos.keys())[self.turno]

    def lanzar_dados(self):
        # Lanza los dados de forma aleatoria o permite elegir valores en modo desarrollador.
        if modo_desarrollador:
            try:
                dado1 = int(input("Ingrese el valor del dado 1 (1-6) o 0 para lanzar real: "))
                if dado1 == 0:
                    dado1 = random.randint(1, 6)
                dado2 = int(input("Ingrese el valor del dado 2 (1-6) o 0 para lanzar real: "))
                if dado2 == 0:
                    dado2 = random.randint(1, 6)
            except ValueError:
                print("Entrada no válida. Lanzando valores aleatorios.")
                dado1, dado2 = random.randint(1, 6), random.randint(1, 6)
        else:
            dado1, dado2 = random.randint(1, 6), random.randint(1, 6)
        return dado1, dado2

    def mover_fichas(self, equipo):
        # Gestiona el movimiento de las fichas del equipo actual.
        dado1, dado2 = self.lanzar_dados()
        print(f"\nTurno del equipo {equipo}, lanzando dados: {dado1} y {dado2}")

        # Obtener fichas del equipo que pueden moverse
        fichas = self.equipos[equipo]
        posibles_movimientos = [ficha for ficha in fichas if ficha.posicion + dado1 <= 68 or ficha.posicion + dado2 <= 68]

        if not posibles_movimientos:
            print("No hay movimientos posibles.")
        else:
            if len(posibles_movimientos) == 1:
                # Si solo hay una ficha que puede moverse, se mueve automáticamente
                ficha_seleccionada = posibles_movimientos[0]
                ficha_seleccionada.mover(dado1)
                ficha_seleccionada.mover(dado2)
            else:
                # Si hay varias opciones, el jugador elige qué ficha mover con cada dado
                print("Selecciona qué ficha mover:")
                for i, ficha in enumerate(posibles_movimientos):
                    print(f"{i + 1}: Ficha en posición {ficha.posicion}")
                try:
                    opcion = int(input("Elige una ficha para mover con el dado 1: ")) - 1
                    posibles_movimientos[opcion].mover(dado1)
                    opcion = int(input("Elige una ficha para mover con el dado 2: ")) - 1
                    posibles_movimientos[opcion].mover(dado2)
                except (ValueError, IndexError):
                    print("Selección inválida. No se mueve ninguna ficha.")

        # Pasar al siguiente turno
        self.turno = (self.turno + 1) % 4

    def jugar(self):
        while True:
            if modo_juego == "1":
                screen.blit(modo_real_img, (0, 0))
            else:
                screen.blit(modo_desarrollador_img, (0, 0))
            pygame.display.update()
            pygame.time.delay(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            equipo_actual = self.obtener_turno_actual()
            self.mover_fichas(equipo_actual)
            self.tablero.dibujar(screen)
            self.tablero.dibujar_fichas(screen, self.equipos)

            pygame.display.update()
            pygame.time.delay(1000)

# Iniciar el juego
juego = Parques()
juego.jugar()
