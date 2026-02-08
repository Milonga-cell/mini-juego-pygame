import pygame
import random
import time

pygame.init()

# =====================
# CONFIGURACIÓN BÁSICA
# =====================
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mini Juego - Esquivar")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)

# Skins del jugador
skins = [AZUL, VERDE, AMARILLO]
skin_actual = 0

# Fuentes
fuente = pygame.font.Font(None, 36)
fuente_grande = pygame.font.Font(None, 64)

reloj = pygame.time.Clock()

# =====================
# FUNCIÓN BOTÓN
# =====================
def boton(texto, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(pantalla, BLANCO, rect, 2)

    txt = fuente.render(texto, True, BLANCO)
    pantalla.blit(txt, (x + 20, y + 10))

    if rect.collidepoint(mouse) and click[0]:
        return True
    return False

# =====================
# PANTALLA DE INICIO
# =====================
def pantalla_inicio():
    global skin_actual
    while True:
        pantalla.fill(NEGRO)

        titulo = fuente_grande.render("Mini Juego", True, BLANCO)
        pantalla.blit(titulo, (ANCHO // 2 - 150, 100))

        txt_skin = fuente.render("Skin del jugador", True, BLANCO)
        pantalla.blit(txt_skin, (ANCHO // 2 - 100, 220))

        pygame.draw.rect(
            pantalla,
            skins[skin_actual],
            (ANCHO // 2 - 20, 260, 40, 40)
        )

        if boton("Cambiar Skin", ANCHO // 2 - 80, 320, 160, 40):
            skin_actual = (skin_actual + 1) % len(skins)
            time.sleep(0.2)

        if boton("Iniciar Juego", ANCHO // 2 - 90, 400, 180, 50):
            return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()
        reloj.tick(60)

# =====================
# JUEGO PRINCIPAL
# =====================
def juego():
    jugador = pygame.Rect(380, 280, 40, 40)
    velocidad_jugador = 5

    # 🔥 MÁS ENEMIGOS (ANTES ERAN 6)
    enemigos = []
    for _ in range(14):
        tamaño = random.randint(20, 60)
        velocidad = max(2, 8 - tamaño // 10)

        enemigo = {
            "rect": pygame.Rect(
                random.randint(0, ANCHO - tamaño),
                random.randint(-800, 0),
                tamaño,
                tamaño
            ),
            "vel": velocidad
        }
        enemigos.append(enemigo)

    vidas = 3
    tiempo_inicio = time.time()

    while True:
        reloj.tick(60)
        pantalla.fill(NEGRO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]:
            jugador.x -= velocidad_jugador
        if teclas[pygame.K_d]:
            jugador.x += velocidad_jugador
        if teclas[pygame.K_w]:
            jugador.y -= velocidad_jugador
        if teclas[pygame.K_s]:
            jugador.y += velocidad_jugador

        for enemigo in enemigos:
            enemigo["rect"].y += enemigo["vel"]

            if enemigo["rect"].y > ALTO:
                enemigo["rect"].y = -enemigo["rect"].height
                enemigo["rect"].x = random.randint(
                    0, ANCHO - enemigo["rect"].width
                )

            if jugador.colliderect(enemigo["rect"]):
                vidas -= 1
                enemigo["rect"].y = -enemigo["rect"].height
                enemigo["rect"].x = random.randint(
                    0, ANCHO - enemigo["rect"].width
                )

                if vidas <= 0:
                    puntos = int(time.time() - tiempo_inicio)
                    return puntos

        puntos = int(time.time() - tiempo_inicio)

        pygame.draw.rect(pantalla, skins[skin_actual], jugador)
        for enemigo in enemigos:
            pygame.draw.rect(pantalla, ROJO, enemigo["rect"])

        txt_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
        txt_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)

        pantalla.blit(txt_vidas, (10, 10))
        pantalla.blit(txt_puntos, (10, 40))

        pygame.display.flip()

# =====================
# GAME OVER
# =====================
def pantalla_game_over(puntos):
    while True:
        pantalla.fill(NEGRO)

        txt = fuente_grande.render("Has perdido", True, ROJO)
        pantalla.blit(txt, (ANCHO // 2 - 170, 200))

        score = fuente.render(f"Puntaje final: {puntos}", True, BLANCO)
        pantalla.blit(score, (ANCHO // 2 - 100, 280))

        if boton("Intentar de nuevo", ANCHO // 2 - 100, 350, 200, 50):
            return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.flip()
        reloj.tick(60)

# =====================
# BUCLE GENERAL
# =====================
while True:
    pantalla_inicio()
    puntos_final = juego()
    pantalla_game_over(puntos_final)
